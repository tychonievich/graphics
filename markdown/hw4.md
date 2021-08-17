---
title: 'HW4: Animation'
...

# Overview

This assignment will have you render animations
as a series of images,
using the `pngs` command from [HW0](hw0.html).

If you didn't figure out how to display animations during HW0,
you should definitely do that now.

Most animator-specified computer animations are the combination of two components:
a scene graph and time-varying parameters.

<!--
While it may not seem obvious that this would be true at first,
most animation tools I've used are a fancy user interface over
a scene graph like the one described above
where the coordinates of the positions and orientations are time-varying numerical values.
Often there is a tool called something like a "graph editor" that will display this underlying representation to the animator and let them edit it directly.
-->

## Scene Graph

In this assignment we'll replicate a version of the scene graph used in many animation tools.

Each *object* will have

- a *parent*, which is either another object or "the world"
- an *origin*, which is a 3-vector defaulting to $(0,0,0)$ (not in the required part of the assignment)
- a *scale*, which is a 3-vector defaulting to $(1,1,1)$  (not in the required part of the assignment)
- a *position*, which is a 3-vector defaulting to $(0,0,0)$ 
- an *orientation*, which will be given either in Euler or Quaternion form defaulting to $\langle 1;0,0,0 \rangle$ 
- geometry, given as vertices and triangles similar to HW2

A matrix to position the vertices of an object can be created by multiplying several component matrices together:
$[\cdots] \quad T_O \; T_P \; R \; S \; T_O^{-1}$
where $T_O$ is a translation matrix moving (0,0,0) to the object's origin;
$T_P$ is a translation matrix moving (0,0,0) to the object's position;
$S$ is a scaling matrix, the diagonal of the object's scale;
$R$ is a rotation matrix defined by the object's orientation;
and $[\cdots]$ is the matrix for the object's parent, or nothing if the parent is the world.

Matrices are not necessary in this case:
you can also apply the operations directly as
$q \odot ((p - O) \otimes S) \odot q^{*} + P + O$
where $\otimes$ is element-wise multiplication,
$q$ is the normalized orientation quaternion,
$q^{*}$ is the conjugate of $q$,
and $\odot$ is the quaternion multiplication operator.
If there are more than a few points, though, constructing the matrix first is more efficient.

:::aside
The quaternion $w + x \mathbf{i} + y \mathbf{j} + z \mathbf{k}$
is written in graphics as just $\langle w;x,y,z \rangle$.
Other notations are also common.

The conjugate of $\langle w;x,y,z \rangle$ is $\langle w;-x,-y,-z \rangle$.

The product $\langle w_1;x_1,y_1,z_1 \rangle \odot \langle w_2;x_2,y_2,z_2 \rangle$
is $$\begin{matrix}
\langle w_1w_2 - x_1x_2 - y_1y_2 - z_1z_2;\\
w_1x_2 + x_1w_2 + y_1z_2 - z_1y_2,\\
w_1y_2 + y_1w_2 + z_1x_2 - x_1z_2,\\
w_1z_2 + z_1w_2 + x_1y_2 - y_1x_2 \rangle
\end{matrix}$$
Notice: the terms above are such that the $x$ coordinate multiplies $x$ and $w$ in both directions
and multiplies the other two coordinates in both directions but puts a negative sign on the one that's out-of-order (xy, yz, and zx are in-order in a wrapping alphabet).

The magnitude of a quaternion $q$ is $q^{*} q = w^2 - (x^2+y^2+z^2)$.
The magnitude is always a scalar (zero $x,y,z$).
A normalized quaternion is one with a magnitude of $1$.

To multiply a point $(x,y,z)$ by a quaternion, treat the point as $\langle 0;x,y,z \rangle$
and use the quaternion product.
Note that this will give a quaternion (non-zero $w$), not a point (zero $w$).
However, $q \odot x \odot q^{*}$ will always be a point if $x$ is a point.

The 3×3 rotation matrix of normalized quaternion $\langle w;x,y,z \rangle$
is $$\begin{bmatrix}
w^2+x^2-y^2-z^2 & 2(xy-zw) & 2(xz+yw) \\
2(xy+zw) & w^2-x^2+y^2-z^2 & 2(yz-xw) \\
2(xz-yw) & 2(yz+xw) & w^2-x^2-y^2+z^2 \\
\end{bmatrix}$$
Notice: the diagonal has positive $w$ and the coordinate of that row;
the off-diagonal have a positive product of the coordinates of the row and column
and a sign-varying product of $w$ and the third coordinate
where the above-diagonal signs are negative if the two-coordinate product is in-order
and the off-diagonal is skew-symmetric.

If we don't wish to normalize the quaternion, we can use the following three equations to get the same rotation matrix:
$$n = w^2 + x^2 + y^2 + z^2$$
$$s = \begin{cases}0 & \text{if} n=0\\\frac{2}{n} &\text{otherwise}\end{cases}$$
$$\begin{bmatrix}
1-s(y^2+z^2) & s(xy-zw) & s(xz+yw) \\
s(xy+zw) & 1-s(x^2+z^2) & 2(yz-xw) \\
s(xz-yw) & s(yz+xw) & 1-s(x^2+y^2) \\
\end{bmatrix}$$
:::

The *camera* is a special object with no geometry.
To position an object's points for rendering by the camera,
use $C^{-1}\, O$ where $C$ is the matrix (constructed as described above) for the camera
and $O$ is the matrix (constructed as described above) for the object.
Recall that:

- For any two matrices $A$ and $B$, $(AB)^{-1} = B^{-1} A^{-1}$
- The inverse of a translation by $(x,y,z)$ is a translation by $(-x,-y,-z)$
- The inverse of a scaling by $(x,y,z)$ is a translation by $(1/x, 1/y, 1/z)$
- The inverse of a rotation matrix $R$ is the transpose of that matrix $R^{-1} = R^{T}$
- The inverse of a rotation quaterion $q$ is its conjugate $q^{*}$

You can compute the inverse of a transformation matrix more accurately using the above rules than you can using a generic matrix inversion routine.

 

All this organization may seem like more bother than its worth, but scene graphs make complicated and interesting animation much easier to create.

## Time-varying parameters

We'll add animation by allowing various numbers, such as the coordinates of an object's position vector, to be defined by a time-varying variable.

Every file will have access to two variables:
`f`, which is equal to the current frame number,
and `l`, which is the last frame number of the animation.

:::example
If the *frames* argument of the `pngs` command is `30`,
`f` will range from 0 on the first frame to 29 on the last frame
and `l` will be 29 for all frames.
:::

You'll implement several ways of defining additional variables.
To avoid the complexities of a full programming language, we'll guarantee that regardless of which variable definition forms you define

- each variable will be defined only once; no `x = x + 1`-type reassignments;
- each variable will be defined before it is used; and
- variable definitions will be individually simple to parse: no parentheses or the like.

The above limitations will make *writing* the input files a bit tedious, but will keep *parsing* them straightforward.

Some full animation systems will animate vectors separately from their coordinates, for example using slurps (spherical linear interpolation) or hlerps (hyperbolic linear interpolation).
Those can be decomposed into per-coordinate trigonometry and other more involved functions, and to keep the input files from getting out of hand we'll only deal with them in that form.

## Code organization

Start with a copy of (at least the required parts of) your HW2 code.

HW2's `trif` and related commands indexed a single global list of points.
For HW4 the indices will reset each time an `object` command is given;
thus `trif 1 2 -1` is a triangle connecting the first two points *of the most recent object* with the last point provided.

You won't need `loadm` directly; the modelview matrix will be given by the object transformations isntead. We will use `loadp` exactly as HW2 did.

You will almost certainly need two maps:
one mapping variable names to their definitions
and one mapping object names to their corresponding objects.

The file will be organized so that what you store can be quite simple
if you are willing to re-read the file once per frame.
Because variables are defined before use, re-reading will allow you to store just the variable values at that frame rather than full defining expressions.
Because each object's position, orientation, scale, and parent are defined before its geometry
and because parent objects are defined before child objects,
it is possible implement the required functionalty
storing only the transformation matrix for each object,
rendering the geometry immediately instead of storing it.

That said, using more involved data structures and code organization
may make your code easier to reason about
and may be necessary to implement some of the optional components.

# Required Features

The required part is worth 50%

## Drawing objects

pngs *width* *height* *filename* *frames*
:	same syntax and semantics as HW0.

object *name* *parent*
:	<a href="files/.txt"><img class="demo floater zoom" src="files/.png"/></a>
	Begin a new object with the given *name*.
    The *name* may be used to indicate this object as the *parent* of later objects.
    The special name "`world`" may appear in the *parent* field to indicate the object has no parent.
    
    You may assume that the *name* is unique in the file, ASCII, and not "`world`";
    and that *parent* is either "`world`" or the name of an object that appeared previously in this file.
    
    Every `object` line will be followed by its transformations (if any)
    and then its geometry.

position $x$ $y$ $z$
:   An optional transformation of the object; if missing, defaults of `position 0 0 0`.
    
    Describes the position of this object relative to its parent, in a coordinate system modified by its parent's position, orientation, and scale
    but not modified by this objects orientation or scale.
    
    Each object will have at most one `position`.
    If present, it will precede any geometry for that object.

quaternion *w* *x* *y* *z*
:   An optional orientation transformation of the object; if missing and no other orientation command is provided, defaults to `quaternion 1 0 0 0`.
    
    Describes the orientation of this object relative to its parent, in a coordinate system modified by its parent's position, orientation, and scale
    but not modified by this objects position or scale.
    
    Each object will have at most one orientation,
    which may be `quaternion` or one of the alternatives given in the optional features section.
    If present, it will precede any geometry for that object.

xyz $x$ $y$ $z$
:	As in HW2.
    Note that point indexing resets with each new object.

trif $i_1$ $i_2$ $i_3$
:	As in HW2.
    Note that point indexing resets with each new object.

loadp $a_{1,1}$ $a_{1,2}$ $a_{1,3}$ $a_{1,4}$ $a_{2,1}$ $a_{2,2}$ ... $a_{4,4}$
:   As in HW2.

color $r$ $g$ $b$
:	As in HW2.

## Basic animation

add `dest` $a$ $b$
:   Create a new variable called `dest` that is equal to $a + b$

sub `dest` $a$ $b$
:   Create a new variable called `dest` that is equal to $a - b$

mul `dest` $a$ $b$
:   Create a new variable called `dest` that is equal to $a \times b$

div `dest` $a$ $b$
:   Create a new variable called `dest` that is equal to $a \div b$

pow `dest` $a$ $b$
:   Create a new variable called `dest` that is equal to $a^b$

sin `dest` $a$
:   Create a new variable called `dest` that is equal to $sin(a)$

cos `dest` $a$
:   Create a new variable called `dest` that is equal to $cos(a)$

Animate transforms
:   <a href="files/.txt"><img class="demo floater zoom" src="files/.png"/></a>
    Allow the arguments of `position` and `quaternion`, as well as the mathematics operators above, to be any mix of variables and numbers.

<hr style="clear:both"/>

# Optional Features

origin $o_x$ $o_y$ $o_z$ (5 pt)
:   An optional origin of the object; if missing defaults to `origin 0 0 0`.
    
    Describes the origin around which other transforms occur.

    Each object will have at most one `origin`; if present, it will precede any geometry for that object.

scale $s_x$ $s_y$ $s_z$ (10 pt)
:   An optional transformation of the object; if missing defaults to `scale 1 1 1`.
    
    Describes the axis-aligned components of the scale of this object relative to its parent, in a coordinate system modified by its parent's position, orientation, and scale
    but not modified by this objects position or orientation.
    
    Each object will have at most one `scale`; if present, it will precede any geometry for that object.

anyscale $s_x$ $s_y$ $s_z$ $w$ $x$ $y$ $z$ (10 pt)
:   An optional transformation of the object.
    
    Describes the scale of this object along arbitrary axes as given by a quaternion.
    The application of `anyscale` is equivalent to rotating by the quaternion,
    scaling along the principle axes by the given factors,
    and then rotating back.
    
    Each object will have one `scale` or one `anyscale` or neither; if either is present, it will precede any geometry for that object.


Animate vertices
:   ...

Animate colors
:   ...

Animate textures
:   ...

Animate projection
:   ...

lerp `dest` $t_1$ $v_1$ $t_2$ $v_2$ ...
:   ...

bez `dest` $t_1$ $a_1$ $b_1$ $c_1$ $t_2$ $a_2$ $b_2$ $c_2$ ... $c_n$ $a_{n+1}$
:   ...

autobez `dest` $t_1$ $v_1$ $t_2$ $v_2$ ...
:   ...

natspline `dest` $t_1$ $v_1$ $t_2$ $v_2$ ...
:   ...

piecewise `dest` $v_1$ $t_1$ $v_2$ $t_2$ \dots $t_n$ $v_{n+1}$
:   

Camera
:   ...

Camera with parent
:   ...

iflt $x$ $y$\
else\
fi
:   If $x < y$, perform the commands between `iflt` and the next `else` but not between the `else` and the next `fi`.
    Otherwise, perform the commands between `else` and `fi`, not between `iflt` and `else`.



<!--

lerp var t val t val t val ...
    (t,val) pairs
    between pairs, linear interpolation
    before first pair, first val
    after last pair, last val

pbez var t val val val t val val val t val val val ... val
    (t1, v1, v2, v3, t2, v4) means a bezier function with CPs
    - t1,v1
    - (2*t1/3+t2/3),v2
    - (t1/3+2*t2/3),v3
    - t2,v4
    
autobez var t val t val t val ...
    same format as lerp
    interpolating cubic bezier spline
    *slope* at point t = (net t's val - previous t's val) / (next t - prev t)
     
sum var s1 s2
diff var pos neg
prod var p1 p2
ratio var num den
sin var arg
cos var arg
pow var base exp

-->


<!--
null objects
camera
animated camera
camera with objects as parents
animated vertices
animated color
animated texture coordinates
bangbang
natural spline
piecewise-equals
-->

<!--
object name parent 
origin x y z
position x y z
quat x y z w      -- or eulxyz eulyzx eulzyx ...
scale x y z
xyz ...
trig ...



-->
