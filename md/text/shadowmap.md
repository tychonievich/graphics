---
title: Shadow maps
summary: Implementation guides for the most common approach to adding shadows to interactive graphics.
...


Here we discuss only the simplest form of shadow mapping:
the case where the shadows are cast by one light
and all fall inside a reasonably-narrow frustum.

# Outline

As discussed in [Using Textures](textures2.html),
the basic steps to shadow mapping are:

1. Load a view and projection matrix to view the scene from the perspective of the light.
2. Render a depth buffer (no color buffer) into a texture map called a shadow map.
3. Load a view and projection matrix to view the scene from the perspective of the viewer.
4. In the fragment shader
    a. find the distance to the light and position of the fragment from the light's perspective
    b. use the position to look up the maximum depth the camera can see in that direction
    c. if the maximum depth from the texture is closer than the fragment's depth, the fragment is in shadow

Elements of realizing this outline are described below.

# Code Organization

You'll want two shader programs:
one with a cheap fragment shader for rendering shadows
and one with an expensive fragment shader for rendering the lit scene.
We also want to send the exact same geometry to both.
That means we'd rather use just one vertex array object, shaded between both programs.

## Fixed-index attributes

Attribute locations can either be specified manually or supplied by the GLSL compiler;
see [Using video memory](buffers.html) and [Our Dialect of WebGL2](dialect.html) for more.
Because shadow maps entail rendering the same geometry with two quite different shader programs, the manual-specification version is much preferred for shadow maps.

## Drawing twice

We'll draw the scene twice each frame.
Once we'll render using the shadow map's shaders and render to a texture.
Then we'll render using the display's shaders and render to the canvas.
To support this, it's best to have the drawing function split in two;
conceptually something like

    drawStuff() {
        draw 1st object
        draw 2nd object
        and so on
    }
    
    drawScene() {
        load shadow program
        set up and clear shadow buffer as destination
        drawStuff()
        
        load display program
        set up and clear canvas as destination
        drawStuff()
    }

If you have a scene where different objects need different shaders this organization will become more complicated.

# Render depth to a texture

WenGL renders to something called a "framebuffer",
which is a raster with two roles.
One role is as the destination where colors and so on are written during rendering.
The other role is as something to display in some fashion.

By default, WebGL creates one RGBA framebuffer for the canvas object;
it's "display in some fashion" is "display in the canvas" and is handled by the browser.

We'll want a second framebuffer for the shadow map;
it's "display in some fashion" will be "use as a texture during the display rendering".
To do that we'll need to

1. Make a texture
2. Set it up with a high-fidelity single channel
3. Make a framebuffer
4. Connect the two

```js
// 1. make a texture
const shadowMap = gl.createTexture();
const smSize = 512;        // power of 2 fastest on some GPUs
gl.bindTexture(gl.TEXTURE_2D, shadowMap);
gl.texImage2D(
    gl.TEXTURE_2D,         // same we bound to in line above
    0,                     // mip level
    gl.DEPTH_COMPONENT32F, // 2. set up high-fi channel
    smSize, smSize,        // width and height
    0,                     // border
    gl.DEPTH_COMPONENT,    // format
    gl.FLOAT,              // 2. set up high-fi channel
    null);                 // no data: we'll render into it instead

// add the usual `gl.textParameteri` calls here;
// typically NEAREST and CLAMP_TO_EDGE are used for shadow maps

// 3. make a framebuffer
const shadowFB = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, shadowFB);
// 4. connect the two
gl.framebufferTexture2D(
    gl.FRAMEBUFFER,       // same we bound to in line above
    gl.DEPTH_ATTACHMENT,  // should get the depth buffer (only)
    gl.TEXTURE_2D,        // destination is bound here
    shadowMap,            // destination is stored here
    0);                   // mip level
```

# Matrices and Lookups

For the shadow map pass, we'll load a view and projection matrix for the light.
For the scene pass, we'll load a view and projection matrix for the camera.
We'll also presumably have various model matrices for different scene objects.

In the scene pass's fragment shader, we'll have a fragment coordinate
and want to find which texel of the shadow map it corresponds to.
There are multiple ways to do that, but the easiest to describe is this:

1. Interpolate world position (post-model, pre-view) to each fragment.
2. Replicate the shadow's vertex shader and viewport work:
    a. multiply the interpolated world position by the shadow's (projection × view) matrix
    b. divide $x$, $y$, and $z$ by $w$
    c. mimic viewport: add 1 to $x$ and $y$ and scale $x$ and $y$ by `smSize/2`
3. look up the shadow map texel at the given $x$ and $y$ and compare the value there with the $z$ you have

:::exercise
Parts of the fragment shader work above can be moved to the vertex shader, improving runtime by doing the work only once per vertex instead of once per fragment.
How much can be so moved?
:::


# Avoiding self-shadowing

Naively implemented, shadow maps will cause roughly half of all not-in-shadow fragments to appear to be in shadow.
This is because the texel in the shadow map was generated in a slightly different place on the model than the fragment was, meaning it was generated at a different depth from the camera.
The name for this phenomenon is "shadow acne".

Several solutions to this are possible.

1. Shadow bias.

    A *bias* is decision process that favors one outcome over the other.
    A shadow bias favors "not in shadow" by checking $z_{\text{shadow map}} + \epsilon < z_{\text{fragment}}$ where $\epsilon$ is the bias.
    
    This is easy to implement but hard to tune:
    too small a bias gives self-shadowing
    while too large a bias gives bleed-through lighting when the shadow caster is close to the shadow receiver.

2. Culling.

    If all your objects are 2-sided and have consistent triangle winding directions
    then you can cull front faces during shadow projection
    and back faces during scene rendering.
    Because shadows are being case by the back of the object
    but received by the front, they will only self-shadow for very thin objects.

3. Multiple samples.
    
    Instead of using the GLSL built-in `texture` function to look up texels,
    we could manually compute several indices into the texture:
    `textureSize(shadowMap, 0)` retrieves the texture's dimensions
    and `texelFetch(shadowMap, someVec2i, 0)` retrieves a specific texel.
    We could, for example, say that a fragment is in shadow
    only if all four of its surrounding shadow map texels are closer to the light than it is.
    
    Taking multiple samples is also one way to create soft shadows,
    though the best techniques for that work in different ways.
