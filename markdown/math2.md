---
title: Homogeneous Vectors and Transformations
...

# Homogeneous vectors

Homogeneous vectors look like [regular vectors](math1.html), and in most ways behave like them, but they differ in two key ways:

1. They have an extra coordinate, such that a 3D vector has 4 numbers. The extra coordinate is called the $w$ coordinate.
2. We define $a\vec x = \vec x$ for all real-number $a$ and homogeneous vector $\vec x$.

When we need to distinguish them from non-homogeneous vectors, we call the non-homogeneous vectors "Cartesian vectors" after René Descartes who popularized them.
August Möbius invented homogeneous vectors, but I have never heard anyone call them "Möbisian vectors".

In graphics, we almost always deal homogeneous vectors where $w$ is either $1$ or $0$.
If $w=1$, then the homogeneous vector represents a point in space.
If $w=0$, then the homogeneous vector represents a direction or offset.

Confusingly, we use the word "normalize" to mean any of

- Given a homogeneous vector $\vec x$ with $x_w \ne 0$, replace $\vec x$ with $\dfrac{\vec x}{x_w}$
- Given a homogeneous vector $\vec x$ with $x_w = 0$, replace $\vec x$ with $\dfrac{\vec x}{\|\vec x\|}$
- Given a Cartesian vector $\vec x$, replace $\vec x$ with $\dfrac{\vec x}{\|\vec x\|}$

Confusingly, we use the word "length" to mean any of

- The number of dimensions in a Cartesian vector
- The number of values in a Homogeneous vector (1 + the number of dimensions in a Homogeneous vector)
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
$\begin{bmatrix}1&0&0&\Delta x \\ 0&1&0&\Delta y \\ 0&0&1&\Delta z \\ 0&0&0&1\end{bmatrix}$

This matrix has the same effect as adding $(\Delta x, \Delta y, \Delta z, 0)$ to every point and doing nothing to the surface normals.
However, because it is a matrix we can combine it with other transformations.

If $T$ is a translation matrix, $T^{-1}$ is found by replacing each value $v$ on the first three rows of the last column with $-v$.

## Rotation

We can rotate the object about the origin by multiplying every point and surface normal by a rotation matrix.

To rotate $\theta$ degrees about the $x$ axis, we use 
$\begin{bmatrix}1&0&0&0 \\ 0&\cos(\theta)&-\sin(\theta)&0 \\ 0&\sin(\theta)&\cos(\theta)&0 \\ 0&0&0&1\end{bmatrix}$

To rotate $\theta$ degrees about the $y$ axis, we use 
$\begin{bmatrix}\cos(\theta)&0&\sin(\theta)&0 \\ 0&1&0&0 \\ -\sin(\theta)&0&\cos(\theta)&0 \\ 0&0&0&1\end{bmatrix}$

To rotate $\theta$ degrees about the $z$ axis, we use 
$\begin{bmatrix}\cos(\theta)&-\sin(\theta)&0&0 \\ \sin(\theta)&\cos(\theta)&0&0 \\ 0&0&1&0 \\ 0&0&0&1\end{bmatrix}$

Any rotation about the origin can be created as a product of these three axis rotations.

If $R$ is a matrix representing a rotation about the origin, $R^{-1} = R^{T}$.

Rotation about a different center point can be performed by finding a translation matrix $T$ that translates that point to the origin and using $T^{-1} R T$, where $R$ is a rotation matrix.

## Scaling

We can scale the object about the origin along principle axes by multiplying every point and surface normal by a scaling matrix.

To scale by $s_x$ in the $x$ axis,
$s_y$ in the $y$ axis,
and $s_z$ in the $z$ axis,
we use 
$\begin{bmatrix}s_x&0&0 \\ 0&s_y&0&0\\ 0&0&s_z&0 \\ 0&0&0&1\end{bmatrix}$

If $S$ is a matrix representing a scaling along the principle axes, $S^{-1}$ is found by replacing each value $v$ on the main diagonal with $1 / v$.

Scaling around any other axis can be performed by finding a rotation matrix $R$ that rotates the scaling axes to the principle axes and using $R^{-1} S R$, where $S$ is a principle-axis scaling matrix.

Rotation about a different center point can be performed by finding a translation matrix $T$ that translates that point to the origin and using $T^{-1} S T$, where $S$ is a scaling matrix.

Scaling surface normals by the same matrix as points messes up the perpendicular property of the normals.
To keep normals normal to the surface, if we use a scaling matrix $S$ to create a new point $S \vec p$, then we use its inverse to create a new surface normal $S^{-1} \vec n$.


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

If the bottom row is some other vector $\vec b$,
the impact on surface normal $\vec n$ is (from a graphics perspective) destructive and meaningless.
We never multiply surface normals or other offsets or directions by a perspective matrix.



