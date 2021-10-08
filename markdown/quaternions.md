---
title: Quaternions
...

This page is intended to be a brief reference on implementing rotations with quaternions.
It is not intended to be a full discussion of the topic, only a reference.

# Definition

Let $\mathbf{i}$, $\mathbf{j}$, and $\mathbf{k}$ be three different "basis quaternions".
Let $\mathbf{i}^2 = \mathbf{j}^2 = \mathbf{k}^2 = \mathbf{ijk} = -1$.

Quaternion multiplication is associative but *not commutative*: $\mathbf{ji} \ne \mathbf{ij}$.

From this we can derive

- $\mathbf{ij} = \mathbf{k}$ (because $(\mathbf{ij})\mathbf{k} = -1 = \mathbf{kk}$)
- $\mathbf{jk} = \mathbf{i}$ (because $\mathbf{i}(\mathbf{jk}) = -1 = \mathbf{ii}$)
- $\mathbf{ki} = \mathbf{j}$ (because $\mathbf{ki} = (\mathbf{ij})(\mathbf{jk}) = \mathbf{i}(-1)\mathbf{k} = -\mathbf{ik} = -\mathbf{i}(\mathbf{ij}) = --\mathbf{j} = \mathbf{j}$)
- $\mathbf{ji} = \mathbf{-k}$ (because $\mathbf{ji} = \mathbf{j}(\mathbf{jk}) = -\mathbf{k}$)
- $\mathbf{kj} = \mathbf{-i}$ (because $\mathbf{kj} = \mathbf{k}(\mathbf{ki}) = -\mathbf{i}$)
- $\mathbf{ik} = \mathbf{-j}$ (because $\mathbf{ik} = \mathbf{i}(\mathbf{ij}) = -\mathbf{j}$)

Given a quaternion $w + x \mathbf{i} + y \mathbf{j} + z \mathbf{k}$,
its multiplicative inverse is $\displaystyle \frac{w - x \mathbf{i} - y \mathbf{j} - z \mathbf{k}}{w^2 + x^2 + y^2 + z^2}$:
that is, the product of those two quaternions is 1.

Thus the quaternion $w + x \mathbf{i} + y \mathbf{j} + z \mathbf{k}$
are closed under addition, multiplication, and division.

# Storage as vectors

We will write the quaternion $w + x \mathbf{i} + y \mathbf{j} + z \mathbf{k}$
as just $\langle w;x,y,z \rangle$.
This is just one of many notations used in graphics; none seem to have a majority.

The conjugate of $\langle w;x,y,z \rangle$ is $\langle w;-x,-y,-z \rangle$.

The product $\langle w_1;x_1,y_1,z_1 \rangle \langle w_2;x_2,y_2,z_2 \rangle$
is $$\begin{matrix}
\langle w_1w_2 - x_1x_2 - y_1y_2 - z_1z_2;\\
w_1x_2 + x_1w_2 + y_1z_2 - z_1y_2,\\
w_1y_2 + y_1w_2 + z_1x_2 - x_1z_2,\\
w_1z_2 + z_1w_2 + x_1y_2 - y_1x_2 \rangle
\end{matrix}$$
Notice: the terms above are such that the $x$ coordinate multiplies $x$ and $w$ in both directions
and multiplies the other two coordinates in both directions but puts a negative sign on the one that's out-of-order (xy, yz, and zx are in-order in a wrapping alphabet).

The magnitude of a quaternion $q$ is $\sqrt{q^{*} q} = \sqrt{w^2 + x^2+y^2+z^2}$.
The magnitude is always a scalar (zero $x,y,z$).
A normalized quaternion is one with a magnitude of $1$.

To multiply a point $(x,y,z)$ by a quaternion, treat the point as $\langle 0;x,y,z \rangle$
and use the quaternion product.
Note that this will give a quaternion (non-zero $w$), not a point (zero $w$).
However, $q x q^{*}$ will always be a point if $x$ is a point.

# Rotation matrix

The 3×3 rotation matrix of a *normalized* quaternion $\langle w;x,y,z \rangle$
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

The 3×3 rotation matrix of an arbitrary (non-normalized) quaternion can be found without normalizing using the following three equations:
$$n = w^2 + x^2 + y^2 + z^2$$
$$s = \begin{cases}0 & \text{if } n=0\\\frac{2}{n} &\text{otherwise}\end{cases}$$
$$\begin{bmatrix}
1-s(y^2+z^2) & s(xy-zw) & s(xz+yw) \\
s(xy+zw) & 1-s(x^2+z^2) & s(yz-xw) \\
s(xz-yw) & s(yz+xw) & 1-s(x^2+y^2) \\
\end{bmatrix}$$

There are many terms in the above formulae and thus many of chances for a typo.
A quick sanity check is that the matrix of a random quaternion times its own transpose should be the identity matrix.


## Inverse

Given a rotation matrix, we can also derive a quaternion that represents it.
Note that there are many such quaternions, as multiplying a quaternion by a scalar does not change the rotation it represents.

The basic approach here is to add cells of the matrix together to cancel some terms.
Using the normalized quaternion form, we have four ways we can do this:

- Add the main diagonal to get $3w^2 - x^2 - y^2 - z^2$; 
    because $w^2 + x^2 + y^2 + z^2 = 1$, this is equivalent to $4w^2 - 1$,
    so we can find $w$.
    Then we can subtract antidiagonal pairs (like $2(yz-xw) - 2(yz+xw) = -4xw$) and divide by $w$ to get the other terms.
    
    - $w = \frac{1}{2} \sqrt{a_{0,0} + a_{1,1} + a_{2,2} + 1}$
    - $x = \dfrac{a_{2,1} - a_{1,2}}{4w}$
    - $y = \dfrac{a_{0,2} - a_{2,0}}{4w}$
    - $z = \dfrac{a_{1,0} - a_{0,1}}{4w}$

- Subtract two main diagonals from the third to get $3x^2 - w^2 - y^2 - z^2$, which again is equivalent to $4x^2-1$ to find $x$;
    then add antidiagonal pairs (like $2(xy-zw) + 2(xy+zw) = 4xy$) and divide by $x$ to get the other terms.

    - $x = \frac{1}{2} \sqrt{a_{0,0} - a_{1,1} - a_{2,2} + 1}$
    - $y = \dfrac{a_{0,1} + a_{1,0}}{4x}$
    - $z = \dfrac{a_{0,2} + a_{2,0}}{4x}$
    - $w = \dfrac{a_{2,1} - a_{1,2}}{4x}$
    
- Subtract two main diagonals from the third to find $y$:
    
    - $y = \frac{1}{2} \sqrt{a_{1,1} - a_{0,0} - a_{2,2} + 1}$
    - $x = \dfrac{a_{1,0} + a_{0,1}}{4y}$
    - $z = \dfrac{a_{1,2} + a_{2,1}}{4y}$
    - $w = \dfrac{a_{0,2} - a_{2,0}}{4y}$

- Subtract two main diagonals from the third to find $z$:
    
    - $y = \frac{1}{2} \sqrt{a_{2,2} - a_{0,0} - a_{1,1} + 1}$
    - $x = \dfrac{a_{0,2} + a_{2,0}}{4y}$
    - $z = \dfrac{a_{1,2} + a_{2,1}}{4y}$
    - $w = \dfrac{a_{1,0} - a_{0,1}}{4y}$

All four will work in principle, but to maximize numerical accuracy we want the discriminant (the value inside the square root) to be as large as possible.

Note that this process only works if the matrix given was in fact a rotation, as only rotation matrices can be represented as a quaternion.
