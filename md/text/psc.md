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

- Create inequalities that are positive only inside the triangle, and evaluate them at every (plausible) pixel.
    
    These approaches minimize up-front work per triangle at the cost of more work per pixel, making them preferable for small triangles.
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

# Motivation {#math}

To know what pixels a triangle covers,
three of the coordinates of the vertices are important:
$x$, $y$, and $w$.
Other coordinates have value ($z$ for the depth buffer, $s$ and $t$ for textures, etc)
but we'll come back to them later on.

Each edge of a triangle is a straight line on the 2D screen.
In 2D, a straight line has the equation $Ax + By + C = 0$,
or for homogeneous coordinates $Ax + By + Cw = 0$.

Points on difference sides of a 2D line have different signs in this equation:
$Ax + By + Cw$ is positive on one side of the line and negative on the other side.

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

If we know the coefficients of these three line equations
then telling if a pixel was inside of outside of a triangle
is a 3×3 matrix-vector multiply and checking three sign bits.

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
We can pick any positive $k$ we want, and will just consider to be some positive constant for now.

Re-writing the system of equations in matrix form gives us
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
\tag{1}
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
\begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}
=
\begin{bmatrix}k&0&0\\0&k&0\\0&0&k\end{bmatrix}
=
k \mathbf{I}
$$
This looks like the definition of a matrix inverse:
$$
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
=
k \begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}^{-1}
$$

Matrix inverse is a tricky topic in general because of the possibility of singular matrices
and the efficiency of complicated algorithms at scale,
but for a 3×3 matrix there's a simple equation for it:
$$
\mathbf{M}^{-1} = \begin{bmatrix}x_0&x_1&x_2\\y_0&y_1&y_2\\w_0&w_1&w_2\end{bmatrix}^{-1}
=
\frac{1}{\operatorname{det}(\mathbf{M})}
\begin{bmatrix}
y_1 w_2 - y_2 w_1 & x_2 w_1 - x_1 w_2 & x_1 y_2 - x_2 y_1 \\
y_2 w_0 - y_0 w_2 & x_0 w_2 - x_2 w_0 & x_2 y_0 - x_0 y_2 \\
y_0 w_1 - y_1 w_0 & x_1 w_0 - x_0 w_1 & x_0 y_1 - x_1 y_0
\end{bmatrix}
$$
Note that each row of $\mathbf{M}^{-1}$ is the cross product of two columns of $\mathbf{M}$.

That $\frac{1}{\operatorname{det}(\mathbf{M})}$ term is a bit of an annoyance,
but if we make $k = \operatorname{det}(\mathbf{M})$ it conveniently vanishes^[If the three vertices are colinear, then $\mathbf{M}$ will be singular and $\operatorname{det}(\mathbf{M}) = 0$. In this case no pixels should be shown and the triangle skipped. Computing $\operatorname{det}(\mathbf{M})$ can be done by taking the dot product of the first column of $\mathbf{M}$ and the first row of the adjugate matrix.].
The matrix we're left with,
$$
\begin{bmatrix}A_0&B_0&C_0\\A_1&B_1&C_1\\A_2&B_2&C_2\end{bmatrix}
=
\begin{bmatrix}
y_1 w_2 - y_2 w_1 & x_2 w_1 - x_1 w_2 & x_1 y_2 - x_2 y_1 \\
y_2 w_0 - y_0 w_2 & x_0 w_2 - x_2 w_0 & x_2 y_0 - x_0 y_2 \\
y_0 w_1 - y_1 w_0 & x_1 w_0 - x_0 w_1 & x_0 y_1 - x_1 y_0
\end{bmatrix}
$$
is called the "adjugate matrix"^[Or sometimes the transpose of the adjugate matrix; confusingly, whether the adjugate refers to this matrix or its transpose varies by between sources.].

# Finding pixels {#basic}

The pixels inside a triangle can be found as follows:

:::algorithm
Pixel coverage

1. Find the adjugate matrix of the matrix $\mathbf{M}$ made from the $x$, $y$, and $w$ coordinates of the three vertices
2. If the matrix is singular, there are no pixels in this triangle
3. For <mark>every pixel</mark> $(x,y)$,
    a. Compute $\vec s = \mathbf{M} [x,y,1]^{T}$
    b. If all coordinates of $s$ are <mark>positive</mark>, the pixel is inside the triangle

See notes for more on "every pixel" and "positive".
:::

We still need to find the other coordinates of the points this discovers are inside the triangle,
but there are two other issues (highlighted above) to resolve as well.

Checking *every pixel* coordinate is very inefficient:
most triangles cover only a very small percentage of the screen.
Taking a bounding box of the triangle
(by finding the minimum and maximum of $x/w$ and $y/w$ for the three vertices)
can save significant time, but still means that long thin diagonal slivers
might have a very large bounding box but cover very few triangles.
Recursive approaches
that rasterize at a low resolution
to find squares of pixels to rasterize at full resolution
can make large diagonal slivers faster,
at the expense of extra steps for every triangle.


Checking for coordinates with *positive* coordinates finds pixels inside a triangle,
but what about pixels exactly on a pixel edge
where the coordinate will be 0?
The common use-case of triangles is subdividing a surface into many adjoining triangles:
if we leave out on-edge pixels then there will be some missing pixels between these triangles
while if we include them then there will be some pixels draw twice, which will be visible if the triangles are translucent.
We need a tie-breaker that will ensure each such pixel is drawn exactly once.
A common tie-breaker is to consider a coordinate $s_i$ to mean the point is inside the triangle if

- $s_i > 0$, or
- $s_i = 0$ and $A_i > 0$, or
- $s_i = 0$ and $A_i = 0$ and $B_i > 0$

<details class="aside"><summary>Why this tie-breaker?</summary>

Consider an pixel on an edge between two triangles.
We want one triangle to draw that pixel and the other not to.

Because the edge divides the two triangles, what is on the positive side for one will be on the negative side for the other.

If $A_i$ is positive, that means that increasing $x$ makes the equation more positive
meaning this edge is on the left side of the triangle, and hence must be on the right side of its adjoining triangle.

If $A_i$ is zero, then the edge is perfectly horizontal,
so we check $B_i$ to see if the edge is on the top or bottom side of the triangle for a similar final tie breaking.

</details>

# Finding other coordinates

Every point on a triangle is a weighted average of its vertices,
meaning
$$\vec p = \lambda_0 \vec v_0 + \lambda_1 \vec v_1 + \lambda_2 \vec v_2$$
where the $\lambda_i$ are called the **barycentric coordinates** of point $\vec p$
and have the properties of all being non-negative and summing to 1.

Because we used the same $k$ for all three plane equations in (1),
the vector $\vec s$ found in [the pixel coverage algorithm](#basic)
is a linear multiple of $\vec \lambda = (\lambda_0, \lambda_1, \lambda_2)$.
However, because we are using homogeneous coordinates,
what multiple of $\vec \lambda$ it is will vary from one pixel to another.
Fortunately, we knew that $\vec \lambda$ has to sum to 1,
so $\vec \lambda = \vec s / \sum \vec s$.

For the most coordinates, the $\lambda$-based average of the vertex coordinates
gives exactly the perspective-correct interpolation of that coordinate that we want;
however, for $z$ it does not.
Projection matrices modify the $x$, $y$, $z$, and $w$ coordinates
to map a frustum of $\left({x \over w}, {y \over w}, {z \over w}\right)$ into a linear box.
The use of homogeneous line equations
has handled the $x \over w$ and $y \over w$ parts for us,
but we still need ${z \over w}$ to complete the frustum.
Fortunately, we can get both $z$ and $w$ using $\vec \lambda$,
so we can also get $z \over w$ with an additional division.

<details class="aside"><summary>What if I don't divide $z$ by $w$?</summary>

If you forget to divide $z$ by $w$, at first things will look correct.
After all, $z$ doesn't impact where things appear on the screen
and generally doesn't impact color either (unless you add something like fog).

Not dividing $z$ by $w$ means that all shapes will be curved in 3D space:
projecting from a frustum to a box in $x$ and $y$ but not in $z$ makes lines into hyperbolas.
That will make the near and far clipping planes cut them on a curve, not on a straight line,
and for some inputs can cause the depth buffer to put the wrong shape's pixels in front.

Additionally, $z / w$ is important to create a visually-uniform depth buffer
when the depth buffer is made of fixed-point numbers, as it is on graphics hardware.

</details>

# Clipping

The top, bottom, left, and right clipping planes are handled implicitly in this approach
by only checking the plane equations for pixels that are on screen.

The near and far clipping planes are handled per pixel
by ensuring that $0 \le z \le 1$,
rejecting any pixel for which that is not true.

Other clipping planes can be handled on a per-pixel level similarly,
checking the coordinates of the pixel against the equation of the plane. 
