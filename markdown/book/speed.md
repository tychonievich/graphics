---
title: Speed of scan-converting vs raytracing
args:
    html-math-method:
        method: katex
...


Let

- $w$ be the width of the screen in pixels
- $h$ be the height of the screen in pixels
- $p$ be the number of pixels in the screen: $p = w h$
- $l$ be the number of light sources in the scene
- $a$ be the amount of super-sample antialiasing
- $T$ be the number of triangles in the scene
- $o$ be the average number of overlapping triangles in any given pixel

# Scan Conversion

Scan converting one triangle involves three steps:

- Some fixed work to set up slopes and order points
- Some work for each scanline to increment up the edges
- Some work for each pixel covered by the triangle

In a full scene, the complexity of each of those is

- $\Theta(T)$ for the per-triangle work
- roughly $\Theta(\sqrt{p o a T})$ for the per-scanline work, assuming triangles are each of similar size and are roughly as wide as they are tall
- $\Theta(p o a l)$ for the per-covered-pixel work

In the expression $\Theta(T + \sqrt{p o a T} + p o a l)$,
either $T$ or $p o$ is the dominant term; $\sqrt{p o a T}$ never is,
so by asymptotic analysis we can simplify it to just $\Theta(T + p o a l)$.

When a scene contains a very large number of triangles simply lit, the $T$ term dominates and graphics card performance can be usefully characterized as "triangles per second."
When a scene is rendered at very high resolution, or at a high level of anti-aliasing, or without proper occlusion culling, or with fancy per-pixel lighting, the $p o a l$ term dominates instead.

# Ray tracing

Ray tracing a scene involves 

- casting $a$ rays per pixel
- with $l$ shadow rays per ray
- with between $T$ and $\log(T)$ intersection tests per ray

for a complexity of $O(\log(T) p a l)$



Let us compare the runtime efficiency of rasterizing vs raytracing.

# Rasterizing

To rasterize a triangle requires some (constant-time) up-front work to sort out the stepping direction and so on.
So we have a $T$ term in the runtime, where $T$ is the number of triangles in the scene.

Each triangle also requires work proportional to its area to step across the scanlines of its interior.
Rather than expressing this as a per-triangle term, we look at the entire scene.
In a raster is $w$ pixels wide and $h$ pixels high and on average triangles are stacked $d$ deep, we have a $w h d$ term, regardless of $T$.

Each triangle also requires work proportional to the vertical extent of the triangle to step along its edges.
Assuming that most triangles are of roughly the same size and are roughly as wide as they are tall, each triangle covers $\frac{w h d}{T}$ pixels and is thus on the order of $\sqrt{\frac{w h d}{T}}$ pixels tall,
for a term on the order of $T \sqrt{\frac{w h d}{T}} = \sqrt{w h d T}$.

Thus, our full complexity for rasterizing is

$$O(T + w h d + \sqrt{w h d T}$$

Which term dominates varies with triangle size.
When $\frac{w h}{T}$ is large, the screen size term ($w h d$) dominates the runtime.
When $\frac{w h}{T}$ is small, the triangle term ($T$) dominates the runtime.
The vertical term is never the dominant term, but can be significant when the other two terms are roughly equivalent.

Anti-aliasing is most commonly performed by rendering at a higher resolution and down-scaling. We'll use $a$ for the anti-aliasing factor (often 4 or 16).

Higher-quality lighting is performed per pixel, including for pixels that will be occluded by other pixels.
We'll use $l$ for the number of lights.

A common approach to shadows is to render a shadow buffer for each light and perform a check during lighting for each buffer.
We'll use $s$ for the linear resolution of a shadow buffer.

Putting these together we have

$$O(T + a l w h d + \sqrt{w h d T} + l s^2 d + s \sqrt{d T}$$

# Ray tracing

The naive approach to raytracing performs a ray-intersection test for every triangle in the scene for every pixel, giving us $O(T w h)$.
An optimal spatial bounding hierarchy can reduce that by a logarithm, but adds a hierarhcy nagivation time term we'll denote with $b$ for a full complexity of

$$O(b \log(T) w h)$$

Anti-aliasing is most commonly performed by shooting more rays per pixel (often hundreds).

Higher-quality lighting is performed per pixel.
We'll use $l$ for the number of lights.

A common approach to shadows is to use shadow rays to each light at each ray-object intersection point.

Putting these together we have

$$O(b \log(T) a l w h)$$

# Which is faster?

We've ignored constants throughout, and those change.
We've also ignored parallelism, and both approaches are highly parellelizable.
So instead we'll compare how much changing things in a scene matters.

As a baseline, suppose we have a 720p scene with 1 million triangles.
Roughly 1 million pixels and 1 million triangles suggests the $T$ term dominates the rasterization runtime.

Doubling the number of pixels (to 1080p) or level of anti-aliasing
has limited impact on rasterization because the $T$ term still dominates.
It doubles the runtime of raytracing.

Doubling the number of triangles (without increasing the amount of overlap)
doubles the runtime for rasterization
but has only a 3.3% impact on raytracing because of the log term around $T$.

