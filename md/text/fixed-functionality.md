---
title: Things your GPU doesn't let you program
author:
    - Luther Tychonievich
license: CC-BY-SA
see also: 'https://webgl.brown37.net/'
summary: WebGL 2's fixed functionality, including the DDA algorithm and common blending functions.
...

The purpose of this text is to describe the algorithms in the non-programmable part of GPUs circa 2020. These can be categorized into two board categories:

1. Rasterization, which turns primitives into fragments and interpolates values to those fragments.
2. Blending and Masking, which takes many fragments and reduces them into a single pixel.

Both of these have several customizeable options (composing having more than rasterizing), but neither is commonly programmable today.

These fit into the most common 3D rendering pipeline as follows:

1. A variety of artist- and programmer-controlled actions result in a set of primitives to draw.
    - These typically include modeling and transformations, and may also include simulation, tesselation, and fancier projections.
    - Each primitive is a connected set of vertexes; only a few kinds of primitives are supported by any given GPU
    - Vertexes have homogeneous positions and may have any number of other scalar- or vector-valued properties.
2. Rasterization
3. A variety of artist- and programmer-controlled actions convert the interpolated values from each vertex into a set of buffer values for a fragment.
    - These typically include lighting and texturing, and may also include move advanced per-pixel operations.
    - Color (a 4-vector) and depth (a scalar) buffers are common; the stencil buffer (a Boolean or integer) is also sometimes used.
4. Blending and Masking
5. A variety of programmer-controlled post-processing occurs converting the rendered image to a different rendered image.
    - Many programs do nothing here.
    - Lens flair, bloom, and adaptive exposure are done at this stage.
    - Many real-time 3D pipelines lack this stage entirely and fake it using two rendering passes per frame.

# Rasterization

## Triangles (and two more primitives)

GPUs support three (and only three) primitives:
points, line segments, and triangles.

GPU APIs might provide more pseudo-primitives, but if they do so they also describe how those fancier shapes are just shorthand for several of the true primitives.

Triangles are by far the most interesting of the three primitives,
both because their rasterizing algorithms are the most interesting
and because they are the easiest to use in assembling more complicated shapes.




## Clipping

The projection stage is going to divide values by the $w$ component of vertices,
so it is necessary to ensure no $w=0$ vertices remain.
It's also good for both efficiency correctness to discard geometry that would be off-screen when rendered.
Both goals are achieved by clipping primitives in homogeneous coordinates.

Clipping is done with clipping planes.
There are six clipping planes enabled by default, though some GPUs may allow the user to add more.
The six are:
$$\begin{matrix}
-w &\le& x &\le& w\\
-w &\le& y &\le& w\\
-w &\le& z &\le& w\\
\end{matrix}$$
Put another way, vertices are inside the clipping region if the following results in a vector of non-negative numbers:
$$\begin{bmatrix}
1&0&0&1\\
-1&0&0&1\\
0&1&0&1\\
0&-1&0&1\\
0&0&1&1\\
0&0&-1&1\\
\end{bmatrix} \begin{bmatrix}
x\\y\\z\\w
\end{bmatrix}$$
This second form is useful because each of the six resulting numbers is a signed distance from one of the six clipping planes, and signed distances make finding intersection points easy.

Vertices that violate any one of the inequalities are discarded.
Vertices that satisfy all six of the inequalities are kept.
Edges that connect a kept and discarded vertex result in the creation of a new vertex that lies exactly on the clipping plane,
potentially changing the number of vertices in the primitive.

:::example
The edge with endpoints $(1,2,3,4)$ and $(4,1,-1,2)$ crosses the $x \le w$ clipping plane (because $1<4$ but $4 \not<2$).

Rewriting the plane $x \le w$ as a plane distance equation we get $1x + 0y + 0z - 1w \le 0$.
Plugging in the two vertices, we get distances $-3$ and $2$, respectively.
Our new point is thus
$$\begin{split}
&\;\dfrac{\big(2(1,2,3,4))-\big(-3(4,1,-1,2)\big)}{2-(-3)}\\
=&\;
\dfrac{(2,4,6,8)+(12,3,-3,6)}{5}\\
=
&\;(2.8,1.4,0.6,2.8)
\end{split}$$
This point lies on the plane ($2.8 = 2.8$) and on the edge (being a linear combination of $(1,2,3,4)$ and $(4,1,-1,2)$).
:::

Clipping is partly an optimization: it means out-of-view object are never rendered.
But it also has correctness properties,
preventing division-by-zero errors during projection
and removing numerical instabilities caused when dividing a large number by a small number.

## Projection

Any conversion of 3D coordinates onto a 2D plane is called a *projection*.
Many projections can be defined, but GPUs support only those that convert all straight 3D lines into straight 2D lines.
Conveniently, all of these can be defined using homogeneous coordinate normalization.

Homogeneous coordinates are used for various purposes;
for the purpose of projections, they have an auxiliary $w$ coordinate appended to the 3D $(x,y,z)$ coordinates, where $w$ is a divisor: the projected coordinate to draw is actually $\left(\frac{x}{w},\frac{y}{w}\right)$ (with $\frac{z}{w}$ as a "depth" component, used by the [depth buffer]).
With this single rule we can create several kinds of projections by setting $w$s in different ways.

### Orthographic

If all $w=1$ then division by $w$ does nothing and we achieve an orthographic projection.
Orthographic projections used for blueprints, maps, birds-eye views, and other images where the projected size of an object should be independent from its distance from the camera.

### Perspective

We view the 3D world from a point inside that world, with closer objects appearing larger than more distant objects.

A naive approach to implementing this would be to have $w$ be the distance a vertex is from that viewing point.
That, however, will not work in practice: division by $w$ will project points onto a sphere, not a plane, and spheres do not have the required preservation of straight lines.

Instead, we set $w$ to the distance *along a single axis* that the vertex is from that viewing point; that axis is called the "forward" direction of the viewer.
Thus, a vertex beside the viewer is neither forward nor backwards from it and will be given $w=0$.
Setting $w$s in this way projects vertices onto a plane instead of a sphere, while still giving the expected sense of depth.

:::aside
A note about $z$

A naive implementation of perspective projection will make $w = z$,
but that will mess up clipping and make a depth buffer useless.

When providing data for future perspective projection, we pick a near and far distance
and modify $z$ so that
points at the near distance will have $\frac{z}{w} = -1$
and points at the far distance will have $\frac{z}{w} = 1$.

Commonly, this is achieved using a matrix like the following (possibly differing in sign depending on if $+z$ or $-z$ is taken as "forward"), called "the projection matrix":
$$\begin{bmatrix}
s_x & 0 & 0 & 0 \\
0 & s_y & 0 & 0 \\
0 & 0 & \frac{\text{far}+\text{near}}{\text{far}-\text{near}}& \frac{-2\cdot\text{near}\cdot\text{far}}{\text{far}-\text{near}}\\
0 & 0 & 1 & 0 \\
\end{bmatrix}\begin{bmatrix}
x\\y\\z\\1\end{bmatrix}$$
:::

### Non-Euclidean

Often, orthographic and perspective projections are described as the only two options
provided by the GPU's homogeneous normalization approach, but technically that is not correct.
It can also be used to create projections of points in non-Eucliean geometries.
For elliptic geometries $w$s can be used to realize the hyperspherical model;
for hyperbolic geometries, $w$s can be used to realize the Minkowski model.
In both cases, $w$ should be additionally augmented by a distance term if a perspective (instead of orthographic) projection in the geometry is desired.

## Viewport

Graphics input is provided in a coordinate system that is independent of display size,
but eventually it needs to be mapped to specific pixels.
This mapping is called the "viewport transformation"
and is a simple offset-and-scale operation in $x$ and $y$:

$$\begin{split}
x_{\text{screen}} &= \dfrac{x_{\texttt{input}} + 1}{2}(\text{width in pixels})\\
y_{\text{screen}} &= \dfrac{y_{\texttt{input}} + 1}{2}(\text{height in pixels})\\
\end{split}$$

Note that this *always* maps the coordinate range $-1$ to $+1$ to the viewport in both dimensions, even if the viewport is rectangular instead of square.
It is common to apply a scaling to the scene data to make sure this does not squish content.

## Interpolation

### DDA (Obsolete)

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

Output
:   - A set of points $\vec p$ where each $p_d$ is an integer

Process
:   *Setup:*
    
    1. If $a_d = b_d$, return the empty set
    2. If $a_d > b_d$, swap $\vec a$ and $\vec b$
    3. Let $\vec \Delta = \vec b - \vec a$
    4. Let $\vec s = \vec \Delta \div \Delta_d$

    *Find the first potential point:*
    
    5. Let $e = \lceil a_d \rceil - a_d$
    6. Let $\vec o = e \vec s$
    7. Initialize $\vec p$ as $\vec a + \vec o$
    
    *Find all points:*
    
    8. While $p_d < b_d$ repeat:
        i. add $\vec p$ to the set to be returned
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
    in either case, we can simply return the empty set: no meaningful points (1).
    
    To get the initial $\vec p$
    we need to figure out how far the starting end of the segment is from an integer $d$ coordinate ($e$, 5)
    make a vector offset that will move us to that point
    ($\vec o$ with $o_d = e$, 6)
    and add that offset to the starting end of the segment (7).
    
    All of this assumed we were stepping in the positive $d$ direction,
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

### Bresenham (Current)

Bresenham's line algorithm achieves the same results as DDA,
but using only integer values.
Because it uses only integers, it is both faster (integer arithmetic requires less hardware than floating-point hardware)
and more precise (no rounding error) than DDA.
It works on integer, rational, and fixed-point endpoints and outputs.
Because of its efficiency and precision, it is commonly used in graphics hardware.

Bresenham's line algorithm can be derived by writing out DDA using rational numbers
and tracking the integral and fractional parts of each number separately.
The result is less intuitive and more complicated code than DDA,
but simpler and smaller hardware because the individual components require many fewer transistors.

Jack Elton Bresenham derived this algorithm not as a form of DDA, but rather by considering the implicit equation for a line,
and also showed how it could draw other polygonal curves such as circles.
Those generalizations are suitable for hardware implementation, but are not commonly implemented in hardware.

### Linear (Obsolete)

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


### Hyperbolic (Current)

In 1992 Jim Blinn wrote [a paper](https://doi.org/10.1109/MCG.1992.10028) explaining how interpolation could be made perspective-correct using something called **hyperbolic interpolation**;
all graphics hardware now uses his approach.

Hyperbolic interpolation assumes that three components of the vector of values at each vertex of a triangle are special.
$x$ and $y$ are special because they correspond to pixel locations;
and $w$ is special because in homogeneous coordinates they are used to create frustums and perspective projection.
It is traditional to also treat $z$ as special because it gives better [depth buffer] precision for up-close objects where errors would be more visible.

Suppose we have a supplied vertex coordinate $(x,y,z,w,r,g,b,s,t)$.
We first perform perspective projection in $x$ and $y$ by dividing by $w$;
we also divide everything else by $w$ while we're at it, getting
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

Consider the two points $(12,0,6,3, 150, 30, 0)$ and $(2,0,-6,1, 0, 30, 150)$.

Division by $w$ gives $(4,0,2,\frac{1}{3}, 50, 10, 0)$ and $(2,0,-6,1, 0, 30, 150)$.

Interpolation to the midpoint gives $(3,0,2,\frac{2}{3}, 25, 20, 75)$.

Multiplication by the interpolated $\frac{1}{w}$ gives $(3,0,2,1.5,37.5,30,112.5)$.
:::


# Blending and Masking

After a fragment is shaded, a series of steps are used to decide if and how it should end up in the raster.

| Name | Parameterizable | Behavior |
|-----|:----:|----------------------|
| Ownership | No | Discards fragments occluded by other windows. |
| Scissor | `Scissor` | Discards fragments outside of a rectangular subregion of the rendered area. |
| Multisample coverage | several `enable`able options | Decides if this sample should be included in the final color averaging. |
| [Stencil](#stencil-buffer) | `StencilFunc`<br/>`StencilOp` | See below |
| [Depth](#depth-buffer) | `DepthFunc` | See below |
| Query | No | If any fragments make it to here, that fact is visible using an occlusion query API |
| [Blending] | `BlendEquation`<br/>`BlendFunc`<br/>`BlendColor` | See below |
| sRGB | No | Applies the piece-wise gamma encoding defined in the sRGB specification |
| Dithering | No | Reduces high-def color values to representable values either probabilistically (if dithering is enabled) or deterministically (otherwise) |
| Multisample combination | No | If there are multiple samples, they are averaged in an implementation-defined way to produce a final color. |

All of the above are disabled by default in OpenGL except the ownership test and sRGB conversion.
Dithering and blending technically happen even when disabled, just in a simple way.

## Stencil buffer

The stencil buffer allows some rendering actions to disable some future rendering actions for specific pixels. It can be used to make windows, mirrors, portals, and other rendered holes in the scenery.

Mechanically, the stencil buffer stores an integer (which doubles as a bit vector) for each pixel.

`StencilFunc` allows checking a formula of the form `(bufferValue & mask) [op] reference`
where `mask` and `reference` are constants and `[op]` is a comparison operator, all supplied to the `StencilFunc` call.
If this check yields false, the fragment is discarded.

`StencilOp` can define three different stencil value updates:
one for when the stencil test fails, one for when the depth test fails, and one for when the depth test succeeds.
The allowable operations are fairly limited but with a little creativity can create many interesting effects.

## Depth buffer

Each pixel has a depth value between $-1$ and $1$. This is compared to the $z$ value of the fragment using a comparison defined by the depth func; if it fails the fragment is discarded, otherwise the fragment is kept and the depth buffer value is changed to be the fragment's $z$.

Although the depth buffer is disabled by default, it is used in almost every 3D graphics program, and some 2D programs as well to control stacking.

## Blending

Blending is the process of deciding what color to make a pixel,
given three pieces of data:

- The new fragment's color (or "source color"), $(r_s, g_s, b_s, a_s)$
- The pixel's current color (or "destination color"), $(r_d, g_d, b_d, a_d)$
- A special constant color, $(r_c, g_c, b_c, a_c)$ (defined with `BlendColor`)

These are combined by applying one of several weighting functions selected with `BlendFunc` and one of several combining operations selected with `BlendEquation`.

:::example
The default blending is to just use the new fragment's color.
This is performed via $$1 (r_s, g_s, b_s, a_s) + 0 (r_d, g_d, b_d, a_d)$$
:::

:::example
One of the most common alternative blending modes treats alpha as an opacity channel
and performs what's known as the "over" operator:
$$\begin{split}
a' &= a_s + a_d(1-a_s)\\
(r',g',b') &= \dfrac{a_s}{a'} (r_s, g_s, b_s) + \dfrac{(1-a_s)a_d}{a'} (r_d, g_d, b_d)
\end{split}$$
This only works as expected if objects are sorted by distance from the camera and rendered farthest to nearest.
:::

It is common^[
    While premultiplied alpha is common, it is not universal,
    and in general could be specified differently
    for how WebGL stores its colors during blending,
    how the browser assumes the WebGL canvas's colors are represented,
    and how each imported image stores its colors.
    See [this StackOverflow post](https://stackoverflow.com/questions/39341564/webgl-how-to-correctly-blend-alpha-channel-png#answer-39354174) for an example of the complexities this can cause.
] to store $(ra, ga, ba, a)$ instead of $(r,g,b,a)$.
This is called "premultiplied alpha" and makes some operations more efficient.

:::example
The over operator with premultiplied alpha is
$$1 (r_s, g_s, b_s, a_s) + (1-a_s) (r_d, g_d, b_d, a_d)$$
:::

