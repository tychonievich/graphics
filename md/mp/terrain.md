---
title: "Terrain MP"
...

In this MP you will

1. Generate a grid of user-specified size
2. Use a simple fracture-based fractal to make it look like rough terrain

This MP is core, with no elective components.
It assumes you have already completed the [Logo MP](logo.html).

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

## HTML input setup

HTML input elements, styling, and event handling are beyond the scope of this class, so we simply give you what you need here.

Your HTML file should have the following after the various `<script` elements:

```html
    <style>
    body {
        margin: 0; border: none; padding: 0;
        display: flex; flex-direction: column;
        width: 100%; height: 100vh;
    }
    .controls {
        flex: 0 0 auto;
    }
    .controls > * { margin: 1em; }
    .display {
        flex-grow: 1;
        line-height: 0rem;
    }
    </style>
</head>
<body>
<form class="controls" action="javascript:void(0);">
    <label>Grid size: <input id="gridsize" type="number" value="50"/></label>
    <label>Faults: <input id="faults" type="number" value="50"/></label>
    <input id="submit" type="submit" value="Regenerate Terrain"/>
</form>
<div class="display">
    <canvas width="300" height="300"></canvas>
</div>
</body>
</html>
```

You should register the following with a `window.addEventListener('resize',fillscreen)`{.js} in your setup function after setting `window.gl` to handle canvas resize:

```js
function fillScreen() {
    let canvas = document.querySelector('canvas')
    document.body.style.margin = '0'
    canvas.style.width = '100%'
    canvas.style.height = '100%'
    canvas.width = canvas.clientWidth
    canvas.height = canvas.clientHeight
    canvas.style.width = ''
    canvas.style.height = ''
    gl.viewport(0,0, canvas.width, canvas.height)
    // TO DO: compute a new projection matrix based on the width/height aspect ratio
}
```

You should listen to input events like so:

```js
document.querySelector('#submit').addEventListener('click', event => {
    const gridsize = Number(document.querySelector('#gridsize').value) || 2
    const faults = Number(document.querySelector('#faults').value) || 0
    // TO DO: generate a new gridsize-by-gridsize grid here, then apply faults to it
})
```

Because the program starts with no terrain generated yet,
add a check in your draw callback that skips drawing if there's nothing to draw.

## Generate terrain

When the button is clicked,

1. [Create a square grid](../text/make-geom.html#grids) with `gridsize` vertices per side.

    Don't duplicate vertices.
    We will check that it has exactly `gridsize*gridsize` vertices
    and `(gridsize-1)*(gridsize-1)*2` triangles.
    
    Your code should work for any integer `gridsize` between 2 and 255, inclusive.
    
    <div class="note">
    Most students find it easier to make the grid occupy the same range of $x$ values regardless of the `gridsize`,
    as that simplifies setting up the view and projection matrices.
    Positions between $-1$ and $+1$ are the most popular choice.
    </div>
    
    Larger `gridsize` should result in higher-resolution terrain,
    but not otherwise change the visual appearance;
    for example, the terrain should occupy the same part of the field of view,
    have the same ratio of height to width, etc.,
    at all `gridsize`s.

2. Displace the vertices in the grid with `faults` faults.
    
    For 0 faults, the result should be perfectly flat.
    For more faults it should approach a fractal bumpy terrain.
    
    Your code should work for any non-negative integer `faults`; there is no upper limit to what we might provide.
    
    Faults should be distributed uniformly on average,
    with no bias towards particular fault directions
    no parts of the grid that get many fewer faults than other parts.

3. Normalize heights so that the terrain has the same height regardless of the number of faults
    (assuming there is at least one fault).
    
    To do this, find the min and max heights after faulting,
    then replace each height with 
    $$\text{height}' = c \dfrac{\text{height} - \frac{1}{2}(\text{max} + \text{min})}{\text{max} - \text{min}}$$
    where $c$ is a constant that changes how tall the highest peak is.
  
4. Compute correct [grid-based normals](../text/make-geom.html#rectangular-grid-normals).
  
    Because grids usually have 6 triangles around each vertex, generic triangle-based normals tend to look asymmetric.
    But we can do much better with less work by taking advantage of the structure of the grid.
    
    Consider a vertex $v$ with four neighboring vertices: $s$ to the south, $w$ to the west, $n$ to the north, and $e$ to the east.
    Then the normal at $v$ is $(n - s) \times (w - e)$.
    If $v$ is on the edge of the grid and one or more of those neighbors is missing, use $v$ itself in place of the missing neighbors in the normal computation.

## Render and light

Render the terrain with one white light source
and with both diffuse and specular lighting.
Use an earth tone (i.e. $1 > r > g > b > 0$) for the diffuse color, picking a color light enough that lighting is obvious.
Use white for the specular highlights.
Have the light source coming from above the terrain, but not directly above it.

Have the camera moving around the terrain.
The terrain should fill most of the camera's field of view,
and most of the terrain should be in the camera's field of view.
The camera should be a little above the highest peak in the terrain.

The light source should be fixed relative to the terrain:
that is, changing the view should not change how much diffuse lighting any given part of the terrain has.

<details class="aside"><summary>Fixing light relative to terrain.</summary>

Lighting is created based on three vectors:

- a vector toward the eye or camera
- a vector toward the light
- a vector along the surface normal

The lighting example we gave in class had light fixed relative to the camera.
It did this by having the eye and light vectors fixed (stationary camera and light source)
and changing the normal vector every frame in the vertex shader (moving object).

For this MP, you need to have the light fixed relative to the terrain.
The natural way to do this is to have the light and normal vectors fixed (stationary terrain and sun)
and change the eye vector every frame (moving camera).

In all cases we could [change between view and world coordinates](../text/lighting.html#coordinate-space) to do this in a different way.
The monkey example used view coordinates, but could use world coordinates instead;
the way I described the terrain sounds like world coordinates, but could be transformed into view coordinates instead.
Which one you pick is up to you, but you must be consistent:
if the vector to the eye is in view coordinates, the normal vector and any vector to the light must also be in 

</details>

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should initially be blank.
Once the button is pressed a terrain should appear, filling most of the screen
with a moving camera.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/terrain.webm" type="video/webm"/>
<source src="vid/terrain.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>

To help with lighting we also share three videos where the terrain is set to look like a sphere;
in particular, the terrain height is $\sqrt{1-r^2}$, where $r$ is the distance from the point and the center of the terrain divided by the radius of the terrain; if that square root is an imaginary number, the terrain height is $0$.

First we show a correctly-lit example:

<figure>
<video controls autoplay loop>
<source src="vid/terrain-light.webm" type="video/webm"/>
<source src="vid/terrain-light.mp4" type="video/mp4"/>
</video>
<figcaption>
A video demonstrating **correct lighting** fixed relative to the terrain, not the viewer.
Notice that there is a bright side of the hill and a dark side of the hill, with the camera viewing from all sides;
and that the shine spot moves across the hill as the point of view changes, but the shine never moves into the dark region.
</figcaption>
</figure>

We also show two **incorrectly** lit bad examples:
<figure>
<video controls autoplay loop>
<source src="vid/terrain-badshine.webm" type="video/webm"/>
<source src="vid/terrain-badshine.mp4" type="video/mp4"/>
</video>
<figcaption>
A video demonstrating **incorrect lighting** where specularity is not related to view direction.
Notice that the "shine spots" is just a fixed splotch of white, not acting like specularity does.
</figcaption>
</figure>
<figure>
<video controls autoplay loop>
<source src="vid/terrain-baddiffuse.webm" type="video/webm"/>
<source src="vid/terrain-baddiffuse.mp4" type="video/mp4"/>
</video>
<figcaption>
A video demonstrating **incorrect lighting** where the light source is fixed relative to the camera, not the terrain.
</figcaption>
</figure>


