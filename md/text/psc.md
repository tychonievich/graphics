---
title: Parallel Scan Conversion
summary: Rasterizing triangles without loop conditions
...

There are two broad families of approaches to rasterizing triangles.

- Rasterize the lines along the triangle's edges, then the horizontal scanlines connecting the edges.
  
    These approaches include the DDA and Bresenham algorithms.
    They minimize work per pixel at the cost of more up-front work per triangle, making them preferably for large triangles.
    They have loops with dynamically-computed iteration counts and accumulators,
    making them difficult to parallelize in hardware.

    We have a [separate text page](dda.html) about this approach.    

- Create inequalities that are positive only inside the triangle, and evalaute them at every (plausible) pixel.
    
    These approaches minimize up-front work per triangle at the cost of most work per pixel, making them preferable for small triangles.
    They perform independent work at each pixel,
    making them easy to parallelize in hardware.

    These approaches do not have generally accepted names,
    but include [Fuchs et al 1985](https://dl.acm.org/doi/10.1145/325165.325205),
    [Pineda 1988](https://dl.acm.org/doi/10.1145/54852.378457),
    and [Olano and Greer 1997](https://dl.acm.org/doi/10.1145/258694.258723),
    among others.
    This page primarily focuses on the approach discussed by Olano and Greer,
    which I've also seen replicated without citation
    in several other places.

# Algorithm motivation

To know what pixels a triangle covers,
three of the coordinates of the vertices are important:
$x$, $y$, and $w$.
Other coordinates have value ($z$ for the depth buffer, $s$ and $t$ for textures, etc)
but we'll come back to them later on.

Each edge of a triangle is a straight line on the 2D screen.
In 2D, a straight line has the equation $Ax + By + C = 0$,
or for homogeneous coordinates $Ax + By + Cw = 0$.
Pints on difference sides of a 2D line have different signs in this equation,
meaning $Ax + By + Cw > 0$ tells us all the points on one side.
The interior of a triangle is on the "inside" side of all three of the triangle's edges.
We can set up the line equations to have either side be positive;
let's arbitrarily pick the inside as positive and the outside as negative.
Thus, a point $(x,y,w)$ is inside a triangle only if
$$\begin{split}
A_0x + B_0 y + C_0 w &> 0\\
A_1x + B_1 y + C_1 w &> 0\\
A_2x + B_2 y + C_2 w &> 0\\
\end{split}$$
Or, written as a matrix,
$$
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
\begin{bmatrix}x\\y\\w\end{bmatrix}
>
\begin{bmatrix}0\\0\\0\end{bmatrix}
$$
If we could find the coefficients of these three line equations
then telling if a pixel was inside of outside of a triangle
would be as simple as a 3×3 matrix-vector multiply and checking three sign bits.

Consider one of the line equations,
$A_0x + B_0 y + C_0 w > 0$.
Let's call this the line that does not pass through vertex 0,
meaning it does pass through vertices 1 and 2.
Vertex 0 is on the inside side of this edge, so the equation should be positive for it.
That means
$$\begin{split}
A_0 x_0 + B_0 y_0 + C_0 w_0 &= k > 0\\
A_0 x_1 + B_0 y_1 + C_0 w_1 &= 0\\
A_0 x_2 + B_0 y_2 + C_0 w_2 &= 0\\
\end{split}$$
This is three equations but has four unknowns because of that pesky $k > 0$.
We can pick any positive $k$ we want;
1 is a common choice, but not necessary.

Re-writing in matrix form gives us
$$
\begin{bmatrix}A_0&B_0&C_0\end{bmatrix}
\begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}
=
\begin{bmatrix}k\\0\\0\end{bmatrix}
$$
Repeating with the other edges and vertices (and picking the same $k$ each time to make a future step simpler) gives us similar equations:
$$
\begin{bmatrix}A_1&B_1&C_1\end{bmatrix}
\begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}
=
\begin{bmatrix}0\\k\\0\end{bmatrix}
$$
and
$$
\begin{bmatrix}A_2&B_2&C_2\end{bmatrix}
\begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}
=
\begin{bmatrix}0\\0\\k\end{bmatrix}
$$
Combining all of those together, we get
$$
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
\begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}
=
\begin{bmatrix}k&0&0\\0&k&0\\0&0&k\end{bmatrix}
$$
If we picked $k=1$, this would be the defining equation for a matrix inverse; that is
$$
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
=
\begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}^{-1}
\qquad\text{if }k = 1
$$
Other $k$ would just make a scalar multiple of this equation, so
$$
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
=
k \begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}^{-1}
$$

Matrix inverse is a tricky topic in general because of the possibility of singular matrices
and the efficiency of complicated algorithms at scale,
but for a 3×3 matrix there's a simple equation for it:
$$
M^{-1} = \begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}^{-1}
=
\frac{1}{\operatorname{det}(M)}
\begin{bmatrix}
y_1 w_2 - y_2 w_1 & x_2 w_1 - x_1 w_2 & x_1 y_2 - x_2 y_1 \\
y_2 w_0 - y_0 w_2 & x_0 w_2 - x_2 w_0 & x_2 y_0 - x_0 y_2 \\
y_0 w_1 - y_1 w_0 & x_1 w_0 - x_0 w_1 & x_0 y_1 - x_1 y_0
\end{bmatrix}
$$
Note that each row of $M^{-1}$ is the cross product of two columns of $M$.

That $\frac{1}{\operatorname{det}(M)}$ term is a bit of an annoyance.
We'd like to make $k = \operatorname{det}(M)$ to get rid of it,
but $\operatorname{det}(M)$ could be 0 if the matrix is singular.

The only way for the matrix to be singular for a triangle
is if the triangle has zero area,
and if that was the case the entire matrix would have 0 entries inside it.
If all of our plane equations are zero
then we'll never find any points where they are greater than 0,
meaning we'll find no pixels in the triangle,
which is the behavior we want anyway.

The matrix we're left with
is
$$
\begin{bmatrix}
y_1 w_2 - y_2 w_1 & x_2 w_1 - x_1 w_2 & x_1 y_2 - x_2 y_1 \\
y_2 w_0 - y_0 w_2 & x_0 w_2 - x_2 w_0 & x_2 y_0 - x_0 y_2 \\
y_0 w_1 - y_1 w_0 & x_1 w_0 - x_0 w_1 & x_0 y_1 - x_1 y_0
\end{bmatrix}
$$
which is formally called the adjoint matrix^[Or sometimes the transpose of the adjoint matrix; confusingly, whether the adjoint refers to this matrix or its transpose varies by between sources.].
