---
title: "Spheres MP"
...

In this MP you will

1. Simulate the motion of 50 random elastic spheres
2. Render the simulation

This MP is core, with no elective components.
It assumes you have already completed the [Terrain MP](terrain.html).

# Overview

You will submit a webpage that has

- One canvas
- A self-running animation with 50 random spheres
- Collision resolution and gravity
- Animation restarts every 15 seconds

Submit an HTML file and any number of js, css, glsl, and json files. No image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

## Sphere dynamics

Spheres should be set to a random position and velocity when the animation starts
and again every 15 seconds thereafter.

Spheres should move every frame, subject to the following forces:

- Momentum
    
    A sphere in motion should remain in motion unless acted upon by an outside force.

- Gravity
    
    Spheres should accelerate downward.

- Collisions with walls, with elasticity 0.9.

    Walls should keep the spheres inside a cube that is fully within view.
    The cube should not be rendered.

- Collisions with other spheres, with elasticity 0.9

You may optionally add drag too, but if you do should make it minor enough that it is not a dominant force in sphere motion.

All spheres should be the same size and same mass.
Sphere diameter should be 0.15× cube width, which means spheres can just barely all lie flat but will usually reset before reaching that state.

We recommend using Euler's method with collision resolution as outlined in [the kinetics page](../text/kinetics.html).

:::aside
Common errors

The following are the most common errors made when implementing sphere collisions:

- Trying to model the walls of the cube as geometry. A simple `sphere.center.x + sphere.radius > maxX`{.js} detects collisions with a right wall at $x=\text{maxX}$ and resolving the collision is as simple as `sphere.velocity.x *= -elasticity`{.js} and `sphere.position.x = maxX - sphere.radius`{.js}.

- Counting collisions twice. If sphere 4 and sphere 18 collide, only resolve that once, not once for pair (4, 18) and then again for pair (18, 4).
    
    The usual symptom of this error is either spheres clinging to one another instead of bouncing off one another or spheres gaining energy with every collision.

- Counting the same collision in multiple frames. Two techniques can resolve this (either or both can be used):
    - Update positions as well as velocity to remove overlap as well as resolve momentum
    - Only resolve collisions if spheres are both overlapping and moving toward one another (or overlapping with a wall and moving towards the wall). The sign of new collision speed $s$ indicates this in [our fomulation](../text/kinetics.html)

    The usual symptom of this error is spheres clinging to one another instead of bouncing off one another

- Using the wrong sign for the velocity change operations.
    There are many places where you might introduce a sign flip (such as the order of subtraction of positions to get $\vec d$, the order of subtraction when finding $s$, and the $\pm$ in the velocity update). Changing any one of these should change the resulting motion.
    
    The usual symptom of this error is very rapid speed increases resulting in frenetic or off-the-screen motion

- Never coming to a rest, instead jiggling on the floor.
    This is caused by the order of operations of gravity vs wall collisions and is not a concern for this assignment.

- Slowly sinking into the floor.
    This is caused by only changing velocity, not position, when resolving floor collisions.

- Huge jumps if you go away from the simulation for a few seconds and then come back.
    This is not a concern for this assignment, but if you want to fix it then cap the $\Delta t$ you use in your Euler step to at most 0.1 seconds.
:::

## Sphere appearance

The spheres should be rendered using a polygonal approximation, such as the one in [sphere.json](files/sphere.json).
You should send this geometry to the GPU (i.e. with `gl.bufferData`) only once and re-use it or every sphere in every frame.

Spheres should be lit, with diffuse and/or specular lighting.
Each sphere should have a different random color.

The recommended draw function looks something like this:

    set view matrix, light position, etc
    gl.clear(...)
    for each sphere {
        create model matrix for this sphere
        send color to GPU
        send model-view matrix to GPU
        gl.drawElements(the sphere geometry)
    }


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show 50 spheres moving within an invisible cube and colliding with one another.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/spheres.webm" type="video/webm"/>
<source src="vid/spheres.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result, with two random resets recorded.
</figcaption>
</figure>
