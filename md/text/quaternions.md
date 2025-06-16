---
title: Quaternions
summary: Their definition and use in defining rotations in graphics.
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

# To rotation matrix

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

Note that all of the above quaternion rotation formulae only have pairs of terms from the quaternion, meaning if we replace $q$ with $-q$ we get the same rotation.

<details class="example"><summary>JavaScript code to turn a quaternion into a matrix</summary>
Assuming a column-major 4x4 matrix:
```js
const m4fromQ = (q) => { 
  let n = dot(q,q)
  let s = n ? 2/n : 0
  let xx = s*q[1]*q[1], xy = s*q[1]*q[2], xz = s*q[1]*q[3], xw = s*q[1]*q[0]
  let yy = s*q[2]*q[2], yz = s*q[2]*q[3], yw = s*q[2]*q[0]
  let zz = s*q[3]*q[3], zw = s*q[3]*q[0]
  return new Float32Array([
    1-yy-zz, xy+zw, xz-yw, 0,
    xy-zw, 1-xx-zz, yz+xw, 0,
    xz+yw, yz-xw, 1-xx-yy, 0,
    0,0,0,1,
  ])
}
```
</details>

# From rotation matrix

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

<details class="example"><summary>JavaScript code to turn a matrix into a quaternion</summary>
Assuming a column-major 4x4 matrix:
```js
const m4toQ = (m) => {
  let a00 = m[0], a11 = m[5], a22 = m[10]
  if (a00 + a11 + a22 > 0)
    return normalize([a00+a11+a22+1, m[6]-m[9], m[8]-m[2], m[1]-m[4]])
  if ((a00 > a11) && (a00 > a22))
    return normalize([m[6]-m[9], a00-a11-a22+1, m[1]+m[4], m[8]-m[2]])
  if (a11 > a22)
    return normalize([m[8]-m[2], m[1]+m[4], a11-a00-a22+1, m[6]+m[9]])
  return normalize([m[1]-m[4], m[2]+m[8], m[6]+m[9], a22-a00-a11+1])
}
```
</details>

# Relationship with axis-angle

Rotating $\theta$ radians around the unit-vector axis of rotation $\vec r$
is represented by the quaternion
$c \left\langle \cos\left(\frac{\theta}{2}\right) ; \sin\left(\frac{\theta}{2}\right) \vec r \right\rangle$
where $\left\langle w; \vec v \right\rangle$ is shorthand for $\left\langle w; v_x, v_y, v_z \right\rangle$
and $c$ may be any non-zero constant.

Thus, any quaternion $\langle w; \vec r\rangle$
represents a rotation around axis $\vec r$
by $\theta = 2\arctan\left(\frac{\|\vec r\|}{w}\right)$.


# Slerp

Unit quaternions are used to represent angles primarily to facilitate interpolation of angles. But linearly interpolating unit vectors does not yield other unit vectors, and normalizing interpolated unit vectors causes nonlinear speeds.

With a little trigonometry we can derive an interpolation of unit vectors that progresses across the surface of the unit ball at linear speed.
Instead of the lerp $(1-t)p_0 + (t)p_1$
we use the slerp $$\frac{\sin\big((1-t)\Omega\big)}{\sin(\Omega)}p_0 + \frac{\sin\big((t)\Omega\big)}{\sin(\Omega)}p_1$$
where $\Omega$ is the angle between $p_0$ and $p_1$: i.e. $\arccos(p_0 \cdot p_1)$.
Clearly this is much more expensive to compute than the lerp, so we shouldn't use it on per-vertex computations, but for per-frame computations like interpolating bone orientations it works quite well.

The slerp is numerically unstable for very small $\Omega$, but for very small $\Omega$ the slerp and lerp are effectively identical so we can default to a lerp for small angles instead.
It is also unstable for $\Omega$ near $\pi$, but that is because interpolating between opposite orientations is intrinsically unstable: no numerical trick will make it less so.

Because $q$ and $-q$ represent the same orientation, we sometimes need to invert $q$ to get the best slerp.

:::example
Consider the quaternions representing the rotations of 0°, 120°, and 240° around the $z$ axis:

| angle | option A | option B |
|------:|:---------|:---------|
| 0° | $\langle 1.0; 0,0,0 \rangle$ | $\langle -1.0; 0,0,0 \rangle$ |
| 120° | $\langle 0.5; \sqrt{0.75},0,0 \rangle$ | $\langle -0.5; -\sqrt{0.75},0,0 \rangle$ |
| 240° | $\langle 0.5; -\sqrt{0.75},0,0 \rangle$ | $\langle -0.5; \sqrt{0.75},0,0 \rangle$ |

Slerping between 0°A and 120°A goes the short way around (moving 120°), while slerping between 0°A and 120°B goes the long way (moving 240°).
We can tell a short way because its angle is under 180°, meaning its cosine (i.e. dot product) is positive.

If we want to loop though the three points always going the short way around we'd need to go do something like
0°A → 120°A → 240°B → 0°B → 120°B → 240°A → 0°A.
Note we flipped half-way through: no fixed sign of the three quaternions will always work, we have to pick pairs of signs that match up.
:::

<details class="example"><summary>JavaScript code to slerp unit vectors</summary>
Slerp works for unit vectors of any dimension, including quaternions,
but it only works for unit vectors;
if you have non-unit vectors you must normalize them first.
We also have a sign-picking version `qlerp` for use with quaternions.
```js
const lerp = (t,p0,p1) => add(mul(p0,1-t), mul(p1,t))
const slerp = (t,q0,q1) => {
  let d = dot(q0,q1)
  if (d > 0.9999) return normalize(lerp(t,q0,q1))
  let o = Math.acos(d), den = Math.sin(o)
  return add(mul(q0, Math.sin((1-t)*o)/den), mul(q1, Math.sin(t*o)/den))
}
const qlerp = (t,q0,q1) => {
  let d = dot(q0,q1)
  if (d < 0) { q1 = mul(q1,-1); d = -d; }
  if (d > 0.9999) return normalize(lerp(t,q0,q1))
  let o = Math.acos(d), den = Math.sin(o)
  return add(mul(q0, Math.sin((1-t)*o)/den), mul(q1, Math.sin(t*o)/den))
}
```
</details>

Because [Bézier curves](bezier.html) and various splines use repeated lerps to find points on the curve, we can use slerp to apply the same ideas to make curves of vectors on the unit ball. Note that while this will create smooth curves, it will not create true Bézier curves and many of the properties of Bézier curves, such as the intermediate control points of de Casteljau's algorithm defining smaller Bézier curves and so on, do not apply if slerps are used instead of lerps.

<details class="example"><summary>JavaScript code for spherical Bézier curves</summary>
This is identical to the linear Bézier code, but using `slerp`/`qlerp` instead of `lerp`.
```js
const sbez = (t, ...p) => {
  while(p.length > 1) p = p.slice(1).map((e,i) => slerp(t,p[i],e))
  return p[0]
}
const qbez = (t, ...p) => {
  while(p.length > 1) p = p.slice(1).map((e,i) => qlerp(t,p[i],e))
  return p[0]
}
```
</details>
