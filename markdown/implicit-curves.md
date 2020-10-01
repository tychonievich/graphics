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

:::example
Suppose I tell you the last entry of each row of the table differences constructed using a process like that from the previous problem is $(11, -2, 5, 0, 0, \dots)$, with $11$ being $f(8)$:

                $f(8)$
----    ----   --------
                $11$
        $-2$
$5$

Then you can find $f(9)$ by adding from the last different to the first:

                $f(8)$              $f(9)$
----    ----   -------- ---------  ----------
                $11$                $11+3=14$
        $-2$            $-2+5=3$
$5$             $5$

with the new last row of $(14, 3, 5)$.
We could easily go a few more steps too:
$(22,8,5)$, $(35,13,5)$, etc.

You can also find $f(7)$ by subtracting from the first difference to the last:

                $f(7)$               $f(8)$
----  ----     --------     ----    --------
                $11-(-2)=13$         $11$
      $-2-5=-7$              $-2$
$5$             $5$

for a new last row of $(13, -2, 5)$.
We could easily go a few more steps too:
$(20,-7,5)$, $(32,-12,5)$, etc.
:::

Finite differences are a more complicated idea than we'll use, with the ability to use any fixed step size and with forward and backward variants,
but the simple approach works as follows:

1. Pick the $x,y$ point to start at

2. Evaluate $f(x-i, y-j)$ for all $0 \le i \le o_x+1$ and $0 \le j \le o_y$,
    where $o_x$ is the order of the polynomial in the $x$
    and $o_y$ the order in $y$.
    
    Example $f(x,y) = x^2y + y^3 + x$ has $o_x=2$ and $o_y=3$.
    If we start at $(0,0)$ the grid would be
    
        -41 -31 -27
        -18 -11  -8
         -7  -3  -1
         -2  -1   0

3. Subtract adjacent values repeatedly to create the finite differences
    
    Continuing the previous example, the grid
    
        -41 -31 -27
        -18 -11  -8
         -7  -3  -1
         -2  -1   0

    after one subtraction in $x$
    
         10   4 -27
          7   3  -8
          4   2  -1
          1   1   0

    after two subtractions in $x$
    
          6   4 -27
          4   3  -8
          2   2  -1
          0   1   0

    after one subtractions in $y$
    
          2   1  19
          2   1   7
          2   1   1
          0   1   0

    after two subtractions in $y$
    
          0   0  12
          0   0   6
          2   1   1
          0   1   0

    after three subtractions in $y$
    
          0   0   6
          0   0   6
          2   1   1
          0   1   0
    
    And that's the full difference grid.

    As an optimization, we can throw away 0s in the top-left corner, like so:

                  6
                  6
          2   1   1
          0   1   0
    
    ... though doing so is not necessary.
    If done properly, the resulting shape should match the terms of the polynomial:
    e.g. $x^2y$ should ne 3 wide in x and 2 wide in $y$;
    $y^3$ should be 4 wide in $y$ and 1 wide in $x$; etc.
    We can initially sample less than the full grid based on this end shape if we wish.

4. To evaluate the function a $x+1$ we add each row, right to left

                  6
                  6
          2   3   2
          0   1   1
    
    meaning $f(1,0) = 1$
    
    To evaluate the function a $y+1$ we add each column, bottom to top

                  6
                 12
          2   3   8
          2   4   3

    meaning $f(1,1) = 3$; one more step

                  6
                 18
          2   3  20
          4   7  11

    meaning $f(1,2) = 11$

    To evaluate the function a $x-1$ we subtract each column, left to right

                  6
                 18
          2   1  19
          4   3   8

    meaning $f(0,2) = 3$

    To evaluate the function a $y-1$ we subtract each column, top to bottom

                  6
                 12
          2   1   7
          2   2   1

    meaning $f(0,1) = 1$

This technique, together with the grid walking approach, can find the border of a polynomial function with constant memory, a constant number of multiplications to start out, and a linear number of additions in the length of the curve.

# Application: Circles

One of the most common curves to wish to draw is a circle. The implicit equation for a circle is
$$(x-c_x)^2 + (y-c_y)^2 = r^2$$
which is  second-order polynomial, so we can use the finite difference optimization of edge following.

Circles have a high degree of symmetry, so if the center point $(c_x,c_y)$ has integer coordinates we can get away with only computing ⅛ of the overall border:
for every pixel $(p_x,p_y)$ we decide to plot
we'll plot 8 symmetric points
$(c_x \pm (p_x-c_x), c_y \pm (p_y-c_y)$
and 
$(c_x \pm (p_y-c_y), c_y \pm (p_x-c_x)$.

Because we only need to plot an eighth of the circle, we can pick a portion
were the slope is strictly bounded, as e.g. going from the west to the north-west 
