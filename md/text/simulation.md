---
title: Visual Simulation
summary: An overview good-enough simulation techniques, including Eulerian and Lagrangian methods.
...

Many fields are interested in simulating how some system behaves,
generally with the goal of predicting behavior without the expense of testing a real system.
Computer graphics is also interested in simulating the systems studied by many fields,
but with a different goal: looking believable.
That often means taking methods from other fields
and simplifying them in ways those fields would find objectionable.

# Locality

A major challenge in almost all simulations is locality.
For visualization we generally like large systems:
big crowds, large bodies of water, high-res swirling smoke, and so on.
But most interesting physical systems have non-local behavior:
pressing on water in one place causes water everywhere else to move too.
Those non-local effects generally cause simulations to run with non-linear runtime relative to simulation size and resolution,
which in turn makes visualization slow.

Sometimes we find a purely-local algorithm that is good enough.
The [Boids](https://dl.acm.org/doi/10.1145/37402.37406) algorithm for simulating flocks and herds
and the [Synthetic Topiary](https://dl.acm.org/doi/abs/10.1145/192161.192254) algorithm for simulating growing and pruned plants
are two of the few localized visual simulations.

Usually we have non-local behavior
that we can express through a set of local constraints.
For example, we can express how a stack of blocks behaves
by noting that each block refuses to overlap with its immediate neighbors;
expressed that way each block has just a few local constraints,
but the global solution of those constraints means that lifting any block in the stack still lifts the top block.

# Iterative solvers

Given a set of localized constraints, most graphics simulations solve them iteratively.
There are two common families of solutions for systems of localized constraints.

## Conjugate gradient

Many graphics problems include differential equations.
They have the general form "the rate of change of $x$ is some function of $x$".
For most graphics simulations, the differential equation has no closed-form solution:
the solution families you learn about in differential equations class don't work.
Instead, we solve them by

1. Making a linear approximation of the equations at the current time.

    Because of Newton's Third Law (i.e. "every action has an equal and opposite reaction"), the resulting matrix is usually symmetric.
    
    Because motion is smooth and the linearization of smooth systems is convex, the resulting matrix is positive-definite; that is, all its eigenvalues are positive.
    
    Because the equations were local, the resulting matrix is sparse;
    that is, most of its entries (including most entries on each row) are zero.
    
2. Solve the linear system.

    The [Conjugate Gradient method](conjugate-gradient.html) is particularly good at solving sparse symmetric positive-definite problems.

3. Use the solution to bump up to a slightly greater time

There are two approximations being used here:
first, we treat complicated math as if it were linear,
and, second, we use a bunch of small steps in time instead of a continuous model of time.
These two are related:
as each time step length approaches zero, the linear solution approaches the correct solution.

This approach is particularly suited to cases where we can represent all of the motion we wish to simulate using a single set of constraints.
In those cases, it can be both highly efficient
and if given more spatial and temporal resolution will more closely match physical reality.[^closeness]

[^closeness]:
    More closely ≠ arbitrarily closely.
    Every few years a paper is published fitting the following template:
    
    1. Phenomenon *X* has been simulated in such-and-such ways.
    2. But even with very high res, those ways don't conserve *Y* even though in the real world *Y* is conserved.
    3. Here's a different set of constraints and/or linearization approach that simulates *X* and does conserve *Y*.


## Interleaved solution

Many graphics problems can be approximated using position-based dynamics.
Broadly, this works as follows:

1. Use the difference in state between the last two frames to estimate velocity, and use velocity to create an initial state of this frame based on momentum.

2. For each constraint, make the smallest change to the state that will result in the constraint being satisfied while still conserving momentum and energy.

3. Because the constraints are handled independently, it is likely that solving constraint 2 introduced a violation of constraint 1, so repeat step 2 until the amount of violation is sufficiently small to look OK.

We are again using a time-step approximation,
and additionally approximating the interaction between different constraints
mostly by blind faith that repeated individual application will eventually converge.
Jos Stam published [a paper on Nucleus](https://www.josstam.com/publications#comp-jpohiiw79), a system that uses this approach,
in which he observes that it does converge, but the state it converges to depends on the order in which the constraints are applied.

This approach is particularly suited to cases where several constraints are relevant but are not directly related to one another.
With more iterations it converges on something stable that meets the constraints;
depending on the specific constraints that solution might or might not be physically plausible.


# Directability

Computer simulation can create plausible visual phenomena more cheaply that reality can.
But it can also bend the laws of its simulation to create specific results.

If you want a school of fish that spell out a word,
an eroded terrain that just happens to contain a trademark,
a mushroom cloud that looks like a clown,
or a crashing wave with the shape of a horse in it
then what you want is a directable simulation.

There are many approaches to directable simulations.
A few I've seen in the graphics literature include

- Providing keyframes and then searching for tweens connecting them that minimize how much physics they violate.
- Providing shaping forces so that inside the region of interest gravity pulls a different direction, one that helps create the desired shape.
- Running the simulation without direction, then adjusting the color of the final bits and running them back through time so it looks like they started that way.
    (e.g. [the opening scene from this SIGGRAPH 2017 paper's video](https://youtu.be/eGtB0VXJsuI))


# Euler or Lagrange?

Leonhard Euler and Joseph-Louis Lagrange were both prolific 18^th^-century mathematicians and each have multiple things named after them, including [the Euler Method](https://en.wikipedia.org/wiki/Euler_method) and [Lagrangians](https://en.wikipedia.org/wiki/Lagrange_multiplier), both of which are used in many computer graphics simulations.
However, in computer graphics simulations their names are most often used to distinguish between two disparate approaches to simulating matter.^[Opinions vary as to the appropriateness of these eponyms. Some argue that Euler did discuss a flux-through-a-cell model of liquids and Lagrange did discuss a moving-particle model of liquids, so it is appropriate to keep using their names. Others argue that neither mathematician even approached the things we need to consider in real simulations and that this simple breakdown overlooks importance differences e.g. between Finite Element, Finite Volume, and Finite Difference methods. Regardless of your opinion here, it remains true that computer graphics papers use the adjectives "Eulerian" and "Lagrangian" freely and that your use of the two terms is sometimes used as a [shibboleth](https://en.wikipedia.org/wiki/Shibboleth).]

Eulerian simulations use a grid 
and Lagrangian simulations use moving particles.
I find it helpful to use a memory aid for this based on the shapes of the leading letters:
"E" looks like part of a grid and "L" could be the path of a particle bouncing off of something.

Eulerian simulations break space into many individual fixed cells:
grids of squares or cubes are easiest to program
but simplical complexes (i.e. breaking a plane into triangles or a volume into tetrahedra) have superior numerical properties.
The physics of the material is expressed in terms of the motion of material through the grid:
incompressibility says that any material entering a cell must be matched by a like amount leaving the cell,
momentum says that the velocity of the material in the cell moves with it to other cells over time,
and so on.

Lagrangian simulations break the material into many individual moving chunks or particles.
The physics of the material is expressed in terms of forces on individual particles (such as momentum and gravity)
and constraints on a particle and its current "neighbors" (such as incompressibility and viscosity friction).

Eulerian methods are good at solving non-local constraints (typically via [conjugate gradient] methods).
Lagrangian methods are good at keeping track of mass, shape, and boundaries.

There are also hybrid approaches, notably the Particle In Cell (PIC) method and its descendants.
These methods have both Lagrangian particles and an Eulerian grid in the simulation.
Each frame they

1. Apply particle-like physics (momentum, gravity) to the particles
2. Transfer particle properties (density, momentum) to the grid
3. Resolve non-local physics (incompressibility, viscosity, plasticity) on the grid
4. Transfer changes from the grid back to the particles

Such hybrid methods show great promise and have been the source of many advances in simulations since around 2015,
sometimes by expressing the physics of new material types
and sometimes by designing more expressive ways of transferring information between particles and grids.

