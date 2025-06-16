---
title: "Height map MP"
...

In this MP you will make a copy of your [Terrain MP](terrain.html) that applies a rainbow of colors based on terrain altitude.

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

## Rainbow height map

The color of each pixel should be based on the altitude of the terrain beneath it, plus lighting.
The color should move smoothly through several different colors so as to make a rainbow effect.

The colors should change smoothly through multiple colors even if there is only one fracture.
A good way to make the changes smooth is with a [lerp](../text/lerp.html),
$(1-t)x + (t)y$
such as we also used in [the Bézier notes](../text/bezier.html)
and for linearly interpolated textures.

## No input-varying branches

As always, [our WebGL2 dialect](../text/dialect.html) applies.
You'll probably find the [warp parallelism](../text/dialect.html#warp-parallelism) part of the dialect a little frustrating
as it means that your fragment shader cannot include an `if` with the height as part of the condition.
You'll need to use expression-based conditions instead.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should initially be blank.
Once the button is pressed a terrain should appear with a rotating camera with colors varying by height.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/height-map.webm" type="video/webm"/>
<source src="vid/height-map.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result showing three different generated terrains.
</figcaption>
</figure>

