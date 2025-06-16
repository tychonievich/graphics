---
title: "OBJ file loading MP"
...

In this MP you will

1. Load geometry from the OBJ file format
2. Render it in a lit, possible texture-mapped way

This MP is elective, with no core components.
It assumes you have already completed the [Terrain MP](terrain.html)
and optionally also the [Textures MP](textures.html).

# Overview

You will submit a webpage that has

- One or two text entry fields
- One button
- One canvas
- A 3D view of a loaded OBJ

Submit an HTML file and any number of js, glsl, and css files. No image or JSON files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

## HTML input setup

Have one input text field for entering an OBJ file name.
Optionally, also have one for entering a texture map image file name.

HTML input elements, styling, and event handling are beyond the scope of this class.
See the [Terrain MP](terrain.html) for example code for setting up inputs.

For this assignment, you should use `type="text"` instead of the `type="number"` used by the Terrain MP.
You should also remove the `Number(...) || defaultValue` wrappers on the inpupt checking in your JavaScript.

## Read OBJ files

Given an OBJ file,
parse it into a geometry object.
You should support at least per-vertex positions and colors.
We provide three example files that have just positions or just positions and colors:

- [`triangle.obj`](files/triangle.obj), the smallest meaningful OBJ file we could make
- [`teapot.obj`](files/teapot.obj), with positions only
- [`cow.obj`](files/cow.obj), with positions and colors

We also provide a [guide to reading OBJ files](../text/obj.html).

Once loaded, you should display the model with the following criteria:

- It should be lit with both diffuse and specular illumination, meaning you'll need to generate surface normals if none are provide.
- It should be centered and scaled to fit on the screen and not be too small on the screen.
- It should be rotating under a fixed light source. This is most easily done by rotating the normals in the vertex shader.
- If there are no vertex colors, it should be a light gray color

This part is worth half of the points of this assignment.

## Normals and Textures

To earn the other half of the points of this assignment,
also handle OBJ-file-supplied normals and texture coordinates.
We provide two example files for this:

- [`bevel.obj`](files/bevel.obj) has surface normals that are not the ones you'd compute
- [`suzanne.obj`](files/suzanne.obj) has texture coordinates and normals

Additionally, you should allow a the user to provide an image to use as a texture map.
If an image is provided (i.e. isn't the empty string) you should use a vertex shader that uses the texture to pick the diffuse color of the model.
If there are no texture coordinates the shader will default to using the top-left pixel as the object's color -- this will probably happen automatically, no special effort needed by you.
If no image is provided, use the non-texture shader like usual.

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should initially be blank.
Once an OBJ (and optionally image) file name is entered and the button is pressed, the model should appear, filling most of the screen.

On the submission server, the following paths exist even if you didn't upload them:

- `triangle.obj`
- `teapot.obj`
- `cow.obj`
- `bevel.obj`
- `suzanne.obj`
- `example.jpg`

<figure>
<video controls autoplay loop>
<source src="vid/obj-basic.webm" type="video/webm"/>
<source src="vid/obj-basic.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result of the basic part (half of the points).
</figcaption>
</figure>

<figure>
<video controls autoplay loop>
<source src="vid/obj-normal.webm" type="video/webm"/>
<source src="vid/obj-normal.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result of the custom normals.
Note that this OBJ file gives each face of the cube flat normals and the bevels around its edges curved normals.
</figcaption>
</figure>

<figure>
<video controls autoplay loop>
<source src="vid/obj-texture.webm" type="video/webm"/>
<source src="vid/obj-texture.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result of texture mapping, using [example.jpg](files/example.jpg) as the texture map.
</figcaption>
</figure>
