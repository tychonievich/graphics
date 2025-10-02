---
title: Math Review
summary: Vectors and matrices.
...


# Vectors 

A mathematical vector (or more precisely, a vector over the field of the real numbers)
is a list of numbers with a set of operations.
We use mathematical vectors in computer graphics to represent five things:

- Points in space
- Vectors: that is, direction and magnitude
- Directions, more commonly called "unit vectors" (or "normals" if the direction is defined by a surface)
- Homogeneous vectors: these have [their own writeup](math2.html)
- Mathematical vectors alone, with no additional structure

When dealing with a vector, it is common to call numbers "scalars".

Let $s$ be a scalar,
$\vec x = (x_1, x_2, \dots, x_n)$ and $\vec y = (y_1, y_2, \dots, y_n)$ be two vectors,
and $\theta$ be the angle between $\vec x$ and $\vec y$.

Operation           Result                                  Notes
------------------- --------------                          -------------------
$\vec x + \vec y$   $(x_1+y_1, x_2+y_2, \dots, x_n+y_n)$    Vector addition, element-wise addition
$\vec x - \vec y$   $(x_1-y_1, x_2-y_2, \dots, x_n-y_n)$    Vector subtraction or difference, element-wise subtraction
$s \vec x$          $(s x_1, s x_2, \dots, s x_n)$          Scaling, multiplication by a scalar
$\dfrac{\vec x}{s}$ $(x_1/s, x_2/s, \dots, x_n/s)$          Scaling, division by a scalar
$\vec x\cdot\vec y$ $x_1y_1 + x_2y_2 + \cdots + x_ny_n$     Dot product, inner product; also written $\vec x^{T} \vec x$; is a scalar equal to $\|\vec x\| \|\vec y\| \cos(\theta)$
$\|\vec x\|$        $\sqrt{\vec x \cdot \vec x}$            Magnitude, length, $\ell_2$ norm

Depending on what vectors represent, their operations may represent specific things:

- point 1 − point 2 = vector extending from point 2 to point 1
- point + vector = new point
- vector ± vector = vector
- point + point = error
- vector ÷ its own magnitude = direction. This operation is called "normalizing the vector"
- direction × scalar = vector made out of direction and magnitude

Two vectors are said to be orthogonal or perpendicular if their dot product is $0$.

A vector is called a unit vector if its magnitude is $1$.

Two-dimensional vectors have just two components $(x_1, x_2)$.
They have two special operations:

- $(-x_2, x_1)$ is perpendicular to $(x_1, x_2)$
- the 2D cross product $(x_1, x_2) \times (y_1,y_2) = x_1y_2-x_2y_1$ is scalar
equal to $\|\vec x\| \|\vec y\| \sin(\theta)$ where $\theta$ is the angle between the two vectors.

Three-dimension vectors have three components $(x_1, x_2, x_3)$.
They have one special operation:

- the 3D cross product $(x_1, x_2, x_3) \times (y_1,y_2,y_3) = (x_2y_3-y_2x_3, x_3y_1-y_3x_1,x_1y_2-y_1x_2)$ is a vector perpendicular to both input vectors with a magnitude equal to $\|\vec x\| \|\vec y\| \sin(\theta)$.

<details class="example"><summary>Javascript code implementing these operators</summary>
```js
const add = (x,y) => x.map((e,i)=>e+y[i])
const sub = (x,y) => x.map((e,i)=>e-y[i])
const mul = (x,s) => x.map(e=>e*s)
const div = (x,s) => x.map(e=>e/s)
const dot = (x,y) => x.map((e,i)=>e*y[i]).reduce((s,t)=>s+t)
const mag = (x) => Math.sqrt(dot(x,x))
const normalize = (x) => div(x,mag(x))
const cross = (x,y) => x.length == 2 ?
  x[0]*y[1]-x[1]*y[0] :
  x.map((e,i)=> x[(i+1)%3]*y[(i+2)%3] - x[(i+2)%3]*y[(i+1)%3])
```
</details>



# Matrices

A matrix is a grid of numbers.
They can be seen as a vector of vectors in two ways:
either as a vector of columns or a vector of rows.

The matrix transpose $A^T$ is computed by treating the rows of $A$ as columns and vice versa.
If $A = A^T$ we say $A$ is symmetric.
If $A = -A^T$ we say $A$ is skew-symmetric or antisymmetric.

:::example
$$\begin{bmatrix}1&2&3&4 \\ 5&6&7&8 \\ 9&10&11&12\end{bmatrix}^T = \begin{bmatrix}1&5&9\\2&6&10\\3&7&11\\4&8&12\end{bmatrix}$$
:::

The matrix product $A B$ is a matrix $C$.
The value in $C$ at row $r$ and column $c$ is equal to
the dot product of row $r$ of $A$ and column $c$ of $B$.
Hence, the matrix product $A B$ is only defined if $A$ has the same number of columns as $B$ has rows.

:::example
$$\begin{bmatrix}1&2&3 \\ 4&5&6\end{bmatrix} \begin{bmatrix}7&8 \\ 9&10 \\ 11&12\end{bmatrix} = \begin{bmatrix}58&64\\139&154\end{bmatrix}$$
:::

The matrix-vector product $A \vec x$ is computed by treating $\vec x$ as if it were a matrix with just one column.

:::example
$$
\begin{bmatrix}1&2&3 \\ 4&5&6\end{bmatrix} \vec x=
\begin{bmatrix}1&2&3 \\ 4&5&6\end{bmatrix} \begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix} =
\begin{bmatrix}1x_1+2x_2+3x_3\\4x_1+5x_2+6x_3\end{bmatrix}
=(x_1+2x_2+3x_3,4x_1+5x_2+6x_3)$$
:::

Some texts define the vector-matrix product $\vec x A$ to be treating $\vec x$ as if it were a matrix with just one row, but others disagree and say vectors are always columns an write $\vec x^T A$ instead.

Any linear system of equations can be written as $A \vec x = \vec b$

:::example
The linear system of equations
$$\begin{matrix}
3x &+& 4y &+& 3z &=& 0\\
&& 2y && &=& -1\\
-x && &+& z &=& 4\\
\end{matrix}$$
can be written as
$$\begin{bmatrix}3&4&3\\0&2&0\\-1&0&1\end{bmatrix}\begin{bmatrix}x\\y\\z\end{bmatrix} = \begin{bmatrix}0\\-1\\4\end{bmatrix}$$
:::

A square matrix has the same number of rows and columns.

The main diagonal of a matrix are the cells with the same row and column index.
A diagonal matrix is square and has zeros everywhere except along the main diagonal.

:::example
The following is a diagonal matrix
$$\begin{bmatrix}3&0&0&0\\0&-4&0&0\\0&0&0&0\\0&0&0&1\end{bmatrix}$$

The following is not a diagonal matrix because it has non-zero values on the wrong diagonal:
$$\begin{bmatrix}0&0&3\\0&-4&0\\1&0&0\end{bmatrix}$$

In graphics^[In some non-graphics contexts non-square diagonal matrices are permitted], we'd say the following is not a diagonal matrix because it is not square:
$$\begin{bmatrix}3&0&0&0\\0&-4&0&0\\0&0&1&0\end{bmatrix}$$
:::

An identity matrix is a diagonal matrix with 1 as the value on its main diagonal.
An identity matrix is often written as $I$, and often called *the* identity matrix
even though there are several of them (one for each square matrix size).

Two vectors $\vec x$ and $\vec y$ are said to be conjugate with respect to a matrix $A$ if $\left(\vec x\right) \cdot \left(A \vec y\right) = 0$.
If $A = I$, conjugate is a synonym for orthogonal or perpendicular.
Note that "conjugate" is also a common term for complex numbers and [quaternions](quaternions.html) with a different meaning in those contexts.

An orthogonal matrix is a square matrix with the property that $\forall \vec x \;.\; \|A \vec x\| = \|\vec x\|$.
Each row of an orthogonal matrix is a unit vector that is orthogonal to all other rows.
Each column of an orthogonal matrix is a unit vector that is orthogonal to all other columns.
Each orthogonal matrix is either a rotation matrix or a reflection matrix.
If $A$ is orthogonal, then $A^T A = A A^T = I$.
"Orthogonal matrix" and "real-valued unitary matrix" are synonyms.

Every matrix can be written as $A = U S V^T$ where $U$ and $V$ are both orthogonal matrices
and $S$ is a diagonal matrix.
This is called the singular value decomposition of $A$.
The values on the main diagonal of $S$ are called $A$'s singular values.

The condition number of a matrix is the ratio of its largest singular value to its smallest singular value.
The farther from 1 the condition number of a matrix $A$ is, the less effective (less efficient and/or less precise) almost all algorithms using $A$ become.
The condition number of any orthogonal matrix is exactly 1, making them computationally optimal in many situations.

Every matrix also has an eigendecomposition,
based on eigenvalues and eigenvectors;
this is somewhat like the singular value decomposition
and can be easier to compute, but it generally has complex numbers in it
and is rarely used in graphics.

The inverse of a square matrix $A$ is written $A^{-1}$ and has the property that $A^{-1}A = A^{-1}A = I$.
$A$ has an inverse if and only all of its singular values are non-zero.


<details class="example"><summary>Javascript code implementing some of these operators</summary>
WebGL2 assumed 4×4 matrices in column-major order; this code only works for that specific case.
```js
const m4row = (m,r) => new m.constructor(4).map((e,i)=>m[r+4*i])
const m4rowdot = (m,r,v) => m[r]*v[0] + m[r+4]*v[1] + m[r+8]*v[2] + m[r+12]*v[3]
const m4col = (m,c) => m.slice(c*4,(c+1)*4)
const m4transpose = (m) => m.map((e,i) => m[((i&3)<<2)+(i>>2)])
const m4mul = (...args) => args.reduce((m1,m2) => {
  if(m2.length == 4) return m2.map((e,i)=>m4rowdot(m1,i,m2)) // m*v
  if(m1.length == 4) return m1.map((e,i)=>m4rowdot(m2,i,m1)) // v*m
  let ans = new m1.constructor(16)
  for(let c=0; c<4; c+=1) for(let r=0; r<4; r+=1)
    ans[r+c*4] = m4rowdot(m1,r,m4col(m2,c))
  return ans // m*m
})
```
</details>


