---
title: "Cliffs MP"
...

In this MP you will make a copy of your [Terrain MP](terrain.html) that uses two different materials, picking between them by slope.

This MP is elective, with no core components.
It assumes you have already completed the [Terrain MP](terrain.html).

# Overview

You will submit a webpage that has

- Two number entry fields
- One button
- One canvas
- A 3D view of dynamically-generated fractal terrain

Submit an HTML file and any number of js and glsl files. No image files, JSON files, or CSS files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

All specs from the [Terrain MP](terrain.html) apply to this MP too except as noted below.

## Two materials

Inside your fragment shader, use two different materials,
one for shallow slopes and one for steep slopes.
The boundary between these should be crisp, not gradual or fuzzy.

:::note
The steepness of the slope is proportional to the upward coordinate of the normalized surface normal.
That will be 1 on flat areas, 0 on infinitely steep cliffs.
:::

The shallow slope material should be

- Green -- RGB = (0.2, 0.6, 0.1)
- With small bright shine spots

The steep slope material should be

- Red -- RGB = (0.6, 0.3, 0.3)
- With larger dimmer shine spots

## No input-varying branches

As always, [our WebGL2 dialect](../text/dialect.html) applies.
You'll probably find the [warp parallelism](../text/dialect.html#warp-parallelism) part of the dialect a little frustrating
as it means that your fragment shader cannot include an `if` with the slope as part of the condition.
You'll need to use expression-based conditions instead.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should initially be blank.
Once the button is pressed a terrain should appear with a rotating camera, shiny green where flat and duller red where steep.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/cliffs.webm" type="video/webm"/>
<source src="vid/cliffs.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>
