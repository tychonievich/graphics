---
title: "Many Spheres MP"
...

In this MP you will

1. Redo your [Spheres MP](spheres.html) to run much more quickly

This MP is elective, with no core components.
It assumes you have already completed the [Spheres MP](spheres.html).

# Overview

You will submit a webpage that has

- One canvas
- A self-running animation with a user-specified number of random spheres with random size
- Collision resolution and gravity
- Animation restarts every 15 seconds

Submit an HTML file and any number of js, css, and glsl files. No json or image files are permitted for this assignment.
Do not include spaces in file names as the submission server does not process them well.

You are welcome to use a JavaScript math library, such as [the one used in in-class examples](../code/math.js) or others you might know.

# Specification

## An input and an frames per second (FPS) display

Add the following to your HTML after the canvas element but still inside the body.

```html
<div id="fps" style="position:fixed; bottom:1ex; right:1ex; display:table;"></div>
<form class="controls" action="javascript:void(0);" style="position:fixed; top:1ex; left:1ex; display:table;">
    <label>Spheres: <input id="spheres" type="number" value="50" style="width:5em;"/></label>
    <input id="submit" type="submit" value="Restart simulation"/>
</form>
```

Every frame, set `document.querySelector('#fps').innerHTML = fps.toFixed(1)`{.js}, where `fps` is the current frame rate (i.e., `1/dt`{.js} if `dt` is the number of seconds since the last frame).

Listen for clicks of the submit button and restart the simulation with the requested number of spheres.
Also restart the simulation every 15 seconds, as you did for the [Spheres MP](spheres.html).


## Variable size and number of spheres

Let the user specify the number of spheres to use in the animation.

Randomly allocate sphere sizes so that the largest has 5× the radius of the smallest
and the full set of spheres when at rest will fill the bottom of the cube several spheres deep.
One way to do this is
```js
radius = (Math.random()+.25) * (0.75/n**(1/3))
```
where `n` is the number of spheres.

Have sphere mass be proportional to volume, which is proportional to the cube of radius.
Thus, when a large and small sphere collide the small one should usually do most of the moving out of the way.

## Efficient rendering

One major source of inefficiency in the [Spheres MP](spheres.html)
is the number of times the CPU speaks to the GPU.
In my reference implementation, that was $3n+5$ calls per frame.
Each such call requires the GPU to wait for the last one to complete,
meaning most of the GPU's possible parallelism is ineffective.

To fix this, change how spheres are drawn.

- Remove the sphere geometry and `gl.drawElements` and instead use `gl.drawArrays` with mode `gl.POINTS`.

- Have three attribute arrays: one of sphere centers, one of sphere radii, and one of sphere colors.

- Each frame, re-send the sphere centers buffer using `gl.DYNAMIC_DRAW` instead of `gl.STATIC_DRAW`.

- In the vertex shader, compute the on-screen radius and store it in `gl_PointSize`
    - This is the product of four values:
    1. Viewport size in pixels in either $x$ or $y$. You’ll have to pass this in as a `uniform float`{.glsl}; you can get it as `gl.canvas.width`{.js} or `gl.canvas.height`{.js}.
    2. Projection matrix scaling in the same axis. Assuming you are using a standard perspective projection matrix, this is either `proj[0][0]`{.glsl} for $x$ or `proj[1][1]`{.glsl} for $y$, where `proj` is your projection matrix.
    3. The inverse of the $w$ value for this point. That is `1/gl_Position.w`{.glsl}.
    4. The radius of the sphere.
    - This isn't perfect, as it will always render circular outlines but spheres tend to stretch into elliptical outlines away from the center of the projection, but it will be good enough for our purposes. The error might make large spheres appear to collide before they touch.

- In the fragment shader, render the square point as a lit sphere using `gl_PointCoord`
    - `gl_PointCoord` is a `vec2` ranging from $(0,0)$ in the top-left corner to $(1,1)$ in the bottom right
    - If you re-map this to a range from $(-1,-1)$ to $(1,1)$ it gives you the screen-space $(n_x,n_y)$ of the unit surface normal.
    - The full surface normal should have magnitude $1$, from which you can compute $n_z$.
    - If $(n_x,n_y)$ is longer than $1$ then the fragment is outside the sphere and can be discarded (e.g. as `if (nxylength > 1) discard;`{.glsl}). Note: `if`s that have `discard;` as their sole statement are handled efficiently by the GPU and are an exception to our course's usual prohibition on warp-breaking `if`s.
    
If done correctly, this should result in a fixed number of GPU invocations per frame ($10$ in my reference implementation) with much better runtime efficiency.
It should also create perfectly-circular, perfectly-smooth spheres with no polygonal approximation.

## Collision detection

Another major source of inefficiency is collision detection.
Most implementations of [the Spheres MP](spheres.html) detects collisions by checking every pair of spheres every frame, for a $O(n^2)$ runtime.
We need to do much better to scale up to thousands of spheres.

Because our spheres are relatively similar in size and spread out so as not to overlap,
we achieve $O(n)$ instead using the following method:

1. Divide the simulation space into a grid of cells, where cell dimension ≥ largest sphere diameter
2. Put a pointer to each sphere in the cell where its center lies
3. Check for collisions with sphere $s$ with the spheres in the same cell as $s$ and in all neighboring cells

There are other tricks that can make this even faster, but it provides a significant asymptotic speedup as-is.

If done correctly, doubling the number of spheres should halve the frames per second.

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should show perfectly circular spheres moving within an invisible cube and colliding with one another.
Frames per second should scale linearly with number of spheres
and be able to render 1000 spheres at reasonable speed.
One example motion might be the following:

<figure>
<video controls autoplay loop>
<source src="vid/many-spheres.webm" type="video/webm"/>
<source src="vid/many-spheres.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result, on a machine with a fairly fast CPU and an 88Hz refresh rate; on a slower computer it would have a lower FPS.
Note that the frame rate for 2000 spheres is about half that for 1000 spheres.
</figcaption>
</figure>
