---
title: Smoothed Particle Hydrodynamics
summary: Simplified to have as little math as I can get it.
...

<details class="tldr"><summary>Overview of this method</summary>

In Smoothed Particle Hydrodynamics, fluids are modeled as collections of particles.

Particles move under their own momentum, creating **advection**.

Three forces are based on neighboring particles: pressure, viscosity, and surface tension.

Neighboring particles are determined via weighting **kernels** which we are free to design to have nice computability properties.
In particular, we want kernels with easily-expressed gradients and Laplacians.

**Density** $\rho$ is the kernel-based average of particle mass.

**Pressure** $p$ is the difference between desired and actual density.

**Pressure force** is the gradient of pressure.

**Viscosity** is the Laplacian of velocity.

**Surface tension** is mimicked using the gradient and Laplacian of a special "color field" to make particles with few neighbors move towards their neighbors.

Most of the above need to be symmetrized to ensure the "equal and opposite reaction" feature of physics that helps conserve momentum and kinetic energy.

Because all components are based on localized computations, the fluid is compressible and shocks propagate at the time sampling rate.

Care is needed to pick a time step that satisfies [CFL conditions](cfl.html).

Grids can accelerate SPH significantly by making kernel computation linear time instead of quadratic.

</details>


# Overview

Smoothed Particle Hydrodynamics (SPH)[^sph] simulated fluids and other mutable material as follows:

- A set of particles move about under their own momentum
- Various emergent properties of the fluid are estimated at each particle using a weighted average of nearby particles
- Forces are added to counter nonphysical results of those averages

[^sph]:
    The core components of SPH was first introduced in
    [L. B. Lucy (1977) "A numerical approach to the testing of the fission hypothesis" *The Astronomical Journal*, 82:1013–1024](https://doi.org/10.1086/112164).
    
    SPH was brought to graphics for non-fluids in
    [M. Desbrun, M-P. Gascuel (1996) "Smoothed particles: a new paradigm for animating highly deformable bodies" *Proceedings of the Eurographics workshop on Computer animation and simulation*, 61–76.](http://www.geometry.caltech.edu/pubs/DC_EW96.pdf)
    
    The first use of SPH for liquid in graphics that I know of is 
    [M. Müller, D. Charypar, M. Gross (2003) "Particle-based fluid simulation for interactive applications" *Proceedings of the 2003 ACM SIGGRAPH/Eurographics symposium on Computer animation*, 154–159.](https://doi.org/10.5555/846276.846298).
    
    The most helpful reference I've found on SPH so far is from [Lucas Schuermann's website](https://lucasschuermann.com/writing/particle-based-fluid-simulation).

## Vector field derivatives

We'll also need a few of derivative-like functions
of spatially-defined functions.

Gradient $\nabla$
:   A vector field pointing towards larger function values.

    If $T$ is the temperature in the room then moving towards $\nabla T$ will help me find the warmest part of the room.
    
    If $H$ is the height of terrain then $\nabla H$ will point uphill.
    
    The gradient can be computed via dimension-wise derivatives:
    $\nabla f(x,y,z) = \left(\dfrac{\partial f}{\partial x}, \dfrac{\partial f}{\partial y}, \dfrac{\partial f}{\partial z}\right)$

Divergence $\nabla \cdot$
:   A scalar field that measures how much a vector field points away from an area.
    
    If $\vec P$ is the motion of individual people then $\nabla \cdot \vec P$ at my house is negative as people are arriving for a party, zero during the party, and positive as people are departing.
    
    If $\vec V$ is the velocity of cars on the road
    then $\nabla \cdot \vec V$ is negative at the slow-down at the beginning of a traffic jam because vehicles are arriving at higher speeds than they're departing
    and positive at the end of the traffic jam because vehicles are departing at higher speeds than they're arriving.

    The divergence can be computed via dimension-wise derivatives:
    $\nabla \cdot \big(f_x(x,y,z), f_y(x,y,z), f_z(x,y,z)\big) = \dfrac{\partial f_x}{\partial x} + \dfrac{\partial f_y}{\partial y} + \dfrac{\partial f_z}{\partial z}$
    
    For SPH, we primarily use the divergence as part of the Laplacian.

Laplacian $\nabla^2$
:   The divergence of the gradient, or $\nabla \cdot \nabla$
    
    The Laplacian is a measure of nonlinearity.
    Regardless of a function's slope,
    its Laplacian is 0 if the function is flat,
    positive if the function is concave,
    and negative if the function is convex.
    
    The Laplacian of a vector field is another vector field pointing away from outliers.
    If $\vec V$ is the velocity of cars on the road
    then $\nabla^2 \vec V$ points forward for the slowest-moving car,
    and backward for the fastest-moving car, and is zero for a car going with the flow.

    The Laplacian can be computed via dimension-wise second derivatives:
    $\nabla^2 f(x,y,z) = \dfrac{\partial^2 f}{\partial x^2} + \dfrac{\partial^2 f}{\partial y^2} + \dfrac{\partial^2 f}{\partial z^2}$

# Kernel Functions

The key to SPH is the kernel function.
The kernel function tells us how to check nearby particles to estimate multi-particle values like density and pressure.
Good kernel functions should 

- Be smooth
- Be radially symmetric: i.e. they depend on distance (often denoted $r = \|\vec r\|$ where $\vec r$ is the offset from the center of the kernel), not angle
- Have finite support: i.e. beyond some distance (often denoted $h$) they should be zero
- Have a well-defined and easily-computable gradient and Laplacian
- Integrate to 1

## Example kernels and their derivatives 

[Müller, Charypar, and Gross](https://doi.org/10.5555/846276.846298) proposed using different kernels for different forces.
These provide a nice balance between computability and accuracy, so I repeat them here.

In the following, $r$ means $\|\vec r\|$, i.e. the magnitude or length of $\vec r$.

1. A bell-shaped kernel for most measures to avoid instability when particles get very close together.
    We'll also need both the gradient and the Laplacian of this kernel:

    $$\begin{align*}
    W_{\text{poly6}}(\vec r, h) &= \frac{315}{64\pi h^9}\begin{cases}
    (h^2-r^2)^3
    & 0 \le r \le h \\
    0 & \text{otherwise}
    \end{cases}
    \\
    \nabla W_{\text{poly6}}(\vec r, h) &= \frac{315}{64\pi h^9}\begin{cases}
    -6 (h^2-r^2)^2\vec r
    & 0 \le r \le h \\
    \vec 0 & \text{otherwise}
    \end{cases}
    \\
    \nabla^2 W_{\text{poly6}}(\vec r, h) &= \frac{315}{64\pi h^9}\begin{cases}
   -6 ( 3 h^4 - 10 h^2 r^2 + 7 r^4 )
    & 0 \le r \le h \\
    0 & \text{otherwise}
    \end{cases}
    \end{align*}$$


2. A kernel with a spike near 0 for pressure to push very close-together particles apart.
    We'll only need the gradient of this kernel:

    $$\begin{align*}
    W_{\text{spiky}}(\vec r, h) &= \frac{15}{\pi h^6}\begin{cases}
    (h-r)^3
    & 0 \le r \le h \\
    0 & \text{otherwise}
    \end{cases}
    \\
    \nabla W_{\text{spiky}}(\vec r, h) &= \frac{-45}{\pi h^6}\begin{cases}
    (h-r)^2\dfrac{\vec r}{r}
    & 0 < r \le h \\
    \vec 0 & \text{otherwise}
    \end{cases}
    \end{align*}$$

3. A kernel with a positive Laplacian for viscosity to ensure viscosity never adds energy.
    We'll only need the Laplacian of this kernel:

    $$\begin{align*}
    W_{\text{visc}}(\vec r, h) &= \frac{15}{2\pi h^3}\begin{cases}
    \dfrac{-r^3}{2h^3} + \dfrac{-r^2}{2h^2} + \dfrac{h}{2r} - 1
    & 0 \le r \le h\\
    0 & \text{otherwise}
    \end{cases}
    \\
    \nabla^2 W_{\text{visc}}(\vec r, h) &= \frac{45}{\pi h^6}\begin{cases}
    h - r
    & 0 \le r \le h\\
    0 & \text{otherwise}
    \end{cases}
    \end{align*}$$

The normalizing coefficients of all three kernels assume particles in 3D.
In 2D
$W_{\text{poly6}}$ and its derivatives use an initial coefficient of $\dfrac{4}{\pi h^8}$;
$\nabla W_{\text{spiky}}$ uses an initial coefficient of $\dfrac{-10}{\pi h^5}$,
and 
$\nabla^2 W_{\text{visc}}$ uses an initial coefficient of $\dfrac{40}{\pi h^5}$.

:::aside
If you don't normalize the kernel functions properly then target density $\rho_0$, viscosity $\mu$, and external forces like gravity all need to be scaled differently.
Pressure and surface tension don't, as they have the normalizing factor cancel out in their computation.
The overall dynamics of SPH should still work even with non-normalized kernels.
:::

## Kernel-defined values

Given a kernel $W$
we can use it to compute the density at particle $i$ as
$$
\rho_i = \sum_{j} m_j W(\mathbf{x}_i-\mathbf{x}_j, h)
$$
where $\mathbf{x}_j$ is the location of particle $j$
and $m_j$ is the mass of particle $j$.

We can also interpolate any other value $A$
at any point $\mathbf{x}$
as long as we can express how particle $i$ contributes to $A$ as $\hat A_i$;
the resulting equations are
$$\begin{align*}
A_i(\mathbf{x}) &= \sum_{j} \frac{\hat A_j}{\rho_j} W(\mathbf{x}-\mathbf{x}_j, h)
\\
\nabla A_i(\mathbf{x}) &= \sum_{j} \frac{\hat A_j}{\rho_j} \nabla W(\mathbf{x}-\mathbf{x}_j, h)
\\
\nabla^2 A_i(\mathbf{x}) &= \sum_{j} \frac{\hat A_j}{\rho_j} \nabla^2 W(\mathbf{x}-\mathbf{x}_j, h)
\end{align*}$$

# Approximating incompressible fluids

Incompressible fluids are governed by a set of equations known as the Navier-Stokes equations,
which are beyond the scope of this page.
Their key property from a visual standpoint
is that

- Fluids self-advect.

    Fluid particles move and carry fluid properties
    like velocity and temperature
    with them.

- Fluids are (nearly) divergence-free.
    
    The divergence of the velocity field of the fluid is zero (except at moving fluid boundaries).
    For any given region of fluid, the fluid that comes in matches the fluid that goes out.

Simulating these properties is enough to create something that resembles fluid flow.
More interesting fluid behaviors require us to also model other properties of fluids (such as vorticity and turbulence) but we'll ignore those for this introduction.

## Self-advection

In SPH, self-advection is easy: we move particles based on their velocity,
typically using [Euler's method](kinetics.html#eulers-method).

As a corollary to this, we want all other aspects of fluid motion
to result in a force at each particle location $\vec F_i$
that we can turn into an acceleration via the the usual $\vec F = m \vec a$ equation as $\vec a_i = \dfrac{\vec F_i}{\rho_i}$.

## Pressure force

Common SPH methods use a quasi-realistic pressure force
modeled after pressures created by ideal gasses
but simplified for ease of computation
and scaled to give visually-useful results with large time steps.
We need two components to get there: a way of computing pressure
and a way of turning pressure into a force.
Because we're only inspired by, not directly modeling, real pressure there are many ways to achieve both.

For pressure, an easy approach is to use how far the fluid is from a target density: $p = k(\rho - \rho_0)$.
Per tradition, pressure is denoted with a lowercase Latin pē "$p$"
and density with a lowercase Greek rho "$\rho$", which can be confusing as the two look quite similar in most typefaces.
Two parameters we pick:
$\rho_0$ is the target density, with larger $\rho_0$ resulting in more particles per unit volume;
and $k$ a scaling parameter, with larger $k$ resulting in less-compressible (but also less-numerically-stable) fluid.

For the force resulting from pressure, we want something based on the gradient of pressure
that is symmetric (to conserve energy and momentum).
Again, there are several approaches to achieving this but a simple one is
$$\vec F_i^{\text{pressure}} = -\sum_j m_i m_j \left(\dfrac{p_i}{\rho_i^2} + \dfrac{p_j}{\rho_j^2}\right) \nabla W_{\text{spiky}}(\mathbf{x}_i - \mathbf{x}_j, h)$$

Traditionally, this force is not shown with a strength parameter
because the pressure strength parameter $k$ serves that purpose instead.

## Viscosity

Each bit of fluid exerts drag on nearby bits of fluid,
smoothing out fluid flow
and causing the fluid to act like a unified substance
instead of a collection of independent particles.
The name for this force is "viscosity".

Viscosity is proportional to the Laplacian of velocity.
If a particle is moving slower than its neighbors than it forms a pit in the velocity field, giving a positive Laplacian which makes it speed up;
conversely if it is faster it has a negative Laplacian and slows down.

As with pressure, there are several ways to make the viscosity force symmetric
but a simple one is 
$$\vec F_i^{\text{viscosity}} = \mu \sum_j m_j \dfrac{\vec v_j - \vec v_i}{\rho_j^2} \nabla^2 W_{\text{visc}}(\mathbf{x}_i - \mathbf{x}_j, h)$$

The $\mu$ is a viscosity strength parameter we pick.


## Surface tension

Surface tension in liquids is caused by liquid molecules being attracted to one another.
Inside the fluid this pulls them every direction and has little impact,
Liquid molecules on the surface of the fluid are pulled deeper into the fluid, resulting in a smoothing effect.
When generalized to large particles instead of tiny molecules, we also want to add a curvature term to represent how peaked areas are pulled in towards the surface more strongly than other areas are.

To achieve this, it is common to define a "color field"
that simply tracks particle locations.
The gradient of the color field then points towards nearby particles
and the Laplacian of the color field tells us how peaked an area is.

$$\begin{align*}
\nabla c_i &= \sum_{j} \frac{m_j}{\rho_j} \nabla W_{\text{poly6}}(\mathbf{x}_i-\mathbf{x}_j, h)
\\
\nabla^2 c_i &= \sum_{j} \frac{m_j}{\rho_j} \nabla^2 W_{\text{poly6}}(\mathbf{x}_i-\mathbf{x}_j, h)
\\
\vec F_i^{\text{surface}} &= -\sigma \nabla^2 c_i \frac{\nabla c_i}{\|\nabla c_i\|}
\end{align*}$$

The $\sigma$ is a surface tension strength parameter we pick.

# Time integration

Given the above equations for determining forces on each particle,
the remaining component of PH simulation is to iterate from one time step to another.
[Euler's method](kinetics.html#eulers-method) or any similar method may be used.

Care must be taken in choosing time steps.
With large time steps
compression in one area will be over-corrected by the pressure force,
resulting in decompression there that will be over-corrected the other way in the next time step,
resulting in rapidly increasing oscillation speeds and then fluid explosion.
You'll need some kind of [CFL condition](cfl.html),
though the viscosity of the simulation should mean velocities of nearby particles are fairly similar so you might be able to get away with a fairly large constant.

Your simulation speed will be dramatically increased if you use an acceleration structure to optimize the various sums above.
Because $W$ has finite support, you only need to sum over particles within $h$ of the current particle.
Partitioning particles into a grid with cells of size $h$
will mean that all such particles will be at most one cell away from the current particle (i.e. check 9 cells in 2D, 27 in 3D).
Grids with cells of size $2h$ reduce the number of cells needed (4 cells in 2D, 8 in 3D) at the cost of more particles per cell and adding a "which side of the cell is it nearest" checks.

Cells also don't need to be fully populated.
A dynamic dictionary with cell-coordinate keys and list-of-particles values can save memory compared to a preallocated 3D array in cases where the fluid ranges over a much larger area than it fills at any one time.

