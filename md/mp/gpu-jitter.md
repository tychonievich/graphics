---
title: "GPU Jitter MP"
...

In this MP you will write a simple vertex shader that moves each vertex of a logo independantly.

This MP is elective, with no code components.
It assumes you have already completed the [Logo MP](logo.html).

# Overview

You will submit a webpage that has

- One canvas
- A 2D animation of the majestic and inspiring University of Illinois logo, jittering about

Submit an HTML file and any number of js, css, glsl, and json files. No image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

Your program should be generally the same as your Logo MP submission,
except that the vertex shader should move each vertex independently, keeping it roughly near its original position.
We recommend removing the matrix-based movement you used in the Logo MP to make the jittering more visible.
That will probably require both (a) sending some time-varying uniform to the vertex shader
and (b) also using the `gl_VertexID` to parameterize movement.

The end result should ensure that lines that were parallel in the static logo
are not parallel in most frames of the jittering logo.

You'll need to follow the usual CS 418 dialect of WebGL
as checked by [wrapWebGL2.js](../code/wrapWebGL2.js);
notably, this means you can't use `gl_VertexID` in an `if`, `for`, or `while`.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show an I logo with jittering vertices.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/gpu-jitter.webm" type="video/webm"/>
<source src="vid/gpu-jitter.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>
