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

![pixel stepping rules](files/implicit2.svg){style="width:14em"}

The third rule above is a problem case: it can only arise if the shape has a narrow region or cusp, and the grid walking algorithm itself cannot pick the right reaction to it.
Heuristics can be used with reasonable consistency, however, by picking either "don't cross a positive diagonal" or "don't cross a negative diagonal": it doesn't matter which one is picked, but it needs to be consistent.

This approach doesn't lend itself to drawing an 8-connect boundary line,
but does let us draw the pixels on one side of the curve.
For example, in the following image it will visit the marked pixels;
it can distinguish the red from the blue;
and it knows that the outlined pixels, although visited, where not adjacent to the curve because they were adjacent to two other pixels of the same sign.

![grid walking results](files/implicit3.svg){style="width:18em"}

