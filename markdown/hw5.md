---
title: 'HW5: Simulation'
notes:
    - bones
        - track to
            - principle axis via cross product
        - track point to
            - (track pt) (track goal) (track pt)^-1
        - track and scale to
        - track and stretch to
        - FABRIK
        - FABRIK with starter pose
    - fireworks
        - bounce walls
        - reburst
        - time-lapse dynamics
        - keyframe
    - boids
    - landscape
        - square-square
        - diamond-square
        - erosion
        - keyframe
    - tree
        - L-system
        - stochastic
        - pruned
        - light and gravity
    - rope
        - mass-spring
        - tri-diagonal
    - fluid
        - shallow water
        - stam
...

<!--
<blockquote style="background-color:#fbb; font-size:150%">This page is a work-in-progress and may change at any time without notice.</blockquote>
-->


# Overview

This assignment may result in several different programs.
Instead of `make run` we will use several different make targets, one for each broad simulation type.

The required part of this assignment is "earn 50 points on this assignment".
The optional part is any points in excess of 50 that you earn.

## `make bones` *filename* (15–100 points)

This is an extension of HW4: everything that was required in HW4 is required in this program too.

You may find our [bones writeup](bones.html) to be helpful.

bone $d$
:   This may appear at most once in any `object`.
    If present, it means that this object is considered to be a bone,
    with object-space origin $(0,0,0)$ and object-space tip $(0,0,d)$.
    
    A bone may have geometry, but doesn't need to.
    A bone may have the `world`, another bone, or a non-bone as its parent.
    
    The remaining keywords in this section apply only to bones and will follow the `bone` command in the input.

track *object* (requires `bone`; 15–30 points)
:   After applying other transformations (including positioning and rotation),
    rotate the object to the bone's tip points toward the named *object*.
    This should be a minimal rotation to achieve that goal, staying as close to the previous orientation as possible.

    Basic (15 points)
    :   <a href="files/hw5bones-track1.txt"><img class="demo zoom" src="files/hw5track1.png"/></a>

    Rotation and negative length (5 points)
    :   <a href="files/hw5bones-track2.txt"><img class="demo zoom" src="files/hw5track2.png"/></a>

    Tracking parent and target (10 points)
    :   <a href="files/hw5bones-track3.txt"><img class="demo zoom" src="files/hw5track3.png"/></a>

trackroll *primary* *axis* *secondary* (requires `track`; 10–20 points)
:   After applying other transformations (including positioning and rotation),
    rotate the object to the bone's tip points toward the named *primary* object.
    There are many such rotations; pick the one that points the bone's *axis* points toward the named *secondary* object as much as possible.
    *Axis* will always be one of `+x`, `-x`, `+y`, or `-y`.
    
    Basic (10 points)
    :   <a href="files/hw5bones-trackroll.txt"><img class="demo zoom" src="files/hw5trackroll.png"/></a>
    
    Tracking parent and target (10 points)
    :   <a href="files/hw5bones-trackroll2.txt"><img class="demo zoom" src="files/hw5trackroll2.png"/></a>

trackscale *object* (requires `track`; 10 points)
:   <a href="files/hw5bones-trackscale.txt"><img class="demo zoom" src="files/hw5trackscale.png"/></a>
    Like `track`, but also scale along the object's $z$ axis to that the tip of the bone exactly reaches the given object. Do not scale along the object's other two axes.

trackstretch $x$ $y$ $z$  (requires `trackscale`; 5 points)
:   <a href="files/hw5bones-trackstretch.txt"><img class="demo zoom" src="files/hw5trackstretch.png"/></a>
    Like `trackscale`, but also scale uniformly along the object's $x$ and $y$ axes such that the volume of the bone is conserved.

fabrik *object* *iterations* (20–35 points)
:   Use FABRIK to perform inverse kinematics,
    where the IK chain consists of this bone and all its bone parents.

    Recall that one iteration of FABRIK moves the bone tip to *object*,
    then moves the chain root back to its starting location.
    Compute *iterations* iterations in total.
    
    Each frame should begin the iteration from the positions provided by any `position` and `quaternion` commands.
    None of the bones in an IK chain will have a track or related command.
        
    FABRIK produces the origins and tips of a chain of bones.
    Use the same math as `position` and `track` to align the bones with these points.

    Basic (20 points)
    :   <a href="files/hw5bones-fabrik.txt"><img class="demo zoom" src="files/hw5fabrik.png"/></a>
        
    With moving root (15 points)
    :   <a href="files/hw5bones-fabrik2.txt"><img class="demo zoom" src="files/hw5fabrik2.png"/></a>

## `simulation fluid` (70–120 points)

This is not an extension of any other assignment.
You'll output 2D fluids directly to the pixels of an image file (I guess we could say it's an extension of HW0?).

Use back-advection to provide unconditionally stable simulations.
When back-advecting off the grid, assume velocity is 0 and temperature is equal to the nearest on-grid temperature.

:::aside
Fluid simulations tend to be somewhat all-or-nothing: either you have fluid, or you don't.
Thus, you should plan to test each components prior to integrating them.
In particular, you'll need

- A sparse (3–5 nonzero entries per row) positive definite [matrix solver](math1.html#implementing-a-sparse-matrix-solver).
- Linear-weighted sampling of a grid at non-integer indices
- Sampling a grid with two out-of-bounds rules: either always 0 or nearest in-bounds value
- Back advection of both cell contents and velocity
    (which means you'll need two copies of each grid)
- A means of turning a grid of divergences into a single long vector

We recommend using a staggered grid, with velocities on cell boundaries and temperature in cell centers, as this simplifies divergence computation and boundary conditions and makes for nicer results at no additional computational cost.
:::

pngs *width* *height* *filename* *frames*
:   same syntax and semantics as HW0.
    
    Each pixel in the image will represent a cell in a Eulerian fluid grid.
    Bigger images = higher-resolution fluids.
    Every cell will be full of fluid.

heat *h* *bouyancy* *mag* (70 points)
:   <a href="files/hw5fluid-basic.txt"><img class="demo zoom" src="files/hw5fluidbasic.png"/></a>
    <a href="files/hw5fluid-basic2.txt"><img class="demo zoom" src="files/hw5fluidbasic2.png"/></a>
    To create motion in the fluid, track something we'll call the "temperature" of each pixel.
    We won't simulate temperature-based expansion, but will approximate temperature-based buoyancy.
    
    We'll let temperature range from $-1$ to $1$.
    Each pixel experiences an upward force with strength *temperature* × *bouyancy* pixels / *frame*<sup>2</sup>.
    
    The input *h* represents a rate of heat transfer into the fluid.
    The bottom row of pixels is heated, so $t' = h + (1-h)t$ each frame;
    the top row is cooled, so $t' = -h + (1-h)t$ each frame.
        
    Use heat as the color of each pixel.
    Linearly interpolate between the following colors:
    
    | Temperature |  Color  |
    |:-----------:|:-------:|
    | $1$         |`#ff0000`|
    | $0$         |`#000000`|
    | $-1$        |`#00B2FF`|
    
    If temperatures are outside this range, you may color them in an implementation-defined manner.
    
    For the first frame, set each cell to have a random temperature between −*mag* and +*mag*. This randomization breaks symmetry and gets the simulation started.
    Because of randomization, each run of a given file will produce a different result (but with the same overall dynamics).

diffuse *rate* (10 points)
:   <a href="files/hw5fluid-diffuse.txt"><img class="demo zoom" src="files/hw5fluiddiffuse.png"/></a>
    Diffuse heat at the given *rate* each frame using a [discrete Gaussian filter](diffusion.html) with *rate* as $t$.

viscosity *rate* (10 points)
:   <a href="files/hw5fluid-viscosity.txt"><img class="demo zoom" src="files/hw5fluidviscosity.png"/></a>
    Diffuse velocity at the given *rate* each frame using a [discrete Gaussian filter](diffusion.html) with *rate* as $t$.

subsample *n* (10 points)
:   <a href="files/hw5fluid-subsample.txt"><img class="demo zoom" src="files/hw5fluidsubsample.png"/></a>
    Render one image every *n* frames, where *n* is a positive integer.

    for example, if the *frames* in the `pngs` is 100 and the *n* in `subsample` is 4
    then you'll simulate 400 frames but render only 100 images.

confine (requires viscosity; 10 points)
:   <a href="files/hw5fluid-confine.txt"><img class="demo zoom" src="files/hw5fluidconfine.png"/></a>
    <a href="files/hw5fluid-confine2.txt"><img class="demo zoom" src="files/hw5fluidconfine2.png"/></a>
    The linear weights involved in advection
    and the linear approximation of incomprehensibility created by using a matrix
    both tend to add unwanted "numerical viscosity".
    
    As a work-around, if the word `confine` appears in the input file
    then measure the kinetic energy of the fluid before each of these steps
    and artificially scale all velocities afterward to restore the previously-measured kinetic energy.

tconfine (requires diffuse; 10 points)
:   <a href="files/hw5fluid-tconfine.txt"><img class="demo zoom" src="files/hw5fluidtconfine.png"/></a>
    <a href="files/hw5fluid-tconfine2.txt"><img class="demo zoom" src="files/hw5fluidtconfine2.png"/></a>
    The linear weights involved in advection
    tends to add unwanted "numerical diffusion".
    
    As a work-around, if the word `tconfine` appears in the input file
    then measure mean and variance of the temperatures fluid before each advection step
    and artificially shift and scale all temperatures afterward to restore the previously-measured mean and variance.

Other examples
:   Combined viscosity and diffusion:
    <a href="files/hw5fluid-diffvisc.txt"><img class="demo zoom" src="files/hw5fluiddiffvisc.png"/></a>
    
    <div style="clear:both"></div>

    Intense starting temperatures with no heating:
    <a href="files/hw5fluid-slosh.txt"><img class="demo zoom" src="files/hw5fluidslosh.png"/></a>
    
    <div style="clear:both"></div>
    
    Combined confinement:
    <a href="files/hw5fluid-confineboth.txt"><img class="demo zoom" src="files/hw5fluidconfineboth.png"/></a>
    
    <div style="clear:both"></div>
    
    A 40s 720p simulation [input file](files/hw5fluid-720p.txt)
    and [result (in video player)](player.html#hw5fluid720p.webm)


## `simulation springs` (50–120 points)

This is not an extension of any other assignment.
Rather, it outputs input files for HW3.

This is a mass-spring simulation with moving spheres, fixed planes, and springs.
We discussed several approaches to this in class.
To replicate my results, each iteration 

1. update ball positions and velocities based on momentum and gravity
2. update ball positions and velocities based on springs
3. move balls to not overlap each other and update velocities if the bounce off of each other
4. move balls to not overlap with anchors (non-dynamic balls) and update velocities if the bounce off of them
5. move balls to not overlap with walls and update velocities if the bounce off the wall

I did this in a single pass per frame, acting on the balls in the order I created them.
Ball-ball collisions are resolved in order of the first ball in the pair,
so the collision of the first and last ball is resolved before the collision of the second and third ball.

This order does mean that a later action cases an earlier fix to be partially undone,
but I wanted something easy to describe to increase the chances everyone's code would make the same animation.


txts *w* *h* *base* *frames*
:   Create *frames* different input files for HW3.
    Each should begin with `png` *w* *h* *base*`-`*frame*`.png`
    where *frame* is a 3-digit zero-padded number between 0 and *frames* − 1.
    Each should be named *base*`-`*frame*`.txt`.
    
    <div class="example">
    If the input file opens with
    
        txts 30 40 example- 12
    
    when it should make 12 new text files, named `example-000.txt` through `example-011.txt`.
    The last of these would start with the line
    
        png 30 40 example-011.png

    </div>

pass through
:   Any line that is not a command you've implemented for this assignment should be passed through as-is in every generated file.
    
    <div class="example">
    If the input file contains
    
        txts 30 40 example- 1

        sphere 1 -0.8 -1 0.5
        sphere 0 0 -1 0.3

        sun 1 1 1
    
    then, because the only line that starts with a HW5 keyword is `txts`, the output file will be
    
        png 30 40 example-000.png

        sphere 1 -0.8 -1 0.5
        sphere 0 0 -1 0.3

        sun 1 1 1

    </div>

wall *A* *B* *C* *D*
:   Create a barrier ensuring that all balls will remain entirely in the region of space where $Ax+By+Cz+D \ge 0$.
    
    This line is used only internally and does not appear in any form in the resulting output files.
    
    This barrier is invisible. HW3's visible variant was `plane` *A* *B* *C* *D*, but visible planes and interacting walls should be handled separately.

ball $p_x$ $p_y$ $p_z$   $v_x$ $v_y$ $v_z$
:   <a href="files/hw5spring-ball.txt"><img class="demo zoom" src="files/hw5springball.png"/></a>
    Create an animated ball at location $(p_x, p_y, p_z)$
    with velocity $(v_x, v_y, v_z)$.
    Use the currently active `radius` and `mass` for the ball.
    
    Each `ball` line in the input file becomes a `sphere` line in the output file;
    in particular, `sphere` $c_x$, $c_y$, $c_z$, $r$
    where $(c_x,c_y,c_z)$ is the sphere's center location on that frame
    and $r$ is the spheres radius.

ball property specification (extra 5 if do both mass and elasticity)
:   <a href="files/hw5spring-elasticmass.txt"><img class="demo zoom" src="files/hw5springelasticmass.png"/></a>
    Each of the following sets a value that will be applied to balls created after it.
    Each may be overridden by appearing multiple times in the input.
    Each is used only internally and does not appear in any form in the resulting output files.
    
    radius *r*
    :   <a href="files/hw5spring-radius.txt"><img class="demo zoom" src="files/hw5springradius.png"/></a>
        The radius of subsequent `ball`s.
        At least one `radius` command will always precede the first `ball` command.

    mass *m* (5 points)
    :   <a href="files/hw5spring-mass.txt"><img class="demo zoom" src="files/hw5springmass.png"/></a>
        The mass of subsequent `ball`s.
        If no `mass` has been encountered, use `mass 1`.

    elasticity *k* (10 points)
    :   <a href="files/hw5spring-elasticity.txt"><img class="demo zoom" src="files/hw5springelasticity.png"/></a>
        <a href="files/hw5spring-elastic.txt"><img class="demo zoom" src="files/hw5springelastic.png"/></a>
        The elasticity of subsequent `ball`s.
        If no `elasticity` has been encountered, use `elasticity 1`.
        
        In a ball-wall or ball-anchor collision, the coefficient of restitution used should be the ball's elasticity.
        In a ball-ball collision, use the mean of the two elasticities.

gravity *x* *y* *z* (requires `ball`, `radius`, `wall`, and `txt`; 30 pts)
:   Accelerate all balls by $\vec g = (x,y,z)$ / frame<sup>2</sup>.
    
    Recall that motion under acceleration works as follows:
    
    - new $\vec v$ = old $\vec v + \Delta t \vec g$
    - new $\vec p$ = old $\vec p + \Delta t$ old $\vec v + \frac{1}{2}\Delta t^2 \vec g$

anchor $p_x$ $p_y$ $p_z$   $v_x$ $v_y$ $v_z$ (15 pts)
:	<a href="files/hw5spring-anchor.txt"><img class="demo zoom" src="files/hw5springanchor.png"/></a>
    Like `ball`, except an anchor ignores physics; instead it moves at a constant velocity, passing through walls and other anchors.
	Balls hitting anchors should act like they hit a wall (i.e., use only their own elasticity, not that of the anchor)
	but should correctly handle velocity added by hitting a moving anchor.

subsample *n* (10 pts)
:   <a href="files/hw5spring-subsample.txt"><img class="demo zoom" src="files/hw5springsubsample.png"/></a>
    <a href="files/hw5spring-ball.txt"><img class="demo zoom" src="files/hw5springball.png"/></a>
    For each frame, perform *n* distinct updates.
    For example, if $n=10$ then instead of one update of 1 time unit per frame
    you'd do 10 updates of 0.1 time unit each per frame.
    
    The math should be such that this makes spring and collision computations more precise
    but does not change the result of freely-moving balls at all.

springconst $k$ (requires `subsample`, `mass`, and `elasticity`)
:   The spring constant of subsequent springs.
    If no `springconst` has been encountered, use `springconst 0` -- i.e., ignore the springs.

	For stability of simulation, it is recommended that input files keep $\dfrac{\text{springconst}}{\text{subsample}} < 1$.

tri $n$   $a_x$ $a_y$ $a_z$   $b_x$ $b_y$ $b_z$   $c_x$ $c_y$ $c_z$ (requires `springconst` and `anchor`; 35 pts)
:   <a href="files/hw5spring-tri.txt"><img class="demo zoom" src="files/hw5springtri.png"/></a>
    <a href="files/hw5spring-tri2.txt"><img class="demo zoom" src="files/hw5springtri2.png"/></a>
    Create a triangle of balls by interpolating between the three given corner ball positions
    with $n+1$ balls per side of the triangle.
    Attach springs in a triangular grid.
    
    Set all balls to initial velocity 0
    and all springs to rest length = their initial length.
    
    :::example
    `tri 3` ... would produce 10 balls 18 springs arranged as illustrated in the following ASCII art:
    
              c
             / \
            * - * 
           / \ / \
          * - * - * 
         / \ / \ / \
        a - * - * - b
    :::

tet $n$   $a_x$ $a_y$ $a_z$   $b_x$ $b_y$ $b_z$   $c_x$ $c_y$ $c_z$   $d_x$ $d_y$ $d_z$ (requires `tri`; 10 pts)
:   Create a tetrahedreon of balls by interpolating between the four given corner ball positions
    with $n+1$ balls per edge of the tetrahedron.
    Attach springs in a tetrahedral grid.
    
    Set all balls to initial velocity 0
    and all springs to rest length = their initial length.
    


<!--
## `simulation landscape`


## `simulation boids`

Implement [Craig Reynold's Boids algorithm](https://www.red3d.com/cwr/boids/)

distance $d$
:   The sensing distance, as defined in the Boids algorithm page linked above.

angle *degrees*
:   The sensing angle, as defined in the Boids algorithm page linked above.

maxturn *degrees*
:   Limit each boid to turning at most the given number of degrees each frame

speed *min* *max*
:   Keep each boid moving between these two units-per-frame speed bounds

steering $s$ $a$ $c$
:   Defines the balance between the three steering behaviors.

    Separation $s$ turns away from neighbors, with weight proportional to inverse squared distance.
    
    Alignment $a$ turns the boid to face in the average direction of all other boids at speed ½(*min* + *max*)
    
    Cohesion $c$ turns toward the mean position of neighbors.
    
    Compute the desired turn and speed for each of these three forces independently,
    then average them using the weights given.
    We will only provide $s+a+c = 1$.
    
    
## `simulation trees`


## `simulation fireworks`

burst *type* $n$ $x$ $y$ $z$ $t$ $v$
:   At frame $t$, create a burst of $n$ moving particles of the given *type* centered at $(x,y,z)$ with burst velocity $v$.
    The types are:
    
    `normal`
    :   Select velocities from a 3D normal distribution with standard deviation $v$
    
    `sphere`
    :   Select velocities uniformly from a radius-$v$ sphere

    `shell`
    :   Select velocities uniformly from the surface of a radius-$v$ sphere

    Every `burst` command will be followed by a shape command
    
billboard $w$
:   A shape command: draw each particle from the preceding `burst` as a $w$-by-$w$ square
    that is aligned to point to the camera.
    And orientation other than that (side up, point up, etc) is up to you.

dart $w$
:   A shape command: draw each particle from the preceding `burst` as an equilateral triangle with edge length $w$
    aligned with a face toward the camera
    and a point in the direction of its motion.

box $w$
:   A shape command: draw each particle from the preceding `burst` as a global axis-aligned cube with $w$-length edges.

gravity $x$ $y$ $z$
:   Accelerate moving particles by $x$ units-per-frame in the x axis, $y$ units-per-frame in the y axis, and $z$ units-per-frame in the $z$ axis

drag $d$
:   Decelerate moving particles by $dv$ where $v$ is the participles current units-per-frame velocity.
    You may assume $0 \le d \le 1$;
    if $d = 1$ then particles will instantly stop; if $d = 0$ then there is no drag.

wall *bounciness* $A$ $B$ $C$ $D$
:   An infinite plane that particles cannot penetrate;
    enforce that $Ax + By + Cz + D \ge 0$ for all particles.
    If *bounciness* is 0, remove all velocity into the plane.
    If *bounciness* is 1, reverse any velocity into the plane.
    For intermediate *bounciness*, reverse velocity into the plane and reduce its magnitude.

reburst *type* *chance* $n$ $t$ $v$
:   $t$ frames after the start of the preceding `burst`,
    each particle created by that `burst` is destroyed.
    For each such particle, there is a *chance* percent chance that it becomes the center of a new `burst` of the given *type*, $n$, and $v$
    and a (100 − *chance*) percent chance that it instead simply vanishes.

selfcollide *elasticity* $r$
:   Treat each particle as a sphere with radius $r$
    and resolve particle-particle collisions so that no to particles ever overlap.
    When a collision occurs, use the given *elasticity* to resolve it:
    *elasticity* 0 causes the two to stick together, *elasticity* 1 causes them to bounce off with full energy.
    
    Assume all particles have the same mass. All particle-particle collisions should preserve momentum.
    
-->
