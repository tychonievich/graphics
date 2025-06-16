---
title: Particle Effects
summary: Simple heuristic-based visual effects.
...

Broadly speaking, visual effects in 3D graphics can be categorized based on what is being manipulated.

Particles
:   Have location, momentum, and size, but not orientation.
    Points and spheres are simulated as particles.

Rigid bodies
:   Have shape, orientation, and angular momentum
    in addition to what particles have.
    Blocks, tables, and other hard objects are simulated as rigid bodies.

Soft bodies
:   Have deformation, stress, and strain in addition to what rigid bodies have.
    *Stress* refers to force that attempts to deform the object;
    *strain* refers to deformations away from the rest state.
    Rope, cloth, flesh, and other deformable objects with a fixed rest state are simulated as soft bodies.

Fluids
:   Are like soft bodies with unlimited deformations.
    *Incompressible* fluids do not change volume and include most liquids.
    *Viscous* fluids diffuse internal velocities, settling over time to all parts of the fluid having the same velocity;
    as viscosity increases they act more like rigid bodies.
    *Visco-Elastic* fluids exhibit both viscosity and internal forces that attempt to counter strain; as elasticity increases they act more like soft bodies.
    *Stress-thinning* fluids have viscosity that decreases as more pressure is applied and include anything spreadable, like paint and mayonnaise.
    *Stress-thickening* fluids have viscosity the increases as more pressure is applied and include materials like oobleck, silly putty, and gak.

This page discusses some topics related to particle effects.

# Meshes, Points, or Volumes

Suppose we have a set of particles we wish to draw.
Three primary methods for doing so are available to us.

## Mesh instancing

We can create a mesh and draw one instance of it centered at each particle's location.
The easy way to do this is looks like:

1. For each particle
    a. Load a model matrix for the particle's location and size
    b. Render the mesh

That, however, involves multiple calls between CPU and GPU per particle.
For very large numbers of particles it is more efficient (but more difficult to program) to do this instead:
    
1. Load all particle data into a 1D texture
2. Use `gl.drawElementsInstanced` to draw the mesh many times
3. In the vertex shader, use the `gl_InstanceID` to look up particle data from the 1D sampler

## Point rendering

We can put the particle locations in an array buffer and use `gl.drawArrays(gl.POINTS, ...)` to draw them,
then set `gl_PointSize` in the vertex shader
and color them in the fragment shader using `gl_PointCoord` to shade them.

Somewhat annoyingly, `gl_PointSize` is given in pixels
while all other coordinates in the vertex shader are given in some type of normalized coordinate system.
If we wish to achieve a particular world-space size, we need to set `gl_PointSize` as the product of four values:

- Viewport size in pixels in either $x$ or $y$.
    You'll have to pass this in as a `uniform float`;
    you can get it as `gl.canvas.width` or `gl.canvas.height`.

- Projection matrix scaling in the same axis.
    Assuming you are using a [standard perspective projection matrix](text/math2.html#division),
    this is either `proj[0][0]` for $x$
    or `proj[1][1]` for $y$, where `proj` is your projection matrix.

- The inverse of the `w` value for this point. That is `1/gl_Position.w`.

- The desired world-space diameter of the particle.

Inside your fragment shader you'll have access to `gl_PointCoord`, a `vec2` that is `vec2(0,0)` at the top-left corder of the point,
`vec(0.5, 0.5)` in the center of the point,
and `vec(1,1)` at the bottom-right corner of the point.
To make it just a circle, you can do

````glsl
if (length(gl_PointCoord* - vec2(0.5,0.5) > 0.25) discard;
````

The `discard` keyword tells GLSL not to use the fragment at all, and is handled in such a way that putting it in an `if` like this does not slow down the GPU the way `if`s usually do.


:::aside
Because division by $w$ is a linear (not spherical) projection,
spheres near the edge of the screen will render as non-circular.
The correct ellipse can be found with additional work;
see e.g. <https://iquilezles.org/articles/sphereproj/> and <https://jcgt.org/published/0002/02/05/paper.pdf>
:::

## Volumes

If particles are used to represent the volume of a material,
the surface of that material can be found by treating the particles as [metaballs](https://en.wikipedia.org/wiki/Metaballs) and polygonalizing the boundary using [marching cubes](https://en.wikipedia.org/wiki/Marching_cubes).
The details of those algorithms are beyond the scope of this page.

# What we do with Particles

## Gravity, collisions, and drag

See [the page on these topics](kinetics.html#particle-state-and-forces).

## Fire and Smoke

Particles can provide crude approximations of fire and smoke.
The key components are as follows:

### Billboards

When rendering fire and smoke with particles, it is common to treat the particles as *billboards*.
A **billboard** is an image rendered with 3D location directly facing the camera.
Points are a convenient way to render billboards,
though some GPUs will refuse to render very large billboards
so a more portal solution is to position, orient, and render textured quads instead.

For smoke and fire, it is typically best to have the image (texture map) resemble roughly symmetric burst of fire or puff of smoke
and render it as being quite transparent.

### Glowing

To make fire appear to glow, three considerations are useful.

1. Use additive blending.
    
    [`gl.blendFunc`](https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/blendFunc) allows many ways of combining colors;
    additive blending uses `gl.ONE` as the `dfactor`
    so that brightness can only increase.
    The most common `sfactor` is `gl.SRC_ALPHA`, with an `alpha` close to zero to ensure each particle only adds a little light.

2. Read but don't write the depth buffer.
    
    We want fire to be able to be occluded by other things,
    but we don't want other things to be occluded by it.
    The easiest way to achieve this is to first render all the non-fire,
    then diable depth buffer writing but keep depth-buffer checking and render the fire particles.

    Depth is controlled by three parameters.
    
    1. `gl.enable(gl.DEPTH_TEST)` turns using the depth buffer on
    2. [`gl.depthFunc`](https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/depthFunc) controls how the depth buffer is checked
    3. [`gl.depthMask`](https://developer.mozilla.org/en-US/docs/Web/API/WebGLRenderingContext/depthMask) controls how the depth buffer is written

3. Add light
    
    A point light source near the center of the flame and with a similar color to it will help the fire look like it is illuminating the scene.
    Adjusting the intensity of the light can help add a flame-like flicker effect.

### Smoke

Smoke should partially occlude sight of what is behind it.
If the smoke is purely black, that can be accomplished by using subtractive blending (the counterpart of additive blending mentioned for glowing), but for more reflective smoke that is not sufficient.
Instead, we'll need the following two parts.

1. Use [over-operator blending](fixed-functionality.html#blending).

2. Because over-operator blending is order-dependent,
    sort the particles by distance from the viewer before rendering.
    Sorting needs to be done on the CPU, not GPU.
    
    Because the primitives of a single draw call may all be rendered in parallel, it common to render particles one at a time with a separate invocation of `gl.drawElements` or `gl.drawArrays` for each particle.
    
    It is also possible to sort the particle values in a `gl.DYNAMIC_DRAW` array buffer and render them all at once.
    This approach is defined to work (per the spec, "one primitive must be drawn completely before any subsequent one can affect the framebuffer")
    though anecdotally some older graphics cards may not correctly implement this feature.

Smoke should should also partially shadow both itself and the scene behind it, a topic that is beyond the scope of this page.

## Particles driving animations

Particle effects result in the position and velocity of each particle at each frame.
Those can be used as input to and system that can build on top of that.

A common example is to use some kind of flocking/herding/crowd algorithm like [boids](https://www.red3d.com/cwr/boids/) on a set of particles,
then use the output to position models of creatures with the addition of some kind of movement animation like flapping wings or walking feet.
