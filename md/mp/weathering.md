---
title: "Weathering MP"
...

In this MP you will make a copy of your [Terrain MP](terrain.html) that has a third control option, one for the amount of weathering to apply. It will roughly simulate spheroidal weathering.

This MP is elective, with no core components.
It assumes you have already completed the [Terrain MP](terrain.html).

# Overview

You will submit a webpage that has

- Three number entry fields
- One button
- One canvas
- A 3D view of dynamically-generated fractal terrain

Submit an HTML file and any number of js and glsl files. No image files, JSON files, or CSS files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

All specs from the [Terrain MP](terrain.html) apply to this MP too except as noted below.

## Third input

Add a third numeric input, labeled "Weathering"

## Simulate spheroidal weathering

Spheroidal weathering refers to the phenomenon whereby wind, temperature changes, and other non-liquid erosive forces tend to erode sharp edges more quickly than flat surfaces. In other words, it smooths things out.

Smoothing can be done in many ways, but a common and effective one is to replace each vertex's position with the average of its current position and its neighbors positions,
repeated some number of times to provide more smoothing.

:::aside
Why include old position in the average?

We recommend smoothing by replacing $p$ with $\frac{p + m}{2}$, where $m$ is the mean position of $p$'s neighbors.
Usually smoothing will work much more quickly if you just replace $p$ with $m$,
so why include $p$ in the numerator?

Giving $p$ at least 50% weight is necessary to ensure that high-frequency bumps are smoothed away.
Consider a saw-tooth pattern, where every vertex is either high or low
and every high vertex's neighbors are all low:
if we just use $m$ then each step of "smoothing" will simply swap which vertices are high and which are low.
The $\frac{p + m}{2}$ method ensures we don't get that kind of oscillation.
:::

For this assignment, do this only in the height direction: do not move vertices horizontally.

When smoothing, it is important to work in two passes:
first figure out where things should go based on their current positions,
then update their positions.
Trying to update positions as you go introduces biases and produces asymmetric results.

Repeat the entire smoothing operation $n$ times, where $n$ is the number provided by into the "weathering" input.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should initially be blank.
Once the button is pressed a terrain should appear, smoothed based on the new provided input.

<figure>
<video controls autoplay loop>
<source src="vid/weathering.webm" type="video/webm"/>
<source src="vid/weathering.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result, with several levels of weathering applied to a 100×100 grid with 50 faults. The "Grid Size" and "Faults" inputs are not shown to save space.
</figcaption>
</figure>

Smoothing's visual impact is strongly influenced by grid resolution.
Smoothing is purely local, so on larger grids it has smaller visual impact.
A reasonable approximation is
the same overall visual appearance will be seen
on a grid with $n$ times as many vertices on each side
using $n^2$ times as many smoothing iterations.

:::example
We'd expect gridsize 25 with 1 smoothing iteration
to look similar to gridsize 50 with 4 smoothing iterations,
gridsize 75 with 9 smoothing iterations,
gridsize 100 with 16 smoothing iterations,
...
or gridsize 250 with 100 smoothing iterations.
:::
