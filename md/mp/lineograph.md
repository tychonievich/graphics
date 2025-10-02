---
title: "Lineograph MP"
...

In this MP you will implement a 3D version of a [lineograph](https://en.wikipedia.org/wiki/Lineography),
moving a 3D cursor with the keyboard to draw a 3D shape.

This MP is elective, with no code components.
It assumes you have already completed the [Orbits MP](orbits.html).

# Overview

You will submit a webpage that has

- One canvas
- A never-cleared rendering that you can add to each frame
- Key listeners to let the user draw

Submit an HTML file and any number of js, css, glsl, and json files. No image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

We recommend starting with a copy of your [Orbits MP](orbits.html) code,
as that will provide you with a resizing canvas, 3D view, and octahedron geometry.

## Don't clear between frames

Make a 3D scene with a depth buffer, but never clear anything.
This means at least

- Pass `{preserveDrawingBuffer:true}`{.js} as the second argument of `getContext` to tell the browser not to clear the scene for you. You're welcome to add other configuration options to that object too.

- Enable `gl.DEPTH_TEST`.

- Have `gl.clear` invoked only immediately after `gl.viewport` in the canvas resize function, not in the draw function.

Every frame, draw the same small octahedron.

## Listen to keys

JavaScript can listen to events fired when keys are pressed or released.
Those events are not good for moving things in an animation, though,
as we want steady motion while a key is held down.
Thus, track which keys are down using those events
and check them when drawing.

To track keys, you can use the following during setup:

```js
window.keysBeingPressed = {}
window.addEventListener('keydown', event => keysBeingPressed[event.key] = true)
window.addEventListener('keyup', event => keysBeingPressed[event.key] = false)
```

To check keys, you can use `if (keysBeingPressed['q']) ...`{.js}

## Smooth 3-axis motion

If one of six keys is being pressed, the octahedron should move with a slow, steady motion.

The six keys to listen to are:

- `q` should move the octahedron deeper into the screen; `e` should be the opposite motion
- `a` should move the octahedron towards the left side of the screen; `d` should be the opposite motion
- `w` should move the octahedron towards the top of the screen; `s` should be the opposite motion

<!--
The best way to achieve smooth motion is to use the difference between the time of the current render
and the time of the last render
as the distance to move the octahedron in the given direction.
That will keep the motion smooth even if the browser skips frames, etc.
-->

Motion should be implemented by storing a global position
and using it each frame to generate a translation matrix.


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting scene should be a mostly-blank canvas with a single small octahedron in the middle.
When pressing the keys listed, it should move leaving a trail behind it.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/lineograph.webm" type="video/webm"/>
<source src="vid/lineograph.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>

