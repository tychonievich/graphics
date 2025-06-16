---
title: "Fog MP"
...

In this MP you will

1. Auto-generate a terrain (with no user input)
2. Respond to keys to move and rotate the camera
3. Add user-controllable fog

This MP is elective, with no core components.
It assumes you have already completed the [Flight MP](flight.html).

# Overview

You will submit a webpage that has

- One canvas
- A 3D view of dynamically-generated fractal terrain
- Responds smoothly and continuously to keys motion keys
- Responds instantaneously and discontinuously to fog control keys

Submit an HTML file and any number of js, glsl, json, css, and image files.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

## Everything the [Flight MP](flight.hml) does

This MP is an extension of the Flight MP; it should have all the inputs, algorithms, and operations of that MP.

## Fog

Have the background be white or a pale off-white color. Use that same color for the fog.

Have fog that falls off with an exponential fall-off: $v = e^{-fd}$ where $v$ is how visible objects are, $f$ is a fogginess parameter and $d$ is distance between camera and fragment.
For the common projection matrix, $d$ can be approximated as `1 / gl_FragCoord.w`{.glsl}.
Initially the fog density parameter should be chosen such that some terrain is visible but the presence of fog is obvious.


Fog should be applied after lighting.
Compute the full lit color
and mix that with the fog color
based on the computed visibility parameter.

## On-press keys

In your `keydown` listener add handling a few keys:

- `g` should decrease fog density by a factor of ×0.8 each time it is pressed
- `h` should increase fog density by a factor of ×1.25 each time it is pressed
- `f` should toggle fog on and off without forgetting the previous fog density when it is toggled off (that fog level will be used again when the fg is toggled back on)

Keep all of the previous key responses from Flight too.

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should show a random terrain with visible fog.
Holding down the WASD and arrow keys should fly around the terrain, with perceived fogginess decreasing as terrain is approached.
Typing the FGH keys should change fog presence and density.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/fog.webm" type="video/webm"/>
<source src="vid/fog.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result, with keys being pressed displayed in the video.
Note the flight happens as keys are held
while the fog changes happen as they are typed.
Note also that the terrain vanishes from view with sufficient distance or fog density.
</figcaption>
</figure>


