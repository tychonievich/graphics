---
title: "Logo MP"
...

In this MP you will

1. Make a 2D model by hand
2. Display the model using WebGL2
3. Animate the model using a matrix

This MP is core, with no elective components.
It assumes you have already completed the [WebGL warmup](warmup-webgl2.html).

# Overview

    
<figure class="floater">
<img alt="University of Illinois Logo" src="../files/ilogo.png" style="width:10em"/>
<figcaption>University of Illinois Logo</figcaption>
</figure>


You will submit a webpage that has

- One canvas
- A 2D animation of the majestic and inspiring University of Illinois logo

Submit an HTML file and any number of js, css, glsl, and json files. No image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

## HTML file

Submit one HTML file.

Including `DOCTYPE`, `lang`, `charset`, and `title`.

Have at least one `script` element in the `head`, and none outside the `head`.

Have one `canvas` element.

## Coding

Draw using a `webgl2` context.

Use `requestAnimationFrame` to animate the canvas at the browser's natural frame-rate.
This should begin as soon as the page has loaded, requiring no user action to start.

Code following our recommended practices.
In particular, if you put [wrapWebGL2.js](../code/wrapWebGL2.js) in the same directory as your HTML file
and include `<script src="wrapWebGL2.js"></script>` before any other `<script ...>` element
there should be no warnings or errors displayed in the console (except perhaps an error about not finding favicon.ico[^favicon]).

[^favicon]:
    If you want to get the favicon error to go away, you need to provide a favicon.
    The shortest way to do this is to tell the HTML to use a default icon by adding this to the HTML `<head>`{.html}:
    
    ````html
    <link rel="icon" href="data:,">
    ````


## Graphics


Make a reasonable polygonal approximation of the University of Illinois logo.
No need to model the curves where the vertical bar meets the serifs.
    
According to the [Office of Strategic Marketing and Branding](https://marketing.illinois.edu/visual-identity/color),
the logo has RGB 255/95/5, which converted to 0–1 colors used by WebGL is $(r,g,b) = (1, 0.373, 0.02)$.
Sometimes the logo has a blue outline; if you wish to do that
it should be RGB 19/41/75 meaning $(r,g,b) = (0.075, 0.16, 0.292)$.

You should create this model by hand, such as by drawing the logo on graph paper.
The by-hand requirement isn't something we'll even try to enforce or grade, but doing it that way will help build your brain's ability to convert between shapes and coordinates, a valuable skill in graphics.
    
<details class="aside"><summary>A process for creating 2D models by hand</summary>

1. Draw the shape on graph paper
2. Put a bold dot at each corner of the shape
3. Number the points in any order, starting with 0
4. Pick an origin and scale for the graph paper
5. Create an array of vertices in numbered order, using coordinates from the graph paper
6. Fill in a triangle on the graph paper and add the number of its three vertices to the triangles index array
7. Repeat step 6 with another triangle, and then another, until the entire shape is filled in

WebGL displays things between $-1$ and $+1$ in $x$ and $y$.
If you modeled the logo with different bounds, you can adjust it in the vertex shader as e.g. by finding a scaling factor `s` and offsets `dx` and `dy` and using them as

````glsl
gl_Position = vec4(vert.x*s + dx, vert.y*s + dy, 0, 1);
````

</details>


The logo should move about the canvas because its vertex positions are being modified by a matrix that varies with time.
This means

- having a `uniform mat4` in your vertex shader (and no other `uniform`s in the vertex shader)
- assigning the matrix a new value each frame to create the desired motion

Your animation should look smooth (no sudden jumps from one image to another),
should keep the logo constantly moving and mostly on-screen,
and should do **at least two of**

- moving the logo
- rotating the logo
- changing the logo's size

Do not squish or stretch the logo: any size changes should be uniformly applied to all dimensions.

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show a moving I logo.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/logo.webm" type="video/webm"/>
<source src="vid/logo.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>

