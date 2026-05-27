---
title: Pixels within a triangle on screen
subtitle: Ray casting, scan conversion with DDA or Bresenham, and edge-function rasterization
...

There are three common algorithms used to find which pixels a triangle covers,
and where within the triangle each such pixel is.
Each has pros and cons, so this page overviews all them all.

The "where within the triangle" part is often represented using <dfn>barycentric coordinates</dfn>,
which are three numbers (one per triangle vertex) that sum to 1.
Given a triangle with vertices $(\mathbf v_1, \mathbf v_2, \mathbf v_3)$,
each point $\mathbf p$ in the triangle
has unique barycentric coordinates $(w_1, w_2, w_3)$
such that $\mathbf p = w_1 \mathbf v_1 + w_2 \mathbf v_2 + w_3 \mathbf v_3$.
This applies no matter the dimensionality of $\mathbf p$:
if $\mathbf p = (x,y,z)$ the barycentric coordinates tell its location in 3D space,
while if $\mathbf p = (x,y,z, s,t, r,g,b,a)$
the barycentric coordinates tell its location in 3D space, its texture coordinates, its color, and its opacity.

Before explaining each method in depth, here is a brief summary of how they work:

Ray casting
:   1. Find a line through the eye and the pixel.
    2. Find the intersection of that line and the plane containing the triangle.
    3. Find the barycentric coordinates of that point.
    4. If all barycentric coordinates are positive, the pixel is part of the triangle.
    
    Ray casting is optimal if we are checking just a single pixel,
    and thus is used for things like finding what object the mouse pointer is pointing at
    or computing reflections and refractions where the "eye" is different for each sample.

Scan conversion
:   1. Transform the triangle so the camera view direction aligns with the $z$ axis.
    2. Find where the three edges of the triangle cross each integer $y$ (a row of pixels)
    3. Pair edge crossings with the same $y$ and find where each single-$y$ line crosses each integer $x$ (a pixel)

    This reduces triangle rendering to repeated line rendering.
    There are two common line rendering algorithms:
    
    DDA
    :   1. Find a vector between the line endpoints.
        2. Scale that vector to be 1 pixel long.
        3. Add part of that scaled vector to one endpoint to get an integer coordinate.
        4. Repeatedly add the scaled vector to the point to find each other point.
        
        DDA is simpler to explain than Bresenham and works well with floating-point numbers.
    
    Bresenham
    :   1. Find the rise (extent in $y$) and run (extent in $x$) of the line.
        2. Starting from one endpoint, represent its $x$ location using mixed number where the fractional part'd demoninator is the rise.
        3. Repeatedly add 1 to $y$ and the run to the numerator of the mixed-number; if the numerator exceeds the denominator, modify the integer point to make that no longer true.
        
        Bresenham uses only integer math, meaning it has no numerical error.
    
    For both line algorithms, barycentric coordinates are found by appending them to the vertices before beginning the computation, working with longer vectors as a result.
    Sometimes the values that would be interpolated with those barycentric coordinates are appended instead.
    
    Scan conversion is optimal if we are rendering many pixels on a large triangle
    using a sequential processor like a CPU.

Edge-function rasterization
:   1. Transform the triangle so the camera view direction aligns with the $z$ axis.
    2. Create a matrix from the triangle's vertices and invert it.
    3. For each pixel that might be in the triangle, multiply it by the inverted matrix to find its barycentric coordinates.
    4. If all barycentric coordinates are positive, the pixel is part of the triangle.
    
    Edge function rasterization is optimal if we are rendering many pixels on a large triangle
    using a highly parallel processor like a GPU.

This page tries to describe the costs of various algorithms
by counting the number of operations performed,
using the `1/`, `?:`, `*+`, and `+-` introduced for this class on the page [Understanding hardware performance](hwcycle.html)
and assuming 4-wide SIMD.

# Ray casting

A <dfn>ray</dfn> is a semi-infinite line:
it has a start point, called the ray's <dfn>origin</dfn> $\mathbf o$,
and extends infinitely in one direction from that point.
It is common to store that direction as a unit vector $\hat d$,
allowing any point along the ray to be represented by its distance $t$ along the ray,
where the point at $t$ is $\mathbf o + t \hat d$.
Ray casting seeks to find the smallest positive $t$
where the ray intersects with some object in the scene.

Ray casting is generally used in cases where each ray's origin will be different.
When many rays would come from a single origin, [scan conversion] and [edge function rasterization] are better able to take advantage of that shared origin for faster processing.

The primary work needed for rendering using ray casting
is computing ray-object intersections.
When the objects are triangles,
each such intersection will produce a $t$ value (needed to find the nearest intersection)
and the barycentric coordinates of the intersection point.

Ray-triangle intersection works as follows.

1. Find the $t$ where the ray intersects the plane that contains the triangle.

    If $t$ is negative, there is no intersection: the plane is behind, not in front of, the ray.

    If $t$ is larger than a $t$ found earlier, this is not the nearest intersection.

2. Find the point at that $t$ using $\mathbf p = \mathbf o + t \hat d$.

3. Find the barycentric coordinates of that point.

    If any barycentric coordinate is negative, there is no intersection.

## Finding $t$

Finding $t$ can be done using an arbitrary vertex of the triangle $\mathbf v_i$
and the triangle's geometric^[By "geometric normal vector" I mean the one that is perpendicular to every vector contained within the triangle's plane. It is common to use different visual normal vectors defined at each vertex and interpolated across the triangle using barycentric coordinates to create the illusion of smoothly curved surfaces, but those visual normal vectors are not used when finding ray-triangle intersections.] normal vector $\hat n$.

The $t$ we want places the intersection point within the plane,
meaning a vector between that point and any point in the plane (such as $\mathbf v_i$)
is perpendicular to the normal vector $\hat n$:
$$
\big((\mathbf o + t \hat d) - \mathbf v_i\big) \cdot \hat n = 0
$$
Because dot products distribute over addition and subtraction,
we can re-write that as
$$
t \hat d \cdot \hat n = (\mathbf v_i - \mathbf o) \cdot \hat n
$$
which means
$$\begin{equation}
t = \frac{(\mathbf v_i - \mathbf o) \cdot \hat n}{\hat d \cdot \hat n}
\end{equation}$$
This has a total cost of one `1/`, three `*+`, and three `+-`.

:::aside
It is tempting to precompute $k = \mathbf v_i \cdot \hat n$ for each triangle
to have a scalar instead of vector subtraction:
$$
t = \frac{k - (\mathbf o \cdot \hat n)}{\hat d \cdot \hat n}
$$
While this change saves two operations on a CPU,
on a GPU it is still one `1/`, three `*+`, and three `+-`.
Even on a non-SIMD CPU, the extra memory needed to store $k$
is generally not worth the benefit of saving two subtraction operations.
:::

## Finding barycentric coordinates

Be definition, barycentric coordinate $a_i$ is 1 at $v_i$ and 0 at the other two vertices, $v_j$ and $v_k$,
varying linearly between these.
Because it varies linearly, it can be found as an affine function of the point:
$a_i = A_i p_x + B_i p_y + C_i p_z + D_i$.
Affine functions like this are also called <dfn>plane equations</dfn>.

Finding a plane equation that gives the barycentric coordinates for a given vertex
is typically done in three steps:

1. A vector $(A',B',C')$ is chosen which is perpendicular to the edge $(\mathbf v_j - \mathbf v_k)$.

2. The vector is scaled to $(A_i,B_i,C_i) = \dfrac{1}{(A', B', C') \cdot (\mathbf v_i - \mathbf v_j)}(A', B', C')$; using $v_j$ in that equation is arbitrary, $v_k$ works too.

    This costs one `1/`, two `*+`, and one `+-` per plane equation.

3. The affine coordinate is found to make the equation 0 at $v_j$ and $v_k$: $D_i = - \mathbf v_j \cdot (A_i,B_i,C_i)$; again, using $v_k$ instead of $v_j$ works too.

    This costs one `*+` and one `+-` per plane equation.

This process leaves undefined which of the infinite number of $(A',B',C')$ that are perpendicular to the edge $(\mathbf v_j - \mathbf v_k)$ to pick.
There are three common choices:

1.  Make the plane pass through the ray origin.

    $(A', B', C') = (\mathbf v_j - \mathbf o) \times (\mathbf v_k - \mathbf o)$; the other order of cross product works too.

    This costs two `*+` per plane equation
    and one `+-` per triangle vertex.

    This choice of $(A', B', C')$ allows the barycentric coordinate computation to be done before or in parallel with finding $t$
    because the same coordinates will be found for any point along the ray, be that $\mathbf p$ or $\mathbf o + \hat d$ or something else.

    This choice of $(A', B', C')$ depends on the ray origin, requiring re-computing these coordinates for each new ray.
    That cost makes this a bad decision in most ray casting situations:
    if the ray origin is fixed, scan conversion or edge function rasterization will be faster
    and if it changes, the inability to precompute and store these barycentric coordinates
    makes this method much more computationally expensive than the other options here.
    However, it the ray origins are fixed but the other assumptions of scanline or edge function rasterizing aren't met (for example when rasterizing with a fisheye lens) this choice can be optimal.

1.  Make the plane perpendicular to the triangle.

    $(A', B', C') = \hat n \times (\mathbf v_j - \mathbf v_k)$; the other order of cross product works too.

    This costs two `*+` per plane equation.

    This choice of $(A', B', C')$ minimizes the impact of out-of-plane rounding errors on the barycentric coordinate computation.

1.  Pick a plane where one of $A$, $B$, or $C$ is 0 to simplify other computations.
    It's important not to pick a coordinate that makes the barycentric plane coplanar with the triangle,
    so this process begins by picking an axis.

    a. Pick the axis where $\hat n$ has the largest magnitude. Below we assume that was $z$.

    b. Discard that coordinate from the edge $(\mathbf v_j - \mathbf v_k)$, resulting in $(e_x, e_y)$.

    c. Use the 2D perpendicular to get $(A', B', C') = (-e_y, e_x, 0)$; the other sign $(e_y, -e_x, 0)$ works too.

    This costs two `?:` to pick the axis; there is no other computation needed.

The three plane equations can then be put together into a matrix
that yields all three barycentric coordinates, $(a_1, a_2, a_3)$:
$$
\begin{bmatrix}a_1\\a_2\\a_3\end{bmatrix} =
\begin{bmatrix}
A_1 & B_1 & C_1 & D_1 \\
A_2 & B_2 & C_2 & D_2 \\
A_3 & B_3 & C_3 & D_3 \\
\end{bmatrix}
\begin{bmatrix}x\\y\\z\\1\end{bmatrix}
$$

However, we only need two of the rows of that matrix
because by construction $a_1 + a_2 + a_3 = 1$,
so we can find $a_3 = 1 - a_1 - a_2$,
which is just a single `+-` operation on a GPU.
Finding only two rows also means computing only two of the three plane equations,
which will also allow us to find only two of the three edge vectors.

Regardless of how the barycentric plane equations are computed,
using them is always just two dot products (each being one `*+` and one `+-`) to get two of the coordinates
and one `+-` to get the third.




# Scan converting

Scan converting was one of the first 3D graphics algorithms
and was particularly suited for early CRT displays
which fundamentally drew lines,
passing a narrow beam of electrons over a screen covered in phosphors to make the phosphors glow.
Because it uses lines, scan conversion is also sometimes called the scanline algorithm.
It remains the most efficient way for a CPU to do basic rasterization today.

Scan conversion is generally presented assuming 2D pixel coordinate inputs.
Getting those inputs from 3D geometry involves multiplying by a view and projection matrix
and dividing by $w$.
Some nuances related to division by $w$ are discussed in the section "[perspective-correct]" below.

Scan converting is based on a line rasterizing algorithm.
These algorithms take a line segment,
defined by its two endpoints,
and finds all points on that segment that have an integer value for a particular component.

:::example
The line segment between $(1.5,2.5)$ and $(5.5, 7.3)$ has integer $x$ coordinates at the points
$(2,3.1), (3,4.3), (4,5.5), (5,6.7)$.

<figure>
<svg viewBox="-10 -10 620 820" transform="scale(1,-1)" style="max-width: 20em">
<line x1="150" y1="250" x2="550" y2="730" fill="none" stroke="#000" stroke-width="2"/>
<path d="M-10,0h620 M-10,100h620 M-10,200h620 M-10,300h620 M-10,400h620 M-10,500h620 M-10,600h620 M-10,700h620 M-10,800h620" fill="none" stroke="#000"/>
<path d="M0,-10v820 M100,-10v820 M200,-10v820 M300,-10v820 M400,-10v820 M500,-10v820 M600,-10v820 M700,-10v820" fill="none" stroke="#000"/>
<circle cx="150" cy="250" r="5" fill="blue"/><text x="150" y="-230" transform="scale(1,-1)" text-anchor="middle">(1.5, 2.5)</text>
<circle cx="550" cy="730" r="5" fill="blue"/><text x="550" y="-740" transform="scale(1,-1)" text-anchor="middle">(5.5, 7.3)</text>
<circle cx="200" cy="310" r="3" fill="red"/><text x="205" y="-305" transform="scale(1,-1)">(2, 3.1)</text>
<circle cx="300" cy="430" r="3" fill="red"/><text x="305" y="-425" transform="scale(1,-1)">(3, 4.3)</text>
<circle cx="400" cy="550" r="3" fill="red"/><text x="405" y="-545" transform="scale(1,-1)">(4, 5.5)</text>
<circle cx="500" cy="670" r="3" fill="red"/><text x="505" y="-665" transform="scale(1,-1)">(5, 6.7)</text>
<text x="5" y="-5" transform="scale(1,-1)">(0, 0)</text>
</svg>
<figcaption>The line segment between $(1.5,2.5)$ and $(5.5, 7.3)$ has integer $x$ coordinates at the points
$(2,3.1), (3,4.3), (4,5.5), (5,6.7)$.</figcaption>
</figure>
:::

Given a line rasterizing algorithm,
scan converting then

1. Uses the line algorithm in $y$ on the edges of the triangle.
    Between the three edges, this will result in either 2 or 0 points for each integer $y$.

1. Uses the line algorithm in $x$ between pairs of edge points with the same $y$.
    This results in every point that has integer $x$ and $y$ inside the triangle,
    which is the task of rasterization.

There are two line rasterizing algorithms that are often used in scan conversion,
[DDA] and [Bresenham].

There is a need to handle edge cases specially here:
if one line segment ends where another begins and they meet at an integer coordinate,
we want to ensure that one line but not the other will find the integer coordinate where they meet.
Traditionally, we do that by
including the small-number endpoint:
a line rasterizer going between $(2,5)$ and $(7,-3)$ finding integer $x$s will include $(2,5)$ but not $(7,-3)$;
finding integer $y$'s the same algorithm will include $(7,-3)$ but not $(2,5)$.
If the endpoint are not integers, this special small-but-not-big rule doesn't arise.

## DDA

<abbr>DDA</abbr>, short for Digital Differential Analyzer, can be described
as a vector-based line rasterizing algorithm for floating-point numbers.
Its name and design long predate computer graphics,
appearing in the late 1940s as a hardware design
and being ported to software not long afterward.

As a line-drawing algorithm, DDA in $x$ runs as follows:

1. Let $\mathbf p$ be the endpoint of the segment with smaller $x$ and $\mathf q$ be the other endpoint.
2. Find a vector parallel to the line segment that has $1$ in its $x$ coordinate.
3. Find the point on the line segment with $x = \lceil p_x\rceil$.
4. Repeatedly add the vector to the point until the point's $x$ reaches or passes $q_x$.

The points found (except the last one that passed $q_x$) are the points on the line segment with integer $x$ coordinates.

Step 1 is a simple comparison.

Step 2 is a subtraction and scaling: $\dfrac{\mathbf q - \mathbf p}{q_x - p_x}$.

Step 3 is the least obvious part, but isn't hard once you see the trick.
We want a point that has an $x$ that is $\lceil p_x\rceil - p_x$ past $\mathbf p$,
and we have a vector (found in step 2) that has $x=1$,
so if we add $\lceil p_x\rceil - p_x$ times that vector to $\mathbf p$ we get the point we want.

Step 4 is a simple while loop.


:::example
Consider using DDA to step in $y$
from $(1.1, 1.8)$ to $(5, 12.2)$.

1. $\mathbf p = (1.1, 1.8)$ and $\mathbf q = (5, 12.2)$
2. $\dfrac{\mathbf q - \mathbf p}{q_y - p_y} = (0.375, 1)$
3. $\lceil p_y\rceil - p_y = 0.2$ so we add $0.2(0.375, 1)$ to $\mathbf p$ to get $(1.175, 2)$
4. Keep adding $(0.375, 1)$ to that point to get
    - $(1.175, 2)$
    - $(1.55, 3)$
    - $(1.925, 4)$
    - $(2.3, 5)$
    - $(2.675, 6)$
    - $(3.05, 7)$
    - $(3.425, 8)$
    - $(3.8, 9)$
    - $(4.175, 10)$
    - $(4.55, 11)$
    - $(4.925, 12)$
    
    The next point, $(5.3, 13)$, has a $y > 12.2$ so it is not included and we stop looping
:::

DDA is easy to implement and extends naturally to any number of dimensions.
It can also step in any axis by picking a different coordinate instead of $x$.
However, it involves a division operation, which approximate when using floating-point numbers,
and that approximation is compounded as the loop iterates,
which means that DDA is not ideal for precise rendering.


## Bresenham

Bresenham's algorithm was introduced by Jack Elton Bresenham explicitly to be an improvement on DDA.
He did not immediately publish it,
instead using it as part of a work project in 1962,
sharing it with friends shortly thereafter,
talking about it in a conference in 1963,
and finally publishing it in the IBM Systems Journal in 1965.

Bresenham's algorithm was originally posed only for integer values,
but was almost immediately adapted to fixed-point numbers as well.
The core ideas used in Bresenham's algorithm inspired many other algorithms
for drawing circles and other curves, but those extensions have not proved as useful to modern 3D graphics
as they were in early memory-constrained 2D graphics.

The integer version of the algorithm stepping in $x$ runs as follows:

1. Let $\mathbf p$ be the endpoint of the segment with smaller $x$ and $\mathf q$ be the other endpoint.

2. Compute the displacement vector $\vec d = \mathbf q - \mathbf p$

3. Divide each coordinate of $d$ by $d_x$, keeping the integer quotients in $\vec i$ and the remainders in $\vec r$.

    This should be flooring division, so that $\vec r$ contains only positive numbers.
    Thus $5 \div 3$ is $1$ remainder $2$, while $-5 / 3$ is $-2$ remainder $1$.

4. Initialize the accumulated error vector $\vec e = (0, 0, ... 0)$^[Some sources use $\vec r / 2$ instead, which saves work if the pixels found were to be later rounded to integer values in all coordinates but is less helpful for scan conversion.] and the pixel $\mathbf a = \mathbf p$

5. Repeatedly
    a. add $\vec i$ to $\mathbf a$
    b. add $\vec r$ to $\vec e$
    c. for each coordinate of $\vec e$ that is larger than $d_x$,
        add $1$ to that coordinate of $\vec i$ and subtract $d_x$ from that coordinate of $\vec e$
    d. the point $\vec i + \dfrac{\vec r}{d_x}$ is on the line

Extending Bresenham to work with fixed-point numbers
is equivalent to taking steps integer steps larger than 1,
effectively by computing $\vec i$ and $\vec r$ as $k \vec d \div d_x$ in step 3 above
where $k$ is the multiplier needed to turn a fixed-point number into an integer.
There may also be an initial offset set to reach an integer value, just as there is with DDA,
which can be found by using a similar computation as with $\vec i$ and $\vec a$
but using the offset needed to reach an integer instead of $k$.

:::example
Consider using Bresenham to step in $y$
from $(1.1, 1.8)$ to $(5, 12.2)$,
where we're using base-10 fixed-point numbers with one digit to the right of the decimal place.

1. We treat these numbers as integers by multiplying by $k = 10$ to get $\mathbf p = (11, 18)$ and $\mathbf q = (50, 122)$
2. $\vec d = (39, 104)$
3. The division is of $10(39, 104)$, meaning $(390, 1040) \div 104$, which gives $\vec i = (3, 10)$ and $\vec r = (78, 0)$
4. $\vec e = (0,0)$ and $\vec a = (11, 18)$

    Because $y$ in fixed point is 1.8, which is not an integer, we need to find a point that is by adding 2 (or fixed-point 0.2) to it.
    To find that offset, we do the same we did in step 3 but with $2$ instead of $10$ as a numerator multiplier:
    $(78, 208) \div (104)$ gives integer offset to $a$ of $(0,2)$ and new $\vec e$ of the remainder, $(78, 0)$.
    
    $\vec e = (78,0)$ and $\vec a = (11, 20)$ represents the point $(1.1 + \frac{78}{1040} = 1.175, 20)$, the same point found during DA
    
5. The loop finds
    -   $\vec a = (14,30)$\
        $\vec e = (156,0)$\
        because $156 \ge 104$, $a_x = 15$ and $e_x = 52$\
        the point $(1.5 + \frac{52}{1040} = 1.55, 3)$ is on the line
    
    -   $\vec a = (18,40)$\
        $\vec e = (130,0)$\
        because $130 \ge 104$, $a_x = 19$ and $e_x = 26$\
        the point $(1.9 + \frac{26}{1040} = 1.925, 4)$ is on the line

    -   $\vec a = (22,50)$\
        $\vec e = (104,0)$\
        because $104 \ge 104$, $a_x = 23$ and $e_x = 0$\
        the point $(2.3 + \frac{0}{1040} = 2.3, 5)$ is on the line

    -   $\vec a = (26,60)$\
        $\vec e = (78,0)$\
        the point $(2.6 + \frac{78}{1040} = 2.675, 6)$ is on the line
        
    -   $\vec a = (29,70)$\
        $\vec e = (156,0)$\
        because $156 \ge 104$, $a_x = 30$ and $e_x = 52$\
        the point $(3.0 + \frac{52}{1040} = 3.05, 7)$ is on the line
    
    -   $\vec a = (33,80)$\
        $\vec e = (130,0)$\
        because $130 \ge 104$, $a_x = 34$ and $e_x = 26$\
        the point $(3.4 + \frac{26}{1040} = 3.425, 8)$ is on the line

    -   $\vec a = (37,90)$\
        $\vec e = (104,0)$\
        because $104 \ge 104$, $a_x = 38$ and $e_x = 0$\
        the point $(3.8 + \frac{0}{1040} = 3.8, 9)$ is on the line

    -   $\vec a = (41,100)$\
        $\vec e = (78,0)$\
        the point $(4.1 + \frac{78}{1040} = 4.175, 10)$ is on the line

    -   $\vec a = (44,110)$\
        $\vec e = (156,0)$\
        because $156 \ge 104$, $a_x = 45$ and $e_x = 52$\
        the point $(4.5 + \frac{52}{1040} = 4.55, 11)$ is on the line
    
    -   $\vec a = (48,120)$\
        $\vec e = (130,0)$\
        because $130 \ge 104$, $a_x = 49$ and $e_x = 26$\
        the point $(4.9 + \frac{26}{1040} = 4.925, 12)$ is on the line
:::


Because Bresenham operates without floating-point numbers,
it was significantly more efficient than DDA when it was first introduced.
That performance gap has since closed on CPUs with improved floating-point hardware,
while GPUs added SIMT and switched to edge-function rasterization,
meaning Bresenham's main advantage over DDA today is its lack of rounding errors.


## Perspective-correct

Both DDA and Bresenham are optimized based on the regular spacing of pixels in 2D.
That regularity does not apply directly to interpolating values over the 2D projection of 3D surfaces.

To understand why simple interpolation does not work, recall that perspective causes more distant things to be smaller in their projection.
This includes the more distance parts of a single object:
if you view a wall from near one end of the wall,
the more distant half of the wall looks much smaller than the closer part,
meaning the middle of the wall in 3D space
is not in the middle in your view of the wall.

<figure>
<svg viewBox="-2 -3.2 9 6.4" style="max-width:22.5em">
<g fill="none" stroke="black" stroke-width="0.03"> <path d="M -1.5,-1 -1.5,1 1.5,3 1.5,-3 Z"></path> <path d="M -0.75,-1.5 v 3"></path> <path d="M 0,-2 v 4"></path> <path d="M 0.75,-2.5 v 5"></path> </g> <g fill="none" stroke="black" stroke-width="0.03" transform="translate(5,0)"> <path d="M -1.5,-1 -1.5,1 1.5,3 1.5,-3 Z"></path> <path d="M -0.75,-1.5 v 3"></path> <path d="M 0,-2 v 4"></path> <path d="M -1.2,-1.2 v 2.4"></path> </g>
</svg>
<figcaption>
On the left is a trapezoid divided at equally-spaced points in $x$ using linear interpolation.
On the right is a rectangle seen in perspective, divided at equally-spaced points along its length.
Note that the middle of the wall appears much closer to the far end than the near end,
while the middle of the trapezoid does not have that property.
</figcaption>
</figure>

The scanline rasterization algorithm achieves perspective
by first dividing $x$ and $y$ coordinates by the depth coordinate $w$.
To achieve correct 3D interpolation, we have to divide everything else by $w$ too,
even things like color that don't reduce with distance.
After interpolating these other properties down to their final pixel coordinates
we then undo the division by $w$ by dividing again, this time by an interpolated $1 / w$.

In practice, we often have a supplied vertex coordinate $(x,y,z,w,a_1,a_2,a_3)$
where the $a$ values are barycentric coordinates.
We first perform perspective projection in $x$ and $y$ by dividing by $w$;
we also divide everything else by $w$ while we're at it, getting
$\left(\dfrac{x}{w},\dfrac{y}{w},\dfrac{z}{w},\dfrac{1}{w},\dfrac{a_1}{w},\dfrac{a_2}{w},\dfrac{a_3}{w}\right)$.
Note that $w$ is replaced by $1 \div w$ not $w \div w$.
We use these divided coordinates in DDA to get a pixel coordinate
$(x',y',z',w',a_1',a_2',a_3')$.
The $x'$ and $y'$ are the correct pixel $x$ and $y$
and the $z'$, also being a spatial coordinate, is the depth we use in the depth buffer,
but the rest of the coordinates had a spurious division by $w$ which we now undo
to get
$\left(x',y',z',\dfrac{1}{w'},\dfrac{a_1'}{w'},\dfrac{a_2'}{w'},\dfrac{a_3'}{w'}\right)$.

:::example
Hyperbolic interpolation

Consider the two points $(12,0,6,\mathbf{3}, 0.15, 0.3, 0)$ and $(2,0,-6,\mathbf{1}, 0, 0.3, 0.15)$.

Division by $w$ gives $(4,0,2,\mathbf{\frac{1}{3}}, 0.5, 0.1, 0)$ and $(2,0,-6,\mathbf{1}, 0, 0.3, 0.15)$.

Interpolation to the midpoint gives $(3,0,-2,\mathbf{\frac{2}{3}}, 0.25, 0.20, 0.075)$.

Division of the post-$w$ coordinated by the interpolated $w'$ and inversion of $w'$ gives $(3,0,-2,\mathbf{1.5},0.375,0.3,0.1125)$.
:::

If we scan convert with DDA, this division is performed directly on the floating-point numbers.
If we scan convert with Bresenham, the division can be incorporated into the overall integer division with remainder approach.

This division-based approach to perspective-correct scan conversation
was introduced by Jim Blinn in 1992^[James F. Blinn, "Hyperbolic Interpolation," in *IEEE Computer Graphics and Applications*, vol. 12, no. 4, pp. 89-94, July 1992. DOI: [10.1109/MCG.1992.10028](https://doi.org/10.1109/MCG.1992.10028).] under the name **hyperbolic interpolation**, based on the correlation between division by $w$ and hyperbolic geometry.



# Edge-function rasterization

Unlike scan converting, edge-function rasterization is designed with GPUs in mind.
In particular, it works well with SIMT:
it sets up a large number of computations and executes them in parallel with a single control unit.

The core of all edge-function rasterization approaches
is the creation of three functions, one for each edge of the triangle.
Each function is positive for points on the inside part of that edge
and negative for points on the outside part,
meaning a pixel is drawn if and only if all three functions are positive.
In many cases, the functions are chosen not just to be positive inside the triangle
but to evaluate to the exact barycentric coordinate of the vertex opposite the edge.

The edge functions have several forms depending on their exact application,
but a commonly used one was proposed by Marc Olano and Trey Greer in 1997^[Marc Olano and Trey Greer. 1997. "Triangle scan conversion using 2D homogeneous coordinates." In *Proceedings of the ACM SIGGRAPH/EUROGRAPHICS workshop on Graphics hardware (HWWS '97)*. Association for Computing Machinery, New York, NY, USA, 89–95. DOI: [10.1145/258694.258723](https://doi.org/10.1145/258694.258723)].
What follows is a brief summary of this approach.

First, multiply each vertex by a view and projection matrix
to place it in what they call "canonical eye space"
meaning in $(x, y, w)$ there's a 90° field of view from the origin down the $w$ axis.

Next, we want to find a 3×3 matrix
which can convert any $(x,y,w)$ pixel location into the barycentric coordinates of that pixel.
In other words, the matrix we are looking for (let's call it $M$)
times vertex $\mathbf v_1$
should be $(1,0,0)$;
times vertex $\mathbf v_2$
it should be $(0,1,0)$;
and times vertex $\mathbf v_3$
it should be $(0,0,1)$.
$$
M \begin{bmatrix}v_{1 x}&v_{2 x}&v_{3 x}\\v_{1 y}&v_{2 y}&v_{3 y}\\v_{1 w}&v_{2 w}&v_{3 w}\end{bmatrix}
= \begin{bmatrix}1&0&0\\0&1&0\\0&0&1\end{bmatrix}
$$
This means that $M$ is the inverse of a matrix
made from the three vertices of the triangle.

3×3 matrix inverses are readily computed directly using a formula based on the adjugate matrix and determinant.
However, not all matrices are invertible.
For triangle edge functions, the matrix is invertible if and only if
the triangle has non-zero area when rendered,
so we can check for singular matrices and simply not draw those triangles.

Matrix inverses may not be numerically stable:
triangles with a very small but non-zero rendered area can create significant errors in computation.
To avoid this, it is common to round the vertex $(x,y,w)$ coordinates
to some sub-pixel but still fairly course resolution.
This rounding ensures that triangles cannot have super small areas:
they're either exactly zero or they're large enough to compute safely.

Because all of this work was done in homogeneous coordinates,
the result is perspective-correct but may not be correctly scaled;
recall that by definition, homogeneous vectors may be multiplied by any scalar without changing their meaning,
and this process ends up applying differentsuch scalars to different pixels.
To correct for that, we must do two things:

- After finding the barycentric coordinates of a pixel, normalize the result by dividing by the sum of the three barycentric coordinates.

- When making the matrix, normalize the three vertices to all have the same $w$ (usually chosen to be $w = 1$).

Because the input matrix is normalized,
we actually find the inverse of $$\begin{bmatrix}v_{1 x}&v_{2 x}&v_{3 x}\\v_{1 y}&v_{2 y}&v_{3 y}\\1&1&1\end{bmatrix}$$
and those known $1$ values can simplify the inverse computation.
Because we will normalize the scale of each resulting barycentric coordinate,
we also don't need to do the normalizing division by the matrix's determinant that is typically part of creating the adjugate matrix.
Combining these optimizations, we have
$$
\begin{bmatrix}v_{1 x}&v_{2 x}&v_{3 x}\\v_{1 y}&v_{2 y}&v_{3 y}\\1&1&1\end{bmatrix}^{-1} =
k
\begin{bmatrix}
v_{2 y}-v_{3 y} & v_{3 x}-v_{2 x} & v_{2 x}v_{3 y}-v_{3 x}v_{2 y}\\
v_{3 y}-v_{1 y} & v_{1 x}-v_{3 x} & v_{3 x}v_{1 y}-v_{1 x}v_{3 y}\\
v_{1 y}-v_{2 y} & v_{2 x}-v_{1 x} & v_{1 x}v_{2 y}-v_{2 x}v_{1 y}\\
\end{bmatrix}
$$
where $k$ is based on the matrices' determinant but can be ignored: whatever $k$ we pick will be removed later when normalizing the barycentric coordinates.

Overall, the cost of this approach is

| Per | Operations |
|-----|------------|
| Vertex | one 4×4 matrix by 4-vector multiply (4 `*+` and 4 `+-`) |
| Triangle | one simplified adjugate (2 `*+` and 2 `+-`) |
| Pixel | one 3×3 matrix by 3-vector multiply (3 `*+` and 3 `+-` <br> 3 sign checks (3 `?:`) |
| Fragment | one barycenter normalization (1 `1/` and 1 `+-`) <br> one weighted sum per interpolated value (1 `*+` and 1 `+-` per value) |

The per-pixel cost above is per pixel checked, not per resulting fragment.
A naive implementation checks every pixel on the screen
or in the screen-space bounding box of the triangle,
but this can be avoided by applying the algorithm hierarchically.
The details of this hierarchical check vary, but a common model is

- Build an hardware array that checks a 16×16 grid of pixels in parallel.
- Render a slightly larger triangle to a temporary image with pixels 16× as large as the final image (1/256 as may pixels overall).
- Check the 16×16 block of full-resolution pixels that correspond to each pixel found in the temporary image.
 
The "slightly larger" detail is to ensure that a block of pixels that the triangle just grazes
is detected and rendered at higher resolution.
Algorithms that guarantee this are called <dfn>conservative</dfn>,
and conservative versions of both scanline and edge function algorithms exist,
based on computing both $x$ and $y$ steps separately (for Bresenham)
or offsetting the edge functions by a pixel radius (for edge functions).
Conservative rasterization algorithms typically do not provide correct barycentric coordinates.

<details class="aside"><summary>The origins of conservative edge functions</summary>

In February 2004, Tomas Akenine-Möller and Timo Aila released [a PDF](https://fileadmin.cs.lth.se/graphics/research/papers/2005/cr/_conservative.pdf) entitled "A Simple Algorithm for Conservative and Tiled Rasterization"
which contained the first known full and efficient algorithm for conservative edge function rasterization.
But this PDF was never published in a peer-reviewed venue.

In 2005, NVIDIA's in-house publication *GPU Gems 2*
included an article ["Conservative Rasterization"](https://developer.nvidia.com/gpugems/gpugems2/part-v-image-oriented-computing/chapter-42-conservative-rasterization)
by Jon Hasselgren, Tomas Akenine-Möller, and Lennart Ohlsson.
In that article Akenine-Möller and Aila's algorithm is explained with this lead-in note:

> we use an alternative interpretation of a simple test for conservative rasterization (Akenine-Möller and Aila, forthcoming).

In other words, at the time that *GPU Gems 2* was published, they expected Akenine-Möller and Aila's paper to be published later in a reference they could cite.
But it was not, which likely suggests a failure of the peer review process.
I say failure of the process, not the paper,
because Akenine-Möller and Aila's algorithm has become the standard for hierarchical edge-function rasterization
and has been incorporated into every GPU whose rasterization process I've found described since then.

</details>

## Bound and Check

All of the methods above are optimized for large triangles.
Even though many scenes contain many small triangles,
they also tend to contain many large triangles
and that optimization generally makes sense.

The team working on Unreal Engine 5's Nanite engine
successfully created a system that can deliver scenes approaching 1 triangle per pixel.
At that scale, they found a need to rasterize triangles differently.

Broadly, their approach kept edge functions,
but simplified to discard some of the perspective-correct interpolation details found in hardware implementations
and reposed to be updated iteratively in a loop over pixels instead of re-computed from scratch at each pixel.
They also applied it over a per-triangle bounding box,
deferring any triangle with a large bounding box to the regular hardware rasterizer.

Arguably, nothing in this bound and check model is novel;
the simplified edge functions and iterative updates were proposed by Juan Pineda in 1988^[Juan Pineda. 1988. "A parallel algorithm for polygon rasterization." In *Proceedings of the 15th annual conference on Computer graphics and interactive techniques (SIGGRAPH '88)*. Association for Computing Machinery, New York, NY, USA, 17–20. DOI: [10.1145/54852.378457](https://doi.org/10.1145/54852.378457)]
and were a direct predecessor to the homogeneous version Olano and Greer published nine years later,
and the idea of checking pixels in bounding boxes is as old as raster computer graphics.
What was surprising was that handling small triangles this way in software
provided several-fold speedups for their scenes over using dedicated hardware rasterizers.





