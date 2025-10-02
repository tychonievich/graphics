---
title: "Orbits MP"
...

In this MP you will

1. Assemble a scene with several copies of the same geometry
2. Make a simple scene graph using matrices

This MP is core, with no elective components.
It assumes you have already completed the [Logo MP](logo.html).

# Overview

You will submit a webpage that has

- One canvas
- A 3D animation of a stylized solar system made of orbiting cubes and tetrahedra

Submit an HTML file and any number of js, css, glsl, and json files. No image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

## HTML and coding style

As with the [Logo MP](logo.html), there should be one HTML file with one canvas element, scripts only in the head, `requestAnimation` animation, [wrapWebGL2.js](../code/wrapWebGL2.js) not producing any warnings, motion via matrices, etc.

Make the canvas resize to fill the screen, and correct the aspect ratio of the projection matrix to maintain an undistorted view.
See [the 3D example code](../code/3d-webgl/) for examples of how to do this (notably in the `fillScreen` function).

## Graphics

- 3D with depth and perspective
  
    Enable depth tests.
    Render the scene such that the models are in view and seen from perspective.

- Use exactly two models:
    
    A multicolored tetrahedron
    :   positions
        : `[[1,1,1], [-1,-1,1], [-1,1,-1], [1,-1,-1]]`{.js}
        
        colors
        : `[[1,1,1], [0,0,1], [0,1,0], [1,0,0]]`{.js}
        
        triangle indices
        : `[[0,1,2], [0,2,3], [0,3,1], [1,2,3]]`{.js}
    
    A multicolored octahedron
    :   positions
        : `[[1,0,0],[0,1,0],[0,0,1],[0,-1,0],[0,0,-1],[-1,0,0]]`{.js}
        
        colors
        : `[[1,0.5,0.5],[0.5,1,0.5],[0.5,0.5,1],[0.5,0,0.5],[0.5,0.5,0],[0,0.5,0.5]]`{.js}
        
        triangle indices
        : `[[0,1,2], [0,2,3], [0,3,4], [0,4,1], [5,1,4], [5,4,3], [5,3,2], [5,2,1]]`{.js}
    
    Send each of these models to the GPU **only once**,
    drawing the same GPU copy multiple times per frame.

- Orbiting and spinning bodies
    
    Create a scene with the following:
    
    - A large octahedron ("the Sun")
        - fixed at the origin
        - spinning a full rotation once every two seconds
    
    - A smaller octahedron ("the Earth") 
        - orbiting the Sun once every few seconds
        - spinning like a top several times a second
    
    - An octahedron ("Mars") a little smaller than the Earth
        - 1.6 times as far from the Sun as the Earth
        - orbiting the Sun 1.9 times slower than the Earth
        - spinning like a top 2.2 times slower than the Earth
    
    - A tetrahedron ("the Moon") smaller than the Earth
        - smaller than the Earth
        - orbiting the Earth faster than the Earth orbits the Sun but slower than the Earth spins
        - always presenting the same side of itself to the Earth
    
    - A tetrahedron ("Phobos") smaller than Mars
        - orbiting Mars several times faster than Mars spins
        - always presenting the same side of itself to Mars
    
    - A tetrahedron ("Deimos") half the size of Phobos
        - twice as far from Mars as Phobos
        - orbiting Mars only a little faster than Mars spins
        - always presenting the same side of itself to Mars
    
    Handle the motion described above
    by computing a model matrix for each body each frame in JavaScript
    and sending that single model matrix (possibly combined with a view and/or projection marix) to the GPU as a uniform.
    
    <details class="note"><summary>Assembling Matrices</summary>
    When multiplying matrices, put the most local motion on the right
    and the most global on the left.
    For example, for the moon I might use a matrix
    $R_{eo} T_{e} R_{mo} T_{m} S_{m}$
    where
    
    - $S_{m}$ scales the Moon to size around its own origin
    - $T_{m}$ translates the Moon to the right distance from the Earth
    - $R_{mo}$ rotates the Moon around the Earth to create orbiting motion
    - $T_{e}$ translates the center of the Moon's orbit (i.e. the earth) to the right distance from the Sun
    - $R_{eo}$ rotates the center of the Moon's orbit (i.e. the earth) around the Sun to create orbiting motion
    
    As an exercise: if the Moon spun relative to the earth (it doesn't, but Earth does spin relative to the Sun), where would you add that matrix?
    </details>
    
    Do not attempt to match true astronomical scale and speeds; doing so will make the animation almost impossible to see.
    You may add axial tilt if you wish, but doing so is not required.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show orbiting bodies.
One example motion (this one with the optional axial tilt added) might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/orbits.webm" type="video/webm"/>
<source src="vid/orbits.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result, with axial tilt included.
</figcaption>
</figure>
