---
title: Streaming, Level of Detail, and Occlusion
summary: The quest for complexity-independent render times with constant visual quality.
header-includes:
  - "<style>div > dl > dt { clear: none; }</style>"
...

# Highly-detailed scenes

Highly detailed scenes face various challenges that simpler scenes do not:

Video memory limitations
: Video memory is finite, but scene complexity is not. Artists often generate single models with several million triangles and 3D scanning often makes them even larger. With thousands of visible models, all with high-res texture maps as well as the various buffers needed for rendering itself, this can easily result in hundreds of gigabytes of data for a single scene and many terabytes for a large open-world game.
  
Sub-pixel triangles
: When a detailed object is far enough away to cover only a few pixels the vast majority of its triangles will fit entirely between two pixel centers and thus cover no pixels at all. This means a large amount of work that is entirely wasted with no visual impact of any kind.

Occluded geometry
: It is always wasteful to spend resources rendering something that will end up not being visible.
  Common reasons for being invisible include
  
  - Being outside the viewing frustum. If the camera is in the center of the scene, this is commonly the case for between 75% and 95% of all geometry. Frustum clipping will mean this geometry is not rasterized or sent to the fragment shader, but doing additional per-instance frustum culling can save significant vertex shader time, particularly in highly detailed scenes.
  
  - Being a "back face". In most scenes most triangles are part of the boundary between air and an opaque solid and are only ever visible from the air-facing side. Back-face culling can remove the roughly 50% of triangles that are back faces.
  
  - Behind something else, or "occluded". As I write this in my office, all the geometry of all the other offices in the building are occluded by the walls of my office and there's no reason to draw any of them. The larger the scene is, the more geometry will be occluded: in simple scenes most occluded geometry is also a back-face, but as the size of the scene increases there tends to be more and more occluded geometry.

**Streaming** is a common term for dynamically keeping just a subset of visible geometry in memory, storing the rest of it in some larger but slower medium like disk or the cloud, and updating what's in memory as the scene changes. Streaming is primarily used to overcome video memory limitations.

**LOD**, short for **L**evel **o**f **D**etail and implying dynamic, view-dependent changes in level of detail, is a common term for techniques that try to match primitive sizes to a target on-screen size. LOD can be used to resolve sub-pixel triangles and also has a longer history as a technique for matching visual resources to desired areas of focus.

**Occlusion culling** is a common term for removing some portions of geometry before it is rendered because of some knowledge that it will be occluded. Perfect occlusion culling subsumes back-face culling: back-faces are culled because they will be occluded by a front face.

**Popping** is a common problem faced by streaming and LOD implementations where a change in geometry detail causes a change between consecutive frames that, while minor in itself, is noticeable to the change- and motion-sensitive processing of the visual cortex.

**Cracks** are a problem faced by some LOD and occlusion culling implementations geometry of different levels of detail do not quite line up (LOD) or some visible faces are incorrectly culled (culling) resulting in visible holes in rendered geometry.

# Approaches to LOD

There are several common families of approaches to LOD

Subdivision
: The artist supplies the lowest-resolution mesh and rules for how to refine it into high-res versions.
  Those rules generally look like some kind of simple subdivision rule (e.g. "add a vertex on the longest edge of each triangle" or "split each quad into four quads"),
  a mathematical rule for approximating smooth surfaces (such as the Catmull-Clark or Butterfly schemes),
  and an artist-supplied displacement map for deviating from the smooth surface.

Decimation
: The artist supplies the highest-resolution mesh.
    Algorithmic approaches are then used to identify ways to remove or merge vertices with the least geometric impact on the overall mesh.
    Applying that algorithm repeatedly can replace the entire mesh with a lower-res mesh of any desired detail.
    
    Decimation algorithms have many variations.
    Some use special rules to prioritize keeping particular surface features.
    Some remove vertices and re-mesh the holes they leave; others merge pairs of vertices at a newly-added vertex location.
    Some move the vertices of the lower-res mesh to preserve local measures like object volume, surface area, or discrete curvature.
    Some create concrete measures of the error introduced by each reduction while others create a vertex removal order without formally defining error.

Imposters/Billboards/Proxies/Sprites
: These methods all replace 3D geometry with a 2D image of the geometry texture-mapped to a simple quadrilateral.
  There are many options for making this look better than a static image,
  such as storing normals in the image to allow for dynamic lighting,
  storing depth in the image to allow for parallax mapping,
  and rendering several images from different angles and picking between them based on viewing direction.

Alternative modeling methods
: Modeling methods based on point clouds or voxels have some appealing properties for LOD, but most 3D art assets are triangle-based instead.

Artist-generate manual LOD
: When automated LOD techniques fail artists can be tasked with making models at several different levels of detail.
  For example, a character's head might be modeled for close-ups with each hair its own little tube;
  for full-body shots with the hair modeled as a few dozen overlapping triangle ribbons with an alpha texture to look like more hairs; and for long shots with a low-res blob of hair with an opaque picture-of-hair texture.
  Automated LOD methods are improving, but as of 2023 artist-generated LOD remains the only option in many cases.

# Case study: Nanite's approach to LOD

In 2020, Unreal Engine 5 was released with a feature called Nanite that provided one of the most complete approaches to LOD thus far.
Nanite also includes streaming and occlusion as well as various other features such as integrated shadow maps and multi-view rendering.
Brian Karis, one of the engineers of Nanite, presented in [SIGGRAPH 2021](https://www.youtube.com/watch?v=eviSykqSUUw); much of this case study is informed by his presentation.

LOD Family: Decimation. The artist supplies only the highest-res geometry; everything else is handled by the engine.

Novel contribution: a new approach to part-of-mesh decimation without cracks.

## Challenge: cracks

Given a large mesh, part of which is much closer to the viewer than other parts, how can we use a high LOD close to the view and a low LOD farther away without any cracks?

Almost all triangle-based LOD approaches have discrete levels of detail: either a vertex has been removed/added or it has not.
That means that if a single mesh is being displayed at different LOD at different parts of the mesh
then there is a boundary somewhere on the mesh where the LOD is higher on one side of the boundary than the other.
Because higher LOD means more vertices, there's a chance there'll be a vertex on the boundary of the high-res side that is not matched by a vertex on the low-res side, resulting in a crack on that boundary.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">
<path d="m166.85 430.91 300.92 108.7 331.59 54.979 336.81-18.649 315.86-84.247 416.4-13.467 80.241-16.244 9.0097 664.57-1988.7 42.651-264.74-788.48z" fill="#a2ea82"/>
<path d="m-146.17 349.72 40.785-469.42 2209.3 15.073-158.78 520.49-493.06 75.825-652.67 102.9-632.5-163.68z" fill="#b6b6b6"/>
<g fill="none" stroke="#000" stroke-linejoin="round" stroke-width="3">
  <path d="m166.85 430.91 300.92 108.7 331.59 54.979"/>
  <path d="m482.51 790.69-14.744-251.09-407.14 114.69"/>
  <path d="m60.626 654.3 106.22-223.39"/>
  <path d="m1452 491.69 416.4-13.467 80.241-16.244"/>
  <path d="m2058.6 865.47-190.14-387.25-462.15 263.41"/>
  <path d="m1406.3 741.63 45.754-249.94"/>
  <path d="m60.626 654.3-356.38-273.57"/>
  <path d="m-295.75 380.72 462.6 50.185"/>
  <path d="m60.626 654.3-82.042 1.2499"/>
  <path d="m482.51 790.69-421.88-136.4-215.88 357.77"/>
  <path d="m1406.3 741.63 652.3 123.84-812.18 278.42"/>
  <path d="m949.51 824.8 296.88 319.09 159.88-402.26"/>
  <path d="m482.51 790.69-637.77 221.37 667.24 165.26"/>
  <path d="m482.51 790.69 29.469 386.63 437.53-352.52"/>
  <path d="m799.35 594.58-316.84 196.11 467 34.11"/>
  <path d="m949.51 824.8 456.76-83.174-270.11-165.7-186.65 248.87-150.16-230.22"/>
  <path d="m799.35 594.58 336.81-18.649 315.86-84.247"/>
  <path d="m607.73 163 294.07-335.28 244.91 349.25"/>
  <path d="m1146.7 176.98-538.98-13.978"/>
  <path d="m1146.7 176.98 722.6-286.19-417.29 600.9z"/>
  <path d="m607.73 163-176.94-568.72"/>
  <path d="m1375.7-421.15-229 598.13-347.36 417.61-191.62-431.59-713.11-282.7 272.23 550.61 440.88-267.91"/>
  <path d="m1945.1 415.86-1145.7 178.72-632.5-163.68-313.02-81.19"/>
</g>
<g font-family="sans-serif" font-size="48px" text-anchor="middle">
  <text x="795.30334" y="642.83472" text-align="center" style="line-height:1.25" xml:space="preserve"><tspan x="795.30334" y="642.83472">A</tspan></text>
  <text x="1470.8248" y="537.487" text-align="center" style="line-height:1.25" xml:space="preserve"><tspan x="1470.8248" y="537.487">B</tspan></text>
  <text x="1139.9227" y="628.0152" text-align="center" style="line-height:1.25" xml:space="preserve"><tspan x="1139.9227" y="628.01152">C</tspan></text>
</g>
</svg>
<figcaption>Cracks along a LOD boundary. On the low-res size (top, gray), vertices A and B are connected by an edge. On the high-res side (bottom, green), there's a third vertex C in between A and B that is not positioned exactly on the edge, creating a crack.</figcaption>
</figure>

Broadly speaking, there are two approaches to solving these cracks.
Either cracks can be identified and filled by moving the extra vertices on the high-res side to lie on the edge of the low-res side,
or LOD boundaries can be restricted to particular areas where such cracks cannot appear.
The crack-filling approach is computationally expensive and adds complexities related to interpolated surface normals, so constrained boundaries are generally preferred.
Subdivision techniques have options for constraining boundaries by construction,
but decimation techniques cannot control the connectivity of the input meshes and thus have fewer options.

## Avoiding cracks with clusters

Nanite does not do full-mesh decimation all at once.
Instead, it clusters groups of around 100 triangles and decimates inside the cluster, but not on the borders of the cluster.
That way each cluster has two levels of detail: a 100-ish triangle high-res version 1and a 50-ish triangle low-res version.
Significant effort is spent to decimate in a visually-optimal way and to store the error introduced by decimation so that LOD selection can tell how much visual loss there will be using the low-res instead of high-res version.

## Challenge: failure to decimate cluster borders

This cluster-based decimation can be applied recursively by joining low-res clusters into a next-level cluster and decimating them.
However, doing that naïvely does not work well.
Clusters are avoiding cracks by not removing vertices along the borders of the cluster.
Thus, the borders of the level-1 LOD clusters have vertices as dense as the level-0 input mesh.
If we combine to level-1 clusters and decimate it as a level-2 cluster,
the borders of that level-2 cluster will still be the borders of the level-1 and thus level-0 clusters; and so on.
The more steps we do, the more the clusters will be dominated by their super-dense borders.

<figure style="width:100%">
<img src="../files/tree-0.svg" style="width: 45%" alt="16 clusters"/>
<img src="../files/tree-1.svg" style="width: 45%" alt="8 clusters"/>
<img src="../files/tree-2.svg" style="width: 45%" alt="4 clusters"/>
<img src="../files/tree-3.svg" style="width: 45%" alt="2 clusters"/>
<figcaption>Naïve recursive cluster-based decimation.
Each figure merges two clusters from the previous figure
and decimates them to half as many triangles.
Note that the central boundary is a boundary between clusters at every level
and hence is never decimated,
resulting in the last image having most if its internal vertices along that single boundary.
</figcaption>
</figure>

## Decimating borders with group-decimate-split

Nanite avoids the accumulated error of cluster-based decimation
by

1. grouping $2N$ clusters into one large group;
2. decimating that group, keeping the group boundary fixed; and
3. splitting the decimated group into $N$ new decimated clusters.

By itself this process may not seem particularly effective, but as long as $N\ge 2$ groups and splits can be found in such a way that edges that were part of the fixed boundary on one level are not part of a fixed boundary on the next level.

To avoid accumulating large numbers of boundary edges,
we want to group clusters such that the number of edges on the perimeter of each group is minimized.
To facilitate such groupings having few edges on the next level
we want to split decimated groups such that the number of edges separating the split decimated clusters is minimized.
Both of these problems are NP-hard, as can be demonstrated by reduction to a graph problem.

Consider a graph made of the entire mesh with clusters as graph nodes
and edges between clusters that share at least one triangle edge,
with edge weights equal to the number of triangle edges shared.
Grouping clusters is then equivalent to finding a uniform [graph partition](https://en.wikipedia.org/wiki/Graph_partition)
with $2N$ nodes per partition group that minimizes total edge weight between groups.

Consider a graph made of the triangles of a decimated group
with unweighted graph edges connecting triangles that share a triangle edge.
Splitting the group is then equivalent to finding a uniform [graph partition](https://en.wikipedia.org/wiki/Graph_partition)
with $N$ partition groups that minimizes the edge count between groups.

Because graph partitions are NP-hard^[General graph partitions are NP-hard, but the graph generated when grouping or splitting an orientable manifold mesh (which most meshes in graphics are) is planar, and [Bui and Peck showed in 1992](https://doi.org/10.1137/0221016) that planar graphs can be partitioned optimally in subexponential time. That said, I'm not aware of an efficient-in-practice optimal planar graph partitioning algorithm, and evidently neither were the Nanite developers.] and approximation algorithms are fairly involved,
Unreal 5's release of Nanite performs the graph partition computation using [a third-party open-source library](http://glaros.dtc.umn.edu/gkhome/metis/metis/overview).

<figure style="width:100%">
<img src="../files/metis-0.svg" style="width: 45%" alt="16 clusters"/>
<img src="../files/metis-1.svg" style="width: 45%" alt="8 clusters"/>
<img src="../files/metis-2.svg" style="width: 45%" alt="4 clusters"/>
<img src="../files/metis-3.svg" style="width: 45%" alt="2 clusters"/>
<figcaption>Group-and-split-based decimation.
Each figure merges four clusters from the previous figure
and decimates them to half as many triangles,
then splits them into two new clusters.
Note that boundaries only survive two or three steps of the algorithm each
and the last image does not have dense vertices along its central boundary.
</figcaption>
</figure>

Because the clustering, grouping, and decimating all require non-trivial computational effort, this entire process is done offline,
either when models are generated during asset creation
or when they are first loaded during application setup.

## Picking a consistent LOD

With the split decimated groups of clusters, picking a consistent set of levels of detail requires some care.
We can visualize the hierarchy of clusters as a DAG:
with $N=2$ two low-res clusters are the parents of four higher-res clusters.

<figure>
<img src="../files/nanite-dag.svg" style="display: table; margin:auto"/>
<figcaption>Group-and-split results in a DAG:
each group of clusters shares four child clusters
but groups of children can span multiple parent groups.
</figcaption>
</figure>

In such a DAG, a selected LOD is a set of nodes
such that 

- At least one ancestor of each leaf node is included.
  This ensures there is no part of the model omitted.

- If a node is selected, none of its ancestors or descendants are.
  This ensures only one LOD is selected for each part of the mesh.

- The selected nodes can be connected by a cut that does not cross any edges.
  This ensures cluster boundaries do not have cracks.
  The edges in the DAG represent places where the parents may have changed the boundaries of the children, so if we do not cross any such edge
  we know all boundaries must line up.

<figure>
<img src="../files/nanite-dag-cut.svg" style="display: table; margin:auto"/>
<figcaption>A valid cut of a DAG, satisfying the three criteria above.</figcaption>
</figure>
 
One of the consequences of this set of rules is that LOD decisions are made at the group level, not cluster level:
no cut of the DAG can satisfy the rules and include only one of the clusters in a group.

Within these rules, the desired cut is one where
the selected nodes introduce an acceptable approximation error
but their parents introduce an unacceptable approximation error.
This rule can be modeled by recording the approximation error introduced during decimation
and storing it with the groups.

To avoid popping,
Nanite defines "acceptable error" as "resulting in less than a pixel offset."
The size of a pixel relative to a cluster is view-dependent.
A simple way to determine view-dependent error is to store that as a world-space distance
and divide by the distance the cluster is from the viewpoint to convert to pixel-unit distance instead.
That simple approach can be improved on in various ways, for example
considering normals as well as positions
and being more forgiving of changes along the view direction than perpendicular to it.

In general, finding the cut that meets these criteria requires an algorithm that considers all the nodes of the DAG holistically;
that, in turn, means it cannot be efficiently for very large DAGs,
rendering the general solution impractical for deployment.
However, if the approximation errors are monotonic
(that is, the error of a node is never greater than the error of its parents)
then updating the cut can be a purely local process:
a node is part of the cut if both

- its error is small enough, and
- some member of its group's parent's error is too large.

Nanite takes advantage of this by increasing child errors that are smaller than parent errors
so that the cut can be computed efficiently in parallel:
render iff `parentError > threshold && clusterError <= threshold`.

Because the error metrics change if the mesh undergoes non-rigid deformation, the Unreal 5's release of Nanite is limited to static, rigid meshes.
In principle this restriction could be removed with the addition of
either precomputed worst-case error under the expected range of deformation
or more complicated deformation-aware error tracking structures.

## Efficiency on the GPU

Nanite assumes there are a very large number of clusters
and that the vast majority of them not drawn because some ancestor is drawn.
This assumption is justified because it is the goal of LOD:
allow large scenes of very high-res geometry but only render as many triangles as there are pixels.
Given a very large number of clusters, checking all the clusters for appropriate level of detail, even in parallel, is inefficient.

Enter "LOD culling".
A cluster can be "LOD culled" if its parent's error is below threshold;
and if it is LOD culled its children are LOD culled too.
We could do many fewer LOD checks if we started at the root of the DAG and worked down until we culled something.
However, DAGs are complicated structures to walk, especially in parallel.

Instead, we can extract from the DAG a fixed-branching-factor tree (Nanite uses 8 children per node)
where the children of any given node were descendants of that node in the DAG.
Trees are good for parallel computation because their single-parent structure means we'll never have two different threads try to visit the same node.
Fixed branching factors are good for GPU computation because every thread does the same number of operations, allowing wide groups of threads to all operate in a SIMD way.

Culling a large tree on a GPU is a parallel expansion work problem.
Nanite solve this by implementing their own thread pool model with a single shared job queue; roughly, this looks like

:::algorithm
LOD culling

Setup
:   - A group of $N$ threads operate same instructions in lock-step.

    - Each thread has own thread ID $0 < i < N$.

    - Shared memory has a single job queue initialized with the roots of all LOD trees.

Process
:   While the queue is not empty,
    
    1. Pop the job $i$ from head of queue.
        Across the entire thread group, this is pops $N$ queue items.
      
    2. Find the view-dependent parent LOD error for that job.
    
    3. If the error > threshold, push all children jobs onto queue.

Comments
:   - Queue pushes rely on atomic operations.

    - Nanite's implementation depends on an undefined but seemingly-universal property of thread group scheduling in the GPU.

    - Can fall back on less efficient but more reliable depth-step tree traversal or non-hierarchical brute-force checks if needed.
:::

A few foreground objects at much higher LOD than most of the scene can cause many passes through loop with fewer jobs in the queue than there are threads in the group.
Nanite uses the GPU more efficiently by combining LOD culling with occlusion culling in the same GPU dispatch.

## Limitations of Decimation

Decimation approaches, including Nanite's, are effective when a lower-resolution version of a mesh has the same overall structure as a higher-resolution version.
That generally means they require a low topological genus: they can reduce detailed bumpy surfaces to low-res flat surfaces, but they have trouble reducing a screen to a plane or a thousand leaves to a single sphere.
Even advanced approaches that can change topology generally can't capture the visual effects of those changes: for example screens of individual opaque wires should decimate to transparent planes, not opaque ones.

At very small scales, even low-genus objects run into visual changes caused by over-decimation.
Nanite overcomes this by pre-rendering 12×12 pixel imposter images from 144 different view directions in advance and using the image that most closely aligns with the current view direction if the object's on-screen bounding box is less than 12 pixels in size.
That solution requires memory for the set of imposters and can result in popping, so the Nanite devs have expressed a desire for something better.
It also doesn't do much to help with grass, leaves, hair, screens, blinds, and other large objects made from the cumulative visual effect of many small pieces.

# Approaches to occlusion culling

There are several common families of approaches to occlusion culling

Back-face culling
: In most scenes most triangles are part of the boundary between air and an opaque solid and are only ever visible from the air-facing side.
  We call the solid-facing side the "back" face and the air-facing side the "front" face.
  By picking a consistent handedness for the triangles (traditionally, vertices are in a clockwise order from the back, counter-clockwise from the front) back faces can be efficiently identified and culled during primitive assembly before clipping and rasterization.
  In most scenes, back-face culling removes roughly 50% of triangles.

Visibility graphs
: Indoor scenes tend to have walls which are built explicitly to divide the space into individual rooms and corridors and prevent sight from one to another.
  Visibility graph take advantage of that division, creating a node for each such enclosed region and connecting it with edges to the set of other regions visible from it. 
  Each frame we check the region of the viewer and render only the geometry in that region and other regions visible from it.

    There has been some effort to extend visibility graphs to scenes not dominated by walls, but with limited success.

Bounding-box occlusion
: Since circa 2005, GPUs have the ability to perform efficient occlusion tests.
    You can disable depth and frame buffer writes and enable occlusion tests,
    render some geometry,
    and then query how many fragments were generated and passed the depth buffer test.
    We can thus do a fast rendering of a simple object (usually a bounding box of an object of interest);
    if no fragments are drawn, we skip the object; otherwise we re-enable depth and frame buffer writes and render the full-res geometry.
    
    Bounding-box occlusion tends to remove parallelism: the occlusion tests don't distinguish which objects were drawn, only that some were, so bounding boxes need to be tested serially.
    Combining bounding boxes into a hierarchy (similar to the [BVHs used in raytracing](bvh.html)) can help,
    as can using "what was visible last frame" as an initial guess of non-occluded geometry.
    [Wimmer and Bittner have a more detailed discussion of these approaches](https://developer.nvidia.com/gpugems/gpugems2/part-i-geometric-complexity/chapter-6-hardware-occlusion-queries-made-useful).

# Case study: Nanite's approach to occlusion culling

Because of Nanite's cluster-based LOD techniques, it has some advantages other systems don't when it comes to occlusion culling.
The clusters form natural components to cull and allow culling at a much more useful resolution than object-level approaches,

Occlusion Culling Family
:   Bounding-box. Scene elements are bounded and checked for visibility.

Contribution
:   Integration with LOD clusters; scaling to millions of elements.

Terminology
:   Throughout this section I will match the terminology used by the Nanite developers: "hardware" means "algorithms implemented as part of the GPU design" such as its built-in triangle rasterizer; "software" means "algorithms implemented by the programmer as compute shaders executing on the GPU"; and "CPU" means "algorithms implemented by the programmer and executing on the CPU".

## Challenge: *many* visibility tests

Hardware occlusion tests provided by 2020-era GPUs give one test result per GPU dispatch event: that is, you send data to the GPU, the GPU does its work, and the answer is a Boolean. In principle that needn't be the case and the day may come when many distinct occlusion queries can be performed with a single dispatch, but until such time performing hardware occlusion tests for millions of scene elements is too slow for practical implementation.

## Hierarchical Z-Buffer

Nanite avoids the dispatch serialization challenge by doing all occlusion tests in software:
the $z$ values of the pixels on the near faces of a bounding box around the geometry
are compared to all the corresponding $z$ values in the z-buffer
and if any of those $z$ are nearer than the z-buffer values the object is considered to be visible.

Checking each pixel like this is time-consuming, and even though GPU-resident software runs in parallel it cannot compete with the efficiency of the hardware occlusion test for large numbers of pixels.
To bypass that slow-down Nanite uses a trick similar to mipmapping, creating what they call a Hierarchical Z-Buffer or **HZB**.

The level-0 HZB is a standard z-buffer.
As with mipmapping, each subsequent level is half as wide and tall as the level below it,
meaning it has ¼ as many pixels.
Each pixel in level $i$ is created by combining a 2×2 set of pixels in level $i-1$;
unlike mipmapping, the combination function is the max function, not the average:
using the max means that each pixel in one level is at least as deep as each of the pixels it covers in lower levels.

<figure>
<table style="max-width:45%; display: inline-table; vertical-align:top"><tbody>
<tr style="color:#000"><th>Level 0</th><td>0.5</td><td>0.2</td><td>0.7</td><td>0.8</td><td>0.95</td><td>0.9</td><td>0.85</td><td>0.8</td></tr>
<tr style="color:#00F"><th>Level 1</th><td colspan="2" align="center">0.5</td><td colspan="2" align="center">0.8</td><td colspan="2" align="center">0.95</td><td colspan="2" align="center">0.85</td></tr>
<tr style="color:#070"><th>Level 2</th><td colspan="4" align="center">0.8</td><td colspan="4" align="center">0.95</td></tr>
<tr style="color:#A00"><th>Level 3</th><td colspan="8" align="center">0.95</td></tr>
</tbody></table><svg xmlns="http://www.w3.org/2000/svg" viewBox="-10 5 110 80" style="max-width:45%; display:inline-table; vertical-align:top">
<path fill="rgba(0,0,0,0.125)" stroke="#000" d="M 50,-5v20 h-30v10 h50v10 h10v10 h15v10 h-5v10 h-5v10 h-5v20  h25v-110h-55z"/>
<g fill="none" stroke="#a00" stroke-width="0.5">
<ellipse cx="95" cy="45" rx="2" ry="37"/>
</g>
<g fill="none" stroke="#070" stroke-width="0.5">
<ellipse cx="80" cy="25" rx="2" ry="17"/>
<ellipse cx="95" cy="65" rx="2" ry="17"/>
</g>
<g fill="none" stroke="#00F" stroke-width="0.5">
<ellipse cx="50" cy="15" rx="2" ry="7"/>
<ellipse cx="80" cy="35" rx="2" ry="7"/>
<ellipse cx="95" cy="55" rx="2" ry="7"/>
<ellipse cx="85" cy="75" rx="2" ry="7"/>
</g>
<g fill="none" stroke="#000">
<circle cx="50" cy="10" r="2"/>
<circle cx="20" cy="20" r="2"/>
<circle cx="70" cy="30" r="2"/>
<circle cx="80" cy="40" r="2"/>
<circle cx="95" cy="50" r="2"/>
<circle cx="90" cy="60" r="2"/>
<circle cx="85" cy="70" r="2"/>
<circle cx="80" cy="80" r="2"/>
</g>
</svg>
<figcaption>
A 1D version of an HZB.
The z values represent depth into the scene;
using the max function ensures lower-res levels are behind higher-res levels.
</figcaption>
</figure>

With an HZB, software occlusion test can make a performance trade-off decision.
By picking the level where the bounding box rasterizes as a single pixel we can do a single check,
but that check may say the box is visible when it's not because of the conservative way we initialized the levels of the HZB.
Using a lower level means more bounding box depth to compute and more HZB entries to compare, but also more accurate occlusion results
and hence less rendering work to do later.
The initial release of Nanite chose the level where the bounding box filled ≤ 16 pixels as the optimal point in this trade-off, but that's an empirical timing decision rather than an intrinsic optima.



## Assume few per-frame changes

The HZB approach allows a single dispatch to check many bounding boxes for occlusion, but it requires already knowing the depth buffer before beginning.
That is a challenge it shares with other bounding-box methods, and two solutions to it are common:
either sort objects by depth and render near-to-far in batches, using the depth from earlier batches to cull later patches;
or assume that what was visible last frame will be visible this frame and use it to create a z buffer.

Nanite uses the last-frame approach, which with the HZB would naïvely look like

1. Render geometry that was visible last frame.

2. Create the HZB from the z-buffer.

3. Check bounds of geometry that wasn't visible last frame.

4. Render newly-visible geometry.

This outlines the spirit of Nanite's occlusion cull, but not its reality as we see in the next section.

## Challenge: LOD changes and new occlusions

Nanite's LOD system means that each frame the set of active clusters changes.
Some of the clusters visible last frame will not be visible this frame.
In principle the last-frame-visible clusters could still be rendered to initialize the HZB, but because of streaming clusters they might not even be in memory anymore.
If a cluster was removed as being the wrong LOD then some of its ancestors or descendants should be visible, but navigating the DAG every frame is cost-prohibitive and the LOD system makes all of its decisions locally without retaining exact "was replaced by" information.
Nanite needs a way of using last-frame-visible information
even when most of this frame's clusters didn't exist last frame.

Additionally, the naïve approach given above has no way of ever marking something that was visible as now occluded.
If only occluded-last-frame geometry is checked for occlusion
then once geometry is marked as visible it will stay that way.
Any approach based on the outline above needs to check for occlusion of the geometry it did draw as well as of the geometry that it has not drawn yet.

## Two-pass HZB occlusion culling with LOD

Nanite solves both challenges using a two-pass occlusion cull.
The first pass uses the HZB from last frame, rather than last frame's visibility list; this frame's HZB is then initialized, used in the second pass, and then updated.
Nanite also does two tiers of occlusion culling: first per object instance in the scene, then per visible cluster.
The full process is

1. Transform instance bounding boxes with last-frame's transforms and occlude with last-frame's HZB.

2. Transform cluster bounding boxes for non-occluded instances with last-frame's transforms and occlude with last-frame's HZB.

3. Rasterized the non-occluded clusters with this-frame's transforms.

4. Build an HZB from the depth buffer.

5. Transform occluded instance bounding boxes with this-frame's transforms and occlude with the new HZB.

6. Transform cluster bounding boxes for previously-occluded clusters that belonging to newly-not-occluded instances with this-frame's transforms and occlude with the new HZB.

7. Rasterized the newly disoccluded clusters with this-frame's transforms.

8. Build an HZB for use next frame.

Note that this process only uses current-LOD clusters with no need to store an inter-frame visibility list.
It also checks every instance and cluster against one of the two HZBs each frame, ensuring that objects that leave visibility will be occluded.

:::aside
Because the HZB is limited to the viewing frustum, this form of occlusion culling also handles frustum culling.
That said, it can still be advantageous to frustum cull against this frame's frustum before executing the last-frame's-HZB.
:::

This approach works well in many scenes, but suffers from some limitations in common with other previous-frame-based approaches
and arguably exacerbated because of the prevalence of small-screen-space clusters.
When turning the camera a slice of the screen near the edge will have no previous-frame data to be culled against;
the same thing can happen in the middle of the frame when rounding a corner or otherwise exposing a slice of space that was not previously visible.
Such newly-exposed slices of the scene have no occlusion culling under this approach, so the more often that happens in the scene the less effective Nanite's occlusion culling becomes.


## Efficiency on the GPU 

Nanite combines LOD computation and culling with occlusion culling in a single computer shader dispatch.
This could use the hierarchical nature of the LOD and occlude some low-res clusters without generating their hi-res counterparts,
but perhaps more importantly it allows a single shader dispatch to work through both job queues together,
achieving higher thread GPU utilization rates (especially for the LOD computation) and fewer times the CPU needs to wait ft the GPU to finish its work.

Because LOD computation and culling only needs to happen once per frame
but occlusion culling happens twice, once against the old HZB and once against the new one,
the combined LOD+occlusion is done only on the first pass; the second pass does occlusion by itself.


# Approaches to streaming

Streaming dates back the very beginning of graphics.
Computer graphics was invented when memory was still expensive enough that even the pixels of a single frame could not fit into memory and some form of streaming data from disk was all-but required.
As such, the following list is far from complete, mentioning on a few ideas from the last few decades only.

Portals
:   The simplest form of streaming breaks the entire environment into distinct regions, loading and rendering one at a time.
    When the viewer enters specific areas commonly known as "portals" a new region is loaded.
    The simplest form of portal-based streaming fetches the new data only when it would become visible, resulting in a pause-and-load dynamic.
    It is also possible to preload, having the data of both the current region and the region behind the nearest portal in memory at the same time.
    With preloading it is also possible to draw multiple regions each frame;
    when used with a wall-heavy environment and a visibility map
    this can result in a seamless experience where the viewer is unaware the portals even exist.
    
    Stop-and-load portals are common in level-based games.
    Seamless portals are common in large maze-crawling games such as many first-person shooters.

Tiles
:   A common approach for streaming large open worlds of geometry
    is to break it into tiles.
    Each tile is available in several levels of detail,
    with the highest LOD in memory for the tile the camera is in
    and decreasing LOD for more distant tiles.
    Each time the camera crosses a tile boundary the new geometry is streamed in,
    with the old geometry rendered until the new geometry is available.
    
    Tiles are common in large open-world games, including most MMORGPs.

Virtual Textures
:   Virtual textures^[Named in reference to [virtual memory](https://en.wikipedia.org/wiki/Virtual_memory).]
    are used to facilitate streaming textures rather than geometry.
    They involve combining all textures of all objects in a scene into one huge texture and translating all texture coordinates into that larger coordinate space;
    mipmapping the big texture;
    splitting each mip level into tiles
    and storing them all on disk.
    A subset of those tiles is swapped into the GPU
    on demand;
    if an object would need a tile that's not resident a lower-res tile or a default value is used instead until the desired tile can be streamed in.
    
    Support for streaming virtual texture became available in the graphics cards shipped in the 2010s and have been used as an efficiency and detail boost in many games since then.
    CPU-based versions were in use before that.
    I do not know of any way to tell that a given program is using virtual textures besides looking at its code,
    but increasingly if there are many detailed textures then it's likely they are in use.


# Case study: Nanite's approach to streaming

Nanite uses virtual textures in the usual way.

Nanite also stores clusters on disk and swaps them into GPU memory when they are requested by the LOD computation.
The cluster hierarchy metadata needed to compute LOD selection is stored in memory, but the geometry in each cluster is stored on disk until the cluster is needed.
Unlike virtual texture tiles, clusters are not guaranteed to have a fixed one-disk-page size; so Nanite uses a separate paging system to manage the swapping, prioritizing keeping groups of clusters on as few pages as possible.

Conceptually, this means the LOD evaluation outputs both the set of resident clusters that best matches the desired LOD, to be used in rendering the current frame;
and a list of better but not-in-memory clusters.
That second list is read by the CPU which fills in any nodes from the full DAG that the GPU missed but are needed to make a consistent cut,
then fetches those clusters from disk and sends them to the GPU for rendering in a future frame.

That handles fetching needed clusters, but streaming also requires evicting unused data.
The LOD process flags each cluster it visits with a priority
based on visible error that would be introduced if that LOD were the one rendered.
Shadow map renders and other indirect views are given a lower priority than the primary render;
thus as pages get further from being in-LOD, their priority decreases.
The CPU then swaps in high-priority missing clusters and swaps out low-priority resident clusters to make room.

# Other details in Nanite

Nanite also contains several optimizations that are motivated by how they handle highly-details scenes, but are not intrinsically part of the handling of detail itself.

## Doubly-deferred shading

[Deferred shading](deferred.html) refers to rendering in multiple passes:
the first pass processes geometry to determine what is visible on the screen at the pixel level;
and the second pass processes materials to determine how those pixels should be colored.

Nanite adds a third pass to this deferred pipeline.

First Pass
:   All the LOD, occlusion, and cluster streaming discussed above.
    Renders clusters to a raster.
    Stores only three values:
    depth, instance ID, and triangle ID within instance.
    Ignores all the usual attribute interpolation work done in the first pass of the traditional deferred shading pipeline.
    
    Because all geometry has the same kinds of inputs and outputs during pass 1
    and the set of clusters to draw is computed by GPU-resident software,
    the entirety of pass 1 can be a single GPU dispatch,
    not one per instance or material as in a standard pipeline.

Second Pass
:   Interpolate values to each pixel as follows:
    
    1. Look up the pixel's instance and triangle.
    
    2. Transform the three vertices of the triangle with the instance's matrix.
        Note that Unreal 5 limits Nanite to rigid objects with a single matrix per instance.
    
    3. Derive [barycentric coordinates](rays.html#inverse-mapping-and-barycentric-coordinates) for the pixel given the vertex positions.
    
    4. Compute interpolated pixel attributes as the barycentric-coordinate-weighted sum (i.e. lerp) of the vertex attributes.

    Because all geometry has the same kinds of inputs and outputs during pass 2
    it can be done in a single GPU dispatch.
    
    This is significantly more work than the traditional rendering pipeline.
    Every vertex is transformed multiple times (at least during the first pass's vertex shader and the second pass's step 2, and likely multiple times in step 2 because most vertices are shared by several triangles that collectively cover many pixels).
    There's additional barycentric coordinate generation
    and the lerp is more work to compute than a simple DDA or Bresenham offset step.
    
    In his SIGGRAPH 2021 talk on this, Nanite developer Brian Karis said
    
    > That sounds *crazy*, doesn't it? But it's not as slow as it seems.
    
    ... because there are many cache hits[^cache] and the extra cost of computing is offset by the reduced cost of CPU/GPU communication and synchronization resulting from the first two passes each being a single draw call no matter how many objects are in the scene.

    Some shading operations (notably selecting a mip level for textures) require the screen-space derivative of some interpolated value.
    The screen-space derivative of a barycentric coordinate is constant across any given triangle,
    meaning the derivative of the interpolation can be computed along with the interpolation at minimal cost.

[^cache]:
    Caching is not a topic covered in the required prerequisites to this course.
    Broadly speaking, caching means that memory accesses are faster if the same or similar addresses are accessed repeatedly:
    reading the same address twice in a row might be as fast as reading it only once
    while reading widely varying addresses might take hundreds of cycles for each memory read.
    
    When someone refers to many cache hits, think "memory access isn't the bottleneck, computation is," which is likely how you were trained to understand performance initially.
    When they refer to few cache hits or many cache misses, think "ignore the computation; what's taking time here is memory accesses."

Third pass
:   Color each pixel.
    
    Nanite does this with one draw command per material.
    The material used by each pixel is computed during the second pass
    and is stored in a buffer.
    Each material draw during the third pass ignores pixels that don't have the desired material.
    Using some hardware developed to speed up depth buffers[^HiZ],
    this can skip entire materials if they are not visible.
    To increase the frequency of such material skips,
    Nanite renders the third pass in tiles instead of the entire screen at once
    to increase the likelihood that a given tile will skip most materials.
    
    The third pass computes the usual range of shading operations
    such as shadows, ambient occlusion, environment mapped reflections, etc.
    
    It is common for shading code to do some math on interpolated values
    prior to using them in shading, including in shading operations that depend on derivatives such as texture lookup and mip level selection.
    Nanite has the derivatives of attributes available from the second pass
    and can usually apply the chain rule to propagate the derivatives through such operations,
    but it has a fallback approximation based on the difference in adjacent pixels for the few operations that do not have well-defined derivatives.

[^HiZ]:
    There are various advances in depth comparisons;
    the one Nanite uses is called "Hierarchical Z-Buffer" (not to be confused with the same-named HZB Nanite uses for occlusion culling) or "HiZ".
    Conceptually, this works as follows:
    
    1. Store tiles or low-res copies of the z-buffer, similar to the HZB noted above but with both min and max values, sometimes called an "HTILE."
    
    2. If a chunk of incoming geometry's max z is less than a tile's min z, it's all visible, no per-pixel depth checks needed.
        If a chunk of incoming geometry's min z is greater than a tile's max z, it's all invisible, no additional work needed.
    
    In practice, GPUs have developed various optimizations and extensions of this basic idea, handling other kinds of depth tests and other sources of depth information as well.
    
    Nanite uses this with the depth test set to "equal to" instead of the default "less than".
    Depending on the maturity of the GPU's HiZ implementation,
    this should discard a pass where no pixel has a depth (in this case not a true depth but rather a proxy for material ID) equal to the target depth (material) for the current path.

## Software rasterizer

In highly-detailed scenes, the pixel-accurate LOD selection process causes the vast majority of triangles to be on the order of 1 screen pixel in size.
For triangles that small, most of the work done by the GPU's built-in rasterizer is unnecessary;
the three-part deferred pipeline further removes the need for some of the GPU's work.
For example, the following are sometimes implemented and not needed by pixel-sized triangles:

- [Bresenham, like DDA](dda.html#bresenham-hardware) performs some per-triangle work in order to make the per-fragment work as low as possible. When a triangle has only a few fragments, this is not the most optimal decision.

- [Hyperbolic interpolation](dda.html#hyperbolic-more-accurate) is unnecessary because the difference between linear and hyperbolic interpolation is only visible when triangle $w$ values differ by a significant ratio, which they don't for pixel-scale triangles.

- [Frustum clipping](clipping.html) is important for large triangles, but pixel clipping is much faster if the triangles only have a few off-screen pixels.

- Large triangles have poor cache locality so many GPU's render the scene in *tiles*, repeating some computations for triangles that span multiple tiles to get better cache locality.

- Memory operations have better throughput if given more data at a time, so GPUs often send *stamps* of 4 or more adjacent pixels to the frame and z buffer together, adding additional logic to make sure the entire stamp has the same visibility in the depth test first.

- Various optimizations of the z-buffer try to take advantage of large triangles,
    for example by checking a triangles z range against a hierarchical z-buffer before rasterizing as a form of occlusion culling
    or performing depth tests for groups of fragments in a single operation and only checking individual fragments if some but not all the members of the group pass.

- GPUs tend to organize their hardware to prioritize processing many fragments of a triangle in parallel over processing a few fragments each from many triangles in parallel.
    This manifests in them having the hardware to issue 4--8 triangle rasterizations per cycle
    along with hardware to process thousands of fragments per cycle.
    
Put together, this means that the hardware rasterizer is not optimized for Nanite's common case.
Nanite overcomes this by splitting triangles into two cases.
It computes the screen bounding box of each triangle;
if that box is both (a) smaller than *x* pixels (where *x* was tuned by profiling to 256 for Unreal 5)
and (b) fully within screen bounds, then it is rendered by software; otherwise it is sent through the usual hardware rasterizer.
The software rasterizer uses a lightweight algorithm somewhere between linear DDA and loping over all pixels in the bounding box and checking if each is inside the triangle.

To have software and hardware work together, uses neither the hardware-only z buffer nor the frame buffer.
Instead, both the software inner loop and the hardware fragment shader use a 64-bit atomic[^atomics]
to store a bit-encoded (depth, instance ID, triangle ID) tuple in a frame-sized buffer
if and only if the encode tuple has a smaller value (using unsigned integer comparisons) than whatever was in that buffer before.

[^atomics]:
    Atomic operations are an important and ongoing development in computer hardware design, but not covered in any of this course's prerequisites.
    In essence, they define a tiny program that acts as if it runs in an instant with no other threads or processes able to see an intermediate state.
    Typically, these operations are so small you can write them in just a few characters of most programming languages,
    such as `x += y`{.js} or `if (x==y) x = z`{.js}.
    
    Atomic operations are often identified by their bit width:
    it is trivial to make a 1-bit atomic operation
    but the hardware gets more complicated as more bits are involved.
    Nanite's software renderer relies on a GPU-accessible atomic operation
    equivalent to `if (x > y) x = y`{.js} for 64-bit unsigned integers.


## Multiple simultaneous views

Given all the steps discussed above, Nanite's render pipeline is fairly deep.
That depth adds latency to any given frame render
and means that running the entire pipeline multiple times per frame is inadvisable.
But there are many reasons why an application might wish to render multiple views in a single frame:
the most common is rendering to a [shadow buffer](shadowmap.html),
but it is also common to render [dynamic cube maps](textures2.html#dynamic-environment-maps),
render two views for binocular displays such as 3D monitors and VR headsets,
and combining multiple views using a [stencil buffer](other-rasterization.html#stencil-buffer) to create planar reflections, magical portals, and similar effects.

The three-pass rendering means Nanite has a relatively loose separate connection
between most of the rendering pipeline and the frame buffer.
The adjustments needed to support the software rasterizer make that connection even more flexible,
and dynamic-priority LOD selection readily supports having more- and less-important views and balancing resources between them accordingly.
Nanite takes advantage of these features to support rendering to an array of views in a single pass through the Nanite pipeline,
including having different views have different LOD priorities
and stopping at different steps through the pipeline;
for example, shadow views are lower priority than the scene view they are shadowing and only end the first stage of deferred rendering.

## Virtual shadow buffer

Nanite uses a single large (16384×16384) virtual texture for each light source's shadow map.
However, most of this virtual texture is largely empty.
Each frame the mip level needed to make one shadow buffer texel the same size as one pixel for each pixel in the scene is marked.
If those mip levels for those tiles are already populated and neither the light nor the shadow caster has moved, they are left as is.
Otherwise a render view for just that mip and tile is requested as one of the views to be rendered.
LOD and occlusion culling are applied as normal during these renders, allowing the desired resolution of shadow to be generated with minimal effort.

This process has various implementation details that must be handled correctly for the whole process to work.
Given it uses 4-byte depth buffer precision, it would require 1GB per shadow map if it were fully stored anywhere, so sparse paging is a must[^pagetable].
Using the LOD from the viewpoint (i.e. based on distance from the light, not the viewer) is important to achieve the proper shadow resolution
but means that the light and viewer often render the same geometry using clusters at different LODs, meaning depths rarely line up right;
this is fixed by adding a screen-space trace to confirm shadowing, walking a few pixels towards the light source if the difference in depths is small to verify that the shadow caster is in fact present in the scene.
There's also some additional handling needed for directional lights like the sun
and point lights that might cast shadows in any direction.

Virtual shadows are not required by Nanite: it also supports other shadowing techniques.
Virtual shadowing is not practical without Nanite.

## Compression

Nanite uses compressed representations for most data,
and two different compressions: a directly-readable in-memory format
and a more space-efficient but compute-expensive on-dick format.

In memory, the core idea is to bound the range of values per cluster
and store each value with the minimum allowable bits as a bit stream, not a byte stream.
For example, if a cluster's $x$ values range from 0x38.F2 to 0x3A.3E with 8 bits of precision past the binary point, only 10 bits are needed per $x$ value.
Triangle indices are stored with the smallest index in full precision and then two offsets; with 128-triangle clusters and clever ordering of vertices, this can be just 17 bits per triangle.
Texture coordinates, material indices, and normals are encoded with similar bit-oriented reasoning.

On disk, existing [LZ compression](https://en.wikipedia.org/wiki/LZ77_and_LZ78) is used.
These are byte-based, so the bit-oriented approaches of the in-memory design are not a good fit.
The space saving gained by LZ compression is roughly proportional to the skew of the byte distribution: if all 256 byte values are equally common LZ doesn't save space while if 95% of bytes are one of a dozen specific values it can achieve order-of-magnitude compression.
Hardware LZ compression works in windows, so ordering data to have similar bytes nearby in memory is a win.
Nanite has several tricks for transforming cluster data in ways that increase the likelihood of LZ compression being happy with the results and active work to improve this further.

[^pagetable]:
    Sparse paging is widely implemented in hardware and systems software using a set of related data structures called multi-level page tables, generally introduced in either computer architecture or operating systems courses.
