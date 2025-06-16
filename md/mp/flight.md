---
title: "Flight MP"
...

In this MP you will

1. Auto-generate a terrain (with no user input)
2. Respond to keys to move and rotate the camera

This MP is core, with no elective components.
It assumes you have already completed the [Terrain MP](terrain.html).

# Overview

You will submit a webpage that has

- One canvas
- A 3D view of dynamically-generated fractal terrain
- Responds smoothly and continuously to keys

Submit an HTML file and any number of js, glsl, json, css, and image files.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.


# Specification

## Auto-generated terrain

Do not have any `<input ...>` elements in your HTML.
Instead, as soon as the page loads fill a full-screen canvas with a randomly-generated fractal terrain, such as you did as part of the [Terrain MP](terrain.html).
You are welcome to use one of the terrain add-ons
such as [weathering](weathering.html), [cliffs](cliffs.html), [height map](height-map.html), [textures](textures.html), or [shine map](shine-map.html) or other variants of that type.

## Listen to keys

When the user is holding down certain keys, the camera should move smoothly until those keys are released.

| Key | Translation |
|-----|--------|
| `w` | Forward -- the direction the camera is currently looking |
| `s` | Backward -- the opposite of `w` |
| `a` | Leftward -- without changing the direction the camera is looking, move so the things it views pass before it left-to-right as the camera moves to its left |
| `d` | Rightward -- the opposite of `a` |

| Key | Rotation |
|-----|--------|
| `ArrowUp` | Look up -- pitch the camera to look closer to the sky |
| `ArrowDown` | Look down -- pitch the camera to look closer to the ground |
| `ArrowLeft` | Turn left -- pivot along the up-down axis to look to the left |
| `ArrowRight` | Turn right -- pivot along the up-down axis to look to the right |

The JavaScript event system does not directly provide a way of discovering what keys are being held down.
Instead, you'll need to listen to when keys are pressed and when they are released
and keep track of which have been pressed but not released.
One way to do this is

```js
window.keysBeingPressed = {}
window.addEventListener('keydown', event => keysBeingPressed[event.key] = true)
window.addEventListener('keyup', event => keysBeingPressed[event.key] = false)
```

after which you can add something like `if (keysBeingPressed['ArrowUp']) { /* ... */ }`{.js} to your every-frame code.

## Mobile camera

As noted in the [listen to keys] section, the camera should move relative to its current view.
There are two basic approaches to this:
the easy one and the nicely-behaving one.

### Easy approach

The view matrix stores the camera's position and orientation,
so moving the camera can be adjusting the view matrix.

Recall that matrices change the coordinate system.
Thus if I have a rotation matrix $R$ and do something like
$$V := V R$$
then $R$ is applied before $V$ changes the coordinate system,
meaning $V$ will have be rotated in the world coordinate system around the world's origin.
If I instead do something like
$$V := R V$$
then $R$ is applied after $V$'s change of coordinate system
meaning $V$ will be rotated in its coordinate system (i.e., relative to the on-screen axes)
and around its origin (i.e. the eye location).
Thus, this second approach can implement the flight required of this task.

This is easy, but not very nice because it looses track of the fact that humans always want "down" to point in roughly the same direction.
With this approach that is not done;
if look down, then left, then up, then right
you can end up pointing in the same direction as before
but with the camera no longer right-side-up.

This approach also makes it much harder to add limits on the camera's motion,
such as the elective follow-on [Drive MP](drive.html) does.

### Nice approach

In principle a camera has three degrees of freedom:
a 3D location and 3 aspects of orientation.
But we only want 2 aspects of orientation to be controlled by the user
because the camera should always be right-side-up.
Conveniently, we can get those 5 degrees of freedom
by storing two 3D vectors with direct meaning:
the eye location
and the forward direction,
where forward is always a unit vector.

From the camera's forward direction
and the *global* up direction,
we can get the camera's right direction with a (normalized) cross-product;
from the camera's forward and right directions we can get the camera's up direction with another cross product.

Translating the camera means adding (a scalar multiple of) the camera's forward or right direction to its eye location.

Rotating the camera means [rotating its forward vector around its right vector](https://cs418.cs.illinois.edu/website/text/math2.html#rotation) (to pitch up or down)
or the global up direction (to turn left or right).

The view matrix can be constructed from these vectors as $V = R T$
where $T$ translates the eye to the origin
and $R$ puts the camera's right direction on the $x$ axis,
its up direction on the $y$ axis,
and its forward direction on the $-z$ axis
like so:
$$R = \begin{bmatrix}r_x&r_y&r_z&0\\u_x&u_y&u_z&0\\-f_x&-f_y&-f_z&0\\0&0&0&1\end{bmatrix}$$

<details class="note"><summary>WebGL2 and all of the matrix code I provided in this class assume **column-major matrices**</summary>
This means that the matrix

$$\begin{bmatrix}a&b&c&d\\e&f&g&h\\i&j&k&l\\m&n&o&p\end{bmatrix}$$

is provided in code as

```js
[ a, e, i, m
, b, f, j, n
, c, g, k, o
, d, h, l, p
]
```

</details>

This process is a bit more work than the easier approach,
but it results in two benefits.
First, we can easily rotate around the world up axis but the camera's location, thus avoiding the camera ever going upside down.
Second, we have the camera's location in world coordinates which we can use to constrain its motion,
such as we do in the elective [Drive MP](drive.html).


# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting page should show a random terrain.
When keys are held down the camera should fly smoothly through the scene.
One example might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/flight.webm" type="video/webm"/>
<source src="vid/flight.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
To make the relationship between keys and motion clearer,
the keys being pressed in each frame are shown on top of the 3D image.
</figcaption>
</figure>


# Going beyond: Model and View {-}

This MP focuses on view matrices.
The [Orbits MP](orbits.html) focused on model matrices.
Together, those two make up the model-view matrix used in many vertex shaders.

Can you put these together yourself?
Try the following:

1. Modify your orbits code to have a keyboard-controlled camera.
2. Add a key that, when held down, locks the camera to a fixed position relative to the earth and when released lets it fly free again.
3. Add lighting (both diffuse and specular) to the objects in the orbits scene and make sure both the view-dependent specular component and the view-independent diffuse component are working correctly

If you can do this you are probably ready to handle whatever scene arrangement and camera motion you want.
