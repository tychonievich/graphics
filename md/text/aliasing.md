---
title: Aliasing
summary: Two interpretations of rasters and the problems with both.
...

The word "raster" comes from the Latin word for "rake" and has origins in Cathode Ray Tube (CRT) displays.
CRTs work by shooting a narrow ray of electrons emitted from a cathode through a vacuum-filled tube at a thin sheet of phosphors; the phosphors then release the energy provided by the electrons as visible light.
Early CRTs, such as those used in oscilloscopes and vector video game consoles such as that used in the 1979 Asteroids arcade game, make patterns by directing the electron beam to trace out the pattern to be displayed.
Televisions and subsequently most computer monitors instead "raked" the electron beam across the entire screen in a repeating pattern of parallel horizontal lines, varying the intensity of the beam to create images.

<figure>
<img src="../files/raster-r.svg" style="max-width:30em"/>
<figcaption>An example of how raking or rastering a line in rows across a display while varying its intensity (here shown as width) can create shapes.</figcaption>
</figure>

As memory became cheaper and other forms of displays became popular, "raster" shifted meaning from the raking-pattern of an electron beam in a CRT to refer to any grid of pixels.
There remains an implication that the raster is stored in memory in the same order as the raster scan: the top row first, left to right, then the next row also left to right, and so on to the bottom of the screen.
I've heard that this order was chosen because it was reading order in the languages spoken by its inventors, though I haven't been able to find firm backing for that supposition.

Given that "raster" generally means a grid of pixels,
the rasterization of a scene consists of a single color at each pixel.
Rasterizations are the principle output of canvas-style APIs, which themselves are the backing for almost all other graphics APIs.

"Pixel" is a shortened form of "picture element."
A pixel can be thought of in several ways,
but the two most common are as square (making the raster a tiling of adjacent pixels)
or as a mathematical point (making the raster a void with points distributed evenly across it).
These two are not equivalent, and there are pros and cons to each.

Treating pixels as mathematical points creates aliasing,
where the shape of the grid interacts with the shapes in the scene
to create patterns which are distracting to the eye.
The most common aliasing effect is stair-step edges, causing smooth shapes to appear jagged.
Much more significant, however, is the display of scene objects that are narrower than a pixel and effectively "hide between" the points, vanishing entirely from the rasterization.

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

<figure>
<svg x="0" y="0" viewBox="0 0 242 142" style="max-width:15em">
<rect x="21" y="1" width="20" height="20" opacity="0.4"></rect>
<rect x="41" y="1" width="20" height="20" opacity="0.1"></rect>
<rect x="1" y="21" width="20" height="20" opacity="0.15"></rect>
<rect x="21" y="21" width="20" height="20" opacity="0.8"></rect>
<rect x="41" y="21" width="20" height="20" opacity="0.85"></rect>
<rect x="61" y="21" width="20" height="20" opacity="0.45"></rect>
<rect x="81" y="21" width="20" height="20" opacity="0.1"></rect>
<rect x="21" y="41" width="20" height="20" opacity="0.05"></rect>
<rect x="41" y="41" width="20" height="20" opacity="0.4"></rect>
<rect x="61" y="41" width="20" height="20" opacity="0.8"></rect>
<rect x="81" y="41" width="20" height="20" opacity="0.85"></rect>
<rect x="101" y="41" width="20" height="20" opacity="0.45"></rect>
<rect x="121" y="41" width="20" height="20" opacity="0.1"></rect>
<rect x="61" y="61" width="20" height="20" opacity="0.05"></rect>
<rect x="81" y="61" width="20" height="20" opacity="0.4"></rect>
<rect x="101" y="61" width="20" height="20" opacity="0.8"></rect>
<rect x="121" y="61" width="20" height="20" opacity="0.85"></rect>
<rect x="141" y="61" width="20" height="20" opacity="0.45"></rect>
<rect x="161" y="61" width="20" height="20" opacity="0.1"></rect>
<rect x="101" y="81" width="20" height="20" opacity="0.05"></rect>
<rect x="121" y="81" width="20" height="20" opacity="0.4"></rect>
<rect x="141" y="81" width="20" height="20" opacity="0.8"></rect>
<rect x="161" y="81" width="20" height="20" opacity="0.85"></rect>
<rect x="181" y="81" width="20" height="20" opacity="0.45"></rect>
<rect x="201" y="81" width="20" height="20" opacity="0.1"></rect>
<rect x="141" y="101" width="20" height="20" opacity="0.05"></rect>
<rect x="161" y="101" width="20" height="20" opacity="0.4"></rect>
<rect x="181" y="101" width="20" height="20" opacity="0.8"></rect>
<rect x="201" y="101" width="20" height="20" opacity="0.85"></rect>
<rect x="221" y="101" width="20" height="20" opacity="0.2"></rect>
<rect x="181" y="121" width="20" height="20" opacity="0.05"></rect>
<rect x="201" y="121" width="20" height="20" opacity="0.4"></rect>
<path style="stroke:#7f7f7f; stroke-width:0.125; fill:none;" d="m 1 1 240 0 0 20 -240 0 0 20 240 0 0 20 -240 0 0 20 240 0 0 20 -240 0 0 20 240 0 0 20 -240 0 0 -140 20 0 0 140 20 0 0 -140 20 0 0 140 20 0 0 -140 20 0 0 140 20 0 0 -140 20 0 0 140 20 0 0 -140 20 0 0 140 20 0 0 -140 20 0 0 140 20 0 0 -140 "></path>
<path style="stroke:#ff0000; stroke-width:1; fill:none;" d="m 25 10 200 100 -10 20 -200 -100 10 -20"></path>
</svg>
<figcaption>An example of an oblique one-pixel-wide rectangle rendered with square pixels. The darkness of each pixel matches how much of its area overlaps with the rectangle.</figcaption>
</figure>

While square-like pixels have less aliasing than point-like pixels, they still do have some aliasing, particularly when used to display repeating patterns that are sized close to, but not the same as, the pixels themselves.
Some examples of that can be seen using the following interactive 1D pattern resizer.

<figure>
<input type="range" min="10" max="100" step="0.05" value="44.7" oninput="update_figure(event)" style="width:100%"/>
<svg viewBox="0 0 400 300" style="background: white">
<g id="arealike">
<rect x="0" y="0" width="20" height="80" fill="red"/>
<rect x="20" y="0" width="20" height="80" fill=""/>
<rect x="40" y="0" width="20" height="80" fill=""/>
<rect x="60" y="0" width="20" height="80" fill=""/>
<rect x="80" y="0" width="20" height="80" fill=""/>
<rect x="100" y="0" width="20" height="80" fill=""/>
<rect x="120" y="0" width="20" height="80" fill=""/>
<rect x="140" y="0" width="20" height="80" fill=""/>
<rect x="160" y="0" width="20" height="80" fill=""/>
<rect x="180" y="0" width="20" height="80" fill=""/>
<rect x="200" y="0" width="20" height="80" fill=""/>
<rect x="220" y="0" width="20" height="80" fill=""/>
<rect x="240" y="0" width="20" height="80" fill=""/>
<rect x="260" y="0" width="20" height="80" fill=""/>
<rect x="280" y="0" width="20" height="80" fill=""/>
<rect x="300" y="0" width="20" height="80" fill=""/>
<rect x="320" y="0" width="20" height="80" fill=""/>
<rect x="340" y="0" width="20" height="80" fill=""/>
<rect x="360" y="0" width="20" height="80" fill=""/>
<rect x="380" y="0" width="20" height="80" fill=""/>
</g>
<line x1="0" x2="400" y1="150" y2="150" stroke-width="80" stroke="black" stroke-dasharray="19.9809"/>
<g id="pointlike">
<rect x="0" y="220" width="20" height="80" fill=""/>
<rect x="20" y="220" width="20" height="80" fill=""/>
<rect x="40" y="220" width="20" height="80" fill=""/>
<rect x="60" y="220" width="20" height="80" fill=""/>
<rect x="80" y="220" width="20" height="80" fill=""/>
<rect x="100" y="220" width="20" height="80" fill=""/>
<rect x="120" y="220" width="20" height="80" fill=""/>
<rect x="140" y="220" width="20" height="80" fill=""/>
<rect x="160" y="220" width="20" height="80" fill=""/>
<rect x="180" y="220" width="20" height="80" fill=""/>
<rect x="200" y="220" width="20" height="80" fill=""/>
<rect x="220" y="220" width="20" height="80" fill=""/>
<rect x="240" y="220" width="20" height="80" fill=""/>
<rect x="260" y="220" width="20" height="80" fill=""/>
<rect x="280" y="220" width="20" height="80" fill=""/>
<rect x="300" y="220" width="20" height="80" fill=""/>
<rect x="320" y="220" width="20" height="80" fill=""/>
<rect x="340" y="220" width="20" height="80" fill=""/>
<rect x="360" y="220" width="20" height="80" fill=""/>
<rect x="380" y="220" width="20" height="80" fill=""/>
</g>
<path fill="none" stroke="red" stroke-width="0.3" d=" M 10,190 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 " />
<path fill="none" stroke="red" stroke-width="0.3" d=" M 0,80 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 m 20,-30 v 30 " />
</svg>
<script>
function plsample() {
 let da = Number(document.querySelector('line').getAttribute('stroke-dasharray'))
 let g = document.getElementById('pointlike')
 g.querySelectorAll('rect').forEach(r => {
  let x = r.x.baseVal.value + r.width.baseVal.value/2
  let pos = (x/(2*da))%1
  r.setAttribute('fill', pos < 0.5 ? 'black' : 'white')
 })
}
function alsample() {
 let da = Number(document.querySelector('line').getAttribute('stroke-dasharray'))
 let g = document.getElementById('arealike')
 g.querySelectorAll('rect').forEach(r => {
  let x0 = r.x.baseVal.value
  let x1 = x0 + r.width.baseVal.value
  let ink = 0
  x0 /= da
  x1 /= da
  if ((x0|0) == (x1|0)) {
   ink = ((x0|0)&1)
  } else {
   let b=0, w=0;
   if (((x0|0)&1)) b+=Math.ceil(x0)-x0
   else w+=Math.ceil(x0)-x0
   x0 = Math.ceil(x0)
   if (((x1|0)&1)) b+=x1-Math.floor(x1)
   else w+=x1-Math.floor(x1)
   x1 = Math.floor(x1)
   for(let x=x0; x<x1; x+=1) {
    if (x&1) b+=1
    else w+=1
   }
   
   ink = b / (w+b)
  }
  r.setAttribute('fill', 'hsl(0, 0%, '+(ink*100)+'%')
 })
}
function update_figure(event) {
 if (event?.target?.value)
  document.querySelector('line').setAttribute('stroke-dasharray', Math.pow(event.target.value,2)/100)
 plsample(); alsample();
}
update_figure()
</script>
<figcaption>
<p>Adjust the slider to observe 1D aliasing caused by a striped ground-truth with area-like (top) and point-like (bottom) pixels.
Note that when the ground-truth bars are 2 or more pixels wide both patterns look fairly good.
Between 2 and 1 the point-like pixels have thick and tin stripes, while the area-like sometimes look right and other times have spurious gray bands.
Below 1, both have a variety of false patterns not present in the original, with more extreme patterns for the point-like pixels.</p>
<p>Thin red lines show boundary between area-like pixels (top) and the sampling point of point-like pixels (bottom).</p>
</figcaption>
</figure>

In addition to still having some aliasing, square-pixel approaches add a problem that point-like pixels do not have:
many scenes cannot be correctly rendered one piece at a time.

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
    <path d="M 0,0 10,0 10,20 0,20 Z"/>
    <path d="M 30,0 40.5,0 39.5,20 30,20 Z"/>
    <path d="M 60,0 80,0 80,10 60,10 Z"/>
    <path d="M 100,0 110,0 110,20 100,20 Z"/>
    <path d="M 120,0 132,0 128,20 120,20 Z"/>
</g>
<g transform="translate(0,25)">
    <path d="M 0,0 20,0 20,20 0,20 Z" fill="#bcbcff"/>
    <path d="M 30,0 50,0 50,20 30,20 Z" fill="#bdbcfe"/>
    <path d="M 60,0 80,0 80,20 60,20 Z" fill="#bc89e1"/>
    <path d="M 90,0 110,0 110,20 90,20 Z" fill="#bc00bc"/>
    <path d="M 120,0 140,0 140,20 120,20 Z" fill="#bc89e1"/>
</g>
</svg>
<figcaption>A few ways a half-pixel-sized blue shape could overlap with a half-red half-white square pixel region, and the correct resulting color for each.</figcaption>
</figure>

If we use area-like pixels to draw a quadrilateral by splitting it into two triangles sharing an edge and drawing each individually,
pixels along the shared edge will be half-filled by the first triangle
then half-filled again by the second
resulting in only three-fourths-filled pixels along the line.
As a result, area-like pixels will show a seam between the two trangles.

![Two touching black triangles rendered in anti-aliased mode. Note the pixel-width blurred edges that prevent stair-step aliasing and the visible boundary line even though there is no gap between the two triangles.](antialiased.png){style="image-rendering: pixelated; image-rendering: -moz-crisp-edges; -ms-interpolation-mode: nearest-neighbor; width:19em;"}

By contrast, point-like pixels don't have this problem.
Points don't have dimensions, so nothing can cover half of a point.
Point-like pixels do tend to have strong aliasing artefacts,
but they also let us render a scene one object at a time.
One-at-a-time rendering lets us use a very simple API---one simple enough to encode in hardware---*and* lets us process each object in the scene in parallel on a different processor, possibly even slicing the objects into smaller pieces for more parallelism, without any change in the resulting render.
That simplicity and robustness has fueled the development of dedicated graphics hardware and has made point-like pixels the dominant assumption in canvas APIs today.

But what about the aliasing?
Canvas APIs generally offer various "anti-aliased" modes that implements (some approximation of) the square-like pixels, but without changing the simple point-like API design.
If these operate on a pixel basis they don't let 3D graphics work very well,
but they can also be designed to operate on sub-pixel samples.
Multisampling is often used to render the entire scene with point-like samples at a higher resolution that it will be displayed and then average groups of samples into the final displayed pixels.

Because APIs designed for point-like pixels (or point-like multisamples) can operating by creating of rasterization of each element of the scene independently, it is common to refer to all systems that implement this approach as simply "**rasterization**"
and to use a more specific term (raytracing, subdivision, etc) for every other method of filling a raster with a representation of a scene.
In some situations, point-like pixel APIs are named after their most popular algorithms, such as "scan-converting", "Bresenham", or "DDA".

There are several designs of APIs and algorithms that handle square-like pixels correctly; raytracing is definitely the most popular, albeit only for 3D graphics.
