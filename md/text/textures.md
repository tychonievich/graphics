---
title: Textures in WebGL
summary: The mechanics of getting them set up and rendering.
...

A **texture** is a raster, a part of which is interpolated over a triangle.
There are many nuances to consider in doing this, and may ways to use the result.

A pixel in a texture raster is called a **texel**.

This page is an alternative to [Mozilla's page](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Tutorial/Using_textures_in_WebGL); you might find either one easier than the other.

# From file name to Sampler2D

In WebGL, a texture loaded onto the GPU is called a `sampler2D` and is always supplied as a `uniform` in the fragment shader.

:::example
This block starts a running example used across the page
```glsl
uniform sampler2D aTextureIPlanToUse;
```
:::

To use the `sampler2D` we have to look up a texel in it.
The most common tool for this is the `texture` function.

:::example
(continued)
```glsl
vec4 lookedUpRGBA = texture(aTextureIPlanToUse, vec2(s,t));
```
:::

There are many steps to getting things set up so this will work.

1. Load an image in HTML
    
    Images come in many formats, but fortunately your browser knows how to open most of them.
    However, opening an image off-screen can be used by spyware so browsers protect it; you'll need to worry about [CORS](cors.html) and some websites will refuse to let you load their images.
    
    URLs include relative paths for when the image is hosted on the same machine as the HTML file.
    
    <div class="example">
    (continued)
    
    ````js
    let img = new Image();
    img.crossOrigin = 'anonymous';
    img.src = urlOfImageAsString;
    img.addEventListener('load', (event) => {
        // ...
    ````
    </div>
    
    Note that if you need it, the pixel-unit dimensions of the image are accessible as
    `img.width` and `img.height` inside the the `load` callback.
    
2. Pick where to save the image on the GPU
    
    There are three GPU locations being used here:
    
    - `gl.createTexture()` returns a pointer to where the texture data will be stored in GPU memory
    - `gl.TEXTURE0 + slot` picks which of the texture read ports in the fragment shader to use
    - `gl.TEXTURE_2D` is the input slot we use to provide the GPU with information about the texture
    
    <div class="example">
    (continued)
    
    ````js
        // ...
        let slot = 0; // or a larger integer if this isn't the only texture
        let texture = gl.createTexture();
        gl.activeTexture(gl.TEXTURE0 + slot);
        gl.bindTexture(gl.TEXTURE_2D, texture);
        // ...
    ````
    </div>

3. Describe how look-ups should happen
    
    The GLSL `texture` function accepts `float`-valued coordinates in the 0–1 range,
    while images have `int`-valued indices in ranges that vary depending on image resolution.
    We have to tell WebGL how the `texture` function should map between these two
    in at least two ways:
    
    a.  What should happen if the texture coordinate is outside the 0–1 range?
        Options are
        
        - `gl.REPEAT` (default value): 1.2 is treated like 0.2
        - `gl.CLAMP_TO_EDGE`: 1.2 is treated like 1.0
        - `gl.MIRRORED_REPEAT`: 1.2 is treated like 0.8
        
        <div class="example">
        (continued)

        ````js
            // ...
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
            // ...
        ````
        </div>
    
    b. What should happen if the texture is zoomed in (`MAG_FILTER`) or zoomed out (`MIN_FILTER`)?
        Options are
        
        - `gl.LINEAR` (default value for zoomed-in): linearly interpolate colors based on exact texture coordinate
        - `gl.NEAREST`: round to the nearest texel
        - `gl.`*x*`_MIPMAP_`*y* where *x* and *y* are each either `LINEAR` or `NEAREST`: only available for zoomed-out; see [mipmaps](#mipmaps) for details
        
        <div class="example">
        (continued)

        ````js
            // ...
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
            // ...
        ````
        </div>

4. Send the pixel data to the GPU

    <div class="example">
    (continued)

    ````js
        // ...
        gl.texImage2D(
            gl.TEXTURE_2D, // destination slot
            0, // the mipmap level this data provides; almost always 0
            gl.RGBA, // how to store it in graphics memory
            gl.RGBA, // how it is stored in the image object
            gl.UNSIGNED_BYTE, // size of a single pixel-color in HTML
            img, // source data
        );
        gl.generateMipmap(gl.TEXTURE_2D) // lets you use a mipmapping min filter
    })
    ````
    </div>

# Using the texture

Uniforms need to be told what their value is in the draw routine.
For a sampler, we just give that uniform the slot where we put the texture.

:::example
(continued)

````js
gl.uniform1i(program.uniforms.aTextureIPlanToUse, slot) // where `slot` is same it was in step 2 above
````
:::

We also need to have some way to know what texture coordinate to look up.
This can be any `vec2` we want, but we usually make it an attribute supplied with the positions, normals, and other per-vertex model information.

:::example
A miminal vertex and fragment shader pair to use texture coordinates and a texture might be

```glsl
#version 300 es
in location(0) vec4 position;
in location(1) vec2 aTexCoord;
out vec2 vTexCoord;

void main() {
    gl_Position = position;
    vTexCoord = aTexCoord;
}
```

```glsl
#version 300 es
precision highp float; // a precision statmeent is required for fragment shaders
uniform sampler2D image;
in vec2 vTexCoord;
out vec4 color;

void main() {
    color = texture(image, vTexCoord);
}
```
:::


# Mipmaps

When we zoom in on a texture, such that one texel covers many pixels, we can either treat the texels as squares of color (`gl.TEXTURE_MAG_FILTER, gl.NEAREST`) or as pints between which to linearly interpolate (`gl.TEXTURE_MAG_FILTER, gl.LINEAR`).
We could also try fancier interpolations, but that's all we've got:
the four nearest texels, interpolated in some fashion.

But when we zoom out we have a much more complicated set of options.
At the extreme case, if the entire texture fits inside a single pixel,
we want to show not some interpolation of a few texels
but rather the average color of the entire set of texels.
Looping over a potentially-large region of a texture in each fragment is computationally prohibitive, so we want some better way of doing that.

Enter Lance Williams' 1983 contribution of pyramidal parametrics, more popularly known as mipmaps^[
    "mip" from the Latin initialism "*multum in parvo*" meaning "much in a small space";
    and "map" borrowed from "bitmap", a simple kind of image.
].
The idea runs as follows:

1. Store the full image. When texels are covering multiple pixels, use it.
2. Also store a half-size copy of the image, and a quarter-size copy, and so on down to a one-texel copy.
3. When a pixel is about big enough to cover 16 texels, use the quarter-size copy (because there are $\frac{1^2}{4^2} = \frac{1}{16}$ as many texels in that copy so it gets to roughly one pixel per texel)
3. If a pixel would cover a non-power-of-two number of texels,
    we can either pick the nearest-scale level
    (`gl.NEAREST_MIPMAP_`*y* is either `LINEAR` or `NEAREST`)
    or check the two nearby levels and interpolate between them
    (`gl.LINEAR_MIPMAP_`*y* is either `LINEAR` or `NEAREST`).

WebGL lets us specify each level of the mipmap individually, but most often it makes more sense to call
`gl.generateMipmap(gl.TEXTURE_2D)`{.js}
just after calling `gl.texImage2D`.

Once we generate mipmaps and change the `gl.TEXTURE_MIN_FILTER` to use them,
we get nice-looking zoomed-out textured with no additional work.

:::aside
How does the GPU know what level to use?

You may have noticed that nothing in this section had us specify what level to use in the fragment shader's `texture` call.
But we didn't leave anything out: you can just use `texture` and be confident it will pick the right level of the mipmap for you.
How can that be?

The ideal level of detail is based on the spatial derivative of the texture coordinate.
The DDA step size is a close approximation of that derivative for each `in` value in the fragment shader.
Each operator on a value has a corresponding operation it would do on the derivative of the value,
so it is possible to push that derivative all the way through to the texture coordinate no matter how complicated the intervening code may be.

If tracking derivatives like that seems like a lot of work, the [OpenGL ES 3.0 specification](https://registry.khronos.org/OpenGL/specs/es/3.0/es_spec_3.0.pdf#page=167) that WebGL2 conforms agrees with you. After introducing a derivative-based approach in equations 3.20 and 3.21 it then says

> <q>While it is generally agreed that equations 3.20 and 3.21 give the best results
when texturing, they are often impractical to implement. Therefore, an implementation may approximate the ideal $ρ$ with a function $f(x, y)$ subject to these conditions:</q>

... followed by two conditions that are satisfied by a wide set of reasonable approximations.
An example approximation that meets the conditions is to compute the full level of detail at each vertex and then interpolate the results using DDA.
:::

# Cube Maps

See also [WebGL2Fundamentals' introduction to cube maps](https://webgl2fundamentals.org/webgl/lessons/webgl-cube-maps.html)

Some uses of textures prefer to be able to look up using 3D unit vectors;
this is useful for any kind of environment mapping such as emulating reflection and refraction and using full-scene lighting.

The problem is, a sphere of coordinates does not map cleanly to a 2D texture.
That is a problem best studied in terms of [map projections](https://en.wikipedia.org/wiki/Map_projection), but a few solutions are of particular interest in texture mapping.

- **Latitude and Longitude** are a simple way to turn a point on the surface of a sphere into a 2D coordinate.
    In GLSL, we can compute these with the `atan` function.
    
    <div class="example">
    Revising our running example for a cube map, we have
    
    ````glsl
    float longitude = atan(pt.y, pt.x);
    float latitude = atan(pt.z, length(pt.xy));
    vec2 texCoord = vec2(latitude/6.283185307179586+0.5,
                         longitude/3.141592653589793+0.5);
    ````
    </div>
    
    Note, though, that that's a fairly expensive computation: `length` involves a square root and `atan` is a trigonometry function approximated by most hardware using with a high-order polynomial.
    
    Latitude and longitude textures have much more detail near the poles than near the equator, which is often not a wise use of memory.

- The **Equiareal Circular Projection** is a less-common but less-expensive way to turn a point on the surface of a sphere into a 2D coordinate.
    In GLSL, we can compute it with a few vector normalizations:
    
    <div class="example">
    Revising our running example for a cube map, we have
    
    ````glsl
    vec3 bubble = normalize(pt);
    vec3 offset = vec3(bubble.x, bubble.y, bubble.z+1);
    vec3 projected = normalize(offset);
    vec2 texCoord = vec2(projected.x*0.5 + 0.5,
                         projected.y*0.5 + 0.5);   
    ````
    </div>
    
    While this is easier to compute than latitude and longitude and has each texel covering the same amount of space on the sphere,
    it wastes just over 21% of texels and has strangely-shaped texels: near the edge of the circle a texel covers a very wide and thin region of the sphere.

- The **Cube Map** projects the sphere onto the six faces of a cube.
    In GLSL this would be very easy to compute:
    the coordinate with the largest magnitude tells us which of the six images we are looking at
    and dividing the other two coordinates by that largest-magnitude coordinate gives the correct texture coordinate.
    
    However, we don't need to compute it because WebGL gives us built-in support for cube maps, described in the rest of this section.

To use a cube map, we provide the GPU with six separate textures, one for each face.
A revised set of steps is:

1. Load *six* images in HTML, like with we did for 2D textures
    
2. Pick where to save the image on the GPU

    Mostly like 2D textures, but use the `gl.TEXTURE_CUBE_MAP` input slot instead of the `gl.TEXTURE_2D` input slot.
    
    <div class="example">
    Revising our running example for a cube map, we have
    
    ````js
        gl.bindTexture(gl.TEXTURE_CUBE_MAP, texture);
    ````
    </div>

    We only do this once for the full set of six faces, not once per face.

3. Describe how look-ups should happen
    
    Again, like 2D but use `gl.TEXTURE_CUBE_MAP` instead of `gl.TEXTURE_2D`

    <div class="example">
    Revising our running example for a cube map, we have
    
    ````js
        gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
        gl.texParameteri(gl.TEXTURE_CUBE_MAP, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    ````
    </div>
    
4. Send the pixel data to the GPU, once per face.
    
    Here the destination slots are `gl.TEXTURE_CUBE_MAP_POSITIVE_X` and its friends for all `POSITIVE` and `NEGATIVE` `X`, `Y`, and `Z`.

    <div class="example">
    Revising our running example for a cube map, we have
    
    ````js
        // ...
        gl.texImage2D(
            gl.TEXTURE_CUBE_MAP_NEGATIVE_Y, // destination slot
            0, // 0 means not a mipmap; >0 for mipmaps
            gl.RGBA, // how to store it in graphics memory
            gl.RGBA, // how it is stored in the image object
            gl.UNSIGNED_BYTE, // size of a single pixel-color in HTML
            imgNegY, // source data
        );
    }
    ````
    </div>

5. For mipmaps, after supplying all six faces call
    `gl.generateMipmap(gl.TEXTURE_CUBE_MAP)`{.js}

The uniform binding for the cube map is the same as for a 2D texture.

The fragment shader defines it as a `samplerCube` and uses a normalized 3D vector to access it.

<div class="example">
```glsl
uniform samplerCube myCubeMappedTexture;
out vec4 outColor;
in location(2) vec3 texCoord;
void main() {
   outColor = texture(myCubeMappedTexture, normalize(texCoord));
}
```
</div>
