---
title: Bones
...

When manipulating bones in a graphics system, there are a few constraints that are often needed. This page explores how to compute those constraints.


# Vectors to rotation matrices

A rotation matrix has three columns,
each of which is a unit-length vector
all three of which are mutually orthogonal
and the three form a right-handed coordinate system.
When applied to an object, the first column is the direction the positive x-axis in object space ends up pointing,
the second column is where the positive y-axis ends up pointing,
and the third second column is where the positive z-axis ends up pointing.

We can create such a set of vectors using cross products.
Suppose we have some $\vec x_0$, $\vec y_0$, and $\vec z_0$ that will not make a rotation matrix as-is.
We first pick the vector we want to match the most; for this example, let's say that's $\vec x_0$.
We divide it by its length to get $\vec x$ and use it in the matrix:
$$\begin{bmatrix}\vec x & ? & ?\end{bmatrix}$$
Now we pick the second-most important; for this example, let's say that's $\vec y_0$.
We use a pair of cross-products to find a vector orthogonal to $\vec x$ that is as close to $\vec y_0$ as possible:
$\vec y_1 = (\vec x \times \vec y) \times \vec x$
and then divide that my its length to get $\vec y$, the next column:
$$\begin{bmatrix}\vec x & \vec y & ?\end{bmatrix}$$
The third column is then just the cross-product of the other two, in an order to preserve the right-handed coordinate system: $\vec z = \vec x \times y$ or $\vec x = \vec y \times \vec z$ or $\vec y = \vec z \times \vec x$.
No need to divide this one by its length: it will come out unit-length by construction.
$$\begin{bmatrix}\vec x & \vec y & \vec z\end{bmatrix}$$

Note that the least-important vector was not used at all: we only need a primary and secondary vector to perform this rotation matrix construction.
Also note that this process will break down if the two most important vectors are co-planar: we'll get a zero vector from the first cross-product and a divide-by-zero when we try to make it unit length.

The general process of finding a rotation matrix from a set of vectors is called "orthonormalization"
and has other solutions, including one based on the singular value decomposition that doesn't favor particular vectors,
but we'll not use those in this class.

# Point-and-roll constraints

One common bone constraint supplied by 3D animation software is a combination "point the bone at" constraint with a "roll this axis toward" disambiguation.
This constraint is the above vector-to-matrix process almost directly.

:::example
To point the +z axis toward point $(0,4,3)$ and roll the -y axis toward $(0,0,1)$ we'd:

1. normalize the primary vector: $\vec z = (0, 0.8, 0.6)$
1. cross-product the secondary vector: $\vec z \times (0,0,1) = (0.8,0,0)$
1. cross-product that with the primary vector: $(0.8,0,0) \times \vec z = (0,-0.48,0.64)$
1. normalize the result and handle the axis sign: $\vec y = (0, 0.6, -0.8)$
1. find the third axis: $\vec x = \vec y \times \vec z = (1,0,0)$
1. for the rotation matrix $$\begin{bmatrix}1 & 0 & 0 \\ 0 & 0.6 & 0.8\\0 & -0.8 & 0.6\end{bmatrix}$$

And yes, I did pick this example carefully so that the math would work out without any radicals or long decimals.
:::

# Point-at constraints

Sometimes constraints omit the roll-toward part, which in turn leaves the rotation matrix under-constrained.
The usual implication is "the smallest possible change that achieves this point-at".
In general, smallest possible changes require solving linear systems of equations
but for this particular question we can do something simpler.

The minimal change that points an axis to a point is a rotation.
to minimize change, the axis of that rotation should be perpendicular to the axis and the target point.
One way of computing a rotation is by a rotation angle $\theta$ and unit-length rotation axis $\vec r$;
the matrix for that rotation is
$$\begin{bmatrix}
r_x^2(1-c)+c & r_x r_y (1-c) - r_z s & r_x r_z (1-c) + r_y s  \\
r_x r_y (1-c) + r_z s & r_y^2(1-c)+c  & r_y r_z (1-c) - r_x s  \\
r_x r_z (1-c) - r_y s & r_y r_z (1-c) + r_x s & r_z^2(1-c)+c \\
\end{bmatrix}$$
where $c = \cos(\theta)$ and $s = \sin(\theta)$.

The smallest rotation does not move points that are perpendicular to the old and new axis positions.
That means that $\vec r$ is perpendicular to both the old axis $\vec a$ and the target point $\vec p$,
meaning it can be found by a cross product.
A cross product will also give us the sine of the angle ($s$),
and a dot product can give us the cosine of the angle ($c),
which is all we need.
Ergo, we have

- $\displaystyle \vec a' = \frac{\vec a}{\|\vec a\|}$
- $\displaystyle \vec p' = \frac{\vec p}{\|\vec p\|}$
- $\vec r' = \vec a' \times \vec p'$
- $c = \vec a' \cdot \vec p'$
- $s = \|\vec r'\|$
- $\displaystyle \vec r = \frac{\vec r'}{s}$

which, combined with the matrix above, gives us the minimal rotation to point $\vec a$ at $\vec p$.

:::example
To point the +y axis at $(3,12,4)$ we'd compute

- $\displaystyle \vec a' = (0,1,0)$

- $\displaystyle \vec p' = (\frac{3}{13},\frac{12}{13},\frac{4}{13})$

- $\displaystyle \vec r' = (\frac{4}{13}, 0, \frac{-3}{13})$

- $\displaystyle c = \frac{12}{13}$

- $\displaystyle s = \frac{5}{13}$

- $\displaystyle \vec r = (\frac{4}{5},0,\frac{-3}{5})$

and build the matrix

$$\begin{bmatrix}
\dfrac{316}{325} & \dfrac{3}{13} & \dfrac{-12}{325} \\ \\
\dfrac{-3}{13} & \dfrac{12}{13}  & \dfrac{-4}{13} \\ \\ 
\dfrac{-12}{325} & \dfrac{4}{13} & \dfrac{309}{325} \\
\end{bmatrix}$$
:::
