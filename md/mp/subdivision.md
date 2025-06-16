---
title: "Subdivision Surface MP"
...

In this MP you will

1. Import an OBJ (see [the OBJ MP](obj.html))
2. Render it with flat shading based on polygon geometery
3. Apply Catmull-Clark subdivision to the imported mesh

This MP is elective, with no core components.
It assumes you have already completed the [OBJ MP](obj.html).

:::{style="margin:1em; padding: 1ex; border-radius: 1.414ex; box-shadow:0 0 1ex rgba(0,0,0,0.5); background: rgba(255,255,0,0.25); "}
<strong style="font-size:150%">Warning</strong>

This MP is likely to take more effort and time than its point value suggests.
It is intended to be a jumping-off point for students interested in geometry definition and refinement,
which is not a topic given much attention in this course.
:::

# Overview

You will submit a webpage that has

- One file browsing field
- One numeric entry field
- One canvas
- A 3D view of a lit subdivided model

Submit an HTML file and any number of js, glsl, css, and JSON files. No image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

## HTML input setup

Have one file browsing input for uploading an OBJ file.

Have one input numeric field for entering how many rounds of subdivision to do.

HTML input elements, styling, and event handling are beyond the scope of this class. We provide suggested starter code for them:

<details class="aside"><summary>Suggested starter code</summary>

We recommend using the following HTML body:

```html
<body>
<label>OBJ File path: <input id="file" type="file"/></label>
<label>Levels: <input id="levels" type="number" value="0" max="5" min="0" step="1"/></label>
<canvas></canvas>
</body>
```

and the following event listeners

```js
document.getElementById('file').addEventListener('change', async event=>{
  if (event.target.files.length != 1) {
    console.debug("No file selected")
    return
  }
  const txt = await event.target.files[0].text()
  if (!/^v .*^v .*^v .*^f /gms.test(txt)) {
    console.debug("File not a valid OBJ file")
    return
  }
  
  // TO DO: parse the OBJ file from the string in `txt` and display it
})
document.getElementById('levels').addEventListener('change', async event=>{
  const level = Math.min(document.getElementById('levels').value, 5)|0
  
  // TO DO: subdivide (if level > 0) and display the object
})
```

</details>


## Flat-shaded OBJ

You'll load the OBJ file similarly to how you did in the [OBJ MP](obj.html).
The string is retrieved in a slightly different way, but otherwise is the same.

However, you will need to store the resulting mesh differently.
You need to store faces of any number of sides and the interconnections,
which a simple triangle index array does not provide.
We recommend storing them in a [half-edge data structure](../text/halfedge.html),
either using straightforward object-oriented structures like

```js
class HalfEdge {
    v
    next
    twin
    constructor(v, next, twin) {
        this.v = v;
        this.next = next;
        this.twin = twin;
    }
    sideCount() {
        let ans = 1
        for(let he=this.next; he!=this; he=he.next) ans += 1
        return ans
    }
}
```

or by using parallel arrays, as is outlined in [Dupuy and Vanhoey's 2021 paper](https://onrendering.com/data/papers/catmark/HalfedgeCatmullClark.pdf).

You also need to flat-shade the polygons, meaning you have one normal per face, not one per vertex.
The easiest way to accomplish this is to [use `drawArrays` instead of `drawElements`](../text/webgl-geometry.html),
providing each vertex one per face it touches with a different normal each time.
To compute the normals themselves, take the cross product of two edges of a triangle
or of the two diagonals of a quad; for 5+-sided shapes, the normal of any triangle or quad inside it will work.

## Catmull-Clark subdivision

If the rounds of subdivision is greater than 0,
that many rounds of [Catmull-Clark subdivision](../text/make-geom.html#center-point).
[Dupuy and Vanhoey's 2021 paper](https://onrendering.com/data/papers/catmark/HalfedgeCatmullClark.pdf) explains one algorithm for doing this, but there are many other algorithms available online or derivable by yourself from the definition of Catmull-Clark's scheme.

Store the resulting levels (or at least the level-0 mesh) so that you can go back to a lower level after being at a higher one.

## Render and light

Render the geometry with both diffuse and specular lighting.
Have the camera or geometry moving so that the geometry can be seen from multiple viewpoints.

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should initially be blank.
Once an OBJ file is loaded, a flat-shaded mesh should appear, filling most of the screen with a moving camera.
As the levels are changed the mesh should be subdivided.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/subdivision.webm" type="video/webm"/>
<source src="vid/subdivision.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>

Your program should work correctly for at least the following subdivision-friendly meshes:

- [`tetrahedron.obj`](files/tetrahedron.obj)
- [`cube.obj`](files/cube.obj)
- [`nonogon.obj`](files/nonogon.obj)
- [`bevel.obj`](files/bevel.obj)
- [`dodecahedron.obj`](files/dodecahedron.obj)

The [teapot](files/teapot.obj) and [cow](files/cow.obj) models are not designed to subdivide well; your code should run on them, but might give ugly results.

The [Suzanne](files/suzzane.obj) and [triangle](files/triangle.obj) models have edges that are not connected to anything.
We don't require your code to work on them, but if you want it to then have edges of the mesh act the same they would if they were adjoined by zero-width polygons instead.
