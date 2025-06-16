---
title: Finite Differences
summary: An efficient technique for evaluating polynomials on a grid.
...


# Horner's Method: Polynomial at a Point

Multiplications are more expensive to compute than additions.
Additionally, rounding error can accumulate when additions and multiplications are mixed incorrectly.
To evaluate a polynomial $a_n x^n + a_{n-1} x^{n-1} + \cdots + a_2 x^2 + a_1 x + a_0$
at some specific $x$,
the most efficient and accurate solution is to use Horner's Method:
re-write the polynomial as $((\cdots((a_n) x + a_{n-1}) x + \cdots + a_2) x + a_1) x + a_0$
and evaluate left-to-right as $n$ multiplications and $n$ additions.
On hardware with a fused-multiply-add instruction, this reduces further to just $n$ FMA operations.

# Finite Difference

The **finite difference** of some function $f(x)$ at $x$ is defined to be $\dfrac{f(x+b)-f(x+a)}{b-a}$.
For our purposes, we will always use $b=1$ and $a=0$ to get the simpler $f(x+1)-f(x)$,
which is sometimes called "the forward finite difference" for $f$ at $x$,
and write it as $f_x(x)$.

The forward finite difference of the polynomial $f(x) = 7 x^3 - 2 x^2 - 8x + 3$
can be evaluated by expanding $f(x+1)-f(x)$ and combining like terms
to get $f_x(x) = 21x^2 + 17x - 3$.
Taking the forward finite difference of that, we get $f_{xx}(x)=42x+38$,
and the forward finite difference of that is simply $f_{xxx} = 42$.
The forward finite difference of a constant like $42$ is always $f_{xxxx} = 0$.

Just as in this example, the finite difference of any polynomial is a polynomial of one lesser degree.

# Difference addition

If we wish to evaluate a polynomial at a sequence of adjacent integer arguments,
we can use forward finite differences to compute these points very efficiently.
In particular, if we know $f(x)$ and $f_{x}(x)$,
then we can compute $f(x+1) = f(x) + f_{x}(x)$.
If $f_{x}$ is a constant we can keep adding that same value to get $f(x+2)$, $f(x+3), and so on.
If it is not a constant than it is another polynomial we can use this same method on to find the sequence of $f_{x}(x)$s we need.

:::example
Consider the 1st-order polynomial $f(x) = 42x + 38$.
Use Horner's rule, we find $f(-5) = -172$
and $f(-4) = -130$.

Subtracting these, we find $f_{x}(-5) = 42$.
Because $f$ is linear, $f_{x}$ is constant.

We now find other values of $f$:

- $f(-3) = f(-4) + f_{x} = -130+42 = -88$
- $f(-2) = f(-3) + f_{x} = -88+42 = -46$
- $f(-1) = f(-2) + f_{x} = -46+42 = -4$
- $f(0) = f(-1) + f_{x} = -4+42 = 38$

We can also move backwards:

- $f(-6) = f(-5) - f_{x} = -172-42 = -214$
- $f(-7) = f(-6) - f_{x} = -214-42 = -266$
:::

:::example
Consider the 2nd-order polynomial $f(x) = 21x^2 + 17x - 3$.
Use Horner's rule, we find 

- $f(-5) = 437$
- $f(-4) = 265$
- $f(-3) = 135$

Subtracting these, we find

- $f_{x}(-5) = -172$
- $f_{x}(-4) = -130$

and subtracting those we get

- $f_{xx}(-5) = 42$.

Because $f$ is quadratic, $f_{x}$ is linear and $f_{xx}$ is constant.

Now, we know that $f(-2) = f(-3) + f_{x}(-3)$, but we don't yet know $f_{x}(-3)$.
But we know $f_{x}(-3) = f_{x}(-4) + f_{xx} = -130 + 42 = -88$,
which means $f(-2) = f(-3) - 88 = 138 - 88 = 50$.
And we got that with just two additions, no multiplications.
Similarly

 $x$     $f_{xx}(x)$                        $f_{x}(x)$         $f(x)$
-----   --------------------------------   ----------------   --------
$-5$    $42$                                $-172$              $437$
$-4$    $42$                                $-130$              $265$
$-3$    $42$                                $-88$               $135$
$-2$    $42$                                $-46$               $47$
$-1$    $42$                                $-4$                $1$
$0$                                         $38$                $-3$
$1$                                                             $35$
:::

:::example
Let $f(x) = 7 x^3 - 2 x^2 - 8x + 3$.
Evaluating using Horner's rule, we get

- $f(0) = 3$
- $f(1) = 0$ meaning $f_{x}(0) = -3$
- $f(2) = 35$ meaning $f_{x}(1) = 35$ and $f_{xx}(0) = 38$
- $f(3) = 150$ meaning $f_{x}(2) = 115$ and $f_{xx}(1) = 80$ and $f_{xxx}(0) = 42$

We can now find $f$ larger $x$ by adding finite differences:

 $x$     $f_{xxx}(x)$   $f_{xx}(x)$    $f_{x}(x)$     $f(x)$
----    -------------- -------------  ------------   --------
$0$     $42$            $38$            $-3$          $3$
$1$     $42$            $80$            $35$          $0$
$2$     $42$            $122$           $115$         $35$
$3$     $42$            $164$           $237$         $150$
$4$     $42$                            $401$         $387$
$5$     $42$                                          $788$

And at smaller $x$ by subtracting finite differences

 $x$     $f_{xxx}(x)$   $f_{xx}(x)$    $f_{x}(x)$     $f(x)$
----    -------------- -------------  ------------   --------
$0$     $42$            $38$            $-3$          $3$
$-1$    $42$            $-4$            $1$           $2$
$-2$    $42$            $-46$           $47$          $-45$
$-3$    $42$            $-88$           $135$         $-180$
:::

# Summary

The method of finite differences lets us evaluate a single-variable polynomial efficiently at integer arguments.
All we need to do is

- Evaluate the $n$th-order polynomial at $n+1$ adjacent arguments.
    In the last example above, these were $(3,0,35,150)$.
    We'll discard these numbers shortly.
- Subtract, then subtract again, and so on to get a list of finite differences.
    In the last example above, these were $(3,-3,38,42)$.
    These numbers we'll keep, and the first one is the function at the first evaluated $x$.
- To increase $x$, we **add** values in the difference list **left-to-right**:
    $(3-3,-3+38,38+42,42) = (0,35,80,42)$.
- To decrease $x$, we **subtract** values in the difference list **right-to-left**:
    $(?,?,38-42,42) \rightarrow (?,-3-(-4),-4,42) \rightarrow (3-1,1,-4,42) = (2,1,-4,42)$.

# Multivariate finite differences

This also generalizes naturally to multivariate polynomials.
If we have $f(x,y)$ we can find both $f_x(x,y) = f(x+1,y) - f(x,y)$
and $f_y(x,y) = f(x,y+1) - f(y)$.
Conveniently, the order of differencing does not matter:

$$\begin{array}{rcl}
f_{yx}(x,y) &=& f_x(x,y+1) - f_x(x,y) \\
            &=& \big(f(x+1,y+1) - f(x,y+1)\big) - \big(f(x+1,y)-f(x,y)\big) \\
            &=& f(x+1,y+1) - f(x,y+1) - f(x+1,y) + f(x,y) \\
            &=& \big(f(x+1,y+1) - f(x+1,y)\big) - \big(f(x,y+1) - f(x,y)\big) \\
            &=& f_y(x+1,y) - f_y(x,y) \\
            &=& f_{xy}(x,y)
\end{array}$$

:::example
Consider the circle equation $f(x,y) = (x-c_x)^2 + (y-c_y)^2 - r^2$,
so called because $f(x,y) = 0$ is a circle of radius $r$ centered at point $(c_x,c_y)$.
Computing the finite differences, we have:

- $f_x(x,y) = 1+2(x-c_x)$
- $f_{xx}(x,y) = 2$
- $f_y(x,y) = 1+2(y-c_y)$
- $f_{yy}(x,y) = 2$
- $f_{xy}(x,y) = 0$
:::

:::example
Consider drawing a circle of radius 6 centered at (2,3).

We know that $(-4,3)$ is on the circle, and that it is symmetric;
if we can find the points between 0° and 45°, we can mirror them to get the rest of the points.

We find our initial value and differences:

- $f(-4,3) = 0$
- $f_{x}(-4,3) = -11$
- $f_{y}(-4,3) = 1$
- $f_{xx} = f_{yy} = 2$.

Let's abbreviate this as $(f,f_x,f_y)$ so our starting state at $(-4,3)$ is $(0,-11,1)$.

Now we'll repeatedly move up in $y$ and decide if it's better to move right in $x$ or not.

1.  up to $(-4,4)$ gives us $(1,-11,3)$\
    right to $(-3,4)$ would give us $(-10,-9,3)$ but that's further from 0 so let's not\
    plot $(-4,4)$ and its symmetric neighbors.
1.  up to $(-4,5)$ gives us $(4,-11,5)$\
    right to $(-3,5)$ would give us $(-7,-9,5)$ but that's further from 0 so let's not\
    plot $(-4,5)$ and its symmetric neighbors.
1.  up to $(-4,6)$ gives us $(9,-11,7)$\
    right to $(-3,6)$ gives us $(-2,-9,7)$ which is closer to 0 so let's use that\
    plot $(-3,6)$ and its symmetric neighbors.
1.  up to $(-3,7)$ gives us $(5,-9,9)$\
    right to $(-2,7)$ gives us $(-4,-7,9)$ which is closer to 0 so let's use that\
    plot $(-2,7)$ and its symmetric neighbors.
    
    $f_y$ now has larger magnitude than $f_x$, meaning we have reached the 45° point and are done.

The exact details of how we decide to pick between moving in $x$ and not moving depends on if we want to plot points inside, near, or outside the circle.
For inside points, always keep $f(x,y) \le 0$; this is what we'd do to fill it in.
For outside points, always keep $f(x,y) > 0$; this is what we'd do to mask the circle, coloring things outside it.
For nearest points, keep the $f(x,y)$ with the smaller magnitude; this is what we'd do to draw the circle as a single-pixel-width ring.
:::
