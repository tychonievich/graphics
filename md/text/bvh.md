---
title: Bounding Volume Hierarchies
summery: Making raytracing run in logarithmic time.
...

Most 3D scenes are dominated by small non-overlapping primitives.
Bounding Volume Hierarchies (BVH) take advantage of that trend to accelerate finding which object a ray intersects from linear to logarithmic time
by navigating a tree-shaped data structure.

# BVH Overview

As a pre-processing step, most raytracers will create a BVH for the geometry in the scene.
The BVH is a tree-like structure
with scene geometry as the leaf nodes
and special non-rendered geometry on the internal and root notes.
Each such non-rendered object is referred to as a "bounding volume" and is designed such that it encloses all the geometry of its children nodes.

Given a BVH, raytracing becomes a recursive process checking the bounding volume of a node and only checking its children if the ray intersects the bounding volume.
Conceptually, that may look something like the following:

```js
function raytrace(ray, nodeInBVH) {
    if (!ray.intersects(nodeInBVH.boundingVolume)) {
        return noIntersection
    }
    let best = noIntersection
    for(let nodeOrPrimitive of nodeInBVH.children) {
        let option = raytrace(ray, nodeOrPrimitive)
        if (option.betterThan(best)) best = option
    }
    return best
}
```

# BVH design and construction

## Bounding Volume choice

In principle any bounding volumes may be used, but the most common choice is an [axis-aligned bounding box (AABB)](rays.html#ray-aabb-intersection) because (a) they can tile space, (b) it is easy to decide which AABB a primitive belongs to, and perhaps most importantly because (c) ray-AABB intersection is very easy to compute.

## Tree or DAG

Most scenes contain some overlapping geometry such that primitives cannot be neatly divided with each in a separate non-overlapping bounding volume.

:::example
Consider reducing a 3D scene to 1D.
Such a reduction causes all triangles and AABBs to be simply intervals on the number line.

Consider an example 1D scene that contains four objects:
1--4, 3--6, 5--8, and 7--9.
Because every interval overlaps with another interval, we can't separate them nicely into several bounding intervals.
:::

Two solutions to overlap are common:

1. Let the bounding volumes overlap too.
    This preserves the tree structure of the BVH but precludes some BVH structures.
2. Use non-overlapping bounding volumes
    and list every object that is partly contained in a bounding volume as its child.
    This means that primitives that span several bounding volumes will appear several times in the BVH.

:::example
Continuing our previous example,

1. Overlapping bounding intervals would make a tree with 
    - root interval 1--9
        - intermediate interval 1--6
            - leaf 1--4
            - leaf 3--6
        - intermediate interval 5--9
            - leaf 5--8
            - leaf 7--9

2. Non-overlapping bounding intervals would make a directed acyclic graph with
    - root interval 1--9
        - intermediate interval 1--5
            - leaf 1--4
            - leaf 3--6
        - intermediate interval 5--9
            - leaf 3--6 (repeated)
            - leaf 5--8
            - leaf 7--9
:::

When bounding volumes do not overlap they often instead have shared AABB faces,
meaning they can share some of the computation of AABB intersection tests between AABBs, reducing the overall computation needed to navigate the BVH.

## Cluster or Divide

Some BVH are constructed by first bounding all primitives,
then dividing that volume into smaller sub-volumes.
Popular versions of this include the oct-tree, where each node has exactly 8 non-overlapping children each with exactly ⅛ of the volume of its parent;
and the kd-tree, where each node has exactly 2 children divided along a single axis
with the axis chosen round-robin on a path from root to leaf.
These division-based methods often result in non-overlapping bounding volumes with shared leaves, though they can be adjusted to make trees with overlapping volumes instead.

Some BVH are constructed by first grouping nearby objects,
then grouping nearby bounding volumes,
and so on until only one remains.
Many different cluster identification methods have been proposed
as nearest-neighbor computation admits may solutions with varying degrees of precision vs efficiency.
These cluster-based methods result in trees with overlapping volumes.

# Alternatives to BVH

Bounding volumes do not need to be a hierarchy.
Hierarchies achieve logarithmic time in general,
but the constant factor may make them less efficient than flat data structures in some cases.

Very large primitives, such as ground planes or large walls, can interrupt the effectiveness of BVHs.
Some BVH implementations accommodate this by letting large primitives be children of the root node or, in some cases, children of an internal node if they approach the size of the node.
I've also seen discussions of splitting the scene into several scales of primitives and having separate BVH for each; I do not know of implementations of that approach.

Most BVH techniques stop before they finish dividing, often storing 10--30 primitives as children of a single node in the BVH.
This number is generally found empirically by trying various sizes of leaf nodes on various scenes and seeing which seems to perform the best.

If a scene has a relatively uniform distribution of primitives
a simple 3D grid of bounding volumes walked with a 3D version of DDA or Bresenham might outperform a BVH.
While I've seen this approach discussed, I've not seen it in production BVH implementations; thus I assume that it does not work better than a BVH in common practice.

Some interactive 3D games intentionally include large vision-obstructing shapes
such as the walls of a building or maze
and can use those to create a visibility graph:
the camera position is checked against a list of precomputed regions
and a list of primitives visible from that region are used for rendering.
In principle, a similar ray-origin-indexed visibility graph structure could work for raytracing and, for scenes with large obstructing shapes, could in principle outperform more general BVHs.
I have not yet seen these ideas implemented in a raytracer
