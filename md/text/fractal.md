---
title: Fractals
summary: A class of mathematically-defined geometries that look more "natural" than most others.
...

# Fractional Dimension

We often speak of "two dimensional" or 2D and "three-dimensional" or 3D. There are several equivalent ways of defining these ideas; let's consider a specific one: cube counting.

Consider a chunk of some shape that passes though a cube.
Subdivide that cube evenly into $n$ divisions along each axis to make a grid of $n^3$ smaller cubes.
How many of those smaller cubes does the shape pass through?

The exact answer to this question is overly dependent on the specifics of the case^[Some definitions of fractal dimension use spheres instead of cubes, which removes some of these challenges but adds others because [sphere packing](https://en.wikipedia.org/wiki/Sphere_packing) is a nontrivial topic in its own right.]. For example, an axis-aligned straight line passes through $n$ cubes while a straight line between opposite cube corners may passe through as many as $3n$.
In computing we know how to handle such constants: big-O.
Any straight line passes through $\Theta(n^1)$ cubes.
Any flat plane passes through $\Theta(n^2)$ cubes.
Any solid passes through $\Theta(n^3)$ cubes.
We call the exponent in these expressions the dimensionality of the shape.

This formulation suggests we could have a fractional dimension like $1.2$: we just have to find some shape that passes through $\Theta(n^{1.2})$ of the cubes.
One way to construct such a shape is to find a shape that exhibits that ratio at one scale and recursively apply it to itself so that it exhibits that same ratio for every $n$.

:::example
The Koch curve starts with the following shape

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 120 36.641" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M 0,0 40,0 60,34.64101615137754 80,0 120,0 "/>
</svg>
<figcaption>The starting point of the Koch curve, which you could make by moving forward, turning to the right 60°, moving forward, turning to the left 120°, moving forward, turning to the right 60°, and moving forward again, drawing a line n the ground as you go. The ending point is the same you'd get by moving forward 3 times without turning.</figcaption>
</figure>

This shape is chosen to make the number of cubes not scale linearly;
in particular, shrinking the cubes by a factor of 3 requires 4 times as many to cover it.
That's easier to see at this low resolution if we use circles instead of squares:

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -61 252 122" style="max-width:65em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M 0,0 40,0 60,34.64101615137754 80,0 120,0 "/>
<circle cx="60" cy="0" r="60"/>
<g transform="translate(130,0)">
<path d="M 0,0 40,0 60,34.64101615137754 80,0 120,0 "/>
<circle cx="20" cy="0" r="20"/>
<circle cx="50" cy="17.3205" radius="20"/>
<circle cx="70" cy="17.3205" rr20"/>
<circle cx="100" cy="0" r="20"/>
</g>
</svg>
<figcaption>The same path as the previous image, twice. On the left, a single circle of radius 1.5 covers the entire path. On the right, four circles of radius 0.5 jointly cover the path, one covering each straight path segment.</figcaption>
</figure>


With $n=1$ this fits in one cube, but with $n=3$ it needs four cubes, not three, suggesting maybe more than $n^1$. But if we zoom in more we find just lines. Let's fix that by replacing each segment with another copy of the same shape

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 120 37.641" style="max-width:30em">
<path fill="none" stroke="black" d="M 0,35.641 40.0,35.641 60.0,1.0 80.0,35.641 120,35.641"/>
</svg>

Now the pattern holds up to $n=9$; continuing *ad infinitum* we get

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 36.641" style="max-width:30em">
<path fill="none" stroke="black" d="M 0,35.641 1.4815,35.641 2.2222,34.358 2.963,35.641 4.4444,35.641 5.1852,34.358 4.4444,33.075 5.9259,33.075 6.6667,31.792 7.4074,33.075 8.8889,33.075 8.1481,34.358 8.8889,35.641 10.3704,35.641 11.1111,34.358 11.8519,35.641 13.3333,35.641 14.0741,34.358 13.3333,33.075 14.8148,33.075 15.5556,31.792 14.8148,30.509 13.3333,30.509 14.0741,29.226 13.3333,27.943 14.8148,27.943 15.5556,26.66 16.2963,27.943 17.7778,27.943 18.5185,26.66 17.7778,25.377 19.2593,25.377 20.0,24.094 20.7407,25.377 22.2222,25.377 21.4815,26.66 22.2222,27.943 23.7037,27.943 24.4444,26.66 25.1852,27.943 26.6667,27.943 25.9259,29.226 26.6667,30.509 25.1852,30.509 24.4444,31.792 25.1852,33.075 26.6667,33.075 25.9259,34.358 26.6667,35.641 28.1481,35.641 28.8889,34.358 29.6296,35.641 31.1111,35.641 31.8519,34.358 31.1111,33.075 32.5926,33.075 33.3333,31.792 34.0741,33.075 35.5556,33.075 34.8148,34.358 35.5556,35.641 37.037,35.641 37.7778,34.358 38.5185,35.641 40.0,35.641 40.7407,34.358 40.0,33.075 41.4815,33.075 42.2222,31.792 41.4815,30.509 40.0,30.509 40.7407,29.226 40.0,27.943 41.4815,27.943 42.2222,26.66 42.963,27.943 44.4444,27.943 45.1852,26.66 44.4444,25.377 45.9259,25.377 46.6667,24.094 45.9259,22.811 44.4444,22.811 45.1852,21.528 44.4444,20.245 42.963,20.245 42.2222,21.528 41.4815,20.245 40.0,20.245 40.7407,18.962 40.0,17.679 41.4815,17.679 42.2222,16.396 41.4815,15.113 40.0,15.113 40.7407,13.83 40.0,12.547 41.4815,12.547 42.2222,11.264 42.963,12.547 44.4444,12.547 45.1852,11.264 44.4444,9.981 45.9259,9.981 46.6667,8.698 47.4074,9.981 48.8889,9.981 48.1481,11.264 48.8889,12.547 50.3704,12.547 51.1111,11.264 51.8519,12.547 53.3333,12.547 54.0741,11.264 53.3333,9.981 54.8148,9.981 55.5556,8.698 54.8148,7.415 53.3333,7.415 54.0741,6.132 53.3333,4.849 54.8148,4.849 55.5556,3.566 56.2963,4.849 57.7778,4.849 58.5185,3.566 57.7778,2.283 59.2593,2.283 60.0,1.0 60.7407,2.283 62.2222,2.283 61.4815,3.566 62.2222,4.849 63.7037,4.849 64.4444,3.566 65.1852,4.849 66.6667,4.849 65.9259,6.132 66.6667,7.415 65.1852,7.415 64.4444,8.698 65.1852,9.981 66.6667,9.981 65.9259,11.264 66.6667,12.547 68.1481,12.547 68.8889,11.264 69.6296,12.547 71.1111,12.547 71.8519,11.264 71.1111,9.981 72.5926,9.981 73.3333,8.698 74.0741,9.981 75.5556,9.981 74.8148,11.264 75.5556,12.547 77.037,12.547 77.7778,11.264 78.5185,12.547 80.0,12.547 79.2593,13.83 80.0,15.113 78.5185,15.113 77.7778,16.396 78.5185,17.679 80.0,17.679 79.2593,18.962 80.0,20.245 78.5185,20.245 77.7778,21.528 77.037,20.245 75.5556,20.245 74.8148,21.528 75.5556,22.811 74.0741,22.811 73.3333,24.094 74.0741,25.377 75.5556,25.377 74.8148,26.66 75.5556,27.943 77.037,27.943 77.7778,26.66 78.5185,27.943 80.0,27.943 79.2593,29.226 80.0,30.509 78.5185,30.509 77.7778,31.792 78.5185,33.075 80.0,33.075 79.2593,34.358 80.0,35.641 81.4815,35.641 82.2222,34.358 82.963,35.641 84.4444,35.641 85.1852,34.358 84.4444,33.075 85.9259,33.075 86.6667,31.792 87.4074,33.075 88.8889,33.075 88.1481,34.358 88.8889,35.641 90.3704,35.641 91.1111,34.358 91.8519,35.641 93.3333,35.641 94.0741,34.358 93.3333,33.075 94.8148,33.075 95.5556,31.792 94.8148,30.509 93.3333,30.509 94.0741,29.226 93.3333,27.943 94.8148,27.943 95.5556,26.66 96.2963,27.943 97.7778,27.943 98.5185,26.66 97.7778,25.377 99.2593,25.377 100.0,24.094 100.7407,25.377 102.2222,25.377 101.4815,26.66 102.2222,27.943 103.7037,27.943 104.4444,26.66 105.1852,27.943 106.6667,27.943 105.9259,29.226 106.6667,30.509 105.1852,30.509 104.4444,31.792 105.1852,33.075 106.6667,33.075 105.9259,34.358 106.6667,35.641 108.1481,35.641 108.8889,34.358 109.6296,35.641 111.1111,35.641 111.8519,34.358 111.1111,33.075 112.5926,33.075 113.3333,31.792 114.0741,33.075 115.5556,33.075 114.8148,34.358 115.5556,35.641 117.037,35.641 117.7778,34.358 118.5185,35.641 120,35.641"/>
</svg>

By construction, tripling $(3n)^d = 4n^d$ meaning $d = \frac{\log 4}{\log 3} \approx 1.26185\dots$
:::

# Fractals in Graphics

Nothing in nature exhibits a true mathematical fractal: zoom in enough and you find  3D cells or 1D elementary particles.
But many things in nature are visually more fractal than they are Platonic.
Many mountains look more like fractals than they look like spheres,
many trees look more like fractals than they look like cylinders,
dirt accumulates in patterns that look more like fractals than they do gradients,
and so on.
Fractals make a useful starting point for making a stylized model of nature.

Fractals are also useful in that they break up our ability to notice patterns.
The eye is much less likely to notice a low-fidelity image if the image is made up fractals than if it is made up of simple shapes.
Fractals are a useful tool for making a simple model look more detailed than it is.

# Common fractal generation approaches

There are *many* fractals used in graphics, but four are common enough to be worth discussing in more detail.

All of these are forms of fractal noise:
that is, they use pseudorandom parameters to create a fractal that looks random instead of looking mechanical or mathematical.

## fBm Noise

Brownian motion refers to the trajectory followed by a particle that randomly changes direction.
The most common formulation of Fractal Brownian motion (abbreviated fBm) is a 1.x-dimensional fractal created by the position of a 1D Brownian motion on one axis and time on the other.
Many other fBm formulations also exist.

In graphics, "fBm noise" is used to describe any purely stochastic fractal, even if there is no way to characterize it as the motion of a particle.

## Subdivision methods

Subdivision methods provide a computationally simple way of generating a fractal.
Given a low-resolution mesh, replace each primitive with several smaller primitives and then randomly offset the vertices.
Provided the expected magnitude of the random offsets is proportional to the size of the primitive, the result will be fractal.

Naïve fractal subdivision often exhibits visible patterns where the seams between the low-res primitives remain visible in the resulting fractal.
To avoid this the subdivision itself should result in a smooth surface with no visible seams even if there are no random offsets.

## Faulting methods

Faulting methods are not particularly common in graphics,
but they are easy to implement and thus are part of your programming assignments.
As such, we have a [separate page about them](faulting.html).

## Perlin Noise

Ken Perlin made a two-part innovation in the efficient creation of fractals that has become a mainstay of computer graphics.

First, Perlin came up with a readily-computed representation of random smooth bumps.
Pick points on a fixed uniform grid and at each pick a random surface normal,
then fit a surface to those normals.
Conceptually such a surface can be found by making one hill-and-pit pair and placing a rotated copy of it at each point.
Practically it can be found using polynomially-interpolated dot products.

The original Perlin noise used a square grid to create the bumps. The turns out to result in visible axis-aligned patterns, so various alternatives such as simplex noise and opensimplex noise use different grid patterns instead.

Second, Perlin recognized that a fractal can be created from almost any bumpy surface, including his, by adding scaled-down copies of the surface to itself.
This approach, called "octaves", is based on the observation that if $f(x)$ is a bumpy function then $\sum_{n=0}^{\infty} f(2^n x) 2^{-n}$ is a fractal,
and that we can stop the sum early once the $2^{-n}$ term is making the subsequent iterations have no visible impact.

Because of the significance of octave-created fractals, octave fractals that are not based on Perlin's random-gradient bumps are sometimes informally called "Perlin".
