---
title: Fluids on a Grid
summary: The core ideas behind Eulerian fluid simulation.
...

This document provides one way of thinking about divergence-free Eulerian fluids.
It describes a different but similar technique
to [the 1999 stable fluids method](https://www.josstam.com/publications#comp-jpohiiwa14)
and its [more-tutorial presentation in 2003](https://www.josstam.com/publications#comp-jpohiiw834).

# Staggered grid

Assume we discretize 2D space using a square grid.
We'll store different properties of the fluid on different parts of the grid:

- Fluid contents (temperature, color) inside grid cells
- Velocity (or more accurately flux) on boundaries between cells:
    - $x$ velocity on the vertical edge between two horizontally-adjacent cells
    - $y$ velocity on the horizontal edge between two vertically-adjacent cells
- Vorticity would lie on the intersection of four cells,
    but we won't use vorticity in this simulation.

The resulting grid has three separate grids in the computer, of different sizes:
an $w×h$ grid of cell contents,
an $(w-1)×h$ grid of $x$ fluxes,
and an $w×(h-1)$ grid of $y$ fluxes.
We'll usually store these grids as flattened arrays to facilitate rapid access and linear algebra.

:::example
A 3×2 grid we'll use in several examples:

<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 320 220" text-anchor="middle" style="max-width:30em" alt="Cells on the top row are labeled c1, c2, c3 and the bottom row are labeled c4, c5, and c6; x1 is the flow from c1 to c2, x2 from c2 to c3, x3 from c4 to c5, x4 from c5 to c6; y1 is the flow from c1 to c4, y1 from c2 to c5, y1 from c3 to c6.">
<path fill="none" stroke="gray" d="M 0,0 v 200 M 100,0 v 200 M 200,0 v 200 M 300,0 v 200 M 0,0 h 300 M 0,100 h 300 M 0,200 h 300"/>
<text x="50" y="50">c₁</text>
<text x="150" y="50">c₂</text>
<text x="250" y="50">c₃</text>
<text x="50" y="150">c₄</text>
<text x="150" y="150">c₅</text>
<text x="250" y="150">c₆</text>
<path fill="white" stroke="black" d="m 86,60 20,0 0,5 15,-15 -15,-15 0,5 -20,0 "/>
<text x="100" y="55">x₁</text>
<path fill="white" stroke="black" d="m 186,60 20,0 0,5 15,-15 -15,-15 0,5 -20,0 "/>
<text x="200" y="55">x₂</text>
<path fill="white" stroke="black" d="m 86,160 20,0 0,5 15,-15 -15,-15 0,5 -20,0 "/>
<text x="100" y="155">x₃</text>
<path fill="white" stroke="black" d="m 186,160 20,0 0,5 15,-15 -15,-15 0,5 -20,0 "/>
<text x="200" y="155">x₄</text>
<path fill="white" stroke="black" d="m 35,90 0,15 -5,0 20,15 20,-15 -5,0 0,-15 "/>
<text x="50" y="105">y₁</text>
<path fill="white" stroke="black" d="m 135,90 0,15 -5,0 20,15 20,-15 -5,0 0,-15 "/>
<text x="150" y="105">y₂</text>
<path fill="white" stroke="black" d="m 235,90 0,15 -5,0 20,15 20,-15 -5,0 0,-15 "/>
<text x="250" y="105">y₃</text>
</svg>

:::

This setup is called a "staggered grid"
or sometimes a "MAC grid"
after the "marker in cell" method that first popularized it in 1965.

## Divergence-free

Divergence is a property measured in cells
and is positive if more fluid is flowing out of the cell than into it,
negative if more fluid is flowing in than out.

Incompressible fluids have divergence-free velocity fields:
that is, all divergences are 0.
Simple fluid simulation works in two steps:
move the fluid ignoring the divergence-free constraint
and then project the resulting velocities onto the nearest divergence-free flow.

:::example
The divergence of a 3×2 grid:

<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 320 220" text-anchor="middle" font-size="12" style="max-width:40em" alt="c1's divergence is x1+y1; c2's is −x1+x2+y2; c3's is −x2+y3; c4's is x3−y1; c5's is −x3+x4−y2; c6's is −x4−y3.">
<path fill="none" stroke="gray" d="M 0,0 v 200 M 100,0 v 200 M 200,0 v 200 M 300,0 v 200 M 0,0 h 300 M 0,100 h 300 M 0,200 h 300"/>
<text x="50" y="50">x₁ + y₁</text>
<text x="150" y="50">−x₁ + x₂ + y₂</text>
<text x="250" y="50">−x₂ + y₃</text>
<text x="50" y="150">x₃ − y₁</text>
<text x="150" y="150">−x₃ + x₄ − y₂</text>
<text x="250" y="150">−x₄ − y₃</text>
</svg>
:::

## Pressure

To remove divergence, we use the gradient of a pseudo-pressure field.

Real pressure has the property that the force it applies is the gradient of a scalar field
and, like all gradients, is a purely divergent field.
If we can subtract a purely-divergent flow from an existing flow we can make it divergence-free without changing any of the circulation that we want to keep.

True pressure involves terms like the speed of sound and is more complicated than we want to handle.
Instead, we'll make a pressure-like force that just removes divergence.

Given a pressure field

<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 320 220" text-anchor="middle" style="max-width:30em" alt="A pressure field that matches the grid, with p1 where c1 is and so on through p6 where c6 is.">
<path fill="none" stroke="gray" d="M 0,0 v 200 M 100,0 v 200 M 200,0 v 200 M 300,0 v 200 M 0,0 h 300 M 0,100 h 300 M 0,200 h 300"/>
<text x="50" y="50">p₁</text>
<text x="150" y="50">p₂</text>
<text x="250" y="50">p₃</text>
<text x="50" y="150">p₄</text>
<text x="150" y="150">p₅</text>
<text x="250" y="150">p₆</text>
</svg>

its gradient is a flux field created by subtracting adjacent cells of pressure

<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 320 220" text-anchor="middle" font-size="12" style="max-width:40em" alt="A flux field that matches the flow in the grid, with p1−p2 where x1 is, p2−p3 where x3 is, p4−p5 where x3 is, p6−p5 where x4 is, p1−p4 where y1 is, p2−p5 where y2 is, and p3−p6 where y3 is.">
<path fill="none" stroke="gray" d="M 0,0 v 200 M 100,0 v 200 M 200,0 v 200 M 300,0 v 200 M 0,0 h 300 M 0,100 h 300 M 0,200 h 300"/>
<path fill="white" stroke="black" d="m 81,60 30,0 0,5 15,-15 -15,-15 0,5 -30,0 "/>
<text x="100" y="55">p₁−p₂</text>
<path fill="white" stroke="black" d="m 181,60 30,0 0,5 15,-15 -15,-15 0,5 -30,0 "/>
<text x="200" y="55">p₂−p₃</text>
<path fill="white" stroke="black" d="m 81,160 30,0 0,5 15,-15 -15,-15 0,5 -30,0 "/>
<text x="100" y="155">p₄−p₅</text>
<path fill="white" stroke="black" d="m 181,160 30,0 0,5 15,-15 -15,-15 0,5 -30,0 "/>
<text x="200" y="155">p₅−p₆</text>
<path fill="white" stroke="black" d="m 25,90 0,15 -5,0 30,15 30,-15 -5,0 0,-15 "/>
<text x="50" y="105">p₁−p₄</text>
<path fill="white" stroke="black" d="m 125,90 0,15 -5,0 30,15 30,-15 -5,0 0,-15 "/>
<text x="150" y="105">p₂−p₅</text>
<path fill="white" stroke="black" d="m 225,90 0,15 -5,0 30,15 30,-15 -5,0 0,-15 "/>
<text x="250" y="105">p₃−p₆</text>
</svg>

and the divergence of the pressure-induced flow is a sum of fluxes

<svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 -10 320 220" text-anchor="middle" font-size="12" style="max-width:40em" alt="a grid with an equation in each cell, where the equation is the sum of the outgoing flux arrows minux the sum of the incoming flux arrows; the resulting equations are given below the image equated to −d_i for each cell c_i.">
<path fill="none" stroke="gray" d="M 0,0 v 200 M 100,0 v 200 M 200,0 v 200 M 300,0 v 200 M 0,0 h 300 M 0,100 h 300 M 0,200 h 300"/>
<text x="50" y="50">2p₁−p₂−p₄</text>
<text x="150" y="50">3p₂−p₁−p₃−p₅</text>
<text x="250" y="50">2p₃−p₂−p₆</text>
<text x="50" y="150">2p₄−p₁−p₅</text>
<text x="150" y="150">3p₅−p₂−p₄−p₆</text>
<text x="250" y="150">2p₆−p₃−p₅</text>
</svg>

which always equals $n P_i - \sum_j P_j$ where $j$ ranges over cell $i$'s 2--4 neighbors and $n$ is the number of neighbors.
We want to find the pressures that make that divergence equal to the negation of the divergences of the flow we are trying to make divergence-free
$$\begin{align*}
2p_1-p_2-p_4 &= -d_1\\
3p_2-p_1-p_3-p_5 &= -d_2\\
2p_3-p_3-p_6 &= -d_3\\
2p_4-p_1-p_5 &= -d_4\\
3p_5-p_2-p_4-p_6 &= -d_5\\
2p_6-p_3-p_5 &= -d_6\\
\end{align*}$$
which we can pose as a linear system of equations
$$
\begin{bmatrix}
2&-1&   &   -1&&\\
-1&3&-1 &   &-1&\\
&-1&2   &   &&-1\\
-1&&    &   2&-1&\\
&-1&    &   -1&3&-1\\
&&-1    &   &-1&2\\
\end{bmatrix}
\begin{bmatrix}p_1\\p_3\\p_3\\p_4\\p_5\\p_6\end{bmatrix}
=
\begin{bmatrix}d_1\\d_3\\d_3\\d_4\\d_5\\d_6\end{bmatrix}
$$

The resulting system is known as [the discrete Poisson equation](https://en.wikipedia.org/wiki/Discrete_Poisson_equation) and is particularly attractive because it is sparse (no row has more than 5 non-zero entries), symmetric (cell $a_{ij}$ is the same as cell $a_{ji}$), weakly diagonally dominant ($|a_{ii}| = \sum_{j≠i} |a_{ij}|$), and positive definite (all eigenvalues are positive).
While exact solutions can be computed in linear time,
good-enough approximate solutions can be computed much more quickly with a few iterations of the [conjugate gradient method](conjugate-gradient.html)

## A note about circulation

Real fluids preserve local kinetic energy, and hence vorticity or circulation, except as diffused by viscosity.
The Poisson-equation-based removal of divergence does not do this:
it makes velocities smaller to remove diffusion,
removing energy along the way.
When energy is removed because of how we discretize and solve a system, that energy loss is called "numerical damping."

Many approaches have been proposed for removing numerical damping,
generally either by taking some kind of measure of energy or vorticity prior to performing advection and divergence removal and then re-inserting a similar level afterward
or by adding in some kind of particle-based vorticity tracker.
There are also techniques that re-pose the entire fluid problem,
for example in terms of [circulation](http://geometry.caltech.edu/pubs/ETKSD07.pdf) or [turbulence](http://geometry.caltech.edu/pubs/LCDZL20.pdf).

# Advection

All fluid properties (velocity, temperature, color, etc.) move with the fluid.
This is called "advection";
the movement of momentum along the velocity field is called "self-advection".

All forms of advection need two concepts:

Double-buffering
:   Advection assigns a new value based on the velocity and an old value.
    To avoid cascading changes and resolution order-dependence,
    we do this with two copies of every grid:
    the old one we display and read from (sometimes called the "front buffer") and the new one we write to (sometimes called the "back buffer").
    Between time steps we swap the two.

Interpolation
:   We interpolate between grid locations and arbitrary points.
    Linear interpolation is generally used.
    Because we have a staggered grid, we need to interpolate on the correct one.
    
    :::example
    In a 2D grid, interpolating the velocity at point $(2.3, 6.8)$
    needs to consider both the $x$-velocity grid and the $y$-velocity grid.
    
    In the $x$-velocity grid the surrounding four grid cells are
    $(1.5,6)$, $(2.5,6)$, $(1.5,7)$, and $(2.5,7)$
    with weights $0.04$, $0.16$, $0.16$, and $0.64$ respectively.
    
    In the $y$-velocity grid the surrounding four grid cells are
    $(2,6.5)$, $(2,7.5)$, $(3,6.5)$, and $(3,7.5)$
    with weights $0.49$, $0.21$, $0.21$, and $0.09$ respectively.
    :::
    
    Interpolation can be used to read a value at an arbitrary point,
    using the weights to average the values at several grid cells.
    It can also be used to add values at an arbitrary point,
    distributing weighted portions of the value to several grid cells.

Two forms of advection are common

Forward advection
:   Forward advection works as follows:

    1. Zero out the back buffer
    2. For each cell in the front buffer,
        a. Find the (front) velocity $\vec v$ at the cell center $\vec c$ (via interpolation).
            Note this is the cell center for this grid, and is different for cell contents vs each axis of flux.
        b. Find the point $\vec p = \vec c + \vec v \Delta t$ (assuming [Euler's method](kinetics.html#eulers-method); [Runge-Kutta](kinetics.html#runge-kutta) can also work)
        c. Add the (front) value from the cell to the (back) interpolated cells around $\vec p$
    
    Forward advection conserves a value:
    the sum of the value across the grid is the same every time step.
    However, it can violate entropy by concentrating the value in a few cells,
    potentially causing instability if applied to velocity's self-advection.

Backward advection
:   Backward advection works as follows:

    1. For each cell in the back buffer,
        a. Find the (front) velocity $\vec v$ at the cell center $\vec c$ (via interpolation)
            Note this is the cell center for this grid, and is different for cell contents vs each axis of flux.
        b. Find the point $\vec p = \vec c - \vec v \Delta t$ (assuming [Euler's method](kinetics.html#eulers-method); [Runge-Kutta](kinetics.html#runge-kutta) can also work)
        c. Set the (back) value in the cell to be the (front) value at $\vec p$ (via interpolation)
    
    Backward advection is unconditionally stable:
    the maximum magnitude of the value across the grid never increases as result of advection.
    However, it can violate the conservation of mass/momentum,
    potentially causing matter loss and numerical damping.

Since it was introduced [in 1999](https://www.josstam.com/publications#comp-jpohiiwa14),
backward advection has been more popular than forward advection in computer graphics: we generally prefer stability over accuracy.
However, both are used.

