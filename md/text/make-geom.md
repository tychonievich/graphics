---
title: Procedural creating geometry
summary: Grids, subdivision, and deduplication.
...

# Grids

Many 3D geometries we generate are broadly some variation of a grid.
They might be simple grids, as for a terrain or sheet;
looped grids, as for a tube or torus;
or grids connected by seams, as for clothes or bodies.

Graphics cards generally support only triangles,
but humans tend to prefer squares.
This leads to two type of grids both being common.

## Rectangular grids

An $n \times n$ rectangular grid of points like this:

<figure>
<svg viewBox="0 0 225 200" font-size="10" text-anchor="middle" style="max-width: 45em; display:table; margin:auto">
<text x="10" y="20">0</text>
<text x="60" y="20">1</text>
<text x="110" y="20">2</text>
<text x="160" y="20">3</text>
<text x="210" y="20">⋯</text>
<text x="10" y="70">n</text>
<text x="60" y="70">n+1</text>
<text x="110" y="70">n+2</text>
<text x="160" y="70">n+3</text>
<text x="210" y="70">⋯</text>
<text x="10" y="120">2n</text>
<text x="60" y="120">2n+1</text>
<text x="110" y="120">2n+2</text>
<text x="160" y="120">2n+3</text>
<text x="210" y="120">⋯</text>
<text x="10" y="170">⋮</text>
<text x="60" y="170">⋮</text>
<text x="110" y="170">⋮</text>
<text x="160" y="170">⋮</text>
</svg>
<figcaption>Numbering of points in a rectangular grid</figcaption>
</figure>

can be joined into triangles by one of two ways of splitting the squares;

- either join $(i, i+1, i+n)$ and $(i+1, i+n, i+n+1)$

<figure>
<svg viewBox="0 0 130 120" font-size="10" text-anchor="middle" style="max-width: 26em; display:table; margin:auto">
<text x="10" y="20">0</text>
<text x="60" y="20">1</text>
<text x="110" y="20">2</text>
<text x="10" y="70">n</text>
<text x="60" y="70">n+1</text>
<text x="110" y="70">n+2</text>
<text x="10" y="120">2n</text>
<text x="60" y="120">2n+1</text>
<text x="110" y="120">2n+2</text>
<g fill="none" stroke="red">
<path d="M 20,25 50,25 20,50 Z"/>
<path d="M 51,26 51,51 21,51 Z"/>
<path d="M 70,25 100,25 70,50 Z"/>
<path d="M 101,26 101,51 71,51 Z"/>
<path d="M 20,75 50,75 20,100 Z"/>
<path d="M 51,76 51,101 21,101 Z"/>
<path d="M 70,75 100,75 70,100 Z"/>
<path d="M 101,76 101,101 71,101 Z"/>
</g>
</svg>
<figcaption>One way of triangulating a rectangular grid</figcaption>
</figure>


- or join $(i, i+1, i+n+1)$ and $(i+n+1, i+n, i)$

<figure>
<svg viewBox="0 0 130 120" font-size="10" text-anchor="middle" style="max-width: 26em; display:table; margin:auto">
<text x="10" y="20">0</text>
<text x="60" y="20">1</text>
<text x="110" y="20">2</text>
<text x="10" y="70">n</text>
<text x="60" y="70">n+1</text>
<text x="110" y="70">n+2</text>
<text x="10" y="120">2n</text>
<text x="60" y="120">2n+1</text>
<text x="110" y="120">2n+2</text>
<g fill="none" stroke="red">
<path d="M 20,25 50,25 50,50 Z"/>
<path d="M 19,26 49,51 19,51 Z"/>
<path d="M 70,25 100,25 100,50 Z"/>
<path d="M 69,26 99,51 69,51 Z"/>
<path d="M 20,75 50,75 50,100 Z"/>
<path d="M 19,76 49,101 19,101 Z"/>
<path d="M 70,75 100,75 100,100 Z"/>
<path d="M 69,76 99,101 69,101 Z"/>
</g>
</svg>
<figcaption>Another way of triangulating a rectangular grid</figcaption>
</figure>

Rectangular grids are easy to define, but because of the longer diagonal compared to shorter edges the chosen axes can be visually noticeable in some situations.

### Rectangular grid normals

The diagonals on a rectangular grid mess up direct face-based vertex normal computation.
A better way of generating normals is to base it on a subset of its grid-adjacent neighbors.

<figure>
<svg viewBox="0 0 150 150" font-size="10" text-anchor="middle" style="max-width: 30em; display:table; margin:auto">
<text x="10" y="20">nw</text>
<text x="60" y="20">n</text>
<text x="110" y="20">ne</text>
<text x="10" y="70">w</text>
<text x="60" y="70">v</text>
<text x="110" y="70">e</text>
<text x="10" y="120">sw</text>
<text x="60" y="120">s</text>
<text x="110" y="120">se</text>
</svg>
<figcaption>Labeling vertices by compass directions: $v$ in the middle, $n$ north of it, $ne$ north-east of it, $e$ east of it, and so on</figcaption>
</figure>

The simpler way is to take the cross-product of
the vector connecting the vertices on either side of it along one grid axis
and vector connecting the vertices on either side of it along the other grid axis:
$$(n-s) \times (w-e)$$
If we want to also consider the diagonal neighbors, we can take their cross products and do a weighted average,
for example as
$$\dfrac{2\big((n-s) \times (w-e)\big) + 1\big((ne-sw) \times (nw-se)\big)}{3}$$
Either way, any missing vertices that would be off the edge of the mesh can be replaced by the vertices on the edge instead.

Don't forget to normalize the normal vectors,
both in JavaScript and in the fragment shader.

## Triangular grids

Triangular or hexagonal grids can be created by modifying the rectangular grid creation as follows:

1. Move each row over by ½ compared to the row before it
2. Reduce row separation by a factor of $\sqrt{3} / 2$
3. The result is a sheered rectangle
    - to make it hexagonal, omit a point with row and column indices $(r,c)$ if $(r + c) < \frac{n}{2}$ or $(r+c) > \frac{3n}{2}$
    - to make it triangular, omit a point with row and column indices $(r,c)$ if $(r + c) > n$

<figure>
<svg viewBox="0 0 200 120" font-size="10" text-anchor="middle" style="max-width: 40em; display:table; margin:auto">
<text x="10" y="20">0</text>
<text x="60" y="20">1</text>
<text x="110" y="20">2</text>
<text x="35" y="63">n</text>
<text x="85" y="63">n+1</text>
<text x="135" y="63">n+2</text>
<text x="60" y="106">2n</text>
<text x="110" y="106">2n+1</text>
<text x="160" y="106">2n+2</text>
<g fill="none" stroke="red">
<path d="M 20,25 50,25 35,45 Z"/>
<path d="M 60,30 45,50 75,50 Z"/>
<path d="M 70,25 100,25 85,45 Z"/>
<path d="M 110,30 95,50 125,50 Z"/>
<path d="M 45,68 75,68 60,88 Z"/>
<path d="M 85,73 70,93 100,93 Z"/>
<path d="M 95,68 125,68 110,88 Z"/>
<path d="M 135,73 120,93 150,93 Z"/>
</g>
</svg>
<figcaption>Sheered rectangular grid looks triangular/hexagonal</figcaption>
</figure>

### Triangular grid normals

Vertex normals on a triangular grid are best computed
by summing the face normals of each incident face.
Generally it is better to sum the face normals before normalizing them
so that larger faces have more impact on the resulting vertex normal than smaller faces.

The cross product of any pair of edge vectors of a triangle is (a) normal to the triangle and (b) has a length proportional to the triangle's area.
But depending on which two points you pick, it might be pointing in either direction: either "out of" or "in to" the surface the triangle is part of.
A reasonable way to compute a vertex normal is as an area-weighted average of the face normals of its adjacent faces:
in other words, the sum of those cross-product-generated vectors.

Thus, we can find the vertex normals by

1. Initialize a zero-vector for every vertex
2. Loop over every triangle, and for each
    1. Find two edge vectors, $p_2-p_0$ and $p_1-p_0$
    
    2. Take the cross product of the edge vectors
        
        What if it points the wrong way?
        Ideally we'd define the triangles carefully so it never does,
        but for some special cases we can check and fix this; for example, with terrain if the $z$ component is negative, negate the vector.
    
    3. Add the vector to all three vertex's normals
3. Normalize all the resulting normal vectors.
    
    For best performance, normalize them in JavaScript if they won't change frame to frame, in the vertex shader if they will.
    
    Don't forget to *also* normalize them in your fragment shader!
    Normalizing per vertex keeps longer normals from dominating the interpolation;
    normalizing per fragment corrects for the shortening that happens during interpolation.
    

# Subdivision

Subdivision starts with a course mesh
and generates a fine mesh from it.
Usually subdivision involves two parts:
the creation of the new set of vertices and faces
and the positioning of the new vertices based on the old.
This section talks only about the connectivity, not the placement.

There are many possible subdivision patterns, but three are by far the most common.
They don't have standard names, though, so I'm giving them descriptive titles just for ease of reference.

## Center point

This technique works on any kind of mesh, and runs as follows

- Keep all old vertices
- Add a new vertex in the center of each old edge and the center of each old face
- Replace each old $n$-sided face with $n$ new 4-sided faces;
    each is bounded by a new face-center vertex,
    two new edge-center vertices,
    and an old vertex.

After a single iteration, this creates a mesh containing only quadrilaterals.
Old vertices remain regardless of the number of iterations, and keep their initial number of neighbors;
all new non-edge vertices have 4 neighbors.

One of the most popular smooth subdivision surface schemes, Catmull-Clark, uses this style of subdivision.
Because it creates quads, it is popular with square grids.

<details class="aside"><summary>Catmull-Clark subdivision</summary>

Edwin Catmull and Jim Clark's subdivision scheme, published in 1978,
says that 

- new face points should be placed at the average of the face's vertex locations

- new edge points should be placed at the edge's old vertices and the two adjacent new face point locations

- old vertices should be moved to $\frac{1}{n}\big(F + 2R + (n-3)P\big)$
    where $n$ is the number of edges incident to the old vertex,
    $F$ is the average location of the new face points adjacent to the old vertex,
    $R$ is the average location of the new edge points adjacent to the old vertex,
    and $P$ is the vertice's old location.
  
</details>


<figure>
<svg viewBox="0 0 100 100" font-size="10" text-anchor="middle" style="max-width: 40em; display:table; margin:auto">
<g opacity="0.3">
<circle r="4" cx="10" cy="10"/>
<circle r="4" cx="50" cy="10"/>
<circle r="4" cx="90" cy="10"/>
<circle r="4" cx="10" cy="50"/>
<circle r="4" cx="50" cy="50"/>
<circle r="4" cx="90" cy="50"/>
<circle r="4" cx="10" cy="90"/>
<circle r="4" cx="50" cy="90"/>
<circle r="4" cx="90" cy="90"/>
<path fill="none" stroke-width="3" stroke="#000" d="M 10,10 90,10 M 10,50 90,50 M 10,90 90,90 M 10,10 10,90 M 50,10 50,90 M 90,10 90,90"/>
</g>
<g opacity="1">
<circle r="2" cx="10" cy="10"/>
<circle r="2" cx="30" cy="10"/>
<circle r="2" cx="50" cy="10"/>
<circle r="2" cx="70" cy="10"/>
<circle r="2" cx="90" cy="10"/>
<circle r="2" cx="10" cy="30"/>
<circle r="2" cx="30" cy="30"/>
<circle r="2" cx="50" cy="30"/>
<circle r="2" cx="70" cy="30"/>
<circle r="2" cx="90" cy="30"/>
<circle r="2" cx="10" cy="50"/>
<circle r="2" cx="30" cy="50"/>
<circle r="2" cx="50" cy="50"/>
<circle r="2" cx="70" cy="50"/>
<circle r="2" cx="90" cy="50"/>
<circle r="2" cx="10" cy="70"/>
<circle r="2" cx="30" cy="70"/>
<circle r="2" cx="50" cy="70"/>
<circle r="2" cx="70" cy="70"/>
<circle r="2" cx="90" cy="70"/>
<circle r="2" cx="10" cy="90"/>
<circle r="2" cx="30" cy="90"/>
<circle r="2" cx="50" cy="90"/>
<circle r="2" cx="70" cy="90"/>
<circle r="2" cx="90" cy="90"/>
<path fill="none" stroke-width="0.5" stroke="#000" d="M 10,10 90,10 M 10,30 90,30 M 10,50 90,50 M 10,70 90,70 M 10,90 90,90 M 10,10 10,90 M 30,10 30,90 M 50,10 50,90 M 70,10 70,90M 90,10 90,90"/>
</g>
</svg>
<figcaption>Center-point subdivision on a square grid. Shows a low-res grid (grey) with high-res grid (black) superimposed.</figcaption>
</figure>




## Face shrinking

This technique works on any kind of mesh, and runs as follows

- Replace each face with a smaller copy of the face.
    This means each old vertex is replaced by $n$ new vertices, where $n$ is the number of old faces incident to that vertex;
    and each old edge is replaced by 2 new edges, one of each of its incident faces.
- Connect the new vertices generated by each old vertex with a polygon.
- Connect the new edges generated by each old edge with a square.

After a single iteration, all vertices have 4 neighbors.
Most new faces are quads, but each non-quad face remains
and each vertex that had other than 4 neighbors becomes a non-quad face too.

A somewhat popular smooth subdivision surface scheme, Doo-Sabin, uses this style of subdivision.
It is also the cantellation polytope operation
and the polygonal version of beveling.
Because each step removes all old vertices and produces new ones,
it has a built-in smoothing effect
and is sometimes used in operations that want some smoothing
but don't want to use a standard smoothing subdivision.


<details class="aside"><summary>Doo-Sabin subdivision</summary>

Daniel Doo's subdivision scheme, published as part of his PhD dissertation in 1978 and expanded on in a paper with Malcom Sabin that same year,
says that 

- new points should be placed at the average of
    the center of the face,
    the center of each nearby edge,
    and the nearest old vertex.
  
</details>


<figure>
<svg viewBox="0 0 100 100" font-size="10" text-anchor="middle" style="max-width: 40em; display:table; margin:auto">
<g opacity="0.3">
<circle r="4" cx="10" cy="10"/>
<circle r="4" cx="50" cy="10"/>
<circle r="4" cx="90" cy="10"/>
<circle r="4" cx="10" cy="50"/>
<circle r="4" cx="50" cy="50"/>
<circle r="4" cx="90" cy="50"/>
<circle r="4" cx="10" cy="90"/>
<circle r="4" cx="50" cy="90"/>
<circle r="4" cx="90" cy="90"/>
<path fill="none" stroke-width="3" stroke="#000" d="M 10,10 h80 M 10,50 h80 M 10,90 h80 M 10,10 v80 M 50,10 v80 M 90,10 v80"/>
</g>
<g opacity="1">
<circle r="2" cx="20" cy="20"/>
<circle r="2" cx="40" cy="20"/>
<circle r="2" cx="20" cy="40"/>
<circle r="2" cx="40" cy="40"/>
<circle r="2" cx="60" cy="20"/>
<circle r="2" cx="80" cy="20"/>
<circle r="2" cx="60" cy="40"/>
<circle r="2" cx="80" cy="40"/>
<circle r="2" cx="20" cy="60"/>
<circle r="2" cx="40" cy="60"/>
<circle r="2" cx="20" cy="80"/>
<circle r="2" cx="40" cy="80"/>
<circle r="2" cx="60" cy="60"/>
<circle r="2" cx="80" cy="60"/>
<circle r="2" cx="60" cy="80"/>
<circle r="2" cx="80" cy="80"/>
<path fill="none" stroke-width="0.5" stroke="#000" d="M 0,20 h 100 M 0,40 h 100 M 0,60 H 100 M 0,80 h 100 M 20,0 v 100 M 40,0 v 100 M 60,0 v 100 M 80,0 v 100"/>
</g>
</svg>
<figcaption>Face-shrinking subdivision on a square grid. Shows a low-res grid (grey) with high-res grid (black) superimposed</figcaption>
</figure>


## Triangular

This technique only works on triangular meshes, and runs as follows

- Keep all old vertices
- Add a new vertex in the center of each old edge
- Replace each old face with four new faces:
    one connecting each old vertex to its two new edge vertices
    and one connecting the three new edge vertices.

This always only produces triangles.
All new non-edge vertices have 6 neighboring triangles,
while the original vertices keep their original neighbor counts.

A somewhat popular smooth subdivision surface scheme, Loop, uses this style of subdivision.

<details class="aside"><summary>Loop subdivision</summary>

Charles Loop's subdivision scheme, published as part of his Masters Thesis in 1987,
says that 

- new edge points should be placed at $\dfrac{3(a+b) + (c+d)}{8}$
  where $a$ and $b$ are the two points that define its edge
  and $c$ and $d$ are the two vertices not on its edge but on the triangles its edge connects

- old vertices are moved to a new point equal to $\alpha v + (1-\alpha) q$
    where $v$ is its old location,
    $q$ is the average of its old neighboring vertices locations,
    and $\alpha = \left(\frac{3}{8} + \frac{1}{4}\cos\frac{2\pi}{N}\right)^2 + \frac{3}{8}$
    where $N$ is the number of vertices connected by edges to the vertex.

    $\alpha$ for each $N$ can be computed up front, $N$ can only take on a few values.
    Other $\alpha$ formulas can also work, provided that when $N=6$ we get $\alpha = \frac{5}{8}$.
    Several online sources recommend using $\alpha = \frac{5}{16}$ when $N=3$ and $\alpha = \frac{5}{8}$ for all larger $N$ instead of Loop's original formula.
  
</details>



<figure>
<svg viewBox="-50 -50 100 100" font-size="10" text-anchor="middle" style="max-width: 40em; display:table; margin:auto">
<g opacity="0.3">
<circle r="4" cx="0" cy="0"/>
<circle r="4" cx="44" cy="0"/>
<circle r="4" cx="-44" cy="0"/>
<circle r="4" cx="22" cy="38"/>
<circle r="4" cx="-22" cy="38"/>
<circle r="4" cx="22" cy="-38"/>
<circle r="4" cx="-22" cy="-38"/>
<path fill="none" stroke-width="3" stroke="#000" d="M -44,0 44,0 22,38 -22,-38 22,-38 -22,38 Z M -22,38 22,38 M -44,0 -22,-38 M 22,-38 44,0"/>
</g>
<g opacity="1">
<circle r="2" cx="0" cy="0"/>
<circle r="2" cx="44" cy="0"/>
<circle r="2" cx="-44" cy="0"/>
<circle r="2" cx="22" cy="38"/>
<circle r="2" cx="-22" cy="38"/>
<circle r="2" cx="22" cy="-38"/>
<circle r="2" cx="-22" cy="-38"/>
<circle r="2" cx="22" cy="0"/>
<circle r="2" cx="-22" cy="0"/>
<circle r="2" cx="11" cy="19"/>
<circle r="2" cx="-11" cy="19"/>
<circle r="2" cx="11" cy="-19"/>
<circle r="2" cx="-11" cy="-19"/>
<circle r="2" cx="33" cy="19"/>
<circle r="2" cx="33" cy="-19"/>
<circle r="2" cx="-33" cy="19"/>
<circle r="2" cx="-33" cy="-19"/>
<circle r="2" cx="0" cy="38"/>
<circle r="2" cx="0" cy="-38"/>
<path fill="none" stroke-width="0.5" stroke="#000" d="M -44,0 44,0 22,38 -22,-38 22,-38 -22,38 Z M -22,38 22,38 M -44,0 -22,-38 M 22,-38 44,0 M 0,38 -33,-19 M 33,19 0,-38 M 0,-38 -33,19 M 33,-19 0,38 M -33,19 33,19 M -33,-19 33,-19"/>
</g>
</svg>
<figcaption>Triangle subdivision on a triangular grid. Shows a low-res grid (grey) with high-res grid (black) superimposed</figcaption>
</figure>


# Duplicate vertices

A duplicate vertex
is represented by two separate vertices in the data
which have the same position.
Duplicate vertices are useful if we wish to create a visual seam,
a sudden change in normal, texture, color, or other visual effect
along the edge of a triangle.
But if we don't wish that, they are inefficient and make geometrical computations such as computing normals and subdividing not work well.

Ideally, when creating a mesh we design the creation so that no duplicate vertices are created.
But if we fail to do that, we can manually look for and remove duplicates with an approach like the following:

    for every vertex p
      for every other vertex q
        if distance between p and q is very small
          replace every reference to q with a reference to p instead
          delete q

Some notes:

- We want to use "distance very small" instead of "same position" because vertices are stored with floating-point numbers that tend to have rounding error.
- "replace every reference to q" generally means changing edge and/or face definitions.
- "delete q" might mean reducing the length of the attribute array, and thus changing all larger indices too.






