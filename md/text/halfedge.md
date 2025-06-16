---
title: Half-edge data structure
summary: With notes on implementation and how to implement triangle subdivision using it.
...

# Data Structure

The half-edge data structure, also sometimes called the doubly-linked edge list data structure,
is a special type of linked graph data structure for storing polygonal meshes.
It is the simplest of a set of related data structures
including the [winged edge](https://en.wikipedia.org/wiki/Winged_edge)
and the [BMesh](https://wiki.blender.org/wiki/Source/Modeling/BMesh/Design).

The half-edge data structure only works correctly when storing [orientable manifolds](https://en.wikipedia.org/wiki/Orientability),
which is sometimes seen as a benefit rather than a limitation in graphics:
the most common surface meshes in graphics are representing the boundary between two volumes (such as "person" and "air") and all such boundary surface are orientable manifolds, so this data structure limitation can help prevent or detect some kinds of meshing errors.

The core component of a half-edge data structure is a half-edge,
which entirely consists of three pointers:
two (`twin` and `next`) to other half-edges and one (`v`) to a vertex.
Vertices may be stored in any way you wish: a 3D point,
and $n$D point concatenating position with other vertex attributes,
an index into attribute arrays,
etc.

A half-edge's `next` is never null, and walking `next`s always results in traveling around a loop
consisting of the edges of a single polygonal face in the mesh.
Hence, each half-edge belongs to exactly one face,
and each $n$-sided face consists of $n$ half-edges.
To represent this, half-edges are often draw as if they were slightly inset into their face.

Each edge connects to vertices;
its own `v` and the `v` of its `next` half-edge.
To represent this, half-edges are often drawn pointing from their `v` to their `next.v`.

Each geometric edge in a mesh
is either the boundary between two faces
or the edge of the mesh itself.
Edge-of-mesh half-edges have a null `twin`;
other half-edges have their `twin` being the half-edge along the same edge belonging to the neighboring face.
A half-edge and its `twin` always point in opposite directions;
that is, `this.twin.v == this.next.v` and `this.twin.next.v == this.v`.
You can make a half-edge-like structure where the opposite-direction criteria doesn't hold,
but doing so prevents many half-edge algorithms from working properly.


<figure>
```pikchr
V:      dot thick thick thick
        text "this.v" mono at 0.15 heading 180 from V
NV:     dot at 1.5 heading 30 from V
        text "this.next.v" mono at 0.15 heading 0 from NV
NNV:    dot at 1.5 heading 90 from V
        text "this.next.next.v" small mono at 0.15 heading 180 from NNV

This:   arrow thick  from 0.2 heading 50 from V to 0.2 heading 190 from NV "this" big bold mono aligned below
Twin:   arrow thin from 0.2 heading 10 from V to 0.2 heading -130 from NV <- "this.twin" mono aligned above
Next:   arrow thin from 0.2 heading 170 from NV to 0.2 heading -50 from NNV "this.next" mono aligned below
Nnxt:   arrow thin dashed from 0.2 heading 70 from V to 0.2 heading -70 from NNV <- "this.next.next" small mono aligned above
Ntwn:   arrow thin dashed from 0.2 heading 130 from NV to 0.2 heading -10 from NNV <- "this.next.twin" small mono aligned above
```
<figcaption>An illustration of the half-edge data structure</figcaption>
</figure>

Some half-edge data structure sanity checks:

- `this.next != null`{.js}
- `this.next != this`{.js}
- `this.next.next != this`{.js}
- for triangles, `this.next.next.next == this`{.js};<br/>
  for quads `this.next.next.next.next == this`{.js};<br/>
  for $n$-sided faces, adding $n$ `.next`s to `this` gets you back to `this`.
- `this.twin == null || this.twin.twin == this`{.js}
- `this.twin == null || this.v == this.twin.next.v`{.js}
- `this.twin == null || this.twin.v == this.next.v`{.js}
- for closed meshes (no holes), `this.twin != null`{.js}

# Query operations

## Walk a face

To visit all the half-edges around a face:

```js
use(this)
let he = this.next
while(he != this) {
    use(he)
    he = he.next
}
```

## Walk a vertex

To visit all the half-edges exiting a non-boundary vertex:

```js
use(this)
let he = this.twin.next
while(he != this) {
    useExiting(he)
    he = he.twin.next
}
```

## Find every edge

To find one half-edge from a list `half_edges` representing each edge,

```js
for(let he of half_edges) he.used = false;
let one_per_edge = []
for(let he of half_edges) {
    if (he.used) continue
    one_per_edge.push(he)
    he.used = true
    he.twin.used = true
}
```

## Find every face

To find one half-edge from a list `half_edges` representing each face,

```js
for(let he of half_edges) he.used = false;
let one_per_face = []
for(let he of half_edges) {
    if (he.used) continue
    one_per_face.push(he)
    he.used = true
    for(let ptr = he.next; ptr != he; ptr+=1) ptr.used = true;
}
```

# Modification operations

## Flip an edge (triangles only)

To *flip* an edge, merging the two triangles adjacent to the edge into a quad
and then re-split them along the other diagonal.
This results in no next change in the number of triangles, vertices, or edges.

<figure>
```pikchr
dot
dot at 1 heading 30 from 1st dot
dot at 1 heading 90 from 1st dot
dot at 1 heading -30 from 1st dot

arrow from 0.2 heading 170 from 2nd dot to 0.2 heading -50 from 3rd dot 
arrow from 0.2 heading -70 from 3rd dot to 0.2 heading 70 from 1st dot 
arrow from 0.2 heading -10 from 1st dot to 0.2 heading 130 from 4th dot
arrow from 0.2 heading 110 from 4th dot to 0.2 heading -110 from 2nd dot

arrow thick color blue from 0.2 heading 50 from 1st dot to 0.2 heading 190 from 2nd dot
arrow thick color blue from 0.2 heading -130 from 2nd dot to 0.2 heading 10 from 1st dot


dot at 1 heading 90 from 3rd dot
dot at 1 heading 30 from 5th dot
dot at 1 heading 90 from 5th dot
dot at 1 heading -30 from 5th dot

arrow from 0.1 heading -160 from 6th dot to 0.3 heading -30 from 7th dot 
arrow from 0.3 heading -80 from 7th dot to 0.1 heading 40 from 5th dot 
arrow from 0.1 heading 20 from 5th dot to 0.3 heading 140 from 8th dot
arrow from 0.3 heading 100 from 8th dot to 0.1 heading -140 from 6th dot

arrow thick color blue from 0.3 heading 130 from 8th dot to 0.3 heading -70 from 7th dot
arrow thick color blue from 0.3 heading -50 from 7th dot to 0.3 heading 110 from 8th dot

text "← flip →" at 0.5 way between 3rd dot and 8th dot
```
<figcaption>Illustration of the half-edge flip operation. This only works on triangle meshes, and is its own inverse. All 6 half-edges had their `next` field change and the flipped edge also changed their `v` fields, but no `twin` fields changed.</figcaption>
</figure>

## Split an edge (triangles only)

To *split* an edge, add a new vertex in the center of the edge
and six new half-edges to break the original triangles adjacent to the edge
into smaller triangles.

<figure>
```pikchr
dot
dot at 1.2 heading 30 from last dot
dot at 1.2 heading 90 from 2nd last dot
dot at 1.2 heading -30 from 3rd last dot

arrow from 0.2 heading 170 from 3rd last dot to 0.2 heading -50 from 2nd last dot 
arrow from 0.2 heading -70 from 2nd last dot to 0.2 heading 70 from 4th last dot 
arrow from 0.2 heading -10 from 4th last dot to 0.2 heading 130 from last dot
arrow from 0.2 heading 110 from last dot to 0.2 heading -110 from 3rd last dot

arrow thick color blue from 0.2 heading 50 from 4th last dot to 0.2 heading 190 from 3rd last dot
arrow thick color blue from 0.2 heading -130 from 3rd last dot to 0.2 heading 10 from 4th last dot

dot color red at 1.5 heading 90 from 0.5 < 2nd dot, 3rd dot >
dot at 0.6 heading -150 from last dot
dot at 1.2 heading 30 from last dot
dot at 1.2 heading 90 from 2nd last dot
dot at 1.2 heading -30 from 3rd last dot

arrow from 0.2 heading 170 from 3rd last dot to 0.2 heading -30 from 2nd last dot 
arrow from 0.2 heading -90 from 2nd last dot to 0.2 heading 70 from 4th last dot 
arrow from 0.2 heading -10 from 4th last dot to 0.2 heading 150 from last dot
arrow from 0.2 heading 90 from last dot to 0.2 heading -110 from 3rd last dot

arrow thick color blue from 0.2 heading 50 from 4th last dot to 0.2 heading 190 from 5th last dot
arrow color red from 0.2 heading 50 from 5th last dot to 0.2 heading 190 from 3rd last dot
arrow thick color blue from 0.2 heading -130 from 3rd last dot to 0.2 heading 10 from 5th last dot
arrow color red from 0.2 heading -130 from 5th last dot to 0.2 heading 10 from 4th last dot

arrow color red from 0.2 heading 100 from 5th last dot to 0.2 heading -40 from 2nd last dot <-
arrow color red from 0.2 heading 140 from 5th last dot to 0.2 heading -80 from 2nd last dot

arrow color red from 0.2 heading -40 from 5th last dot to 0.2 heading 100 from last dot
arrow color red from 0.2 heading -80 from 5th last dot to 0.2 heading 140 from last dot <-

text "— split →" at 0.5 way between 3rd dot and 9th dot
```
<figcaption>Illustration of the half-edge split operation. This only works on triangle meshes. New vertices and half-edges are shown in red. Of the original 6 half-edges, 0 have new `v`s, 2 have new `twin`s, and 4 have new `next`s.</figcaption>
</figure>

## Refine an edge

To *refine* an edge, add a new vertex in the center of the edge
and two new half-edges to break the original edge into two edges.
This results in increasing the number of sides on each adjacent face by one:
triangles become quads, quads become pentagons, and so on.

There are multiple ways to decide where the old half-edges go and where the new ones go.
The number of changes needed is minimized by keeping the old half-edges with the same `v`s
and making the new half-edges their `twin`s.

<figure>
```pikchr
dot
dot at 1.2 heading 30 from last dot
dot at 1.2 heading 90 from 2nd last dot
dot at 1.2 heading -30 from 3rd last dot

arrow from 0.2 heading 170 from 3rd last dot to 0.2 heading -50 from 2nd last dot 
arrow from 0.2 heading -70 from 2nd last dot to 0.2 heading 70 from 4th last dot 
arrow from 0.2 heading -10 from 4th last dot to 0.2 heading 130 from last dot
arrow from 0.2 heading 110 from last dot to 0.2 heading -110 from 3rd last dot

arrow thick color blue from 0.2 heading 50 from 4th last dot to 0.2 heading 190 from 3rd last dot
arrow thick color blue from 0.2 heading -130 from 3rd last dot to 0.2 heading 10 from 4th last dot

dot color red at 1.5 heading 90 from 0.5 < 2nd dot, 3rd dot >
dot at 0.6 heading -150 from last dot
dot at 1.2 heading 30 from last dot
dot at 1.2 heading 90 from 2nd last dot
dot at 1.2 heading -30 from 3rd last dot

arrow from 0.2 heading 170 from 3rd last dot to 0.2 heading -50 from 2nd last dot 
arrow from 0.2 heading -70 from 2nd last dot to 0.2 heading 70 from 4th last dot 
arrow from 0.2 heading -10 from 4th last dot to 0.2 heading 130 from last dot
arrow from 0.2 heading 110 from last dot to 0.2 heading -110 from 3rd last dot

arrow thick color blue from 0.2 heading 50 from 4th last dot to 0.08 heading 150 from 5th last dot
arrow color red from 0.08 heading 90 from 5th last dot to 0.2 heading 190 from 3rd last dot
arrow thick color blue from 0.2 heading -130 from 3rd last dot to 0.08 heading -30 from 5th last dot
arrow color red from 0.08 heading -90 from 5th last dot to 0.2 heading 10 from 4th last dot

text "— refine →" at 0.5 way between 3rd dot and 9th dot
```
<figcaption>Illustration of the half-edge refinement operation. New vertices and half-edges are shown in red. The refined edges change `twin` and `next`, no other pre-existing edge changes. Note that this increases the number of vertices per face.</figcaption>
</figure>

## Clip a corner (non-triangles only)

To *clip* a corner of a non-triangular face, add two new half-edges connecting the vertices on either side of the triangle.
This results in a reduction in the number of sides of the face by 1
and the creation of a new triangle.

There are multiple ways to define a corner of a face using half-edges.
This integrates most easily with [triangle subdivision]
if the new triangle's edges are `this`, `this.next`, and a new half-edge.

<figure>
```pikchr
dot
dot at 0.6 heading 90 from last dot
dot at 0.6 heading 90 from last dot
dot at 0.6 heading -30 from last dot
dot at 0.6 heading -30 from last dot
dot at 0.6 heading -150 from last dot
arrow thin from 0.2 heading 50 from 1th dot to 0.08 heading 150 from 6th dot
arrow thick color blue from 0.08 heading 90 from 6th dot to 0.2 heading -170 from 5th dot
arrow thin from 0.2 heading 170 from 5th dot to 0.08 heading -90 from 4th dot
arrow thin from 0.08 heading -150 from 4th dot to 0.2 heading -50 from 3th dot
arrow thin from 0.2 heading -70 from 3th dot to 0.08 heading 30 from 2th dot
arrow thin from 0.08 heading -30 from 2th dot to 0.2 heading 70 from 1th dot

dot at 0.6 heading 90 from 3rd dot
dot at 0.6 heading 90 from last dot
dot at 0.6 heading 90 from last dot
dot at 0.6 heading -30 from last dot
dot at 0.6 heading -30 from last dot
dot at 0.6 heading -150 from last dot
arrow thin from 0.2 heading 50 from 7th dot to 0.1 heading 150 from 12th dot
arrow thick color blue from 0.1 heading 45 from 12th dot to 0.2 heading -170 from 11th dot
arrow thin from 0.2 heading 170 from 11th dot to 0.08 heading -45 from 10th dot
arrow thin from 0.08 heading -150 from 10th dot to 0.2 heading -50 from 9th dot
arrow thin from 0.2 heading -70 from 9th dot to 0.08 heading 30 from 8th dot
arrow thin from 0.08 heading -30 from 8th dot to 0.2 heading 70 from 7th dot

arrow color red from 0.1 heading 110 from 12th dot to 0.1 heading -110 from 10th dot
arrow color red from 0.1 heading 70 from 12th dot to 0.1 heading -70 from 10th dot <-

text "— corner clip →" at 0.5 way between 4rd dot and last dot
```
<figcaption>Illustration of the half-edge corner clip operation. New half-edges are shown in red. The refined half-edge's previous half-edge gets a new `next` which bypasses its old `next` and `next.next`. The previous half-edge is not usually stored as part of a half-edge data structure, but can be found by looping `next`s around the face. Note that this decreases the number of vertices per face and won't work if the original face was a triangle.</figcaption>
</figure>

## Triangle subdivision

Triangle subdivision is [one of three common subdivision patterns](make-geom.html),
and can be implemented using the above operations in two different ways.

### Split all, flip some

The first option is to *split* every edge
then *flip* any new edge that connects a new vertex to an old vertex.

<figure>
```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
```

Split an edge

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
dot thick color red at 0.5 < 1th dot, 2th dot >; line color red from last dot to 5th dot
```

Split another edge

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
dot thick color red at 0.5 < 1th dot, 2th dot >; line color red from last dot to 5th dot chop
dot thick color red at 0.5 < 2th dot, 5th dot >
line color red from last dot to 2th last dot chop
line color red from last dot to 4th dot chop
```

Split all the remaining edges

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
dot thick color red at 0.5 < 1th dot, 2th dot >
line color red from last dot to 5th dot chop
dot thick color red at 0.5 < 2th dot, 5th dot >
line color red from last dot to 2th last dot chop
line color red from last dot to 4th dot chop
dot thick color red at 0.5 < 2th dot, 3th dot > // 8
dot thick color red at 0.5 < 2th dot, 4th dot > // 9
dot thick color red at 0.5 < 3th dot, 4th dot > // 10
dot thick color red at 0.5 < 4th dot, 5th dot > // 11
dot thick color red at 0.5 < 1th dot, 5th dot > // 12
line color red from 9th dot to 7th dot chop
line color red from 9th dot to 3th dot chop
line color red from 9th dot to 8th dot chop
line color red from 9th dot to 10th dot chop
line color red from 7th dot to 11th dot chop
line color red from 6th dot to 12th dot chop
```

Identify new edges connecting old and new vertices

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
dot thick color red at 0.5 < 1th dot, 2th dot >
line thick thick color blue from last dot to 5th dot chop
dot thick color red at 0.5 < 2th dot, 5th dot >
line from last dot to 2th last dot chop
line thick thick color blue from last dot to 4th dot chop
dot thick color red at 0.5 < 2th dot, 3th dot > // 8
dot thick color red at 0.5 < 2th dot, 4th dot > // 9
dot thick color red at 0.5 < 3th dot, 4th dot > // 10
dot thick color red at 0.5 < 4th dot, 5th dot > // 11
dot thick color red at 0.5 < 1th dot, 5th dot > // 12
line from 9th dot to 7th dot chop
line thick thick color blue from 9th dot to 3th dot chop
line from 9th dot to 8th dot chop
line from 9th dot to 10th dot chop
line from 7th dot to 11th dot chop
line from 6th dot to 12th dot chop
```

Flip new edges connecting old and new vertices

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
dot thick at 0.5 < 1th dot, 2th dot > // 6
dot thick at 0.5 < 2th dot, 5th dot > // 7
line from last dot to 2th last dot chop
dot thick at 0.5 < 2th dot, 3th dot > // 8
dot thick at 0.5 < 2th dot, 4th dot > // 9
dot thick at 0.5 < 3th dot, 4th dot > // 10
dot thick at 0.5 < 4th dot, 5th dot > // 11
dot thick at 0.5 < 1th dot, 5th dot > // 12
line from 9th dot to 7th dot chop
line from 9th dot to 8th dot chop
line from 9th dot to 10th dot chop
line from 7th dot to 11th dot chop
line from 6th dot to 12th dot chop
line thick color red from 12th dot to 7th dot chop
line thick color red from 8th dot to 10th dot chop
line thick color red from 9th dot to 11th dot chop
```

<figcaption>Illustration of the split-then-flip technique for triangle subdivision</figcaption>
</figure>

This technique is nice in that it only involves triangles at all steps,
meaning it can also be ported to triangle-only data structures in addition to half-edges.
It does involve a bit more bookkeeping than the other technique
because it requires tracking which edges connect new and old vertices.

## Refine all, clip all new

The second option is to *refine* every edge
and then *clip* the corner of every new half-edge,
or equivalently the corner of every old vertex.


<figure>
```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line thin thin from 1th dot to 2th dot
line thin thin from 2th dot to 3th dot
line thin thin from 3th dot to 4th dot
line thin thin from 4th dot to 5th dot
line thin thin from 5th dot to 1th dot
line thin thin from 2th dot to 4th dot
line thin thin from 2th dot to 5th dot
I1_1: 0.08 heading 60 from 1th dot
I2_1: 0.08 heading -60 from 2th dot
I5_1: 0.08 heading 180 from 5th dot
I2_2: 0.08 heading 0 from 2th dot
I4_2: 0.08 heading -120 from 4th dot
I5_2: 0.08 heading 120 from 5th dot
I2_3: 0.08 heading 60 from 2th dot
I3_3: 0.08 heading -60 from 3th dot
I4_3: 0.08 heading 180 from 4th dot
arrow from I1_1 to I5_1
arrow from I5_1 to I2_1
arrow from I2_1 to I1_1
arrow from I2_2 to I5_2
arrow from I5_2 to I4_2
arrow from I4_2 to I2_2
arrow from I2_3 to I4_3
arrow from I4_3 to I3_3
arrow from I3_3 to I2_3
```

Refine every edge; now all faces are hexagons, not triangles

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line thin thin from 1th dot to 2th dot
line thin thin from 2th dot to 3th dot
line thin thin from 3th dot to 4th dot
line thin thin from 4th dot to 5th dot
line thin thin from 5th dot to 1th dot
line thin thin from 2th dot to 4th dot
line thin thin from 2th dot to 5th dot
I1_1: 0.08 heading 60 from 1th dot
I2_1: 0.08 heading -60 from 2th dot
I5_1: 0.08 heading 180 from 5th dot
I2_2: 0.08 heading 0 from 2th dot
I4_2: 0.08 heading -120 from 4th dot
I5_2: 0.08 heading 120 from 5th dot
I2_3: 0.08 heading 60 from 2th dot
I3_3: 0.08 heading -60 from 3th dot
I4_3: 0.08 heading 180 from 4th dot
dot thick color red at 0.5 < 2th dot, 1th dot > // 6
dot thick color red at 0.5 < 2th dot, 5th dot > // 7
dot thick color red at 0.5 < 2th dot, 4th dot > // 8
dot thick color red at 0.5 < 2th dot, 3th dot > // 9
dot thick color red at 0.5 < 1th dot, 5th dot > // 10
dot thick color red at 0.5 < 5th dot, 4th dot > // 11
dot thick color red at 0.5 < 4th dot, 3th dot > // 12
I6_1: 0.5 < I2_1, I1_1 >
I7_1: 0.5 < I2_1, I5_1 >
I10_1: 0.5 < I1_1, I5_1 >
I7_2: 0.5 < I2_2, I5_2 >
I8_2: 0.5 < I2_2, I4_2 >
I11_2: 0.5 < I5_2, I4_2 >
I8_3: 0.5 < I2_3, I4_3 >
I9_3: 0.5 < I2_3, I3_3 >
I12_3: 0.5 < I4_3, I3_3 >
arrow from I1_1 to I10_1; arrow color red from I10_1 to I5_1
arrow from I5_1 to I7_1; arrow color red from I7_1 to I2_1
arrow from I2_1 to I6_1; arrow color red from I6_1 to I1_1
arrow from I2_2 to I7_2; arrow color red from I7_2 to I5_2
arrow from I5_2 to I11_2; arrow color red from I11_2 to I4_2
arrow from I4_2 to I8_2; arrow color red from I8_2 to I2_2
arrow from I2_3 to I8_3; arrow color red from I8_3 to I4_3
arrow from I4_3 to I12_3; arrow color red from I12_3 to I3_3
arrow from I3_3 to I9_3; arrow color red from I9_3 to I2_3
```

Clip the corner of every new half-edge; or equivalently, clip the corner of every old vertex

```pikchr
dot thick
dot thick at 1 heading 90 from last dot
dot thick at 1 heading 90 from last dot
dot thick at 1 heading -30 from last dot
dot thick at 1 heading -90 from last dot
line from 1th dot to 2th dot
line from 2th dot to 3th dot
line from 3th dot to 4th dot
line from 4th dot to 5th dot
line from 5th dot to 1th dot
line from 2th dot to 4th dot
line from 2th dot to 5th dot
dot thick at 0.5 < 1th dot, 2th dot > // 6
dot thick at 0.5 < 2th dot, 5th dot > // 7
dot thick at 0.5 < 2th dot, 3th dot > // 8
dot thick at 0.5 < 2th dot, 4th dot > // 9
dot thick at 0.5 < 3th dot, 4th dot > // 10
dot thick at 0.5 < 4th dot, 5th dot > // 11
dot thick at 0.5 < 1th dot, 5th dot > // 12
line color red from 6th dot to 12th dot then to 7th dot then to 6th dot
line color red from 7th dot to 11th dot then to 9th dot then to 7th dot
line color red from 8th dot to 9th dot then to 10th dot then to 8th dot
```

<figcaption>Illustration of the refine-then-clip technique for triangle subdivision</figcaption>
</figure>

This technique is nice in that it does not require much bookkeeping.
However, its intermediate step is non-triangles so while it works well for half-edge data structures
it does not work as well for some other triangle-only data structures.
