---
title: "Textures MP"
...

In this MP you will

1. Auto-generate a terrain (with no user input)
2. Have two shader programs, one for color and one for texture
3. Let the user change the color and texture

This MP is core, with no elective components.
It assumes you have already completed the [Terrain MP](terrain.html).

# Overview

You will submit a webpage that has

- Two number entry fields
- One text entry field
- One button
- One canvas
- A 3D view of dynamically-generated fractal terrain

Submit an HTML file and any number of js, glsl, json, css, and image files.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

## Everything the [Terrain MP](terrain.hml) does

This MP is an extension of the Terrain MP; it should have all the inputs, algorithms, and operations of that MP.

## Material entry

Add one more `<input type="text" ...>` in your HTML.
Support three types of entry:

- Blank (`value == ''`{.js})
  
  Use the color $(1,1,1,0.3)$ and the non-texture shader program.
  This should also be the initial state of the program before the text has ever changed.

- `#` followed by 8 hexadecimal digits (`/^#[0-9a-f]{8}$/i.test(value)`{.js})

  Parse this as a hex color string:
  the first two hex digits are the red channel on a 0--255 scale,
  the next two green, then blue, then alpha.
  Use this with the non-texture shader program.
  
  The `.substr(i,n)`{.js} method extracts `n` characters from a string starting at index `i`.
  The built-in `Number` function can convert hex numbers to numeric values if the hex is preceded by `0x`.
  Combining these, you might do something like `blue = Number('0x' + value.substr(5,2))`{.js}.

- Any string ending either `.jpg` or `.png` (`/[.](jpg|png)$/.test(value)`{.js})
  
  Treat this as the URL of an image.
  If the loading the image fails (which you can detect with `img.addEventListener('error', callback)`{.js}),
  use the color $(1,0,1,0)$ and the non-texture shader program.
  If it succeeds (which you can detect with `img.addEventListener('load', callback)`{.js}),
  send it as a texture to the GPU and use the with-texture shader program.
  
  We have a [guide to using textures](../text/textures.html) with example code.


Respond to changes in the text entry field as soon as they occur (i.e., without waiting for a button event).
Do this by parsing the material test in a `change` event listener on the text entry input;
leave the terrain generation on the `click` event listener you already have on the button input.

## Two shader programs

Compile and link two different shader programs during setup,
picking between them each frame based on the results of the last material entry change listener.

The non-texture shader program should use a `uniform vec4`{.glsl} RGBA color
and have both diffuse and specular light.
The alpha channel in the color should be treated as a an amount of specular shine to add, not as opacity,
and should not be copied into the output image.
Instead, have the specular intensity (computed via either the Phong or Blinn-Phong model) by multiplied by $3\alpha$.
In the real world light that is used to create a shine is not available to create diffuse light;
simulate this by multiplying the diffuse intensity by $(1-\alpha)$.

The with-texture shader program should use a `uniform sampler2D`{.glsl} texture
and `in vec2`{.glsl} texture coordinate.
It should have diffuse light only with the diffuse color coming from the texture, no specular light at all.
You should modify your terrain generation to place a texture coordinate with every vertex,
with (0,0) in one corner and (1,1) in the other.
Because the non-texture shader will ignore attributes it doesn't have an `in`{.glsl} variable for, you can use this same modified geometry for both shaders.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should show a random terrain.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/textures.webm" type="video/webm"/>
<source src="vid/textures.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
The two textures used are [luther.png](files/luther.png) and [testgrid.png](files/testgrid.png),
both of which are pre-loaded on the submission server.
</figcaption>
</figure>
