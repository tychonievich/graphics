---
title: "Rasterizer MP"
header-includes:
	- |
		<style>.big { width:calc(min(30vh, 18em)); }</style>
	- |
		<script>window.addEventListener('load',e => document.querySelectorAll('dt > code:first-child').forEach(c=>c.parentElement.id = c.textContent))</script>
...

This is the single largest MP in the course,
with both core and elective points.
The core parts are core for two reasons.

In the short term, we're about to learn WebGL2.
WebGL2 is simpler than some other 3D APIs, but it is still quite complicated,
needing to coordinate between multiple processors, memory pools, and languages.
This assignment has you implement (and thus learn and internalize) a portion of that API
a piece at a time in a language you're familiar with
without the complexity of the Browser-CPU-GPU communication component of WebGL2.

In the long term, I want to show you there's no magic in graphics
by revealing how each piece of current graphics systems work.
You remember what you do for far longer than you remember what you've merely been told, so implementing is key to that.
An essential piece of graphics is how triangles are rendered and interpolated across, so that's core.
The various electives are all also common and useful, though less essential.



# Core

Implement the core parts of a simplified version of the WebGL API that we'll be using for most other MPs.
In particular,

1. Write a program that reads a `.txt` file and produces a `.png` file.
	It will be invoked as e.g. `./yourprogram exampleInput.txt`{.sh},
	via a [makefile](#what-you-submit).

2. Handle the input file keywords [`png`](#png), [`position 4 ...`](#position), [`color 3 ...`](#color), and [`drawArraysTriangles`](#drawArraysTriangles).
	See our [notes on program state](#state) for tips on doing this well.

3. Implement the DDA algorithm, and the scanline algorithm which consists of repeated invocations of DDA.
	These algorithms are defined down to the pixel in almost all contexts,
	and should match [the provided input files and their outputs](#test-files) very closely.
	Almost all successful submissions follow [our DDA pseudocode and scanline diagram](../text/dda.html#dda-obsolete) closely.

4. Implement division by $w$ and viewport transformations.
	See our [notes on algorithms](#algorithm) for tips on doing this well.

# Electives

You may stop after implementing the core parts.
Elective parts may be implemented in any set of MPs,
and getting 0 electives here is fine if you do extra electives elsewhere.

The first four elective components complete the core functionality; they are prerequisite to the other electives in this MP.


|Pt| Keywords | Prereqs | Test cases |
|-:|----------|---------|------------|
| 1| [`elements`](#elements) and [`drawElementsTriangles`](#drawElementsTriangles) | | rast-elements.txt |
| 2| [`depth`](#depth) | | rast-depth.txt |
| 1| [`sRGB`](#sRGB) | | rast-sRGB.txt and rast-gammabox.txt |
| 2| [`hyp`](#hyp) | `depth` and `sRGB` | rast-perspective.txt |

The other electives are mostly independent of one another,
with the first four electives as their only prereqs.
However, there are a few exceptions where additional prereqs are needed:

|Pt| Keywords | Additional Prereqs | Test cases |
|-:|----------|--------------------|------------|
| 2| [`frustum`](#frustum) | | rast-frustum.txt and rast-manyclip.txt |
|0.5|[`cull`](#cull) | | rast-cull.txt |
| 1| [`fsaa`](#fsaa) | | rast-fsaa2.txt and rast-fsaa8.txt |
| 2| [`color 4`](#color) | | rast-alpha.txt |
| 2| [`uniformMatrix`](#uniformMatrix) | | rast-matrix.txt | 
|0.5| [`position 3` and `position 2`](#position) | `uniformMatrix` | rast-2d3d.txt |
| 3| [`texture`](#texture) and [`texcoord`](#texcoord) | | rast-textures.txt |
| 2| [`pointsize`](#pointsize) and [`drawArraysPoints`](#drawArraysPoints) | `texture` | rast-points1.txt and rast-points2.txt |
| 1| [`decal`](#decal) | `texture` and `texcoord` | rast-decals.txt |

It is tedious to grade output files for inputs you haven't implemented.
When you upload, you will be asked to select which electives (if any) you've implemented and we should grade.

# What you submit

For this MP you submit one program, in any language of your choosing, that implements all of the core and any elective functionality you choose.
The program will be executed as follows:

```sh
make build
make run file=rast-grey.txt
make run file=rast-smallgap.txt
# ...
make run file=rast-points2.txt
```

See the associated warm-up for more on how to set up a Makefile and generate PNG images.


# Test Files

All test input files, reference output files, and supporting files can be downloaded [as a zip](files/rasterizer-files.zip)

## Core

| Input | Output | Notes |
|:------|:------:|:------|
| [rast-gray.txt](files/rast-gray.txt) | [<img class="demo big" src="files/rast-gray.png"/>](files/rast-gray.png) | Comments inside input file give intermediate computation results. |
| [rast-smallgap.txt](files/rast-smallgap.txt) | [<img class="demo big" src="files/rast-smallgap.png"/>](files/rast-smallgap.png) | Checks especially for boundary via the gap between triangles and the initial offsets via the lack of horizontal bands in the color of the left triangle. |
| [rast-smoothcolor.txt](files/rast-smoothcolor.txt) | [<img class="demo big" src="files/rast-smoothcolor.png"/>](files/rast-smoothcolor.png) | Various interpolation errors can be detected because in this image they'll create a color difference on the front triangle. |
| [rast-checkers.txt](files/rast-checkers.txt) | [<img class="demo big" src="files/rast-checkers.png"/>](files/rast-checkers.png) | More than a hundred adjacent 1-pixel-wide triangles to test alignment. Note especially the white row on the top.<br/>Some pixels DDA generates will be off-screen. You can simply ignore (not draw) those pixels.<br/>You may wish to try this with a higher-res output (up the `png` size several fold on the first line) to see how triangles make this image. |


## Elective but regularly used by WebGL2 programmers

| Input | Output | Notes |
|:------|:------:|:------|
| [rast-depth.txt](files/rast-depth.txt) | [<img class="demo big" src="files/rast-depth.png"/>](files/rast-depth.png) | Created by a combination of (a) depth interpolation to each pixel and (b) comparison with a per-pixel depth value; if you plot the depth of each pixel as a gray-scale color you should get something like this:<br/><img class="demo" src="files/rast-depthvalues.png"/> |
| [rast-elements.txt](files/rast-elements.txt) | [<img class="demo big" src="files/rast-elements.png"/>](files/rast-elements.png) |  |


## Electives that are always enabled in WebGL2

| Input | Output | Notes |
|:------|:------:|:------|
| [rast-sRGB.txt](files/rast-sRGB.txt) | [<img class="demo big" src="files/rast-sRGB.png"/>](files/rast-sRGB.png) | `rast-smoothcolor` with sRGB; note that adding sRGB makes it much brighter overall. |
| [rast-gammabox.txt](files/rast-gammabox.txt) | [<img class="demo big" src="files/rast-gammabox.png"/>](files/rast-gammabox.png) | `rast-checkers` with sRGB; if your monitor is properly calibrated, squinting should make this look uniformly gray. |
| [rast-perspective.txt](files/rast-perspective.txt) | [<img class="demo big" src="files/rast-perspective.png"/>](files/rast-perspective.png) | The left wall is split in the middle, the right wall is not, as shown in this image with a different color for each triangle:<br/><img class="demo" src="files/persp_triangles.png"/><br/> Despite the geometry difference, both should have the same overall color, and both should match the color of the horizontal bar where it crosses them. |
| [rast-frustum.txt](files/rast-frustum.txt) | [<img class="demo big" src="files/rast-frustum.png"/>](files/rast-frustum.png) | Includes both zero and negative $w$ values; if you don't clip it probably won't run at all. |
| [rast-manyclip.txt](files/rast-manyclip.txt) | [<img class="demo big" src="files/rast-manyclip.png"/>](files/rast-manyclip.png) | Two intersecting triangles extending both behind and in front of camera clipped by several frustum walls. |


## Electives that WebGL implements as shaders

| Input | Output | Notes |
|:------|:------:|:------|
| [rast-textures.txt](files/rast-textures.txt) | [<img class="demo big" src="files/rast-textures.png"/>](files/rast-textures.png) | Note that straight lines in the textures look straight because the file uses `hyp`; without that it would have had changes in angle where the two triangles of each face met, like this:<br><img class="demo big" src="files/rast-badtextures.png"/><br>There are multiple places in texture code where rounding can be done in several ways; rather than enumerate them all, we accept images where the textures are shifted up to one full texel from our reference images. |
| [rast-matrix.txt](files/rast-matrix.txt) | [<img class="demo big" src="files/rast-matrix.png"/>](files/rast-matrix.png) | This is an RGB/CMY cube rendered twice using matrices we'll learn to construct later in the course. |
| [rast-decals.txt](files/rast-decals.txt) | [<img class="demo big" src="files/rast-decals.png"/>](files/rast-decals.png) |  |

## Electives related to efficiency 

| Input | Output | Notes |
|:------|:------:|:------|
| [rast-2d3d.txt](files/rast-2d3d.txt) | [<img class="demo big" src="files/rast-2d3d.png"/>](files/rast-2d3d.png) | Cube uses `position 3`; rectangle uses `position 2`; both use `uniformMatrix` to verify that they are converted to 4-vectors internally. |
| [rast-cull.txt](files/rast-cull.txt) | [<img class="demo big" src="files/rast-cull.png"/>](files/rast-cull.png) | Both cubes have the same 12 triangles, though one has them at half the size of the other; but the specification order differs. For example, one cube has triangle `0 1 2` and the other `1 0 2`, leading one to be clockwise and the other counter-clockwise when rendered. |

## Electives related to visual effects

| Input | Output | Notes |
|:------|:------:|:------|
| [rast-alpha.txt](files/rast-alpha.txt) | [<img class="demo big" src="files/rast-alpha.png"/>](files/rast-alpha.png) | There are many different things that can go wrong here; the most common erros are:<br/>• Using premultiplied alpha formulas.<br/>• Using sRGB for one color and linear for the other.<br/>• Trying to apply sRGB to alpha channel.<br/>• Cumulative rounding errors from repeated conversion to bytes and back to floats.<br/>• Not storing the resulting alpha in the frame buffer. |
| [rast-fsaa2.txt](files/rast-fsaa2.txt) | [<img class="demo big" src="files/rast-fsaa2.png"/>](files/rast-fsaa2.png) | re-colored `rast-depth` with 2×2 subpixels for 4 levels of opacity along borders. |
| [rast-fsaa8.txt](files/rast-fsaa8.txt) | [<img class="demo big" src="files/rast-fsaa8.png"/>](files/rast-fsaa8.png) | re-colored `rast-depth` with 8×8 subpixels for 256 levels of opacity along borders.<br/>You may wish to try adding `fsaa 8` to the `rast-gammabox.txt` and see if you can explain what comes out and where the new horizontal bands come from |
| [rast-points1.txt](files/rast-points1.txt) | [<img class="demo big" src="files/rast-points1.png"/>](files/rast-points1.png) | Points, some colored and some textured, overlapping with triangles. |
| [rast-points2.txt](files/rast-points2.txt) | [<img class="demo big" src="files/rast-points2.png"/>](files/rast-points2.png) | The same as `rast-points1` but with different image dimensions, emphasizing that point sizes are specified in pixels and do not expand if placed in a bigger image. |

# State

In this assignment you will implement a subset of the GPU operation of WebGL2 and related rendering libraries.
The commands in the text files we provide are inspired by the WebGL2 API, and will work best if you mimic in your code the GPU state that WebGL2 expects.

You'll have four broad kinds of state:

- Mode-switching state, mostly Booleans like "is the depth buffer on?"
- Uniform state shared by all geometry being rendered, such as texture maps and matrices
- Per-vertex attributes, stored in array buffers
- Connectivity state, stored in element array buffers

The attribute buffers in WebGL2 are assumed to be variable-length arrays of 4-vectors.
WebGL2 lets you specify many such buffers and use them in programmable ways using vertex shaders;
in this assignment we have just a few specific attributes:

- `position`, with coordinates $(x,y,z,w)$
- `color`, with coordinates $(r,g,b,a)$
- `texcoord`, with coordinates $(s,t)$
- `pointsize`, with coordinates $(p)$

WebGL2 lets you specify attributes with different numbers of coordinates than the internal state would suggest.
It fills in missing coordinates as $(0,0,0,1)$:

- if just one value $x$ is supplied use $(x,0,0,1)$;
- if two values $(x,y)$ are supplied use $(x,y,0,1)$;
- if three values $(x,y,z)$ are supplied use $(x,y,z,1)$;
- if four values $(x,y,z,w)$ are supplied use $(x,y,z,w)$.

The element array buffer is just a list of integers.

# Algorithm

Most lines of the input file will be manipulating state,
after which will be a drawing command.
The drawing command tells you which indices in the attribute buffers to connect into primitives.
You'll make those connections and then draw each primitive.

GPUs generally use the Bresenham algorithm to draw triangles,
modified with optimizations for cache locality like tiles,
optimizations for parallelism like stamps,
and optimizations of depth buffers like HiZ.
Bresenham is very efficient in hardware as it can avoid some of the complexities of floating-point arithmetic,
but you're writing code to run on the CPU with full floating-point support so we recommend using the simpler but functionally equivalent DDA algorithm instead.
We also don't recommend adding any of the hardware-oriented optimizations.

DDA works on vectors.
You should definitely code it with vectors, probably with long vectors including all of the attribute values at a point together in one (i.e. $(x,y,z,w,r,g,b,a,s,t)$ if you implement all the elective parts).
The only non-vector operations are:

- Viewport transformation does different things for $x$ and $y$
- DDA should step in $y$ along edges, in $x$ along scanlines
- Divide-by-$w$ is mostly vector, but the new $w$ is $1/w$ not $w/w$
- Divide-by-$1/w$ is mostly vector, but only applies to non-position parts (i.e., color and texcoord)

That's it.
Every other part of DDA uses vectors, and if you find yourself writing `something[2]` or `something.z` anywhere in your DDA code you did something wrong.

The result of DDA is interpolated values at each pixel.
Here you'll access individual coordinates:
$x$ and $y$ to be the pixel coordinate,
$z$ for the depth buffer,
$s$ and $t$ for texture lookups,
$a$ for alpha blending,
and $(r,g,b)$ for color.

# Input keywords

The file may have four types of keywords:

1. the required `png` keyword will always be first
2. mode-setting keywords are optional, but if present will precede any data or drawing keywords
3. data provision will always be present in some form
4. drawing occurs after some data provision, but may be interleaved with it

When a drawing command is encountered, it draws with the data provided so far.

:::example
Suppose a file has something like

1. `position`, `color`, and `texcoord`
2. a draw command
3. `texture` and new `position`
4. a second draw command

Then the first draw uses the first positions and no texture;
the second draw uses the new positions, old texcoord, and texture.
:::

We recommend reading the file once, line by line, modifying state for each non-draw command
and rendering based on the current state for each draw command.

## PNG

`png` *width* *height* *filename*
: - Always present in the input before any other keywords
	- *width* and *height* are positive integers
	- *filename* always ends `.png`

	:::note
	similar to creating a `<canvas>`{.html} element in WebGL2
	:::


## Mode setting

`depth`
: - enables the depth buffer and depth tests
	
	:::note
	similar to `gl.enable(gl.DEPTH)`{.js} in WebGL2
	:::

`sRGB`
: - enables sRGB conversion of colors prior to saving in the PNG file
	
	:::note
	always enabled in WebGL2
	:::

`hyp`
: - enables hyperbolic (also called perspective-correct) interpolation of depth, color, and texture coordinates
	
	:::note
	always enabled in WebGL2
	:::

`fsaa` *level*
: - enables full-screen anti-aliasing, also called multisampling
	- *level* is a small positive integers (between 1 and 8)
	- implement by rendering in a framebuffer and depth buffer with *level*×*level* subpixels per final PNG pixel
	
	:::note
	similar to `getContext('webgl2', {antialias:true})`{.js} when creating a WebGL2 rendering context; enabled by default on some browsers, not in others
	:::

`cull`
: - enables back-face culling

	:::note
	similar to `gl.enable(gl.CULL_FACE)`{.js} and `gl.cullFace(gl.BACK)`{.js} in WebGL2
	:::

`decals`
: - when drawing transparent textures, include the vertex colors underneath
	
	<details class="note"><summary>similar to putting code like this in a WebGL2 fragment shader:</summary>
		
	````glsl
	uniform sampler2D theImage;
	in vec4 vertcolor;
	in vec2 texcoord;
	out vec4 color
	void main() {
		vec4 texcolor = texture(theImage, vec2(s,t));
		color = vec4(texcolor.rgb*texcolor.a + vertcolor.rgb*(1-texcolor.a), 
								 texcolor.a + vertcolor.a - texcolor.a*vertcolor.a);
	}
	````
	
	</details>

`frustum`
: - enables frustum clipping
	
	:::note
	always enabled in WebGL2
	:::

## Uniform state

`texture` *filename*
: - *filename* will always end `.png` and always be the filename of an existing PNG file on the grading server during testing
  - PNG files are specified in sRGB color space; you should either (preferably) convert to linear before processing and then back to sRGB at the end or (less preferably) pass the texel bytes through to the output image unchanged
	
	<details class="note"><summary>similar to the following sequence of WebGL2 calls:</summary>

	````js
	let img = new Image()
	img.src = filename
	img.addEventListener('load', event => {
		let texture = gl.createTexture()
		gl.activeTexture(gl.TEXTURE0)
		gl.bindTexture(gl.TEXTURE_2D, texture)
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT)
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT)
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST)
		gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST)
		gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img)
	})
	let bindPoint = gl.getUniformLocation(program, 'samplerNameInFragmentShader')
	gl.uniform1i(bindPoint, 0)
	````
	
	</details>

`uniformMatrix` *n0* *n1* *n2* ... *n14* *n15*
:	- When drawing, multiply the xyzw coordiantes by the following matrix before other operations:
		$$\begin{bmatrix}n_0&n_4&n_8&n_{12}\\n_1&n_5&n_9&n_{13}\\n_2&n_6&n_{10}&n_{14}\\n_3&n_7&n_{11}&n_{15}\end{bmatrix} \begin{bmatrix}x\\y\\z\\w\end{bmatrix}$$
	
	<details class="note"><summary>similar to the `gl.uniformMatrix4fv(m, false, new Gloat32Array([n0, n0, ... n14, n15])`{.js} in WebGL2 where the vertex shader includes:</summary>

	````glsl
	in layout(location=0) position;
	uniform mat4 m;
	void main() {
		gl_Position = m * position;
	}
	````
	
	and `m` is returned by `gl.getUnformLocation(program, 'm')`{.js}
	
	</details>

## Buffer provision

`position` *size* *num0* *num1* *num2* ...
: - *size* is either `2`, `3`, or `4`
	- there are a *size* multiple of numbers after *size* (e.g. if *size* is 3 there will be 3 or 6 or 9 or 12 or ... additional numbers)
	- the numbers are the coordinates of position vectors for vertices, with missing $z$ being implicitly 0 and missing $w$ being implicitly 1.
		
		<div class="example">
		
		`position 2 4 1 8 0.4 0.1 0.8`
		
		provides 6 numbers paired for 3 vectors:
		$$\big[ (4,1), (8,0.4), (0.1,0.8) \big]$$
		or, filling in the missing coordinates to make 4-vectors,
		$$\big[ (4,1,0,1), (8,0.4,0,1), (0.1,0.8,0,1) \big]$$
		
		</div>
		
	- coordinates are provided in normalized device coordinates, with $x=-1$ being the left edge of the screen and $+1$ the right edge; $y=-1$ the top edge of the screen and $+1$ the bottom edge, etc.
	
	<details class="note"><summary>similar to the following sequence of WebGL2 calls:</summary>
	
	````js
	let buffer = gl.createBuffer()
	gl.bindBuffer(gl.ARRAY_BUFER, buffer)
	gl.bufferData(gl.ARRAY_BUFER, new Float32Array(num0, num1, num2, ...), gl.STATIC_DRAW)
	gl.vertexAttribPointer(7, size, gl.FLOAT, false, 0, 0)
	gl.enableVertexAttribArray(7)
	````
	
	where the vertex shader has `in layout(location=7) position;`{.glsl}
	
	</details>


`color` *size* *num0* *num1* *num2* ...
: - *size* is either `3`, or `4`
	- otherwise similar to `position`, but giving RGBA colors instead of XYZW positions
	- RGB colors are provided in linear color space (not sRGB) with 0 = no intensity and 1 = full-intensity light
	- A, if provided, is opacity with 0 = fully transparent and 1 = fully opaque
	
	:::note
	similar to how WebGL2 blends if you call `gl.enable(gl.BLEND)`{.js} and `gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)`{.js}
	:::

`texcoord` *size* *num0* *num1* *num2* ...
: - *size* is always `2`
	- otherwise similar to `position`, but giving ST texture coordinates instead of XYZW positions
	- coordinates are provided in normalized texel coordinates, with $(0,0)$ one corner of the texture and $(1,1)$ the opposite corner
	- wrap coordinates into the 0–1 range *after* interpolation. For example, texel coordinates $-0.3$, $0.7$, and $1.7$ would all render the same (i.e. as if they were $0.7$).

`pointsize` *size* *num0* *num1* *num2* ...
: - *size* is always `1`
	- otherwise similar to `position`, but giving point sizes instead of XYZW positions
	- coordinates are provided as the size of rendered points, measured in pixels.


`elements` *i0* *i1* *i2* ...
: - all indices are non-negative integers
	
	<details class="note"><summary>similar to the following sequence of WebGL2 calls:</summary>
	
	````js
	let buffer = gl.createBuffer()
	gl.bindBuffer(gl.ELEMENT_ARRAY_BUFER, buffer)
	gl.bufferData(gl.ELEMENT_ARRAY_BUFER, new Uint16Array(i0, i1, i2, ...), gl.STATIC_DRAW)
	````
	
	</details>

## Drawing

`drawArraysTriangles` *first* *count*
: - `count` will be a multiple of 3 (this is not required in WebGL2)
	- draws a triangle with vertices `position[first+0]`, `position[first+1]`, `position[first+2]` and corresponding `color` and `texcoord`s
		
		draws a triangle with vertices `position[first+3]`, `position[first+4]`, `position[first+5]` and corresponding `color` and `texcoord`s
		
		...
		
		draws a triangle with vertices `position[first+count-3]`, `position[first+count-2]`, `position[first+count-1]` and corresponding `color` and `texcoord`s
	
	:::note
	similar to `gl.drawArrays(gl.TRIANGLES, first, count)`{.js} in WebGL2
	:::
	
`drawElementsTriangles` *count* *offset*
: - `count` will be a multiple of 3 (this is not required in WebGL2)
	- draws a triangle with vertices `position[elements[offset+0]]`, `position[elements[offset+1]]`, `position[elements[offset+2]]` and corresponding `color` and `texcoord`s
		
		draws a triangle with vertices `position[elements[offset+3]]`, `position[elements[offset+4]]`, `position[elements[offset+5]]` and corresponding `color` and `texcoord`s
		
		... and so on up to `position[element[offset+count-1]]`
	
	:::note
	similar to `gl.drawElements(gl.TRIANGLES, count, gl.UNSIGNED_SHORT, offset)`{.js} in WebGL2
	:::
	
`drawArraysPoints` *first* *count*
: - draws a square centered on `position[first+0]` with diameter `pointsize[first+0]` pixels and color `color[first+0]`
		
		draws a square centered on `position[first+1]` with diameter `pointsize[first+1]` pixels and color `color[first+0]`
		
		... and so on up to `position[first+count-1]`
	
	- each square has texture coordinates varying from $(0,0)$ in its top-left corner to $(1,1)$ in its bottom-right corner; this is similar to the built-in `gl_PointCoord`{.glsl} in WebGL2

	:::note
	similar to `gl.drawArrays(gl.POINTS, first, count)`{.js} in WebGL2
	:::
	
