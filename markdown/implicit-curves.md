---
title: Implicit curves
...

An implicit curve is defined using an equation of $x$ and $y$
like $x^2 + y^2 = 1$ or ${\sin^2(x) \over \sqrt{y}} = \sqrt[3]{\tan\left({x \over y}\right)}$.
Implicit curves are less common than parametric curves,
such as Bézier curves and B-Splines,
but are still useful for drawing some mathematically-defined shapes like circles.

Implicit surfaces are also common when dealing with blobbies
and rendering particle-based fluids.
This write-up deals primarily with implicit curves in 2D, not implicit surfaces in 3D.

We'll assume the implicit equation is normalized into a form $f(x,y) = 0$.

# Brute-force drawing

A simple brute force algorithm for drawing an implicit curve might look like the following:

    for each pixel (x,y)
        if f(x+0.5,y) and f(x-0.5,y) have different signs
            plot (x,y)
        if f(x,y+0.5) and f(x,y-0.5) have different signs
            plot (x,y)

This will plot an 8-connect line of pixels the curve passes through:

![brute-force results](files/implicit1.svg){style="width:18em"}

But it means evaluating the function 4 tiles at each pixel.
We can actually reduce that to once per pixel with some caching, but still, not very efficient.

# Edge following

We don't need to view every pixel.
Instead, once we find the edge we can follow it.
Basically, we just check the 8 neighboring pixels of each pixel that is plotted.

This

- requires us to keep track of which pixels we've checked (so we don't go around forever)
- doesn't work if there are multiple distinct curve parts (like a hyperbola)
- requires us to find a starting point on the curve

but it can reduce the overall complexity from $O($pixels$)$ to $O($curve length $\times$ data structure complexity$)$, a significant saving in general.

    let queue = [a pixel on edge]
    let visited = [same pixel as queue]
    while queue is not empty
        let p = pop an element from queue
        if f(x+0.5,y) and f(x-0.5,y) have different signs
        or f(x,y+0.5) and f(x,y-0.5) have different signs
            plot (x,y)
            for each (i,j) in (x±1, y) and (x, y±1)
                if (i,j) not in visited
                    put (i,j) in both visited and queue

We can optimize this a little if we assume the curve has no cusps by not checking pointer perpendicular to the direction of the curve, as determined by which "different signs" check was true; and more by picking good data structures for the visited cache (a splay tree is a good choice) and queue (a stack is a good choice),
but it's not too bad as-is.

# Grid walking

If we assume that the curve is smooth and the area it encloses has no narrow bits,
then we can do a more efficient edge following using only constant memory.

To do this, we evaluate the sign of the function at a 2×2 grid of pixels
and move this grid by 1 in either $x$ or $y$ at each step, picking a direction depending on two pieces of data:
what direction we came from last
and how many of the four pixels are positive vs negative.
The rule is simple: exit on the side with different signs that you didn't enter from.

![pixel stepping rules](files/implicit2.svg){style="width:24em"}

The third rule above is a problem case: it can only arise if the shape has a narrow region or cusp,
which grid walking cannot perfectly resolve.
However, picking either "don't cross a positive diagonal" or "don't cross a negative diagonal" (it doesn't matter which one is picked, but it needs to be consistent) will result in sensible, if not perfect, behavior.

This approach doesn't lend itself to drawing an 8-connect boundary line,
but does let us draw the pixels on one side of the curve.
For example, in the following image it will visit the marked pixels;
it can distinguish the red from the blue;
and it knows that the outlined pixels, although visited, where not adjacent to the curve because they were adjacent to two other pixels of the same sign.

![grid walking results](files/implicit3.svg){style="width:18em"}

# Polynomial grid walking

If $f(x,y)$ is a polynomial function, then we can use Bresenham-like tricks to make the grid walking algorithm very computationally efficient
using a grid-spaced analog of derivatives called **finite differences**.
These might be best introduced by example:

:::example
Consider the polynomial $f(x) = 2 x^3 - 4 x^2 + x + 0$.
Let's evaluate it at some regularly-spaced $x$s:

$f(-1)$ $f(0)$  $f(1)$   $f(2)$  $f(3)$  $f(4)$  $f(5)$
------- ------  -------  ------  ------  ------  ------
$-7$    $0$     $-1$     $2$     $21$    $68$    $155$


Now let's find the difference between adjacent entries above


$f(-1)$         $f(0)$          $f(1)$          $f(2)$          $f(3)$          $f(4)$          $f(5)$
------  ----    ------  ----    ------  ----    ------  ----    ------  ----    ------  ----    ------
$-7$            $0$             $-1$            $2$             $21$            $68$            $155$
        $7$             $-1$            $3$             $19$            $47$            $87$

And let's keep going, adding the difference of entries in the last row


$f(-1)$         $f(0)$          $f(1)$          $f(2)$          $f(3)$          $f(4)$          $f(5)$
------  ----    ------  ----    ------  ----    ------  ----    ------  ----    ------  ----    ------
$-7$            $0$             $-1$            $2$             $21$            $68$            $155$
        $7$             $-1$            $3$             $19$            $47$            $87$
                $-8$            $4$             $16$            $28$            $40$
                        $12$            $12$            $12$            $12$
                                $0$             $0$             $0$
                                        $0$             $0$
                                                $0$

Notice that the 4^th^ row is all $12$ and the 5^th^ and subsequent rows are all $0$?
That's not a fluke: for an $n$^th^ order polynomial, the $(n+1)$^th^ row will be constant
and all subsequent rows 0.

Now we can find $f(6)$ with only addition:
we extend the 4^th^ row to have one more 12, then repeatedly add the last entry of the $i$^th^ row to the last entry of the ($i-1$)^th^ row to extend that row

$f(-1)$         $f(0)$          $f(1)$          $f(2)$          $f(3)$          $f(4)$          $f(5)$                  $f(6)$
------  ----    ------  ----    ------  ----    ------  ----    ------  ----    ------  ----    ------      -----       --------
$-7$            $0$             $-1$            $2$             $21$            $68$            $155$                   $155+139=294$
        $7$             $-1$            $3$             $19$            $47$            $87$                $87+52=139$
                $-8$            $4$             $16$            $28$            $40$            $40+12=52$
                        $12$            $12$            $12$            $12$            $12$

Note that that was just 3 additions, rather than the 3 additions and 3 multiplications needed to evaluate a cubic polynomial in general.^[
    How can we evaluate $ax^3+bx^2+cx+d$ with just 3 multiplications and 3 additions?
    By using [Horner's method](https://en.wikipedia.org/wiki/Horner%27s_method):
    $\Big(\big((a)x+b\big)x+c\Big)x+d$.
]
:::

Finite differences have a lot of things they need to be fully described:

- A function $f(x)$.
- There is a 1^st^, 2^nd^, etc finite difference;
    commonly denoted with repeated subscripts, like $f_{xxxx}$ for the 4^th^ finite difference.
- A value at which they are being evaluated, $x=t$;
    commonly denoted with parentheses, like $f_{xx}(3)$ for the 2^nd^ finite difference at $x=3$.
- They are either forward or backward;
    there's no common notation for this, but we'll use an arrow under the symbols, like  $\underrightarrow{f_{xxx}}(t)$ for a forward 3^rd^ difference
    or $\underleftarrow{f_{x}}(t)$ for a backward 1^st^ difference.
- they have a step size, $\Delta$;
    there's no common notation for this, but we'll use a superscript,
    like $\underrightarrow{{f_{xx}}^2}(t)$ for a forward 2^nd^ difference with step-size $2$.

Then

-   The 0^th^ finite difference is simply the function value.

    $\underrightarrow{f^{\Delta}}(t) = \underleftarrow{f^{\Delta}}(t) = f(t)$

-   The $k$^th^ forward difference at $t$
    is the $(k-1)$^th^ forward difference at $t$
    minus the $(k-1)$^th^ forward difference at $t-\Delta$.

    $\underrightarrow{{f_{\Gamma x}}^{\Delta}}(t)
    \triangleq
    \underrightarrow{{f_{\Gamma}}^{\Delta}}(t)
    -
    \underrightarrow{{f_{\Gamma}}^{\Delta}}(t-\Delta)$

-   The $k$^th^ backward difference at $t$
    is the $(k-1)$^th^ backward difference at $t+\Delta$
    minus the $(k-1)$^th^ backward difference at $t$.

    $\underrightarrow{{f_{\Gamma x}}^{\Delta}}(t)
    \triangleq
    \underrightarrow{{f_{\Gamma}}^{\Delta}}(t+\Delta)
    -
    \underrightarrow{{f_{\Gamma}}^{\Delta}}(t)$

-   Given the full set of forward finite differences at $t$,
    
    -   the full set of forward finite differences at $t+\Delta$ is found by
        
        $\begin{aligned}
        &\vdots\\
        \underrightarrow{{f_{xx}}^{\Delta}}(t+\Delta) &= \underrightarrow{{f_{xx}}^{\Delta}}(t) + \underrightarrow{{f_{xxx}}^{\Delta}}(t+\Delta)\\
        \underrightarrow{{f_{x}}^{\Delta}}(t+\Delta) &= \underrightarrow{{f_{x}}^{\Delta}}(t) + \underrightarrow{{f_{xx}}^{\Delta}}(t+\Delta)\\
        f(t+\Delta) &= f(t) + \underrightarrow{{f_{x}}^{\Delta}}(t+\Delta)\\
        \end{aligned}$
    
    -   the full set of forward finite differences at $t-\Delta$ is found by
    
        $\begin{aligned}
        f(t-\Delta) &= f(t) - \underrightarrow{{f_{x}}^{\Delta}}(t)\\
        \underrightarrow{{f_{x}}^{\Delta}}(t-\Delta) &= \underrightarrow{{f_{x}}^{\Delta}}(t) - \underrightarrow{{f_{xx}}^{\Delta}}(t)\\
        \underrightarrow{{f_{xx}}^{\Delta}}(t-\Delta) &= \underrightarrow{{f_{xx}}^{\Delta}}(t) - \underrightarrow{{f_{xxx}}^{\Delta}}(t)\\
        &\vdots\\
        \end{aligned}$
