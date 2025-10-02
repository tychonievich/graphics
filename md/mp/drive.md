---
title: "Drive MP"
...

In this MP you will

1. Auto-generate a terrain (with no user input)
2. Respond to keys to move and rotate the camera
3. Keep the camera a fixed distance above the ground
4. Implement more accurate specular highlights

This MP is elective, with no core components.
It assumes you have already completed the [Flight MP](flight.html).

# Overview

You will submit a webpage that has

- One canvas
- A 3D view of dynamically-generated fractal terrain
- Responds smoothly and continuously to keys

Submit an HTML file and any number of js, glsl, json, css, and image files.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

## Everything the [Flight MP](flight.html) does

This MP is an extension of the Flight MP; it should have all the inputs, algorithms, and operations of that MP.

This MP requires that the camera never bank, always remaining right-side up.

This MP assumes you used the nice approach to flying and have the camera position as a known variable.

## Drive, not fly

The camera should be kept a fixed height above the terrain,
close enough that nearby triangles take up a significant part of the field of view.
It should also translate slowly enough that it takes several frames to move from one vertex of the terrain to another.

The recommend approach to this is to do the following every frame:

1. Move the camera as if flying freely this frame
2. Find the height of the terrain at the camera's horizontal position
3. Change the camera's height to be a small amount higher than the terrain

To find the height of the terrain at some world position, you should use [inverse bilinear interpolation](../text/lerp.html#interpolating-on-a-grid) on the grid of heights you used to create the terrain.
The point-to-grid-coordinate transformation is the inverse of whatever math you use to convert grid cell coordinates to vertex positions when creating the grid.

We do not require any specific behavior when the camera is off the grid
except that the program not crash;
it should either keep the camera on the grid or let it return to the grid later in the program's execution.

## Up-close specular highlights

In class we implemented Blinn's optimization of specular lighting where we treated the halfway vector (or equivalently the direction to the eye) as fixed for all fragments in the scene.
That works well when the scene objects are relatively far from the camera,
but less well when the camera is up close to them.

For this assignment, compute per-fragment directions to the eye
by interpolating the world coordinate of the triangle to each fragment
and computing the direction to the eye from that position and the position of the eye.



# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should show the camera resting on a random terrain.
When keys are held down the camera should drive across the terrain,
rising and falling smoothly as it moves along sloped terrain.
Specular highlights should react to camera location, not its orientation,
which will be particularly noticeable in small motions having large impact on nearby highlights
but less impact on distant highlights.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/drive.webm" type="video/webm"/>
<source src="vid/drive.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result, with keys being pressed displayed in the video.
Note the smooth motion when climbing or descending slopes
and the behavior of nearby specular highlights when moving.
</figcaption>
</figure>


