---
title: 'HW5: Simulation'
notes:
    - bones
        - track to
            - principle axis via cross product
        - track point to
            - (track pt) (track goal) (track pt)^-1
        - track and scale to
        - track and stretch to
        - FABRIK
        - FABRIK with starter pose
    - fireworks
        - bounce walls
        - reburst
        - time-lapse dynamics
        - keyframe
    - boids
    - landscape
        - square-square
        - diamond-square
        - erosion
        - keyframe
    - tree
        - L-system
        - stochastic
        - pruned
        - light and gravity
    - rope
        - mass-spring
        - tri-diagonal
    - fluid
        - shallow water
        - stam
...

<blockquote style="background-color:#fbb; font-size:150%">This page is a work-in-progress and may change at any time without notice.</blockquote>


# Overview

For this assignment you get to pick a few classes of simulation to complete.
Unlike other assignments, you don't need to be able to mix-and-match commands:
the `gravity` command only needs to be supported for the simulations that include gravity, for example.

This assignment builds on the required parts of HW4.
All of the required HW4 commands, including `loadp`, `object`, `position`, `quaternion`, `cos`, and so on are used in this assignment exactly as they were in HW4.

Every file will have the keyword `simulation` prior to any other HW5-specific keyword.
There will always be one keyword after that, indicating which simulation type this file uses.


## `simulation bones`

You may find our [bones writeup](bones.html) helpful.

bone $d$
:	This may appear at most once in any `object`.
	If present, it means that this object is considered to be a bone,
	with object-space origin $(0,0,0)$ and object-space tip $(0,0,d)$.
	
	A bone may have geometry, but doesn't need to.
	A bone may have the `world`, another bone, or a non-bone as its parent.
	
	Unless explicitly stated otherwise, the remaining keywords in this section apply only to bones.

track $x$ $y$ $z$
:	Apply a rotation (after positioning) such the bone's tip points toward the point $(x,y,z)$.
	This should be a minimal rotation to achieve that goal, staying as close to the previous orientation (e.g. as given by a preceding `quaternion`) as possible.

trackroll $x$ $y$ $z$ *axis* $x_2$ $y_2$ $z_2$
:	Apply a rotation (after positioning) such the bone's tip points toward the point $(x,y,z)$.
	There are many such rotations; pick the one that cases *axis* to point as close to point $(x_2,y_2,z_2)$ as possible.
	The *axis* will always be two characters: first either `+` or `-`, then either `x` or `y`.

trackscale $x$ $y$ $z$
:	Like `track`, but also scale along the object's z axis to that the tip of the bone exactly reaches the point $(x,y,z)$. Do not scale along the object's other two axes.

trackstretch $x$ $y$ $z$
:	Like `trackscale`, but also scale uniformly along the object's x and y axes such that the volume of the bone is conserved.

fabrik $x$ $y$ $z$ *iterations*
:	Use FABRIK to perform inverse kinematics,
	where the IK chain consists of this bone and all its bone parents.
	Each frame should use the previous frame's results as its starting point.
	
	FABRIK produces the origins and tips of a chain of bones.
	Use the same math as `position` and `track` to align the bones with these points.
	Use the previous frame's results as each rotation's starting point.
	
## `simulation fireworks`

burst *type* $n$ $x$ $y$ $z$ $t$ $v$
:	At frame $t$, create a burst of $n$ moving particles of the given *type* centered at $(x,y,z)$ with burst velocity $v$.
	The types are:
	
	normal
	:	Select velocities from a 3D normal distribution with standard deviation $v$
	
	sphere
	:	Select velocities uniformly from a radius-$v$ sphere

	shell
	:	Select velocities uniformly from the surface of a radius-$v$ sphere

	Every `burst` command will be followed by a shape command
	
billboard $w$
:	A shape command: draw each particle from the preceding `burst` as a $w$-by-$w$ square
	that is aligned to point to the camera.
	And orientation other than that (side up, point up, etc) is up to you.

dart $w$
:	A shape command: draw each particle from the preceding `burst` as an equilateral triangle with edge length $w$
	aligned with a face toward the camera
	and a point in the direction of its motion.

box $w$
:	A shape command: draw each particle from the preceding `burst` as a global axis-aligned cube with $w$-length edges.

gravity $x$ $y$ $z$
:	Accelerate moving particles by $x$ units-per-frame in the x axis, $y$ units-per-frame in the y axis, and $z$ units-per-frame in the $z$ axis

drag $d$
:	Decelerate moving particles by $dv$ where $v$ is the participles current units-per-frame velocity.
	You may assume $0 \le d \le 1$;
	if $d = 1$ then particles will instantly stop; if $d = 0$ then there is no drag.

wall *bounciness* $A$ $B$ $C$ $D$
:	An infinite plane that particles cannot penetrate;
	enforce that $Ax + By + Cz + D \ge 0$ for all particles.
	If *bounciness* is 0, remove all velocity into the plane.
	If *bounciness* is 1, reverse any velocity into the plane.
	For intermediate *bounciness*, reverse velocity into the plane and reduce its magnitude.

reburst *type* *chance* $n$ $t$ $v$
:	$t$ frames after the start of the preceding `burst`,
	each particle created by that `burst` is destroyed.
	For each such particle, there is a *chance* percent chance that it becomes the center of a new `burst` of the given *type*, $n$, and $v$
	and a (100 − *chance*) percent chance that it instead simply vanishes.

	
## `simulation boids`

## `simulation landscape`

## `simulation trees`

## `simulation springs`

## `simulation fluid`

<!--

# Required Features

The required part is worth 50%

input *filename*
:	load the given RGBA png file as the current image.

output *filename*
:	save the current image as the given RGBA png file.

monochrome *channel*
:	<span class="floater"><a href="files/hw5monochromeL.png"><img class="demo2 zoom" src="files/hw5monochromeL.png"/></a><br/><a href="files/hw5monochromeL.txt">hw5monochromeL.txt</a></span>
	<span class="floater"><a href="files/hw5monochromeS.png"><img class="demo2 zoom" src="files/hw5monochromeS.png"/></a><br/><a href="files/hw5monochromeS.txt">hw5monochromeS.txt</a></span>
	<span class="floater"><a href="files/hw5monochromeH.png"><img class="demo2 zoom" src="files/hw5monochromeH.png"/></a><br/><a href="files/hw5monochromeH.txt">hw5monochromeH.txt</a></span>
	Replace the red, green, and blue channels of the current image with a copy of the given channel.
	Set every alpha value to 1.
	
	You may assume that *channel* is one of the following eight strings: `red`, `green`, `blue`, `alpha`, `hue`, `saturation`, `value`, `lightness`.
	
	This operator can typically be done in-place, though it also works if you copy the image.

equalize *channel*
:	<span class="floater"><a href="files/hw5equalize.png"><img class="demo2 zoom" src="files/hw5equalize.png"/></a><br/><a href="files/hw5equalize.txt">hw5equalize.txt</a></span>
	Find the minimum and maximum value of the specified channel in the image.
	Then replace every pixels' entry in that channel with $channel\_value - minumum \over maximum - minimum$.

	You may assume that *channel* is one of the following three strings: `red`, `green`, `blue`.
	
	This operator can typically be done in-place, though it also works if you copy the image.

gradient
:	<span class="floater"><a href="files/hw5gradient.png"><img class="demo2 zoom" src="files/hw5gradient.png"/></a><br/><a href="files/hw5gradient.txt">hw5gradient.txt</a></span>
	The Scharr 3-by-3 convolution filter
	$\displaystyle \frac{1}{16}\begin{bmatrix}+3&+10&+3\\0&0&0\\-3&-10&-3\end{bmatrix}$
	will find the $y$-gradient of the image; its rotated version
	$\displaystyle \frac{1}{16}\begin{bmatrix}-3&0&+3\\-10&0&+10\\-3&0&+3\end{bmatrix}$
	will find the $x$-gradient.
	You'll need those gradients for many of the optional parts.
	
	For the required part, 
	set the green channel of the image to the $y$-gradient of the lightness channel
	and both the blue and red channels to the $x$-gradient of the lightness channel.
	
	This operator can typically cannot be done in-place; you'll need to make a copy of the image first.


<hr style="clear:both"/>

# Optional Features


## Pixel-based

All Channels (20%)
:	<span class="floater"><a href="files/hw5equalizeL.png"><img class="demo2 zoom" src="files/hw5equalizeL.png"/></a><br/><a href="files/hw5equalizeL.txt">hw5equalizeL.txt</a></span>
	<span class="floater"><a href="files/hw5equalizeH.png"><img class="demo2 zoom" src="files/hw5equalizeH.png"/></a><br/><a href="files/hw5equalizeH.txt">hw5equalizeH.txt</a></span>
	Extend all operations to work on any of the eight channels.
	
	When setting Hue, Saturation, or Value, assume that the other two of those are held constant.
	When setting Lightness, scale R, G, and B by new lightness &div; old lightness.
	
	Black is a special case for almost all of these; you are welcome to handle initially-black pixels however you wish.

posterize *channel* $n$ (10%)
:	<span class="floater"><a href="files/hw5posterize.png"><img class="demo2 zoom" src="files/hw5posterize.png"/></a><br/><a href="files/hw5posterize.txt">hw5posterize.txt</a></span>
	Clamp the given channel to just $n$ distinct values, $i \over n - 1$ for $i \in \{0, 1, 2, \dots, n-1\}$.
	Move every pixel's value in the given channel to the nearest of those values.
	
	You may assume that $n \ge 2$ and that *channel* is one of the following four strings: `red`, `green`, `blue`, `alpha`.

dither *channel* $n$ (10%; requires `posterize`)
:	<span class="floater"><a href="files/hw5dither.png"><img class="demo2 zoom" src="files/hw5dither.png"/></a><br/><a href="files/hw5dither.txt">hw5dither.txt</a></span>
	Clamp the given channel to just $n$ distinct values, $i \over n - 1$ for $i \in \{0, 1, 2, \dots, n-1\}$.
	For any pixel whose value is between two of the output values, pick one of the two nearest values randomly
	with probability proportional to the nearness to each.
	
	You may make the same assumptions about $N$ and *channel* as you did for `posterize`.

rehue $d_H$ (15%)
:	<span class="floater"><a href="files/hw5rehue.png"><img class="demo2 zoom" src="files/hw5rehue.png"/></a><br/><a href="files/hw5rehue.txt">hw5rehue.txt</a></span>
	Replace every color's old hue $H$ with $H+d_H$, wrapping back into the 0--1 range after the addition.

<hr style="clear:both"/>

## Convolution-based

convolve *channel* $w$ $h$ $n_1$ $n_2$ ... $n_{wh}$ (20%)
:	<span class="floater"><a href="files/hw5convolve.png"><img class="demo2 zoom" src="files/hw5convolve.png"/></a><br/><a href="files/hw5convolve.txt">hw5convolve.txt</a></span>
	Apply the specified convolution filter to the given channel of the current image.
	You may assume that $w$ and $h$ are both odd numbers
	and that the *channel* is one of `red`, `green`, `blue`, or `alpha`.
	The result of the convolution should become the new current image.

blur *channel* $n$ (10%)
:	<span class="floater"><a href="files/hw5blur.png"><img class="demo2 zoom" src="files/hw5blur.png"/></a><br/><a href="files/hw5blur.txt">hw5blur.txt</a></span>
	Convolve the given *channel* in x and in y by a discrete approximation of a Guassian filter with $n$ entries.
	The entries should be normalized binomial coefficients (i.e., the $n$^th^ row of [Pascal's triangle](https://en.wikipedia.org/wiki/Pascal%27s_triangle)
	divided by $2^{n-1}$);
	for example, $n=7$ will give the filter $\frac{1}{64}\begin{bmatrix}1&6&15&20&15&6&1\end{bmatrix}$.
	
	You may assume that $n$ is a positive odd integer and that *channel* is one of the following four strings: `red`, `green`, `blue`, `alpha`.

sharpen *channel* $a$ (10%)
:	<span class="floater"><a href="files/hw5sharpen.png"><img class="demo2 zoom" src="files/hw5sharpen.png"/></a><br/><a href="files/hw5sharpen.txt">hw5sharpen.txt</a></span>
	Sharpen the given *channel* of the image by convolving it with the matrix
	$$\begin{bmatrix}-0.1a&-0.15a&-0.1a\\-0.15a&1+a&-0.15a\\-0.1a&-0.15a&-0.1a\end{bmatrix}$$

	You may assume that *channel* is one of the following three strings: `red`, `green`, `blue`.

edges $min$ $max$ (15%)
:	<span class="floater"><a href="files/hw5edges.png"><img class="demo2 zoom" src="files/hw5edges.png"/></a><br/><a href="files/hw5edges.txt">hw5edges.txt</a></span>
	Compute the $x$ and $y$ gradients of the image in all R, G, and B
	and combine those six values using Euclidean distance (i.e., $\sqrt{G_{r,x}^2 + G_{r,y}^2 + G_{g,x}^2+\dots}$).
	Scale the resulting value so that $min$ becomes 0 and $max$ becomes 1.
	Use $1 -$ that result to set the R, G, and B values of the current image; set A to 1.

<hr style="clear:both"/>

## Non-local

flood $x$ $y$ $\Delta$ $r$ $g$ $b$ $a$ (10%)
:	<span class="floater"><a href="files/hw5flood.png"><img class="demo2 zoom" src="files/hw5flood.png"/></a><br/><a href="files/hw5flood.txt">hw5flood.txt</a></span>
	Flood fill the image, starting with the pixel at coordinate $x$, $y$,
	with the color $(r, g, b, a)$.
	Fill any pixel that is four-connected to another filled pixel and is within $\Delta$ (which will be between 0 and 1) of the original pixel at coordinate $x$, $y$ in all four of the RGBA channels.
	
	You may assume the initial color at $(x,y) \ne (r,g,b,a)$ 

carve narrow *and* carve short (30%)
:	<span class="floater"><a href="files/hw5carve.png"><img class="demo2 zoom" src="files/hw5carve.png"/></a><br/><a href="files/hw5carve.txt">hw5carve.txt</a></span>
	Use [seam carving](https://www.cs.virginia.edu/tychonievich/4810/F2016/notes.php?date=20161103) to make the image one pixel `narrow`er in width or `short`er in height.
	Use gradient magnitude as a proxy for visual interest.
	In case of a tie (two or more seams of equally low total interest), pick one arbitrarily.
	
	To find the gradient magnitude,
	compute the $x$ and $y$ gradients of the image in all R, G, and B
	and combine those six values using Euclidean distance (i.e., $\sqrt{G_{r,x}^2 + G_{r,y}^2 + G_{g,x}^2+\dots}$).
	
path $x_1$ $y_1$ $x_2$ $y_2$ $r$ $g$ $b$ (30%)
:	<span class="floater"><a href="files/hw5path.png"><img class="demo2 zoom" src="files/hw5path.png"/></a><br/><a href="files/hw5path.txt">hw5path.txt</a></span>
	Use a shortest-path algorithm to connect the two input pixels $(x_1, y_1)$ and $(x_2, y_2)$.
	Fill the input pixels, and all pixels on the path between them, with the color $(r, g, b, 1)$.
	
	Each pixel has eight neighbors.
	The "distance" to a neighbor is Euclidean distance (1 for 4-connect neighbors, $\sqrt{2}$ for diagonal neighbors)
	times the "flatness" of the neighbor being entered (there are various ways to compute that; we'll use $1 \over \mathrm{gradient\;magnitude} + 0.1$).

	To find the gradient magnitude,
	compute the $x$ and $y$ gradients of the image in all R, G, and B
	and combine those six values using Euclidean distance (i.e., $\sqrt{G_{r,x}^2 + G_{r,y}^2 + G_{g,x}^2 + \dots}$).

advect *chan* $d$ (20%)
:	<span class="floater"><a href="files/hw5advect.png"><img class="demo2 zoom" src="files/hw5advect.png"/></a><br/><a href="files/hw5advect.txt">hw5advect.txt</a></span>
	Use back-advection to move colors around the image.
	The new color of pixel $(x, y)$ should be computed 
	as the color of the image at $(x + g_x d, y + g_y d)$
	where $(g_x, g_y)$ is the gradient of the *chan* channel of the image at $(x, y)$.
	
	When sampling a pixel at location $(x,y)$ with non-integer coordinates, 
	use a weighted average of the pixels at 
	$(\lfloor x\rfloor, \lfloor y\rfloor)$,
	$(\lceil x\rceil, \lfloor y\rfloor)$,
	$(\lfloor x\rfloor, \lceil y\rceil)$, and
	$(\lceil x\rceil, \lceil y\rceil)$.
	
<hr style="clear:both"/>
-->
