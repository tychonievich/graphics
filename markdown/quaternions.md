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

To rotate point $x$ by unit-length quaternion $q$ we use $q x q^{*}$.
But we generally will want to convert the quaternion to a matrix intead.

The 3×3 rotation matrix of an arbitrary (non-normalized) quaternion can be found using the following three equations:
$$n = w^2 + x^2 + y^2 + z^2$$
$$s = \begin{cases}0 & \text{if } n=0\\\frac{2}{n} &\text{otherwise}\end{cases}$$
$$\begin{bmatrix}
1-s(y^2+z^2) & s(xy-zw) & s(xz+yw) \\
s(xy+zw) & 1-s(x^2+z^2) & s(yz-xw) \\
s(xz-yw) & s(yz+xw) & 1-s(x^2+y^2) \\
\end{bmatrix}$$
In the special case of a normalized quaternion, $n = 1$, $s=2$, and we have
$$\begin{bmatrix}
w^2+x^2-y^2-z^2 & 2(xy-zw) & 2(xz+yw) \\
2(xy+zw) & w^2-x^2+y^2-z^2 & 2(yz-xw) \\
2(xz-yw) & 2(yz+xw) & w^2-x^2-y^2+z^2 \\
\end{bmatrix}$$
Note we did a bit of conversion: direct substitution would have given us diagonal terms like $1-2(y^2+z^2)$ but $n = 1$ means we can re-write that as $w^2 + x^2 + y^2 + z^2 - 2(y^2+z^2)$, which simplifies to the matrix given.

There are many terms in the above formulae and thus many of chances for a typo.
A quick sanity check is that multiplying any rotation matrix (including the rotation matrix from a random quaternion) by its transpose should result in the identity matrix.

## Inverse

Given a rotation matrix, we can also derive a quaternion that represents it.
Note that there are many such quaternions, as multiplying a quaternion by a scalar does not change the rotation it represents.

The basic approach here is to add cells of the simpler unit-quaternion matrix together to cancel some terms.

- Add the main diagonal to get $3w^2 - x^2 - y^2 - z^2$; 
    because $w^2 + x^2 + y^2 + z^2 = 1$, this is equivalent to $4w^2 - 1$,
    so we can find $w$.
    Then we can subtract antidiagonal pairs (like $2(yz-xw) - 2(yz+xw) = -4xw$) and divide by $w$ to get the other terms.
    
    - $w = \frac{1}{2} \sqrt{a_{0,0} + a_{1,1} + a_{2,2} + 1}$
    
    - $x = \dfrac{a_{2,1} - a_{1,2}}{4w}$
    
    - $y = \dfrac{a_{0,2} - a_{2,0}}{4w}$
    
    - $z = \dfrac{a_{1,0} - a_{0,1}}{4w}$

    But we can multiply the entire quaternion by a scalar without changing the rotation it represents; multiplying by $4w$, we get

    - $w = a_{0,0} + a_{1,1} + a_{2,2} + 1$
    
    - $x = a_{2,1} - a_{1,2}$
    
    - $y = a_{0,2} - a_{2,0}$
    
    - $z = a_{1,0} - a_{0,1}$


- Subtract two main diagonals from the third to get $3x^2 - w^2 - y^2 - z^2$, which again is equivalent to $4x^2-1$ to find $x$;
    then add antidiagonal pairs (like $2(xy-zw) + 2(xy+zw) = 4xy$) and divide by $x$ to get the other terms.

    - $x = \frac{1}{2} \sqrt{a_{0,0} - a_{1,1} - a_{2,2} + 1}$
    
    - $y = \dfrac{a_{0,1} + a_{1,0}}{4x}$
    
    - $z = \dfrac{a_{0,2} + a_{2,0}}{4x}$
    
    - $w = \dfrac{a_{2,1} - a_{1,2}}{4x}$
    
    Again, we can multiply all four terms by $4x$ to get a more easily computed quaternion representing the same rotation.

... and so on for the other two axes. In the end, we get four quaternion options:

- $\langle a_{0,0} + a_{1,1} + a_{2,2} + 1; a_{2,1} - a_{1,2}, a_{0,2} - a_{2,0}, a_{1,0} - a_{0,1}\rangle$

- $\langle a_{2,1} - a_{1,2}; a_{0,0} - a_{1,1} - a_{2,2} + 1, a_{0,1} + a_{1,0}, a_{0,2} + a_{2,0}\rangle$

- $\langle a_{0,2} - a_{2,0}; a_{1,0} + a_{0,1}, a_{1,1} - a_{0,0} - a_{2,2} + 1, a_{1,2} + a_{2,1}\rangle$

- $\langle a_{1,0} - a_{0,1}; a_{0,2} + a_{2,0}, a_{1,2} + a_{2,1}, a_{2,2} - a_{0,0} - a_{1,1} + 1\rangle$

Assuming $A$ is a rotation matrix, each of these is a scalar multiple of the others, so we only need to compute one of them.
To optimize numerical precision, we should pick the one with the largest four-term sum.

:::example
Consider the rotation matrix
$$\begin{bmatrix}0&1&0\\1&0&0\\0&0&-1\end{bmatrix}$$
The four quaternion equations give us

- $\langle 0;0,0,0 \rangle$
- $\langle 0;2,2,0 \rangle$
- $\langle 0;2,2,0 \rangle$
- $\langle 0;0,0,0 \rangle$

Two of these are useless while the other two are useful.
But there's nothing special about those two; a different rotation
$$\begin{bmatrix}-1&0&0\\0&-1&0\\0&0&1\end{bmatrix}$$
results in

- $\langle 0;0,0,0 \rangle$
- $\langle 0;0,0,0 \rangle$
- $\langle 0;0,0,0 \rangle$
- $\langle 0;0,0,4 \rangle$

In general we must check all four options as any three of them may give zero quaternions.
Because of the way we constructed these equations,
it is sufficient to check the four-term sum alone.
:::
