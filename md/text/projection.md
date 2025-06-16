---
title: Projection
summary: Simulating depth and perspective using w and z.
...

Any conversion of 3D coordinates onto a 2D plane is called a *projection*.
Many projections can be defined, but GPUs support only those that convert all straight 3D lines into straight 2D lines.
Conveniently, all of these can be defined using homogeneous coordinate normalization.

Homogeneous coordinates are used for various purposes;
for the purpose of projections, they have an auxiliary $w$ coordinate appended to the 3D $(x,y,z)$ coordinates, where $w$ is a divisor: the projected coordinate to draw is actually $\left(\frac{x}{w},\frac{y}{w}\right)$ (with $\frac{z}{w}$ as a "depth" component, used by the [depth buffer]).
With this single rule we can create several kinds of projections by setting $w$s in different ways.

# Orthographic

If all $w=1$ then division by $w$ does nothing and we achieve an orthographic projection.
Orthographic projections used for blueprints, maps, birds-eye views, and other images where the projected size of an object should be independent from its distance from the camera.

# Perspective

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



# Non-Euclidean

Often, orthographic and perspective projections are described as the only two options
provided by the GPU's homogeneous normalization approach, but technically that is not correct.
It can also be used to create projections of points in non-Eucliean geometries.
For elliptic geometries $w$s can be used to realize the hyperspherical model;
for hyperbolic geometries, $w$s can be used to realize the Minkowski model.
In both cases, $w$ should be additionally augmented by a distance term if a perspective (instead of orthographic) projection in the geometry is desired.
