---
title: "Goop MP"
...

In this MP you will

1. Implement a 2D version of smoothed particle hydrodynamics

This MP is elective, with no core components.
It assumes you have already completed the [Many Spheres MP](many-spheres.html).


:::{style="margin:1em; padding: 1ex; border-radius: 1.414ex; box-shadow:0 0 1ex rgba(0,0,0,0.5); background: rgba(255,255,0,0.25); "}
<strong style="font-size:150%">Warning</strong>

This MP is likely to take more effort and time than its point value suggests.
It is intended to be a jumping-off point for students interested in fluid dynamics,
which is not a topic given much attention in this course.
:::

# Overview

You will submit a webpage that has

- One canvas
- A self-running animation with a user-specified number of fluid particles
- Pressure, viscosity, and gravity

Submit an HTML file and any number of js, css, and glsl files. No json or image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

Smoothed particle hydrodynamics (SPH) is not usually fast enough to run in interactive system.
It also includes many tuning parameters, which are not easy to select for a good look.
This specification walks you through getting one specific SPH simulation running
with the understanding that you use that as a jumping-off point for other simulations.

## Efficient 2D particle display

Render 2D particles as circles using a dynamic attribute buffer of positions and `gl.POINTS`.

:::note
Recommended approach

1. Copy your [Many Spheres MP](many-spheres.html) solution
2. Remove the $z$ coordinate from the spheres and resize them as given in the parameters table below
3. Remove the view matrix and change the projection matrix to just an aspect-ratio scale: either $\begin{bmatrix}\frac{h}{w}&0&0&0\\0&1&0&0\\0&0&1&0\\0&0&0&1\end{bmatrix}$ if the canvas is wider than it is tall or $\begin{bmatrix}1&0&0&0\\0&\frac{w}{h}&0&0\\0&0&1&0\\0&0&0&1\end{bmatrix}$ if it is taller than it is wide
4. Change the fragment shader to not do lighting

You should be able to run the simulation at the end of each step
:::

## SPH without surface tension

Implement [Smoothed Particle Hydrodynamics](../text/sph.html) without surface tension.
This will mean computing three kernels:
$W_\text{poly6}$ for density,
$\nabla W_\text{spikey}$ for pressure, and
$\nabla^2 W_\text{visc}$ for viscosity.
Note the adjusted coefficients for 2D given after the main equations for these functions.

:::note
Self-influencing particles

Density uses $W_\text{poly6}$ which is non-zero when $r=0$; thus every particle adds to its own density. This is important for the correct operation of the SPH method.

Pressure uses $\nabla W_\text{spikey}$ which is zero when $r=0$ so a particle exerts no pressure on itself.

Viscosity uses $\nabla^2 W_\text{visc}$ which is non-zero when $r=0$, but multiplies it by $\vec v_ji - \vec v_i$ which is the zero vector when $i = j$ so a particle exerts no viscosity on itself.
:::


Use the following parameters:

| Symbol | Value | Notes |
|:------:|:-----:|-------|
| $h$ | $\dfrac{3}{2\sqrt{n}}$ | This is the support radius of the kernels, meaning particles outside this radius do not impact a given particle. |
| $\rho_0$ | $\dfrac{1}{3}$ | This is the target density of the fluid in arbitrary units |
| $k$ | $20$ | This is the "stiffness" of the fluid and controls how strongly it resists compression |
| $\mu$ | $10^{-6}$ | This is the viscosity of the fluid and controls how thick and goopy it is |
| radius | $\frac{h}{3}$ | The visual size of each particle |
| $m_i$ | $\dfrac{h^2}{9}$ | The mass of a 2D particle is the square of its radius |
| $g$ | $1$ | The acceleration of gravity; in other words, $v_y -= 1 \Delta t$ each frame |

Set the bounds of the simulation to between $-1$ and $1$ in both $x$ and $y$.

As a crude approximation of the CFL conditions, use $\Delta t = \dfrac{h}{10}$ regardless of how quickly the browser renders frames.
Note that even this may be too high and result in run-away energy gain and particle explosion if

a. you have under 100 particles (viscosity slows particles down only if there are enough of them)
b. you have more than 2000 particles (the imprecision in initial particle density matters more with more particles)
c. $g$ or $k$ are increased (more force per frame results in faster motions)
d. $\mu$ is decreased (viscosity slows things down)
e. the simulation bounds are increased (farther to move means more time to pick up speed)

If your simulation explodes, try reducing $\Delta t$ or adjusting any of the above parameters away from the explosion state. Reducing $k$ can be an especially effective tool for reintroducing stability and the cost of making the fluid compressible and squishy.


:::note
Recommended approach

First, verify you can find the density of particles in the sphere collision code.
Evaluate $\rho$ for each particle and render it as particle color.
It has fairly arbitrary units; I found that using the color $RGB = (\rho, 0.5\rho, 2\rho)$ resulted in dark purple particles that turned white when pressed together, but your scaling might differ.

A recommended code organization is

1. Find all pairs of particles that are within $h$ of one another
2. Initialize for each particle values that will be added to:
    - a density number (initially the self-term in the density equation)
    - a pressure number (initially 0)
    - a force vector (initially gravity and wall response, or zero if you handle those separately)
3. Loop over the pairs to add the pair-terms to the density of each particle
4. Loop over the particles to compute pressure from density
5. Loop over the pairs to add the pair-terms of pressure force
6. Loop over the pairs to add the pair-terms of viscosity force
7. Loop over the particles to apply the force to velocity: $\vec v_i := \vec v_i + \dfrac{\vec F}{m} \Delta t$
:::


## Near-resting-energy initialization

The initial separation of particles matters hugely in the resulting simulation because SPH is trying to simulation nearly-incompressible fluids; put them too close together and they'll explode.
Additionally, if they are too perfectly aligned they have difficulty entering a stable fluid arrangement.

Use the following method to arrange particles in a well-spaced near-grid on the left side of the screen:

```js
let pos = [radius-1, radius-1]
const gap = radius*2
for(let s of spheres) {
    s.position = [pos[0]+Math.random()*gap/10, pos[1]+Math.random()*gap/10]
    pos[1] += gap
    if (pos[1] > 1-radius) {
        pos[1] = radius-1
        pos[0] += gap
    }
}
```

## Walls, grid, and input

Use an elasticity of 1 for the walls: fluid does not lose energy when colliding with an rigid obstacle.

Use the same kind of grid-based optimization in picking which particles interact as you did in the Many Spheres MP.
Use $2h$ as the grid cell size.

Keep the particle count input from the Many Spheres MP.
Set the default particle count to be at least 200.

Only reset the simulation when the button is pressed, not automatically at any particular interval.

Do not handle sphere-sphere collisions.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show a goopy fluid splashing about in a box.
The motion should be largely similar every time it is run,
though it will vary somewhat because of the small randomization in the initial conditions.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/goop.webm" type="video/webm"/>
<source src="vid/goop.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>

# Going beyond: 3D {-}

For the most part, your code should just work if you change to 3D particles.
You'll need 3D positions and velocities,
a 3D acceleration grid,
and need to change the scalars in the kernels to their 3D forms
but other than that it should work.

We didn't do that because you'll need *many* more particles;
the quiality of the fluid behavior is proportional to the depth of particles;
thus the visual quality we get with $n$ particles in 2D takes $n^{3/2}$ in 3D:
8000 instead of 400 for a basic splash,
30,000 instead of 1000 for elementary waves, and so on.
Simulations that measure particles in the millions are common for 3D movies.



