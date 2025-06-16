---
title: Clipping
summary: Removing off-screen geometry, avoiding divide-by-zero, and using depth buffer bits well via frustum clipping.
...


# Clipping points and lines

The projection stage is going to divide values by the $w$ component of vertices,
so it is necessary to ensure no $w=0$ vertices remain.
It's also good for both efficiency correctness to discard geometry that would be off-screen when rendered.
Both goals are achieved by clipping primitives in homogeneous coordinates.

Clipping is done with clipping planes.
There are six clipping planes enabled by default, though some GPUs may allow the user to add more.
The six are:
$$\begin{matrix}
-w &\le& x &\le& w\\
-w &\le& y &\le& w\\
-w &\le& z &\le& w\\
\end{matrix}$$
Put another way, vertices are inside the clipping region if the following results in a vector of non-negative numbers:
$$\begin{bmatrix}
1&0&0&1\\
-1&0&0&1\\
0&1&0&1\\
0&-1&0&1\\
0&0&1&1\\
0&0&-1&1\\
\end{bmatrix} \begin{bmatrix}
x\\y\\z\\w
\end{bmatrix}$$
This second form is useful because each of the six resulting numbers is a signed distance from one of the six clipping planes, and signed distances make finding intersection points easy.

:::aside
The standard plane equation is $Ax+By+Cz+D = 0$.
The $Ax+By+Cz+D$ part provides the signed distance between the point $(x,y,z)$ and the plane.
For homogeneous points, this equation generalizes to $Ax+By+Cz+Dw = 0$
with distance formula $Ax+By+Cz+Dw$.
Written as a matrix, that is
$$\begin{bmatrix}
A&B&C&D\\
\end{bmatrix} \begin{bmatrix}
x\\y\\z\\w
\end{bmatrix}$$
Thus the matrix form of the constraints above is evaluating six homogeneous plane signed distance formulas at once.
:::

Vertices that violate any one of the inequalities are discarded.
Vertices that satisfy all six of the inequalities are kept.
Edges that connect a kept and discarded vertex result in the creation of a new vertex that lies exactly on the clipping plane,
potentially changing the number of vertices in the primitive.

:::example
The edge with endpoints $(1,2,3,4)$ and $(4,1,-1,2)$ crosses the $x \le w$ clipping plane (because $1<4$ but $4 \not<2$).

Rewriting the plane $x \le w$ as a plane distance equation we get $1x + 0y + 0z - 1w \le 0$.
Plugging in the two vertices, we get distances $-3$ and $2$, respectively.
Our new point is thus
$$\begin{split}
&\;\dfrac{\big(2(1,2,3,4))-\big(-3(4,1,-1,2)\big)}{2-(-3)}\\
=&\;
\dfrac{(2,4,6,8)+(12,3,-3,6)}{5}\\
=
&\;(2.8,1.4,0.6,2.8)
\end{split}$$
This point lies on the plane ($2.8 = 2.8$) and on the edge (being a linear combination of $(1,2,3,4)$ and $(4,1,-1,2)$).
:::

Clipping is partly an optimization: it means out-of-view object are never rendered.
But it also has correctness properties,
preventing division-by-zero errors during projection
and removing numerical instabilities caused when dividing a large number by a small number.

# Clipping a triangle against one plane

A triangle clipped against one plane can result in 0, 1, or 2 triangles.

The general approach is as follows:

1. Find the signed distance of each vertex from the plane, using the plane equation.
2. Count the number of vertices that are outside the plane
3. if 3 are outside, discard the entire triangle
4. if 0 are outside, keep the entire triangle
5. if 2 are outside, make 1 new triangle:
    a. find the edge intersections for the two edges that connect inside and outside vertices
    b. the new triangle connects the inside vertex and the two clip-generated vertices
6. if 1 is outside, make 2 new triangles:
    a. find the edge intersections for the two edges that connect inside and outside vertices
    b. one new triangle connects one clip-generated vertex with the two inside vertices
    c. one new triangle connects one inside vertex to the two clip-generated vertices
    d. the shared edge of the two new triangles connects an inside vertex and a clip-created vertex

<figure>
<svg viewBox="-49 -20 78 41" fill="none" stroke-width="0.3" text-anchor="middle" font-size="1.5">
<path d="m -46,-18 12,6 -8,10 z" fill="#0C0"/>
<path d="m -26,-11 12,6 L -18,0 z" fill="#080"/>
<path d="m -26,-11 L -18,0 -23.2,0 z" fill="#0F0"/>
<path d="M -6,-4 2,0 -5,0 z" fill="#0A0"/>
<path d="m -46,-18 12,6 -8,10 z" fill="none" stroke="#000000"/>
<path d="m -26,-11 12,6 -8,10 z" fill="none" stroke="#000000"/>
<path d="m -6,-4 12,6 -8,10 z" fill="none" stroke="#000000"/>
<path d="m 14,3 12,6 -8,10 z" fill="none" stroke="#000000"/>
<path d="m -50,0 h 100" fill="none" stroke="#FF0000"/>
<path d="m -50,0 h 100 v 100 h -100 z" fill="#FF0000" opacity="0.125"/>
<text x="-46" y="-18.5" fill="#000">1.8</text>
<text x="-34" y="-13" fill="#000">1.2</text>
<text x="-42" y="-0.5" fill="#000">0.2</text>
<text x="-26" y="-11.5" fill="#000">1.1</text>
<text x="-14" y="-6" fill="#000">0.5</text>
<text x="-22" y="6.5" fill="#000">−0.5</text>
<text x="-6" y="-4.5" fill="#000">0.4</text>
<text x="6" y="1" fill="#000">−0.2</text>
<text x="-2" y="13.5" fill="#000">−1.2</text>
<text x="14" y="2.5" fill="#000">−0.3</text>
<text x="26" y="8" fill="#000">−0.9</text>
<text x="18" y="20.5" fill="#000">−1.9</text>
<circle cx="2" cy="0" r="0.5" stroke="none" fill="#00F"/>
<circle cx="-5" cy="0" r="0.5" stroke="none" fill="#00F"/>
<circle cx="-18" cy="0" r="0.5" stroke="none" fill="#00F"/>
<circle cx="-23.2" cy="0" r="0.5" stroke="none" fill="#00F"/>
</svg>
<figcaption>The four cases for a triangle-plane clip.
Signed distances to vertices are indicate near each vertex.
The clipping plane is red, with the outside half-space in pink.
Intersection points are blue.
Triangles that exist after the clip are filled, each in a different shade of green.
</figcaption>
</figure>

# Clipping a triangle against many planes

A triangle clipped against multiple planes may result in many new triangles.
There are sophisticated approaches that try to generate the minimum number of triangles in some kind of canonical order,
but it is far more common to implement the following order-of-planes-dependent approach:

1. Create a set of triangles containing just the triangle you plan to clip
1. For each clipping plane
    a. Create an empty set of clipped triangles
    a. For each triangle in the set
        i. clip the triangle with the plane
        i. add the resulting 0, 1, or 2 triangles to the set of clipped triangles
    a. replace the set of triangles with the set of clipped triangles 


<figure>
<div style="text-align: center">
<svg viewBox="-20 -20 100 100" fill="none" stroke-width="1" style="width:12rem" stroke-linejoin="round">
<path d="M 0,0 h50 v50 h-50 z" stroke="#700"/>
<path d="M 0,-7 60,10 30,80 Z" fill="#0F0"/>
<path d="M 0,12.5 0,-7 30,80 Z" fill="#0A0"/>
<path d="M -10,-10 60,10 30,80 Z" stroke="#000"/>
<path d="M 0,-20 v100" stroke="#F00"/>
</svg>
<svg viewBox="-20 -20 100 100" fill="none" stroke-width="1" style="width:12rem" stroke-linejoin="round">
<path d="M 0,0 h50 v50 h-50" stroke="#700"/>
<path d="M 0,-7 50,7 50,33 Z" fill="#0F0"/>
<path d="M 0,-7 50,33 30,80 Z" fill="#0A0"/>
<path d="M 0,-7 60,10 30,80 Z" stroke="#000"/>
<path d="M 0,12.5 0,-7 30,80 Z" stroke="#000"/>
<path d="M 50,-20 v100" stroke="#F00"/>
</svg>
<svg viewBox="-20 -20 100 100" fill="none" stroke-width="1" style="width:12rem" stroke-linejoin="round">
<path d="M 0,50 h50" stroke="#700"/>
<path d="M 26,0 50,7 50,33 Z" fill="#0F0"/>
<path d="M 9,0 26,0 50,33 Z" fill="#0A0"/>
<path d="M 2.3,0 9,0 50,33 Z" fill="#0FF"/>
<path d="M 2.3,0 50,33 30,80 Z" fill="#0AA"/>
<path d="M 2.3,0 30,80 0,12.5 Z" fill="#DD0"/>
<path d="M 0,0 2.3,0 0,12.5 Z" fill="#AA0"/>
<path d="M 0,-7 50,7 50,33 Z" stroke="#000"/>
<path d="M 0,-7 50,33 30,80 Z" stroke="#000"/>
<path d="M 0,-7 30,80 0,12.5 Z" stroke="#000"/>
<path d="M -20,0 h100" stroke="#F00"/>
</svg>
<svg viewBox="-20 -20 100 100" fill="none" stroke-width="1" style="width:12rem" stroke-linejoin="round">
<path d="M 2.3,0 43,50 20,50 Z" fill="#0F0"/>
<path d="M 2.3,0 50,33 43,50 Z" fill="#0A0"/>
<path d="M 2.3,0 20,50 0,12.5 Z" fill="#0FF"/>
<path d="M 20,50 16.5,50 0,12.5 Z" fill="#0AA"/>
<path d="M 26,0 50,7 50,33 Z" stroke="#000"/>
<path d="M 9,0 26,0 50,33 Z" stroke="#000"/>
<path d="M 2.3,0 9,0 50,33 Z" stroke="#000"/>
<path d="M 2.3,0 50,33 30,80 Z" stroke="#000"/>
<path d="M 2.3,0 30,80 0,12.5 Z" stroke="#000"/>
<path d="M 0,0 2.3,0 0,12.5 Z" stroke="#000"/>
<path d="M -20,50 h100" stroke="#F00"/>
</svg>
<svg viewBox="-2 -2 54 54" fill="none" stroke-width="0.5" style="max-width:24rem" stroke-linejoin="round">
<path d="M 2.3,0 43,50 20,50 Z" stroke="#000"/>
<path d="M 2.3,0 50,33 43,50 Z" stroke="#000"/>
<path d="M 2.3,0 20,50 0,12.5 Z" stroke="#00"/>
<path d="M 20,50 16.5,50 0,12.5 Z" stroke="#000"/>
<path d="M 26,0 50,7 50,33 Z" stroke="#000"/>
<path d="M 9,0 26,0 50,33 Z" stroke="#000"/>
<path d="M 2.3,0 9,0 50,33 Z" stroke="#000"/>
<path d="M 0,0 2.3,0 0,12.5 Z" stroke="#000"/>
</svg>
</div>
<figcaption>Sequence of clips against 4 clipping planes, resulting in final 7-sided polygon made of 8 triangles. Note that changing the order in which the clipping planes are applied or the direction in which quads are split into triangles would result in the same polygon, but a different set of triangles.</figcaption>
</figure>
