---
title: Homogeneous Vectors and Transformations
summary: Including definitions, terminology, and common operations.
...

# Homogeneous vectors

Homogeneous vectors look like [regular vectors](math1.html), and in most ways behave like them, but they differ in two key ways:

1. They have an extra coordinate, such that a 3D vector has 4 numbers. The extra coordinate is called the $w$ coordinate.
2. We define $a\vec x = \vec x$ for all real-number $a$ and homogeneous vector $\vec x$.

When we need to distinguish between homogeneous and other vectors, we call the non-homogeneous vectors "Cartesian vectors" after René Descartes who popularized them.
August Möbius invented homogeneous vectors, but I have never heard anyone call them "Möbisian vectors".

In graphics, we almost always deal with homogeneous vectors where $w$ is either $1$ or $0$.
If $w=1$, then the homogeneous vector represents a point in space.
If $w=0$, then the homogeneous vector represents a direction or offset.

Confusingly, we use the word "normalize" to mean any of

- Given a homogeneous vector $\vec x$ with $x_w \ne 0$, replace $\vec x$ with $\dfrac{\vec x}{x_w}$

- Given a homogeneous vector $\vec x$ with $x_w = 0$, replace $\vec x$ with $\dfrac{\vec x}{\|\vec x\|}$

- Given a Cartesian vector $\vec x$, replace $\vec x$ with $\dfrac{\vec x}{\|\vec x\|}$

Confusingly, we use the word "length" to mean any of

- The number of dimensions in a Cartesian vector
- The number of values in a Homogeneous vector (1 + the number of dimensions in a Cartesian vector)
- Given a Cartesian vector $\vec x$, $\|\vec x\| = \sqrt{\vec x \cdot \vec x}$
- Given a homogeneous vector $\vec x$ with $x_w = 0$, $\|\vec x\| = \sqrt{\vec x \cdot \vec x}$
- Given a homogeneous vector $\vec x$ with $x_w = 1$, $\|\vec x\| = \sqrt{\vec x \cdot \vec x - 1}$


# 3D transformations

Consider a 3D object defined as a set of homogeneous points, including $\vec p$;
and a set of homogeneous surface normals -- that is, directions that are normal to (perpendicular to) the surface at a given point, including $\vec n$.
By definition of points, $p_w = 1$; by the definition of directions, $n_w = 0$.

## Translation

We can move the object to a new location by multiplying every point and surface normal by a translation matrix.
By construction, the translation matrix will have no impact on the surface normals.

To move by $\Delta x$ along the $x$ axis,
$\Delta y$ along the $y$ axis, and
$\Delta z$ along the $z$ axis,
we use
$\begin{bmatrix}1&0&0&\Delta x \\ 0&1&0&\Delta y \\ 0&0&1&\Delta z \\ 0&0&0&1\end{bmatrix}
\vec p$

<details class="example"><summary>JavaScript code to create this matrix</summary>
```js
const m4trans = (dx,dy,dz) => new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, dx,dy,dz,1])
```
</details>

This matrix has the same effect as adding $(\Delta x, \Delta y, \Delta z, 0)$ to every point and doing nothing to the surface normals.
However, because it is a matrix we can combine it with other transformations.

If $T$ is a translation matrix, $T^{-1}$ is found by replacing each value $v$ on the first three rows of the last column with $-v$.

$$
\begin{bmatrix}1&0&0&\Delta x \\ 0&1&0&\Delta y \\ 0&0&1&\Delta z \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}1&0&0&-\Delta x \\ 0&1&0&-\Delta y \\ 0&0&1&-\Delta z \\ 0&0&0&1\end{bmatrix}
=
\begin{bmatrix}1&0&0&0 \\ 0&1&0&0 \\ 0&0&1&0 \\ 0&0&0&1\end{bmatrix}
$$

Surface normals (and other offsets and directions) should not change when an object is translated.
This is handled automatically if the surface normal has $w=0$:

$$
\begin{bmatrix}n_x \\ n_y \\ n_z \\ 0\end{bmatrix}
=
\begin{bmatrix}1&0&0&\Delta x \\ 0&1&0&\Delta y \\ 0&0&1&\Delta z \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}n_x \\ n_y \\ n_z \\ 0\end{bmatrix}
$$


## Rotation

We can rotate the object about the origin by multiplying every point and surface normal by a rotation matrix.

To rotate $\theta$ degrees about the $x$ axis, we use 
$\begin{bmatrix}1&0&0&0 \\ 0&\cos(\theta)&-\sin(\theta)&0 \\ 0&\sin(\theta)&\cos(\theta)&0 \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}\vec p & \vec n \end{bmatrix}$

To rotate $\theta$ degrees about the $y$ axis, we use 
$\begin{bmatrix}\cos(\theta)&0&\sin(\theta)&0 \\ 0&1&0&0 \\ -\sin(\theta)&0&\cos(\theta)&0 \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}\vec p & \vec n \end{bmatrix}$

To rotate $\theta$ degrees about the $z$ axis, we use 
$\begin{bmatrix}\cos(\theta)&-\sin(\theta)&0&0 \\ \sin(\theta)&\cos(\theta)&0&0 \\ 0&0&1&0 \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}\vec p & \vec n \end{bmatrix}$

If $R$ is a matrix representing a rotation about the origin, $R^{-1} = R^{T}$.

$$
\begin{bmatrix}1&0&0&0 \\ 0&\cos(\theta)&-\sin(\theta)&0 \\ 0&\sin(\theta)&\cos(\theta)&0 \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}1&0&0&0 \\ 0&\cos(\theta)&\sin(\theta)&0 \\ 0&-\sin(\theta)&\cos(\theta)&0 \\ 0&0&0&1\end{bmatrix}
=
\begin{bmatrix}1&0&0&0 \\ 0&1&0&0 \\ 0&0&1&0 \\ 0&0&0&1\end{bmatrix}
$$

We also have guides to some fancier rotations:

<details class="example"><summary>Rotate $\theta$ around axis $\vec r$</summary>

1. Normalize $\vec r$ and set $c = \cos(\theta)$ and $s = \sin(\theta)$.
2. The matrix is
    $$\begin{bmatrix}
    r_x^2(1-c)+c & r_x r_y (1-c) - r_z s & r_x r_z (1-c) + r_y s  \\
    r_x r_y (1-c) + r_z s & r_y^2(1-c)+c  & r_y r_z (1-c) - r_x s  \\
    r_x r_z (1-c) - r_y s & r_y r_z (1-c) + r_x s & r_z^2(1-c)+c \\
    \end{bmatrix}$$

</details>

<details class="example"><summary>Rotate as little as possible to have rotated $\vec a$ line up with $\vec b$</summary>

1. Normalize $\vec a$ and $\vec b$.
2. Let $\vec r = \vec a \times \vec b$ and $s = \|\vec r\|$.
3. Let $c = \vec a \cdot \vec b$.
4. Use that $\vec r / s$, $c$, and $s$ in the "rotate around axis $\vec r$" formula.

</details>

<details class="example"><summary>Rotate so that one axis now points towards $\vec p$ and another points as close to $\vec q$ as possible</summary>

1. Set the column of the matrix that corresponds to the axis that should point toward $\vec p$ be a normalized version of $\vec p$.
2. Set the column of the matrix that shouldn't point towards either of the points be a normalized version of $\vec p \times \vec q$.
3. Set the remaining column to be the cross product of the other two.
4. Negate an axis's column if the negative instead of positive axis should point toward a point.
5. Negate the unconstrained column if $(\vec x \times \vec y) \cdot \vec z < 0$.

</details>

<details class="example"><summary>Rotate so $\vec p$ lies on one axis and $\vec q$ as close to another axis as possible</summary>

This is the inverse (which for rotations is simply the transpose) of the rotation that points the axes towards $\vec p$ and $\vec q$.

</details>

<details class="example"><summary>Rotate a "forward" vector to lie along the $-z$ axis and an "up" vector to lie as close to the $+y$ axis as the "forward" allows</summary>

This is special case of the previous item, but one often wanted as part of the "view" matrix.

1. Let $\vec f$ be a normalized version of the "forward" vector
2. Let $\vec r$ be a normalized version of "forward" × "up"
3. Let $\vec u = \vec r \times \vec f$
4. The matrix is
    $$\begin{bmatrix}
    r_x&r_y&r_z&0\\
    u_x&u_y&u_z&0\\
    -f_x&-f_y&-f_z&0\\
    0&0&0&1\\
    \end{bmatrix}$$

In many cases, this is specified by an "eye" location and a "center" location,
where "forward" = "center" &minus; "eye",
and followed by a [translate of "&minus;eye"](#translation),
then a [perspective projection with the $\pm$ being $-$, not $+$](#division).

</details>

<details class="example"><summary>JavaScript code to create some of these matrices</summary>
```js
const m4rotX = (ang) => { // around x axis
  let c = Math.cos(ang), s = Math.sin(ang);
  return new Float32Array([1,0,0,0, 0,c,s,0, 0,-s,c,0, 0,0,0,1]);
}
const m4rotY = (ang) => { // around y axis
  let c = Math.cos(ang), s = Math.sin(ang);
  return new Float32Array([c,0,-s,0, 0,1,0,0, s,0,c,0, 0,0,0,1]);
}
const m4rotZ = (ang) => { // around z axis
  let c = Math.cos(ang), s = Math.sin(ang);
  return new Float32Array([c,s,0,0, -s,c,0,0, 0,0,1,0, 0,0,0,1]);
}
const m4fixAxes = (f, up) => { // f to -z, up to near +y
  f = normalize(f)
  let r = normalize(cross(f,up))
  let u = cross(r,f)
  return new Float32Array([
    r[0],u[0],-f[0],0,
    r[1],u[1],-f[1],0,
    r[2],u[2],-f[2],0,
    0,0,0,1
  ])
}
```
</details>


See also the [page on skeletal animation](bones.html).

## Scaling

We can scale the object about the origin along principle axes by multiplying every point and surface normal by a scaling matrix.

To scale by $s_x$ in the $x$ axis,
$s_y$ in the $y$ axis,
and $s_z$ in the $z$ axis,
we use 
$\begin{bmatrix}s_x&0&0 \\ 0&s_y&0&0\\ 0&0&s_z&0 \\ 0&0&0&1\end{bmatrix}
\vec p$

<details class="example"><summary>JavaScript code to create this matrix</summary>
```js
const m4scale = (sx,sy,sz) => new Float32Array([sx,0,0,0, 0,sy,0,0, 0,0,sz,0, 0,0,0,1])
```
</details>


If $S$ is a matrix representing a scaling along the principle axes, $S^{-1}$ is found by replacing each value $v$ on the main diagonal with $1 / v$.

$$
\begin{bmatrix}s_x&0&0 \\ 0&s_y&0&0\\ 0&0&s_z&0 \\ 0&0&0&1\end{bmatrix}
\begin{bmatrix}{1 / s_x}&0&0 \\ 0&{1 / s_y}&0&0\\ 0&0&{1 / s_z}&0 \\ 0&0&0&1\end{bmatrix}
=
\begin{bmatrix}1&0&0&0 \\ 0&1&0&0 \\ 0&0&1&0 \\ 0&0&0&1\end{bmatrix}
$$

Scaling surface normals by the same matrix as points messes up the perpendicular property of the normals.
To keep normals perpendicular to the surface, if we use a scaling matrix $S$ to create a new point $S \vec p$, then we use its inverse to create a new surface normal $S^{-1} \vec n$: 
$\begin{bmatrix}{1 / s_x}&0&0 \\ 0&{1 / s_y}&0&0\\ 0&0&{1 / s_z}&0 \\ 0&0&0&1\end{bmatrix}
\vec n$

## Other origins and axes

The rotation and scaling matrices above operate along the primary axes centered on the origin.
We can construct matrices that use other origins and axes be multiplying several matrices together.

To rotate or scale about an origin $\vec o$ instead of the usual origin point $(0,0,0,1)$,
we use two helper matrices:
$M$ does the rotate or scale about the origin
and $T_o$ translates $\vec o$ to $(0,0,0,1)$.
The matrix that rotates or scales about $\vec o$ is then $T_o^{-1} M T_o$.

To rotate around or scale along an axis passing through the origin and point $\vec a$,
we use several helper matrices:
$R_z$ rotates $\vec a$ about the z axis until it lies in the $y=0$ plane;
$R_y$ rotates $R_z \vec a$ about the y axis until it lies along the $x$ axis;
and $M$ does the rotate around or scale along or around $x$ axis.
The rotate around or scale along an axis passing through $\vec a$
is then $R_z^{-1} R_y^{-1} M R_y R_z$.

Combining these, our generic matrix using any axis and origin is $T_o^{-1} R_z^{-1} R_y^{-1} M R_y R_z T_o$

<details class="example"><summary>The usual view matrix</summary>
Given a camera location, location to center in view, and up direction
we can make a view matrix $R T$ where

1. $T$ is a translation matrix that moves the camera location to the origin
1. $R$ is a rotation matrix that rotates
    - the "forward" vector (center &minus; camera) to lie along the $−z$ axis
    - the "up" vector to lie as close to the +y axis as the "forward" allows

</details>

<details class="example"><summary>JavaScript code to create a view matrix</summary>
Assuming we use a $-z$ projection matrix (see below):
```js
const m4view = (eye, center, up) => m4mul(m4fixAxes(sub(center,eye), up), m4trans(-eye[0],-eye[1],-eye[2]))
```
</details>


## Division

Notice that all of the matrices given above have the same last row, $\begin{bmatrix}0&0&0&1\end{bmatrix}$.
Matrices with that property are called affine matrices, and the transformations they encode are called affine transformations.
All affine transformations can be represented by a combination of translation, rotation, and scaling.

If the bottom row is some other vector $\vec b$,
the impact on point $\vec p$ is the same as dividing by $\vec b \cdot \vec p$ after the transformation encoded in the matrix.
Such a division causes lines passing through some fixed point in space to become parallel lines instead,
which will be useful in projecting from a 3D perspective to a 2D screen.
Because of that application, matrices with a last row different from $\begin{bmatrix}0&0&0&1\end{bmatrix}$ are often called "perspective" matrices or "projection" matrices.
Because they also cause certain frustums to become rectangular prisms, they are sometimes called "frustum" matrices.

One of the most common perspective or projection matrices does the following:

- Copy $z$ (or in some cases $-z$ into $w$)
- Change $z$ so that
    $\frac{z}{w} = -1$ when $w = \text{near}$, and 
    $\frac{z}{w} = 1$ when $w = \text{far}$
    ^[
    WebGL inherits an odd decision from OpenGL:
    the depth buffer is capped to $[0, 1]$
    but the frustum clipping caps $z$ to $[-1, 1]$.
    There is a viewport-like transformation done between the vertex and fragment shaders to move one range to the other.
    Thus the vertex shader assumes a $-1$-to-$1$ range for $z$
    but the fragment shader assumes a $0$-to-$1$ range for $z$. 
    ] 

$$
\begin{bmatrix}
1&0&0&0\\
0&1&0&0\\
0&0&\pm \dfrac{\text{far}+\text{near}}{\text{far}-\text{near}} & \dfrac{2 \cdot \text{far} \cdot \text{near}}{\text{near}-\text{far}}\\
0&0&\pm 1 & 0\\
\end{bmatrix}
$$

If the bottom row is some other vector $\vec b$,
the impact on surface normal $\vec n$ is (from a graphics perspective) destructive and meaningless.
We never multiply surface normals (nor other offsets or directions) by a perspective matrix.

We also don't adjust normals to handle display aspect ratios, which are handled by scaling $x$ and $y$.
Additionally, the simple $z$-to-$w$ rule means we ave a 90° field of view in both $x$ and $y$, which is rarely what we want.
Because of that, it is common to see a single matrix applied to positions but not normals which has the the form

$$
\begin{bmatrix}
s_x&0&0&0\\
0&s_y&0&0\\
0&0&\pm \dfrac{\text{far}+\text{near}}{\text{far}-\text{near}} & \dfrac{2 \cdot \text{far} \cdot \text{near}}{\text{near}-\text{far}}\\
0&0&\pm 1 & 0\\
\end{bmatrix}
$$

where $s_x = s_y\dfrac{\text{screen height}}{\text{screen width}}$
and $s_y = \cot\left(\dfrac{\text{field of view in y}}{2}\right)$.

<details class="example"><summary>JavaScript code to create this matrix</summary>
Assuming we want $-z$ as $w$, the more common version:
```js
const m4perspNegZ = (near, far, fovy, width, height) => {
  let sy = 1/Math.tan(fovy/2);
  let sx = sy*height/width;
  return new Float32Array([sx,0,0,0, 0,sy,0,0, 0,0,-(far+near)/(far-near),-1, 0,0,(2*far*near)/(near-far),0]);
}
```
</details>

# Common matrix setups

Objects are commonly defined in a reference coordinate system.
A **model** matrix $M$ moves points in that reference position
into their correct location in the scene.

The viewing point may be anywhere in the scene.
A **view** matrix $V$ positions and orients the camera from that arbitrary viewing point
to the origin with the viewing direction down either the $+z$ or $-z$ axis.

:::note
Because most models are defined around the origin,
most model matrices move from the origin to the scene location of a model.
But view matrices move from the scene location of the viewer to the origin.
These are inverses of each other, a common source of confusion.

Suppose you want to render from the viewpoint of the driver of a vehicle,
moving the vehicle model and the viewpoint together.
If $A$ is the model matrix of the vehicle then $A^{-1}$ is the corresponding view matrix (assuming the viewer is positioned at the origin of the vehicle's coordinate space).
:::

A **projection** matrix $P$ changes $z$ and $w$ to provide perspective and scales $x$ and $y$ to control field of view and aspect ratio.
We pick the signs in the matrix so that $w>0$ in the viewing direction.

We expect

- $P$ to change only if the screen is resized
- $V$ to change every frame in which the viewer moves
- $M$ to be different for each object in the scene

Assuming neither $M$ nor $V$ squishes or stretches things, every position $\vec p$ and normal $\vec n$ will be multiplied by both $M$ and $V$.
We can save some CPU-GPU communication and some per-vertex work by combining these into a "model-view matrix" $(V \cdot M)$.
The vertex shader will multiply every position and normal by this combined model-view matrix.

Positions will also be multiplied by $P$, but any lighting information, including normals and usually also positions, will not.
Thus $P$ will be supplied separately.

Thus we might expect something like the following

    CPU setup routine:
        set P based on the field of view and aspect ratio
        send P to the GPU's projection uniform

    CPU draw routine:
        set V from viewing position
        for each object:
            set mv as V * M
            send mv to the GPU's modelview uniform
            send the object's geometry data to the GPU

    GPU vertex shader
        set output view_normal as modelview * input normal
        set output view_position as modelview * input position
        set gl_Position as projection * view_position

# Categories of motion

The various types of matrix have types of motion that can generate by being changed each frame.
Some of these have special names.

|        | matrix | Affine | uniform | Rigid | Linear |
|--------|:------:|:------:|:------:|:-----:|:-------:|
|straight|   ✓    |   ✓    |    ✓   |  ✓    |   ✓     |
|parallel|        |   ✓    |    ✓   |   ✓   |    ✓    |
|angles  |        |        |    ✓   |   ✓   |         |
|size    |        |        |        |   ✓   |         |
|origin  |        |        |        |       |    ✓    |

Any homogeneous matrix (translation + rotation + scaling + perspective) will keep straight lines straight.

An affine matrix (translation + rotation + scaling) will keep parallel lines parallel.

An affine matrix with uniform scaling (translation + rotation + same scaling in every axis) will keep angles between lines unchanged.

A rigid matrix (translation + rotation) is affine and will all lengths and sizes unchanged.

A linear matrix (rotation + scaling) is affine and will keep the origin (0,0,0) fixed.

 

There are various "degenerate" matrices that mess things up by setting something to zero:

- If the bottom row is all 0s, the homogeneous matrix is degenerate and represents not points
- If the top-left 3×3 submatrix is rank deficient, the matrix is degenerate and reduces all shapes to a point (rank 0), line (rank 1), or plane (rank 2)
        
It is common for algorithms and code to assume non-degenerate matrices.
