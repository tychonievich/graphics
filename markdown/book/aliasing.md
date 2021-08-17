---
title: Aliasing
...

A raster is a rectangular grid of pixels.
The rasterization of a scene consists of a single color at each pixel.
Rasterizations are the principle output of canvas-style APIs, which themselves are the backing for almost all other graphics APIs.

A pixel can be thought of in several ways,
but the two most common are as square (making the raster a tiling of adjacent pixels)
or as a mathematical point (making the raster a void with points distributed evenly across it).
These two are not equivalent, and there are pros and cons to each.

Treating pixels as mathematical points creates aliasing,
where the shape of the grid interacts with the shapes in the scene
to create patterns which are distracting to the eye.
The most common aliasing effect is stair-step edges, causing smooth shapes to appear jagged.
Much more significant, however, is the display of scene objects that are narrower than a pixel and effectively "hide between" the points, vanishing entierly from the rasterization.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="-5 -5 80 80" style="max-width:20em">
<g style="stroke:black; stroke-width:0.5">
    <circle cx="5" cy="5" r="2" />
    <circle cx="5" cy="25" r="2" />
    <circle cx="5" cy="45" r="2" />
    <circle cx="5" cy="65" r="2" />
    <circle cx="25" cy="5" r="2" fill="none"/>
    <circle cx="25" cy="25" r="2" fill="none"/>
    <circle cx="25" cy="45" r="2" />
    <circle cx="25" cy="65" r="2" />
    <circle cx="45" cy="5" r="2" fill="none"/>
    <circle cx="45" cy="25" r="2" fill="none"/>
    <circle cx="45" cy="45" r="2" fill="none"/>
    <circle cx="45" cy="65" r="2" />
    <circle cx="65" cy="5" r="2" />
    <circle cx="65" cy="25" r="2" fill="none"/>
    <circle cx="65" cy="45" r="2" fill="none"/>
    <circle cx="65" cy="65" r="2" fill="none"/>
</g>
<g style="fill:none; stroke:gray; stroke-width:0.5;">
    <path d="M 2,2 2,68 30,68 20,2 Z"/>
    <path d="M 66,2 40,68 50,68 Z"/>
</g>
<g style="fill:rgba(255,0,0,0.25);">
    <path d="M -5,-5 -5,75, 35,75 35,35 15,35 15,-5 Z"/>
</g>
<g style="fill:rgba(0,127,0,0.25);">
    <path d="M 35,75 55,75 55,55 35,55 Z M 75,-5 55,-5 55,15 75,15 Z"/>
</g>
</svg>
<figcaption>Two examples of point-like pixels causing aliasing. The outlines are the indended shapes. The circles show the pixel locations. The colored regions are the shapes the eye sees.</figcaption>
</figure>


Treating pixels as square regions removes the worst kinds aliasing:
stair-stepped edges and thin scene objects instead look a bit blurred,
but the blur is less than a pixel wide and generally does not distract the eye.
However, it adds a problem that point-like pixels do not have:
the scene cannot be correctly rendered one piece at a time.

To see this problem, consider a scene containing a white background and two half-pixel-sized black rectangles, both within the same pixel.
If those two black rectangles are side-by-side, together covering the full pixel then the pixel should be black.
If they are fully overlapping, both covering the same part of the pixel, then the pixel should be a gray half-way between black and white.
If they are partly overlapping, the pixel should be a darker gray.
But if we render them one at a time, the first will work fine: we'll add half a pixel of black to a white pixel and get a 50/50 gray.
The second rectangle now adds half a pixel of black to a gray pixel, getting a darker 25/75 gray.
That could be the right result, but it likely isn't and the only way to know is to check not just the rasterization of the scene so far but the geometry of the objects that make up the scene.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="-1 -1 142 47" style="max-width:50em">
<g style="fill:#ff0000">
    <path d="M 0,0 10,0 10,20 0,20 Z"/>
    <path d="M 30,0 40,0 40,20 30,20 Z"/>
    <path d="M 60,0 70,0 70,20 60,20 Z"/>
    <path d="M 90,0 100,0 100,20 90,20 Z"/>
</g>
<path d="M 120,0 140,0 140,20 120,20 Z" fill="#ffbcbc"/>
<g style="fill:#0000ff">
    <path d="M 30,0 40.5,0 39.5,20 30,20 Z"/>
    <path d="M 60,0 80,0 80,10 60,10 Z"/>
    <path d="M 100,0 110,0 110,20 100,20 Z"/>
    <path d="M 120,0 132,0 128,20 120,20 Z"/>
</g>
<g style="fill:none; stroke:gray; stroke-width:0.5;">
    <path d="M 0,0 20,0 20,20 0,20 Z"/>
    <path d="M 30,0 50,0 50,20 30,20 Z"/>
    <path d="M 60,0 80,0 80,20 60,20 Z"/>
    <path d="M 90,0 110,0 110,20 90,20 Z"/>
</g>
<g transform="translate(0,25)">
    <path d="M 0,0 20,0 20,20 0,20 Z" fill="#ffbcbc"/>
    <path d="M 30,0 50,0 50,20 30,20 Z" fill="#bcbcff"/>
    <path d="M 60,0 80,0 80,20 60,20 Z" fill="#bc89e1"/>
    <path d="M 90,0 110,0 110,20 90,20 Z" fill="#bc00bc"/>
    <path d="M 120,0 140,0 140,20 120,20 Z" fill="#bc89e1"/>
</g>
</svg>
<figcaption>A few ways shapes could overlap in a single square pixel region, and the correct resulting color for each.</figcaption>
</figure>


By contrast, point-like pixels don't have this problem.
Points don't have dimensions, so nothing can cover half of a point.
Yes, they tend to have aliasing,
but they also let us render a scene one object at a time.
One-at-a-time rendering lets us use a very simple API---one simple enough to encode in hardware---*and* lets us process each object in the scene in parallel on a different processor, possibly even slicing the objects into smaller pieces for more parallelism, without any change in the resulting render.
That simplicity and robustness has fueled the development of dedicated graphics hardware and has made point-like pixels the dominant assumption in canvas APIs today.

Because APIs designed for point-like pixels can operating by creating of rasterization of each element of the scene independently, it is common to refer to all systems that implement this approach as simply "**rasterization**"
and to use a more specific term (raytracing, subdivision, etc) for every other method of filling a raster with a representation of a scene.
In some situations, point-like pixel APIs are named after their most popular algorithms, such as "scan-converting", "Bresenham", or "DDA".


But what about the aliasing?
Canvas APIs generally offer an "anti-aliased" mode that implements (some approximation of) the square-like pixels, but without changing the simple point-like API design.
The result is that turning on anti-aliasing will remove stair-stepped edges
and help thinner-than-a-pixel objects not vanish,
but will also mean that slicing a shape into two abutting shapes that are mathematically equivalent to the original will cause a visible stair-stepped line of semi-transparency along the cut.

![Two touching black triangles rendered in anti-aliased mode. Note the pixel-width blurred edges that prevent stair-step aliasing and the visible boundary line even though there is no gap between the two triangles.](antialiased.png){style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; -ms-interpolation-mode: nearest-neighbor; width:19em;"}


There are several designs of APIs and algorithms that handle square-like pixels correctly; raytracing is definitely the most popular, albeit only for 3D graphics. And raytracing, as we will see when we [compare complexities](speed.html), is *dramatically* slower than canvas-API rasterization.
