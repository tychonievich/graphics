---
title: Raytracers vs Rasterizers
summary: An analysis of speed and fitness to a purpose.
...


Raytracers and rasterizers both have the same primary task:
decide what part of which shape is visible in each pixel of the scene.
For better image quality, they also have the same secondary task:
for each location visible in that way, decide what light enters that pixel from various directions.

Raytracers and rasterizers optimize solving these problems in very different ways.

The following text includes some asymptotic runtime analysis.
There are many terms in those expressions, listed here for reference:

| Symbol | Meaning |
|:------:|:--------|
| $F$    | Number of fragments; more than $R$ because primitives overlap |
| $O$    | Big-O notation |
| $P$    | Number of primitives (usually triangles) |
| $R$    | Resolution: the number of pixels on the screen |
| $S$    | Setup-up, once per scene or frame |
| $V$    | Number of vertices |

# Rasterizer

Rasterization algorithms are optimized around the existence of a raster, a regular grid of pixel locations of interest.
Regular grids and planar primitives enable algorithms like DDA and Bresenham that very efficiently compute the fragments inside a given primitive.

At a high level, rasterizers do the following work:

1. Up-front work positioning scene objects in the world; $O(S)$
2. View and projection matrices, re-positioning scene objects for the current viewpoint; $O(S)$
3. The vertex shader, typically doing 30–100 multiplications per vertex; $O(V)$
4. DDA or Bresenham, doing a few divisions per triangle and a few additions per fragment; $O(P + F)$
5. The fragment shader, computing a lighting model either per fragment or, with [deferred shading](deferred.html) per pixel instead; $O(R)$.

Overall, this means rendering the full scene has runtime complexity of
$$O(S + V + P + F + R)$$
The remarkable feature of this is that it is linear complexity:
no multiplicative terms.
It gets that linearity because DDA/Bresnham uses the structure of the raster to only do work for the fragments that are actually covered by each primitive.

This approach becomes *much* less attractive if applied to the secondary task of determining the incident light at a point in the scene.
To rasterize from a point in the scene requires setting up a new view matrix, which is near the front of the rasterization pipeline meaning we have to re-do it any everything after it for each point in the scene.

One of the simplest secondary tasks is rendering sharp reflections: at each point visible during the first pass ($R$) we render a 1-pixel image in the reflection direction ($S+V+P$).
That would have complexity
$$O(S + V + P + F + R n (S + V + P))$$
where $n$ is the number of bounces of light we compute.
Gone is our nice linearity: we now have an unscalable algorithm instead.

# Raytracer

Raytracers do not optimize for a raster.
Instead, their guiding principle is every ray for itself:
the assume each and every pixel needs to check the entire scene, sharing nothing with other pixels.

At a high level, raytracers do the following work:

1. Up-front work positioning scene objects in the world; $O(S)$
2. Create a ray for each pixel; each ray checks every primitive to see if it hits it; $O(R P)$
5. Fragment shader-like work, computing a lighting model per pixel; $O(R)$.

Overall, this means rendering the full scene has runtime complexity of
$$O(S + P R + R)$$
Note the multiplicative term:
this scales with the product of pixel count and number of primitives,
not their sum like rasterization has.
Using a bounding volume hierarchy (BVH) can cut that down to a logarithmic factor, at the const of additional setup time creating the BVH:
$$O(S + P\log(P) + R\log(P) + R)$$
Still much worse than rasterization, but much better than the cost without the BVH.

This approach scales nicely with the secondary task of determining incident light at a point in the scene.
Because raytracing didn't take advantage of the raster to start with, we don't have any raster-centric work to reproduce.

One of the simplest secondary tasks is rendering sharp reflections: at each point visible during the first pass we launch another ray in the reflection direction.
That would have complexity
$$O(S + P\log(P) + n R\log(P) + n R)$$
where $n$ is the number of bounces of light we compute.
Note that this still has a multiplicative term, but with a logarithm for a much more scalable complexity than rasterization with true reflections.
The constant is also much lower, often by an order of magnitude or more.


# Which one to use

Rasterizers are *much* faster than raytracers for scenes where the exact light incident to each visible point is not needed.
Coupled fancy fragment shaders and [cube maps](textures2.html), they can render reasonable approximations of many scenes very efficiently.

Raytracers are *much* faster than rasterizers for scenes where light does things that are not easily modeled with a few point light sources and environment maps.
Raytracers can be made to converge on what the scene would actually look like if it were real, typically by using thousands of secondary rays for each pixel and running for minutes, hours, or even days per frame.

In theory, hybrid systems could be imagined that use rasterization for the first task when the rays all align with the raster and raytracing afterward for the no-longer-raster-aligned secondary task.
Because raytracing is usually used in cases where the secondary task dwarfs the primary task, this optimization is rarely seen as worthwhile.
However, doing a few raytracing steps in a mostly-rasterized scene is sometimes proposed to simulate specific visual details without the full cost of raytracing.

