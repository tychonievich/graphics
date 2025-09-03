---
title: DDA (and Bresenham)
summary: Implementing the rasterization of lines and triangles.
...

<details class="tldr"><summary>Summary of rasterization process:</summary>
1. We use $n$-dimensional vectors, like $(x,y,z,w,r,g,b,a,s,t)$, and do almost all math on the entire vector.
2. DDA finds all points on a line segment that have an integer in one specific coordinate.
3. Scanline finds all ($n$-dimensional) points inside a triangle that have integer $(x,y)$ coordinates by
    - using DDA on the edges to find points with integer $y$ coordinates
    - using DDA between pairs of edge points with the same $y$ to find points with integer $(x,y)$ -- these are the ones we plot as pixels
3. DDA is good in software; Bresenham does similar work but uses fewer transistors in hardware.
4. We divide $x$ and $y$ by $w$ to achieve perspective
    - ... but that makes $(r,g,b)$ and so on not match the $\left({x \over w},{y \over w}\right)$, so we divide the entire vector by $w$ before doing DDA
    - ... but that makes DDA find $\left({r \over w},{g \over w},{b \over w}\right)$ so we undo the division at the end, using $\left({r \over w}/{1 \over w},{g \over w}/{1 \over w},{b \over w}/{1 \over w}\right)$ as the color to plot
</details>

# DDA (Software)

Triangles are rasterized by finding all of the integer-coordinate points inside the three edges of the triangle[^abut].
For each such point, we also wish to interpolate an arbitrary number of other values to that point.
We can both find these points and interpolate to them very efficiently using either the **DDA** algorithm or its rational-number cousin the **Bresenham** algorithm.
As both are similar and you're likely more familiar with working in real numbers than in rational numbers, we'll discuss DDA here.


[^abut]:
    Because abutting triangles are often used to represent more complicated shapes,
    special care is taken to insure abutting triangles draw each pixel exactly once.
    In particular, if an edge passes through an integer coordinate point $(x,y)$,
    the point is considered "inside" the triangle if either $(x+\epsilon,y)$ is inside and not on an edge or if $(x+\epsilon,y)$ is inside on an edge and $(x+\epsilon,y+\epsilon)$ is inside and not on an edge, for infinitesimally small positive $\epsilon$.
    
    In the DDA algorithm, this abutment-handling rule
    informs the $<$ (instead of $\le$) condition of the loop,
    the ordering of $\vec a$ and $\vec b$ and the resulting use of $s_d = 1$ (instead of $-1$),
    and the computation of $e$ using ceiling (instead of floor).

The DDA algorithm takes an $n$-dimensional line segment, specified by its two the $n$-vector end points, and finds all points on that line segment that have an integer coordinate in one particular dimension.

:::algorithm
DDA

Officially, DDA stands for "digital differential analyzer" but I've never heard that name used except in explanatory texts like this one. It's always called "DDA", "the DDA algorithm," or "the DDA line-drawing algorithm."

Input
:   - Two $n$-dimensional endpoints, $\vec a$ and $\vec b$
    - The dimension $d$ that should have integer coordinates

Product
:   - Finds all points $\vec p$ between $\vec a$ and $\vec b$ where $p_d$ is an integer

Process
:   *Setup:*
    
    1. If $a_d = b_d$, return (no points found)
    2. If $a_d > b_d$, swap $\vec a$ and $\vec b$
    3. Let $\vec \Delta = \vec b - \vec a$
    4. Let $\vec s = \vec \Delta \div \Delta_d$

    *Find the first potential point:*
    
    5. Let $e = \lceil a_d \rceil - a_d$
    6. Let $\vec o = e \vec s$
    7. Initialize $\vec p$ as $\vec a + \vec o$
    
    *Find all points:*
    
    8. While $p_d < b_d$ repeat:
        i. found point $\vec p$
        ii. add $\vec s$ to $\vec p$

Discussion
:   Working backwards,

    Given a point $\vec p$ on the line segment with integer $p_d$,
    $\vec p + \vec s$ is the next point on the line segment with integer $p_d$
    as long as both $\vec s$ is aligned with the segment
    and $s_d = 1$.
    So once we have one $\vec p$ and $\vec s$, we just loop through adding $\vec s$ to $\vec p$ until we leave the segment (8).
    
    To get $\vec s$ we start with a vector aligned with the line segment by simple subtraction (3)
    and then get $s_d = 1$ by dividing the entire vector by whatever it's $d$ coordinate is (4).

    Any time we have division, we have to consider division by zero.
    In this case division by zero would happen if the line has no extent in the $d$ direction, meaning there are either $0$ or $\infty$ points on the line with integer $d$;
    in either case, we can simply return as there are no meaningful points to find (1).
    
    To get the initial $\vec p$
    we need to figure out how far the starting end of the segment is from an integer $d$ coordinate ($e$, 5)
    make a vector offset that will move us to that point
    ($\vec o$ with $o_d = e$, 6)
    and add that offset to the starting end of the segment (7).
    
    All of this assumes we were stepping in the positive $d$ direction,
    so we swap the order of the segment endpoints if needed to make sure that's the case (2).
:::

The **scanline** algorithm uses DDA to find the pixels in a triangle
by first using DDA in $y$ (i.e., finding points with integer $y$ values)
on the three edge line segments;
then using DDA in $x$ between pairs of points found this way that share the same $y$ value.

<figure>
<svg viewBox="-4.2 -2.7 9.5 6.0" style="max-width:35em; display:table; margin:auto;">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0,0 10,5 0,10 5,5 z" /></marker>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5"><circle cx="5" cy="5" r="5" /></marker>
<marker id="err" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 4,5 0,10 5,6 10,10 6,5 10,0 5,4 Z" /></marker>
</defs>
<circle cx="-2.25" cy="-0.5" r="0.1"/>
<circle cx="4.5" cy="-2.5" r="0.1"/>
<circle cx="2.2" cy="2.5" r="0.1"/>
<g style="stroke:black; fill:none; stroke-width:0.02">
<path stroke-width="0.01" d="M-2.25,-0.5 4.5,-2.5 2.2,2.5 Z" />
<rect x="2.6" y="-2.4" width="0.8" height="0.8"/>
<rect x="3.6" y="-2.4" width="0.8" height="0.8"/>
<rect x="-0.4" y="-1.4" width="0.8" height="0.8"/>
<rect x="0.6" y="-1.4" width="0.8" height="0.8"/>
<rect x="1.6" y="-1.4" width="0.8" height="0.8"/>
<rect x="2.6" y="-1.4" width="0.8" height="0.8"/>
<rect x="-1.4" y="-0.4" width="0.8" height="0.8"/>
<rect x="-0.4" y="-0.4" width="0.8" height="0.8"/>
<rect x="0.6" y="-0.4" width="0.8" height="0.8"/>
<rect x="1.6" y="-0.4" width="0.8" height="0.8"/>
<rect x="2.6" y="-0.4" width="0.8" height="0.8"/>
<rect x="-0.4" y="0.6" width="0.8" height="0.8"/>
<rect x="0.6" y="0.6" width="0.8" height="0.8"/>
<rect x="1.6" y="0.6" width="0.8" height="0.8"/>
<rect x="1.6" y="1.6" width="0.8" height="0.8"/>
</g>
<g style="stroke:green; fill:none; stroke-width:0.04" marker-mid="url(#arrow)" marker-end="url(#err)">
<path d="M 2.8125,-2 -0.5625,-1, -3.9375,0" />
<path d="M 4.27,-2 3.81,-1 3.35,0 2.89,1 2.43,2 1.97,3" />
<path d="M -1.508333,0 -0.025,1 1.458333333,2 2.941666666,3" />
</g>
<g style="stroke:blue; fill:none; stroke-width:0.04">
<path d="M 4.5,-2.5 2.8125,-2" marker-end="url(#arrow)"/>
<path d="M 4.5,-2.5 4.27,-2" marker-end="url(#arrow)"/>
<path d="M -2.25,-0.5 -1.508333,0" marker-end="url(#arrow)"/>
</g>
<g style="stroke:purple; fill:none; stroke-width:0.03" marker-mid="url(#dot)" marker-start="url(#dot)" marker-end="url(#err)">
<path d="M 3,-2 h 1 1"/>
<path d="M 0,-1 h 1 1 1 1"/>
<path d="M -1,0 h 1 1 1 1 1"/>
<path d="M 0,1 h 1 1 1"/>
<path d="M 2,2 h 1"/>
</g>
<g style="stroke:red; fill:none; stroke-width:0.03">
<path d="M 2.8125,-2 3,-2"/>
<path d="M -0.5625,-1 0,-1"/>
<path d="M -1.508333,0 -1,0"/>
<path d="M -0.025,1 0,1"/>
<path d="M 1.458333,2 2,2"/>
</g>
</svg>
<figcaption>
Rasterization of a triangle by first DDA-stepping the edges in $y$, then DDA-stepping between points on the edges in $x$.
Using the notation in the DDA algorithm above:
[blue]{style="color:blue"} lines are $\vec o$ in $y$
and [green]{style="color:green"} lines are $\vec s$ in $y$;
[red]{style="color:red"} lines are $\vec o$ in $x$
and [purple]{style="color:purple"} lines are $\vec s$ in $x$.
</figcaption>
</figure>


:::algorithm
Scanline

Scanline rendering is a generic term for any algorithm that draws triangles or other surfaces
one horizontal row of pixels or "scanline" at a time.
Originally designed to render on raster-path cathode ray tubes without requiring a separate frame buffer,
they survived the transition to framebuffer rasterizers in part because of their cache locality.

Input
:   - Three $n$-dimensional endpoints, $\vec p$, $\vec q$, and $\vec r$

Product
:   - Finds all points $\vec p$ inside the triangle with vertices $\vec p$, $\vec q$, and $\vec r$ which have integer $x$ and $y$ coordinates

Process
:   *Setup:*
    
    1. Let $\vec t$ be the top point of $\{\vec p, \vec q, \vec r\}$ (i.e. with the smallest $y$ value)
    2. Let $\vec b$ be the bottom point of $\{\vec p, \vec q, \vec r\}$ (i.e. with the biggest $y$ value)
    3. Let $\vec m$ be the remaining point of $\{\vec p, \vec q, \vec r\}$ (i.e. with the middle $y$ value)
    4. Run DDA steps 1--7 to setup for the line $\vec t$ to $\vec b$ with $d$ being the $y$ axis.
        This is for the long edge ($\vec t$ to $\vec b$) so we'll label its vectors
        $\vec p_\text{long}$ and $\vec s_\text{long}$.
        
        If it returns in DDA step 1, return (no points found)
    
    *Find points in the top half of the triangle:*

    5. Run DDA steps 1--7 to setup for the line $\vec t$ to $\vec m$ with $d$ being the $y$ axis
        to find $\vec p$ and $\vec s$ for one edge of the top-half triangle.
    6. *Do the DDA loop (DDA step 8) for both $\vec p$ and $\vec p_\text{long}$ at the same time:*
    
        While $p_y < m_y$ repeat:
        
        i. Run DDA in $x$ to find points on the line with endpoints $\vec p$ and $\vec p_\text{long}$   *← this DDA finds pixels; plot them on the image*
        ii. add $\vec s$ to $\vec p$
        iii. add $\vec s_\text{long}$ to $\vec p_\text{long}$

    *Find points in the bottom half of the triangle:*

    7. Run DDA steps 1--7 to setup for the line $\vec m$ to $\vec b$ with $d$ being the $y$ axis
        to find $\vec p$ and $\vec s$ for one edge of the bottom-half triangle.
    8. *Do the DDA loop (DDA step 8) for both $\vec p$ and $\vec p_\text{long}$ at the same time:*
    
        While $p_y < b_y$ repeat:
        
        i. Run DDA in $x$ to find points on the line with endpoints $\vec p$ and $\vec p_\text{long}$   *← this DDA finds pixels; plot them on the image*
        ii. add $\vec s$ to $\vec p$
        iii. add $\vec s_\text{long}$ to $\vec p_\text{long}$
    

Discussion
:   We're finding all the pixels inside a triangle.
    We do this with nested DDA:
    we DDA in one direction to find points along the edges of the triangle,
    then DDA in another direction between those edge points to find points inside the triangle.
    
    Because of memory layout, it is fastest if the innermost loop is in $x$,
    so the edge loop will be in $y$ and the fill loop in $x$.

    First, we'll sort the points in $y$ (1--3).
    
    We'll use this order to consider the triangle in two parts:
    the pixels that lie above the middle point
    and thus between the top-to-middle edge and the top-to-bottom edge;
    and those that lie below it the middle point
    and thus between the middle-to-bottom edge and the top-to-bottom edge.
    
    Because the top-to-bottom edge is needed for both parts, we set up DDA for that edge (4).
    We'll also be setting up DDA for other edges
    so we'll add primes to the $\vec p$ and $\vec s$ for this edge
    to distinguish them from the other edges' $\vec p$ and $\vec s$.

    Now we do almost exactly the same work twice,
    just using a different other edge.
    First we find $\vec p$ and $\vec s$ for the top-to-middle edge (5) and DDA the top-half edges (6);
    then we find $\vec p$ and $\vec s$ for the middle-to-bottom edge (7) and DDA the top-half edges (8).
    In both cases we augment the usual DDA loop to update the top-to-bottom edge in lock-step with the other edges (ii--iii),
    ensuring that $\vec p$ and $\vec p_\text{long}$ always have the same $y$ value.
    
    For each same-$y$ pair of edge points $\vec p$ and $\vec p_\text{long}$,
    we DDA in $x$ between them (i) to find the pixels in the triangle.
    Because DDA produces integer coordinates in the dimension it is stepping in,
    these pixels always have integer $x$ and $y$.   
:::


# Bresenham (Hardware)

Bresenham's line algorithm achieves the same results as DDA,
but using only integer values.
Because it uses only integers, it is both faster (integer arithmetic requires less hardware than floating-point hardware)
and more precise (no rounding error) than DDA when implemented in hardware.
It works on integer, rational, and fixed-point endpoints and outputs,
not the floating-point numbers common in CPUs.
Because of its efficiency and precision, it is commonly used in graphics hardware.

Bresenham's line algorithm can be derived by writing out DDA using rational numbers
and tracking the integral and fractional parts of each number separately.
The result is less intuitive and more complicated code than DDA,
but simpler and smaller hardware because the individual components require many fewer transistors.

Jack Elton Bresenham derived this algorithm not as a form of DDA, but rather by considering the implicit equation for a line,
and also showed how it could draw other polynomial curves such as circles.
The polynomial generalizations are suitable for hardware implementation, but are not commonly implemented in hardware today.

# Linear (Simpler)

A naive implementation of DDA or Bresenham performs linear interpolation of values across a line or triangle. That means in particular that if one end of a line is at $x=0$ and has a red value of $r=0$ and the other end is at $x=100$ and has $r=1$ then at $x=50$ the interpolated $r$ will be $0.5$.

While linear interpolation may seem intuitive, it is incorrect when paired with projection.
To see this, consider the following two images:

<figure>
<svg viewBox="-2 -3.2 9 6.4" style="max-width:22.5em">
<g fill="none" stroke="black" stroke-width="0.03">
<path d="M -1.5,-1 -1.5,1 1.5,3 1.5,-3 Z" />
<path d="M -0.75,-1.5 v 3" />
<path d="M 0,-2 v 4" />
<path d="M 0.75,-2.5 v 5" />
</g>
<g fill="none" stroke="black" stroke-width="0.03" transform="translate(5,0)">
<path d="M -1.5,-1 -1.5,1 1.5,3 1.5,-3 Z" />
<path d="M -0.75,-1.5 v 3" />
<path d="M 0,-2 v 4" />
<path d="M -1.2,-1.2 v 2.4" />
</g>
</svg>
<figcaption>
On the left is a trapezoid divided at equally-spaced points in $x$ using linear interpolation.
On the right is a rectangle seen in perspective, divided at equally-spaced points along its length using hyperbolic interpolation.
</figcaption>
</figure>

If we use linear interpolation in 2D screen space, everything looking 2D and flat.
This can be fixed by interpolating in hyperbolic coordinates instead.

# Hyperbolic (More accurate)

In 1992 Jim Blinn wrote [a paper](https://doi.org/10.1109/MCG.1992.10028) explaining how interpolation could be made perspective-correct using something called **hyperbolic interpolation**;
all graphics hardware now uses his approach.

Hyperbolic interpolation assumes that three components of the vector of values at each vertex of a triangle are special.
$x$ and $y$ are special because they correspond to pixel locations;
and $w$ is special because in homogeneous coordinates they are used to create frustums and perspective projection.
It is traditional to also treat $z$ as special because it gives better [depth buffer](other-rasterization.html#depth-buffer) precision for up-close objects where errors would be more visible.

Suppose we have a supplied vertex coordinate $(x,y,z,w,r,g,b,s,t)$.
We first perform perspective projection in $x$ and $y$ by dividing by $w$;
we also divide everyithing else by $w$ while we're at it, getting
$\left(\dfrac{x}{w},\dfrac{y}{w},\dfrac{z}{w},\dfrac{1}{w},\dfrac{r}{w},\dfrac{g}{w},\dfrac{b}{w},\dfrac{s}{w},\dfrac{t}{w}\right)$.
Note that $w$ is replaced by $1 \div w$ not $w \div w$.
We use these divided coordinates in DDA to get a pixel coordinate
$(x',y',z',w',r',g',b',s',t')$.
The $x'$ and $y'$ are the correct pixel $x$ and $y$
and the $z'$ is the depth we use in the depth buffer,
but the rest of the coordinates had a spurious division by $w$ which we now undo
to get
$\left(x',y',z',\dfrac{1}{w'},\dfrac{r'}{w'},\dfrac{g'}{w'},\dfrac{b'}{w'},\dfrac{s'}{w'},\dfrac{t'}{w'}\right)$.

:::example
Hyperbolic interpolation

Consider the two points $(12,0,6,\mathbf{3}, 150, 30, 0)$ and $(2,0,-6,\mathbf{1}, 0, 30, 150)$.

Division by $w$ gives $(4,0,2,\mathbf{\frac{1}{3}}, 50, 10, 0)$ and $(2,0,-6,\mathbf{1}, 0, 30, 150)$.

Interpolation to the midpoint gives $(3,0,-2,\mathbf{\frac{2}{3}}, 25, 20, 75)$.

Division of the post-$w$ coordinated by the interpolated $w'$ and inversion of $w'$ gives $(3,0,-2,\mathbf{1.5},37.5,30,112.5)$.
:::

When integrated with DDA, this means we

1. Divide by $w$.
2. Do the entire DDA, from vertices to edges to interior pixels, on those over-$w$ values.
3. Divide DDA-interpolated non-position coordinates (color, texture coordinates, and so on) at each pixel by the DDA-interpolated $1/w$ to get the value we actually use.
4. Apply any other per-pixel operations like alpha blending, gamma correction, etc.


# Textures

It is common to wish to provide color and other material properties at a different resolution than geometry.
The usual way to realize this is by
(a) interpolating "texture coordinates" to each fragment
and (b) at each fragment looking up the color and so on at those coordinates in an image or array called a "texture".
We have [a separate page on using Textures in WebGL](textures.html)
and one on [various applications of textures](textures2.html);
this section covers only basic texture lookups.

Normalized texture coordinates
:   Most applications of textures assume texture coordinates are normalized to a 0--1 range regardless of texture size.
    Thus, if a texture coordinate is $(0.2, 0.5)$ and the texture image is 300×500 texels^[pixels in a texture are usually called "texels" instead] in size
    then we look up the texel with coordinates $(60, 250)$.

Wrapping
:   There are various options for what to do with a texture coordinate outside the 0--1 range;
    the most common is to wrap them, treating 1.2 as 0.2 and -0.3 as 0.7.

Interpolation and mipmaps
:   Naive texture lookups have a whole range of aliasing problems.
    Full implementations will store multiple sizes of the texture, called [mipmaps](textures.html#mipmaps),
    selecting the size to approximately achieve one texel per fragment,
    and will interpolate between texture sizes and surrounding texels
    to minimize that aliasing.
    The full details are outside the scope of this page.

Replace or combine
:   There are *many* values that could be stored in a texture,
    but simple texture mapping stores object color.
    If the texture contains an alpha channel,
    using that alpha for the fragment can allow parts of a triangle to be transparent and other parts opaque, increasing the apparent complexity of the geometry.
    Sometimes instead the texture is treated as a "decal",
    adjusting the color only for a part of the triangle,
    and the alpha is composited on top of the interpolated object color.

