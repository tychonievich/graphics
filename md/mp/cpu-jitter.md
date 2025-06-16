---
title: "CPU Jitter MP"
...

In this MP you will supply new vertex positions for the same geometry every frame,
causing the geometry to jitter and decay.

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
except that the vertex data in the attributes changes every frame.
This change should be something that would be very difficult to do as a [GPU jitter](gpu-jitter.html);
for example, adding a small cumulative `Math.random()`{.js} to each vertex location each frame.
Your vertex shader may not do anything fancier than a simple matrix multiply.

The end result should ensure that lines that were parallel in the static logo
are not parallel in most frames of the jittering logo.

Dynamic attributes can be created by four changes to the usual rendering process:

1. When you `gl.createBuffer()`{.js} the buffer that will have changing data, store the result in a global variable or another place you can get at it again.

2. For that buffer, call `gl.bufferData(..., gl.DYNAMIC_DRAW)`{.js} instead of the usual `gl.STATIC_DRAW`{.js}

3. Every frame, change the contents of the `Float32Array`{.js}

4. Every frame after `gl.bindVertexArray`{.js} and before `gl.drawElements`{.js} repeat the `gl.bindBuffer`{.js} and `gl.bufferData`{.js} calls with the updated `Float32Array`{.js}

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show an I logo with jittering vertices.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/cpu-jitter.webm" type="video/webm"/>
<source src="vid/cpu-jitter.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of the first few seconds of an example result.
</figcaption>
</figure>
