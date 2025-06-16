---
title: Deferred Shading
summary: Using more memory to reduce time needed for fancy lighting effects.
...

There are three common ways to light a scene

Gouraud shading
:   Compute lighting per vertex in the vertex shader; let DDA/Bresenham interpolate the resulting colors to fragments.
    
    Pro
    :   - fast in common case where there are many fewer vertices than fragments
        - no memory required
    
    Con
    :   - polygon edges become visible to the casual observer
        - localized effects like point lights and specular highlights tend to behave erratically, with too-strong impact when near a vertex and too-weak impact when near the middle of a triangle
    
    Overall
    :   Was common in the 1990s, less so in the 2000s, mostly unused since in the 2010s


Baked lighting
:   Include texture maps that are already lit, with shadows and so on pre-computed.
    
    Pro
    :   - almost no GPU work needed
        - allows indirect lighting and other computationally expensive lighting
    
    Con
    :   - resolution must be predetermined
        - scene geometry and lighting must be static
        - does not scale well with very large scenes
        - may require multiple textures per object to model angle-dependent effects such as specular highlights
    
    Overall
    :   Common for ambient diffuse lighting, but rarely the entire lighting solution.

Per-pixel lighting
:   Also called "Phong shading" (not to be confused with [Phong lighting](lighting.html#specular-light)), in this model the data needed to performing the lighting is interpolated via DDA/Bresenham to each pixel, where the actual lighting happens.
    
    Pro
    :   - handles localized effects like point lights well
        - handles angle-dependent effects such as specular highlights well
        - easily integrates with other effects like shadow and bump mapping and toon shading
    
    Con
    :   - significantly more work from the GPU, especially if there are many light sources
    
    Overall
    :   The default for most interactive 3D graphics today

----

Within the per-pixel lighting model there are two common approaches

Forward rendering
:   Light every fragment, even though some will be replaced by other fragments by the depth buffer.

    Pro
    :   - simple to program
        - no additional memory required
    
    Con
    :   - much of the GPU's work is discarded without being seen
        - culling lights requires CPU-intensive matrix-aware computation and many fragment shaders

Deferred rendering
:   Also called "deferred shading"^[Some people use "deferred rendering" and "deferred shading" to mean two different but related ideas, but most sources I consulted in 2022 used them as synonyms.], this is a two-pass system.
    
    Pass 1: instead of a color buffer, the data needed to compute colors are stored in several "G-buffers". filtered by the depth buffer so that we end up with just one position, normal, and material per pixel.
    
    Pass 2: iterate over the G-buffers, computing one color per pixel (not per fragment like forward rendering does).
    
    Pro
    :   - lighting complexity is independant of scene geometry complexity
        - compatible with readily-implemented tile-based culling of lights
        - compatible with various post-process effects like depth of field and fisheye lenses
    
    Con
    :   - more involved to program
        - much more GPU memory required
        - only faster if the scene is complicated

# Implementing deferred shading in WebGL2

You'll need (at least) two GLSL programs to implement deferred rendering.

## Pass 1 shaders

The first pass's geometry inputs and vertex shader source are the same you'd use for forward rendering.

The first pass's fragment shader should have several `out vec4`s.
WebGL2 guarantees you can use at lest 4, and depending on the GPU and browser maybe as many as 16; most GPUs and browsers I checked in 2022 supported either 4 or 8.

The fragment shader should do as little work as possible.
If you have few enough inputs that all of them can fit into the available `out vec4`, just put them there and end.
If you have too many, do the minimal amount of work needed to get the remaining information to fit in those `out vec4`.
For example, if you have a base color with a translucent texture overlay you could look up the texture and combine the two into a single color -- but only do this if you can't fit the texture coordinate and mip-map level into the `out vec4`s.

## Calling the two passes

Pass 1 needs to render into a G-buffer, which we implement using an off-screen structure called a frame buffer

```js
var gBuffer = gl.createFramebuffer() // make the G-buffer
gl.bindFramebuffer(gl.FRAMEBUFFER, gBuffer) // and tell GL to use it
```

The frame buffer needs to store its various out vectors into textures for the second pass to use

```js
gl.activeTexture(gl.TEXTURE0) // in pass 1, can re-use one active texture

// set up the output buffers
var outBuffers = []
var targets = []
for(let i=0; i < numberOfOututs; i += 1) {
    var target = gl.createTexture()
    gl.bindTexure(gl.TEXTURE_2D, target)
    // ... set up pixelStore and texParameteri here like usual ...
    gl.texStorage2D(gl.TEXTURE_2D, 1, gl.RGBA16F,
        gl.drawingBufferWidth, gl.drawingBufferHeight)
    gl.framebufferTexture2D(gl.FRAMEBUFFER,
        gl.COLOR_ATTACHMENT0 + i, gl.TEXTURE_2D, target, 0);
    targets.push(target)
    outBuffers.push(gl.COLOR_ATTACHMENT0 + i)
}
gl.drawBuffers(outBuffers)

// also need a depth buffer
var depthTexture = gl.createTexture()
gl.bindTexure(gl.TEXTURE_2D, depthTexture)
// ... set up pixelStore and texParameteri here like usual ...
gl.texStorage2D(gl.TEXTURE_2D, 1, gl.DEPTH_COMPONENT16,
    gl.drawingBufferWidth, gl.drawingBufferHeight)
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.DEPTH_ATTACHMENT,
    gl.TEXTURE_2D, depthTexture, 0);
```

The second pass setup needs all of the G-buffer textures, and may need others for usual texture look-up too

```js
for(let i = 0; i < targets.length; i+=1) {
    gl.activeTexture(gl.TEXTURE0 + i)
    gl.bindTexture(gl.TEXTURE_2D, targets[i])
}
// bind other textures using `gl.TEXTURE0 + targets.length` and beyond
```


The first pass drawing code needs to use the framebuffer and depth tests

```js
gl.bindFramebuffer(gl.FRAMEBUFFER, gBuffer)
gl.useProgram(glslProgramForFirstPass)
gl.enable(gl.DEPTH_TEST)
gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFER_BIT)
// draw the geometry here
```

The second pass drawing code needs to use the default framebuffer and no depth

```js
gl.bindFramebuffer(gl.FRAMEBUFFER, null)
gl.useProgram(glslProgramForSecndPass)
gl.disable(gl.DEPTH_TEST)
gl.clear(gl.COLOR_BUFFER_BIT)
// draw the full-screen quad here
```

## Pass 2 shaders

The second pass geometry should be a simple quad that fills the screen with a "where on the screen is it" texture coordinate.

The second pass fragment shader should look up the data stored by the first pass in the supplied `uniform sampler2D`s and use them to complete the lighting and shading computation.

    

