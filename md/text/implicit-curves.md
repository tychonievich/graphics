---
title: Rasterizing Polynomial Curves
summary: How circles, parabolas, and so on can be drawn almost as easily as lines.
...

# Implicit curves

Remember conic sections from algebra class?
Circles, ellipses, parabolas, and hyperbolas:
the four types of curves you can get from an expression of the form
$$Ax^2 + Bxy + Cy^2 + Dx + Ey + F = 0$$
We could generalize that (and depending on your algebra class you might have) into the form
$$P(x,y) = 0$$
where $P$ is a polynomial function.
Curves expressed as $f(x,y) = 0$ for some function $f$ are called **implicit curves**, and if $f$ is a polynomial they are called **implicit polynomial curves**.

A slight generalization of the formulation
$$P(x,y) \ge 0$$
allows us to meaningfully define the implicit curve as the boundary between two regions: areas where $P$ is positive and areas where it is negative.
As we'll see, that generalization will simplify some of our algorithm design.

We can write algorithms that rasterize implicit polynomial curves directly
in a very efficient way using two parts:

1. We want to *evaluate* the function $P$ at integer $x$ and $y$ coordinates (i.e., pixel centers) efficiently.
    In practice, "efficiently" means "with just additions, no multiplications".
    We'll achieve that using a little-taught discrete variant of a derivative called a "finite difference".

2. We want to *identify* the border between the two regions with as few evaluations of $P$ as possible. We'll achieve that by walking borders in a specific way.

The solutions we'll find for these will turn out to encompass the Bresenham line-drawing algorithm as the special case when $P$ is linear.

# Finite Differences

We have a [larger writeup on finite differences](finite-differences.html);
we present here a summary.

The first finite difference in $x$ of $f$ is defined to be
$$f_x(x,y) \triangleq f(x+1,y) - f(x,y)$$
The finite difference in $y$, $f_y$ is defined similarly.

The finite difference of a polynomial is always 1 lower in degree than the original polynomial,
so if $f$ is cubic in $x$ then $f_x$ is quadratic.
We can continue this until we get a constant:
a cubic $f$ means a linear $f_{xx}$ and constant $f_{xxx}$.

:::example
Consider the quadratic function
$f(x,y) = 2x^2 + xy - y^2 - 4x + 2y + 5$.
Evaluating that at a few adjacent integers we get
$$\begin{array}{c|c:c:c}
   &x=0&x=1&x=2\\\hline
y=0& 5 & 3 & 5' \\\hdashline
y=1& 6 & 5''' &   \\\hdashline
y=2& 5'' &   &   \\
\end{array}$$
The primes are to help distinguish between the four $5$s in the results.

$f(0,0)$ is thus $5$.

Subtracting a few cells above gives us
$f_x(0,0) = 3-5 = -2$
and 
$f_y(0,0) = 6-5 = 1$.

To get $f_{xx}(0,0) = f_x(1,0)-f_x(0,0)$
we need $f_x(1,0) = 5'-3 = 2$,
meaning $f_{xx}(0,0) = 2-(-2) = 4$.

Likewise, $f_y(0,1) = 5''-6 = -1$
meaning $f_{yy}(0,0) = -1-1 = -2$.

$f_{yx}(0,0) = $f_y(1,0)-f_y(0,0)$
meaning we need $f_y(1,0) = 5'''-3 = 2$
for $f_{yx}(0,0) = 2-1 = 1$.

Likewise, $f_{x}(0,1) = 5'''-6 = -1$
meaning $f_{xy}(0,0) = -1-(-1) = 1$.

Note that $f_{xy} = f_{yx}$ is not just a coincidence: this always happens.
:::

Mixed finite differences do not depend on differencing order.
$$\begin{split}
f_{xy}(x,y) &= \big(f(x+1,y+1) - f(x,y+1)\big) - \big(f(x+1,y) - f(x,y)\big)
\\
&= f(x+1,y+1) - f(x,y+1) - f(x+1,y) + f(x,y)
\\
&= f(x+1,y+1) - f(x+1,y) - f(x,y+1) + f(x,y)
\\
&= \big(f(x+1,y+1) - f(x+1,y)\big) - \big(f(x,y+1) - f(x,y)\big) = f_{yx}(x,y)
\end{split}$$

Rearranging the defining function shows us that we can use finite differences to evaluate a function at adjacent points using just a few additions:
$$\begin{split}
f(x+1,y) &= f(x,y) + f_x(x,y)\\
f(x-1.y) &= f(x,y) - f_x(x-1,y)
\end{split}$$

:::example
Suppose we know that at point $(5,9)$ the quadratic function $f$ and its finite differences are

$$\begin{matrix}
f=5&f_x=-2&f_{xx}=4\\
f_y=1&f_{xy}=1&\\
f_{yy}=-2&&\\
\end{matrix}$$

We can find values at $(6,9)$ by adding $x$ differences to $(5,9)$:
$$\begin{matrix}
\mathbf{3}&\mathbf{2}&4\\
\mathbf{2}&1&\\
-2&&\\
\end{matrix}$$

We can find values at $(6,10)$ by adding $y$ differences to $(6,9)$:
$$\begin{matrix}
\mathbf{5}&\mathbf{3}&4\\
\mathbf{0}&1&\\
-2&&\\
\end{matrix}$$

We can find values at $(5,10)$ by subtracting $x$ differences from $(6,10)$:
$$\begin{matrix}
\mathbf{6}&\mathbf{-1}&4\\
\mathbf{-11}&1&\\
-2&&\\
\end{matrix}$$
Note that subtractions are evaluated with differences first: $f_x = 3-4 = -1$ first, then $f = 5-(-1) = 6$ using the $-1$ we just created.
:::

Thus, we can evaluate a polynomial function at integer coordinates
evaluating the full polynomial a few times up front
and then doing just a few additions per additional value desired.


# Drawing Curves

Suppose I am given an arbitrary implicit polynomial curve (of known degree) and asked to draw it.

First, we need some point on the edge of the polynomial.
This might be explicitly derivable (e.g., we can find a point on the edge of a circle by adding its radius in $x$ to its center)
or might be provided (e.g., we might be asked to draw a curve conencting two points);
if neither of those is the case we'll have to search for a starting point.

Given a point on the border, use finite differences to evaluate a 2×2 square of function values.
Because it's a border, some will be positive and some won't.
We then use finite differences to walk the 2×2 box along the border:
if we step and get two new values with the same sign, we step in a perpendicular direction next;
if we step and get two new values with different signs, we step in that same direction again next.

This process is not truly general:
implicit polynomials curves could have several discontinuous regions (e.g. hyperbola) and if the curve has interesting details smaller than a pixel the curve following could get confused.
However, for any given class of polynomial curves those cases can be analyzed in advance and work-around defined.

:::example
Drawing Circles

In 1967 Michael Pitteway published an algorithm for drawing conic sections, comparing his work to Jack Bresenham's 1962 line drawing algorithm.
20 years later it was common to call the circle-drawing part of Pitteway's work the "Bresenham circle drawing algorithm", though it's not clear to me why.

Given a circle with integer center $(c_x, c_y)$ and radius $r$,

- start at $(c_x-r, c_y)$
- use symmetry: any time you draw $(c_x-a,c_y+b)$ also draw all other combinations of $(c_x\pm a,c_y\pm b)$ and $(c_x\pm b, c_y \pm a)$
- hence, only step up one octant of the circle, from $(c_x-r, c_y)$ to $\left(c_x-\frac{r}{\sqrt{2}}, c_y+\frac{r}{\sqrt{2}}\right)$

The circle equation is $(x-c_x)^2 + (y-c_y)^2 - r^2 = 0$.
The initial finite differences are

- $f(c_x-r,c_y) = 0$
- $f_x(c_x-r,c_y) = -2r+1$
- $f_y(c_x-r,c_y) = 1$
- $f_{xx} = f_{yy} = 2$

We can freely multiply that entire set by any constant we want.
If $r$ is a rational number, it is common to multiply by its denominator to provide integer arithmetic.

We proceed as follows:

1. While $f_x \ge f_y$ (i.e., we haven't passed the 45° point yet)
    1. Draw the point
    2. Step in $y$ by
        - $y += 1$
        - $f += f_y$
        - $f_y += f_{yy}$
    3. If $f > 0$ we exited the circle, so step in $x$ by
        - $x += 1$
        - $f += f_x$
        - $f_x += f_{xx}$
    
This will draw pixels that are on the inside of the border of the circle.
To draw pixels that approximate the border, we can use the "midpoint" algorithm by initialize the differences for a circle with radius $r+\frac{1}{2}$ instead.
$f(-r-\frac{1}{2},0)=-r-\frac{1}{4}$ and $f_x(-r-\frac{1}{2},0) = -2r$;
after multiplying by $4$ to get rid of the denominator that gives initial finite differences of

- $f(c_x-r,c_y) = -r-1$
- $f_x(c_x-r,c_y) = -8r$
- $f_y(c_x-r,c_y) = 4$
- $f_{xx} = f_{yy} = 8$
:::
