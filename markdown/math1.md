---
title: Math Review
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
$\vec x - \vec y$   $(x_1+y_1, x_2+y_2, \dots, x_n+y_n)$    Vector subtraction or difference, element-wise subtraction
$s \vec x$          $(s x_1, s x_2, \dots, s x_n)$          Scaling, multiplication by a scalar
$\dfrac{\vec x}{s}$ $(x_1/s, x_2/s, \dots, x_n/s)$          Scaling, division by a scalar
$\vec x\cdot\vec y$ $x_1y_1 + x_2y_2 + \cdots + x_ny_n)$    Dot product, inner product; also written $\vec x^{T} \vec x$; is a scalar equal to $\|\vec x\| \|\vec y\| \cos(\theta)$
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

# Matrices

A matrix is a grid of numbers.
They can be seen as a vector of vectors in two ways:
either as a vector of columns or a vector of rows.

The matrix transpose $A^T$ is computed by treating the rows of $A$ as columns and vice-versa.
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

An orthogonal matrix is a square matrix with the property that $\forall \vec x \;.\; \|A \vec x\| = \|\vec x\|$.
Each row of an orthogonal matrix is a unit vectors that is orthogonal to all other rows.
Each column of an orthogonal matrix is a unit vectors that is orthogonal to all other columns.
Each orthogonal matrix is either a rotation matrix or a reflection matrix.
If $A$ is orthogonal, then $A^T A = A A^T = I$.

Every matrix can be written as $A = U S V^T$ where $U$ and $V$ are both orthogonal matrices
and $S$ is a diagonal matrix.
This is called the singular value decomposition of $A$.
The values on the main diagonal of $S$ are called $A$'s singular values.

Every matrix also has an eigendecomposition,
based on eigenvalues and eigenvectors;
this is somewhat like the singular value decomposition
and can be easier to compute, but it generally has complex numbers in it
and is rarely used in graphics.

The inverse of a square matrix $A$ is written $A^{-1}$ and has the property that $A^{-1}A = A^{-1}A = I$.
$A$ has an inverse if and only all of its singular values are non-zero.

# Differential Equations

Many graphics problems include differential equations.
They have the general form "the rate of change of $x$ is some function of $x$".
For most graphics simulations, the following all hold:

- We describe the differential equation locally.
    For example, the motion of each bit of cloth depends on its state and the states of the nearby bits of cloth.

- But the local bit chain together to form non-local results.

- And the resulting equation has no closed-form solution:
    the solution families you learn about in differential equations class don't work.

- So we solve them by
    1. Making a linear approximation of the equations at the current time.
    
        Because of Newton's Third Law, the resulting matrix is usually symmetric.
        
        Because motion is smooth and the linearization of smooth systems is convex, the resulting matrix is positive-definite; that is, all its eigenvalues are positive.
        
        Because the equations were local, the resulting matrix is sparse;
        that is, most of its entries are zero.
        
    2. Solve the linear system.
    
        The Conjugate Gradient method is particularly good at solving sparse symmetric positive-definite problems.
    
    3. Use the solution to bump up to a slightly greater time

There are two approximations being used here:
first, we treat complicated math as if it were linear,
and, second, we use a bunch of small steps in time instead of a continuous model of time.
These two are related:
as each time step length approaches zero, the linear solution approaches the correct solution.

# Implementing a sparse matrix solver

Given a linear system $A \vec x = \vec b$,
where $A$ is sparse, symmetric, and positive-definite:

1. Store $A$ well. The operation we'll do with $A$ is $A \vec v$ for various $\vec v$,
    so we need a storage that makes multiplication by a vector fast.
    [LIL](https://en.wikipedia.org/wiki/Sparse_matrix#List_of_lists_(LIL)) is the easiest such storage technique to code:
    A matrix is a list of rows
    and each row is a list of (column index, value) pairs for the non-zero entries in that row.

2. Optionally, precondition the system.
    Instead of solving $A \vec x = \vec b$,
    solve $E^{-1}A(E^{-1})^T \vec y = E^{-1}\vec b$ and $\vec y = E^T x$.
    
    Preconditioning is a topic we'll not really discuss in this class.
    A good $E$ can make the algorithm converge faster, but that's all they are: an optimization.

3. Use the following algorithm, given an initial estimate $\vec x$, iteratively improves it:

    1. $\vec r = \vec b - A \vec x$ <small style="padding-left: 1em">// the residual vector; stores the error of the current estimate</small>
    
    1. $\vec p = \vec r$ <small style="padding-left: 1em">// the direction we'll move $\vec x$ in to improve it</small>
    
    1. $\rho = \vec r \cdot \vec r$ <small style="padding-left: 1em">// the squared magnitude of $\vec r$</small>
    
    1. repeat until $\rho$ is "sufficiently small":
        
        1. $\vec a_p = A \vec p$
        
        1. $\alpha = \dfrac{\rho}{\vec p \cdot \vec a_p}$ <small style="padding-left: 1em">// how far to move in the $\vec p$ direction</small>
    
        1. $\vec x \mathrel{+}= \alpha \vec p$ <small style="padding-left: 1em">// move</small>
        
        1. $\vec r \mathrel{-}= \alpha \vec a_p$ <small style="padding-left: 1em">// update the error</small>
        
        1. $\rho' = \vec r \cdot \vec r$
        
        1. $\beta = \dfrac{\rho'}{\rho}$ <small style="padding-left: 1em">// used to ensure each direction is conjugate with all previous directions</small>
        
        1. $\rho := \rho'$ <small style="padding-left: 1em">// update the error squared magnitude</small>
        
        1. $\vec p \mathrel{\times}= \beta$ <small style="padding-left: 1em">// update the direction for the next step</small>
        
        1. $\vec p \mathrel{+}= \vec r$ <small style="padding-left: 1em">// update the direction for the next step</small>


