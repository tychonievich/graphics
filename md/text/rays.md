---
title: Raytracing
summary: Basic theory and algorithms of ray intersections and discussion of generating secondary rays.
...

# Overview

Raytracing tries to solve the same problem as rasterization---that is, create a set of pixel colors to represent a mathematical description of stuff---but goes about it in reverse.
Where rasterization asks the questions "what pixels are contained within this object"
raytracing asks instead "what objects are visible within this pixel?"

Raytracing is currently slower than rasterization,
though it admits almost unlimited amounts of parallelism
causing some people think it will become faster in years to come.
Currently its primary advantage is that the process does not depend on raster structure
and so it can easily model reflection, transparency, and similar optical properties.

The speed of a raytracing system depends largely on the quality of the spatial hierarchy used.
Conceptually, the idea here is to collect a group of nearby objects and find a bounding box for them;
if a box is not visible from a particular pixel, none of the objects within it are either.
Such hierarchies are not a topic for this document.

## Primary and Secondary Rays

A ray is a semi-infinite line; 
it is typically stored as a point called the ray origin, $\mathbf{r_o}$; and a direction vector $\vec r_d$.
Then the ray itself is the set of points 
$\{\mathbf{r_o} + t \vec r_d \;|\; t \in \mathbb{R}^{+}\}$,
and the goal of raytracing is to find the point in the ray on the surface of another object
which is closest to the ray origin (that is, with minimal $t$).

Ray tracing creates one or more rays per pixel.
Those rays are intersected with objects in the scene and then, generally,
several secondary rays are generated from those intersection points,
and intersected with the scene again, and then more are generated, etc.,
until you get tired of shooting rays, 
at which point you do some sort of [direct illumination](lighting.html) and call it good.

There are a number of ways to generate rays from pixels.
For all of them we need the camera position and orientation, 
given by the eye position $\mathbf{e}$ and the forward, up, and right directions $\vec f$, $\vec u$, and $\vec r$.
The ray origin is generally just $\mathbf{e}$.
The most common choice for ray direction is designed to replicate the standard rasterization perspective look:
given normalized device coordinates for a pixel $(x,y)$, its ray direction is $\vec f \cos(\theta) + (x \vec r + y \vec u)\sin(\theta)$, where $\theta$ is the field of view.
Fish-eye $\left(x \vec r + y \vec u + \sqrt{1-x^2-y^2}\vec f\right)$ 
and cylindrical $\left(y \vec u + \cos(x) \vec f + \sin(x) \vec r\right)$
projections are also used in some settings.

# Rays and Ray-\* Intersections

In general, the intersection of a ray $\mathbf{r_o}+t \vec r_d$ with some object $g(\mathbf{p}) = 0$
is found as the minimal $t$ for which $g(\mathbf{r_o}+t \vec r_d) = 0$.
Constrained minimization of this type is a widely-studied problem in numerical analysis, optimization, 
and many branches of engineering and science.
However, most raytracers use only three particular solutions:
ray-plane, ray-AABB, and ray-sphere intersections.

<figure>
<svg viewBox="-6.4 -2.2 10.8 5.4" style="display:table; margins:auto; max-width: 40em; border: thin solid gray;" stroke-width="0.015">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0,0 10,5 0,10 5,5 z" /></marker>
<marker id="arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M 0,0 10,5 0,10 5,5 z" /></marker>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5"><circle cx="5" cy="5" r="5" /></marker>
</defs>
<circle cx="2" cy="0" r="1.51" fill="none" stroke="black" stroke-width="0.03"/>
<circle cx="-5" cy="2" r="0.05"/>
    <text x="-5" y="2.3" text-anchor="middle" font-size="2.5%" font-family="KaTeX_Main" font-weight="700">r<tspan dy="1%" font-size="70%">o</tspan></text>
<circle cx="2" cy="0" r="0.05"/>
    <text x="2" y="-0.2" text-anchor="middle" font-size="2.5%" font-family="KaTeX_Main" font-weight="700">c</text>
<circle cx="2.175" cy="0.565" r="0.05"/>
    <text x="2.175" y="0.965" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">c<tspan dy="-2%" font-size="50%">′</tspan></text>
<circle cx="0.75" cy="0.85" r="0.05"/>
    <text x="0.65" y="1.25" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">c<tspan dy="-2%" font-size="50%">′′</tspan></text>
<circle cx="-2" cy="1.4" r="0.05"/>
    <text x="-2" y="1.8" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">p<tspan dy="-2%" font-size="50%">′</tspan></text>
<circle cx="-5.4" cy="-0.3" r="0.05"/>
    <text x="-5.4" y="-0.5" text-anchor="middle" font-size="2.5%" font-family="KaTeX_Main" font-weight="700">p</text>
<g stroke="black">
<line x1="-5" y1="2" x2="-4" y2="1.8" marker-end="url(#arrow)" stroke-width="0.03" id="ray-direction"/>
<line x1="-5" y1="2" x2="1.9" y2="0.03" marker-end="url(#arrow2)" stroke-dasharray="0.1" id="r-to-c"/>
<line x1="-5" y1="2" x2="-5.38" y2="-0.1" marker-end="url(#arrow2)" stroke-dasharray="0.1" id="r-to-p"/>
<line x1="-5.4" y1="-0.3" x2="-5.9" y2="0.7" marker-end="url(#arrow)" stroke-width="0.03" id="normal"/>
<line x1="-6.4" y1="-0.8" x2="1.6" y2="3.2" stroke-width="0.03" id="plane"/>
<line x1="2" y1="0" x2="0.93" y2="-1.07" id="radius"/>
<line x1="2" y1="0" x2="2.175" y2="0.565" id="c-to-ray"/>
<line x1="-5" y1="2" x2="4.3" y2="0.14" marker-end="url(#arrow2)" id="ray" opacity="0.25"/>
</g>
    <text x="-5.9" y="0.2" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-style="italic">n⃗</text>
    <text x="-4.3" y="2.2" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-style="italic">r⃗<tspan dy="1%" font-size="70%">d</tspan></text>
    <text x="2.1" y="0.28" text-anchor="left" font-size="2%" font-family="KaTeX_Main" font-style="italic">d</text>
    <text x="1.5" y="-.7" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-style="italic">r</text>
    <text x="-0.6" y="0.5" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">c<tspan  font-weight="100"> − </tspan>r<tspan dy="1%" font-size="70%">o</tspan></text>
    <text x="-5.1" y="1" text-anchor="right" font-size="2%" font-family="KaTeX_Main" font-weight="700">p<tspan  font-weight="100"> − </tspan>r<tspan dy="1%" font-size="70%">o</tspan></text>
</svg>
<figcaption>Some of the geometry used in the ray-plane and ray-sphere intersection routines, all also defined in the surrounding text.</figcaption>
</figure>

## Ray-Plane Intersection

Planes can be described in a number of ways;
principle among them are implicit equations $A x + B y + C z + D = 0$,
point-and-normal form ($\vec n$, $\mathbf{p}$),
and three-point form ($\mathbf{p_0}$, $\mathbf{p_1}$, $\mathbf{p_2}$).
We will use the point-normal version, noting that $$\vec n \equiv (A,B,C) \equiv (\overrightarrow{\mathbf{p_1}-\mathbf{p_0}}) \times (\overrightarrow{\mathbf{p_2}-\mathbf{p_0}})$$
and that the point $\left(-\frac{D}{A},0,0\right)$ is on the plane.

The distance between the ray origin $\mathbf{r_o}$ and a plane is 
$(\overrightarrow{\mathbf{r_o}-\mathbf{p}}) \cdot \vec n\frac{1}{\|\vec n\|}$.
The distance the ray travels toward the plane per unit $t$ is $\vec r_d \cdot \vec n\frac{-1}{\|\vec n\|}$.
Setting these equal to one another we get
$t = \frac{(\overrightarrow{\mathbf{p}-\mathbf{r_o}}) \cdot \vec n}{\vec r_d \cdot \vec n}$.
If $t$ is positive, we can use that $t$ in the ray equation to find the intersection point $\mathbf{p'} = t \vec r_d + \mathbf{r_o}$.
If $t$ is not positive there is no intersection.

:::algorithm
Ray-Plane Intersection

Input
:   - Ray with origin $\mathbf{r_o}$ and direction $\vec r_d$
    - Plane with normal $\vec n$ through point $\mathbf{p}$

Output
:   Either "no intersection"

    Or intersection distance $t$ and point $\mathbf{p'}$

Process
:   1. Let $t = \dfrac{(\overrightarrow{\mathbf{p}-\mathbf{r_o}}) \cdot \vec n}{\vec r_d \cdot \vec n}$
 
    2. If $t > 0$, intersection found at depth $t$ is $\mathbf{p'} = t \vec r_d + \mathbf{r_o}$.
        
        Otherwise, no intersection
:::


## Ray-Sphere Intersection

Given a sphere with center $\mathbf{c}$ and radius $r$, 
we first evaluate if the ray originates inside the sphere ($\|\overrightarrow{\mathbf{c}-\mathbf{r_o}}\|^2 < r^2$) or not.
We then find the $t$ value of the point where the ray comes closest to the center of the sphere,
$t_c = \frac{(\overrightarrow{\mathbf{c}-\mathbf{r_o}}) \cdot \vec r_d}{\|\vec r_d\|}$.
If the ray origin is outside and $t_c$ is negative, there is no intersection.
Otherwise we proceed to find the squared distance of closest approach
$d^2 = \|\mathbf{r_o} + t_c \vec r_d - \mathbf{c}\|^2$.
If $d^2 > r^2$, which can only happen if the ray originates outside the sphere, then there is no intersection;
otherwise we find how far from the point of closest approach the point of intersection is as $t_{\text{offset}} = \frac{\sqrt{r^2 - d^2}}{\|\vec r_d\|}$.
If the origin is inside, the point of intersection is $\mathbf{r_o} + (t_c + t_{\text{offset}}) \vec r_d$;
otherwise, it is $\mathbf{r_o} + (t_c - t_{\text{offset}}) \vec r_d$.

:::algorithm
Ray-Sphere Intersection

Input
:   - Ray with origin $\mathbf{r_o}$ and **unit-length** direction $\vec r_d$
    - Sphere with center $\mathbf{c}$ and radius $r$

Output
:   Either "no intersection"

    Or intersection distance $t$ and point $\mathbf{p'}$

Process
:   1. let `inside` be $\left(\|\overrightarrow{\mathbf{c}-\mathbf{r_o}}\|^2 < r^2\right)$
    2. let $t_c = \dfrac{(\overrightarrow{\mathbf{c}-\mathbf{r_o}}) \cdot \vec r_d}{\|\vec r_d\|}$
        
        _This is the distance along the ray to $\mathbf{c}'$, the rays' closest approach to $\mathbf c$, but we don't need $\mathbf{c}'$, only $t_c$_
    3. if not `inside` and $t_c < 0$, no intersection
    4. let $d^2 = \|\mathbf{r_o} + t_c \vec r_d - \mathbf{c}\|^2$
    5. if not `inside` and $r^2 < d^2$, no intersection
    6. let $t_{\text{offset}} = \dfrac{\sqrt{r^2 - d^2}}{\|\vec r_d\|}$
    
        _This is the difference between $t$ and $t_c$; rays intersect spheres twice (once entering, once exiting) so $t_c \pm t_{\text{offset}}$ are both intersection points_
    7. if `inside`, intersection found at depth $t=t_c + t_{\text{offset}}$ is $\mathbf{c''} = t \vec r_d + \mathbf{r_o}$
        
        otherwise, intersection found at depth $t=t_c - t_{\text{offset}}$ is $\mathbf{c''} = t \vec r_d + \mathbf{r_o}$
:::



## Ray-AABB Intersection
It is rare to want to create images of axis-aligned bounding boxes (AABBs),
but it is easy to find ray-AABB intersections and easy to find the AABB that contains a set of objects,
so most raytracers try AABB intersections for sets of nearby objects before checking for intersections with the objects within the AABB.

AABBs consist of six axis-aligned planes. 
For the axis-aligned case, the ray-plane intersection becomes quite simple because the normal has only one non-zero element;
thus, for the plane, e.g., $x = a$, the $t$ value of intersection is $t_{x=a} = \frac{a - \mathbf{r_o}_x}{\overrightarrow{r_d}_x}$.
The ray then intersects the AABB if and only if there is some positive $t$ between all six planes;
for minimum point $(a,b,c)$ and maximum point $(A,B,C)$, we have
$$[0,\infty) \cap [t_{x=a}, t_{x=A}] \cap [t_{y=b}, t_{y=B}] \cap [t_{z=c}, t_{z=C}] \ne \emptyset.$$
It is usually not important to know the $t$-value for an AABB intersection,
but if needed it is simply the smallest $t$ in the interval defined above.

# Inverse Mapping and Barycentric Coordinates

Once you have found an intersection with some object
it is generally desirable to know where you hit it
so that you can apply texture mapping, normal interpolation, or the like.
This process is called "inverse mapping."


## Inverse Sphere Mapping

For a sphere, if the point of intersection is $\mathbf{p}$
then the normal simply points from the center to the point of intersection,
$\vec n = \frac{1}{r}\left(\overrightarrow{\mathbf{p} - \mathbf{c}}\right)$.
From that it is easy to derive that the longitude is $\mathtt{atan2}(n_x, n_z)$
and the latitude is $\mathtt{atan2}\left(n_y, \sqrt{n_x^2 + n_z^2}\right)$.

## Inverse Triangle Mapping

For a triangle, the typical inverse mapping gives you the Barycentric coordinates of the point of intersection.
Barycentric coordinates are three numbers, one per vertex of the triangle,
which state how close to each of the three vertices the point in question is.
In particular, given an intersection point of $\mathbf{p}$ and vertices $\mathbf{p_0}$, $\mathbf{p_1}$, and $\mathbf{p_2}$, the barycentric coordinates $(b_0, b_1, b_2)$ satisfy the two properties that

a. they sum to 1, and
b. $\mathbf{p} =  b_0\mathbf{p_0} + b_1\mathbf{p_1} + b_2\mathbf{p_2}$.

Every point in the same plane as the triangle has a unique set of Barycentric coordinates,
and all three coordinates are positive if and only if the point is within the triangle's bounds.

There are many techniques for inverse mapping a triangle.
The one I present here is not the most common,
but is easy and efficient as long as you compute and store the information only once.
First, observe that since $b_i$ is the "nearness" to point $\mathbf{p_i}$, 
it is also the distance from the edge joining the other two points.
This distance can be found directly by using a dot product with a vector perpendicular to this edge.

<figure>
<svg viewBox="-4.5 -2.7 8 5.5" style="display:table; margins:auto; max-width: 40em; border: thin solid gray;" stroke-width="0.015">
<defs>
<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0,0 10,5 0,10 5,5 z" /></marker>
<marker id="arrow2" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M 0,0 10,5 0,10 5,5 z" /></marker>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5"><circle cx="5" cy="5" r="5" /></marker>
</defs>
<circle cx="-2" cy="-2" r="0.05" id="p0"/>
<circle cx="3" cy="-2" r="0.05" id="p1"/>
<circle cx="-4" cy="2" r="0.05" id="p2"/>
<circle cx="0" cy="-1" r="0.05"/>
<path fill="none" stroke="black" d="M -2,-2 3,-2, -4,2 Z"/>
<g stroke="black" marker-end="url(#arrow2)" stroke-dasharray="0.1">
<line x1="-1" y1="-2" x2="-1" y2="2" id="e2"/>
<line x1="-2.25" y1="-1.5" x2="1.75" y2="0.5" id="e1"/>
<line x1="-2" y1="0.8333333" x2="-3.333333" y2="-1.666666" id="e0"/>
<line x1="-2" y1="-2" x2="-0.06" y2="-1.03" id="off" stroke-dasharray="0.03"/>
</g>
<!---->
<text x="0.1" y="-1" text-anchor="left" font-size="2%" font-family="KaTeX_Main" font-weight="700">p</text>
<!---->
<text x="-2" y="-2.2" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">p<tspan dy="1%" font-size="70%">0</tspan></text>
<text x="3" y="-2.2" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">p<tspan dy="1%" font-size="70%">1</tspan></text>
<text x="-4" y="2.3" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-weight="700">p<tspan dy="1%" font-size="70%">2</tspan></text>
<!---->
<text x="-3.4" y="-1.8" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-style="italic">e⃗<tspan dy="1%" font-size="70%">0</tspan></text>
<text x="1.8" y="0.6" text-anchor="left" font-size="2%" font-family="KaTeX_Main" font-style="italic">e⃗<tspan dy="1%" font-size="70%">1</tspan></text>
<text x="-1" y="2.3" text-anchor="middle" font-size="2%" font-family="KaTeX_Main" font-style="italic">e⃗<tspan dy="1%" font-size="70%">2</tspan></text>
</svg>
<figcaption>Finding Barycentric coordinates.  If $\vec{e_2} \cdot (\mathbf{p_2}-\mathbf{p_0}) = 1$, then $b_2 = \vec e_2 \cdot (\mathbf{p}-\mathbf{p_0})$, and similarly for $b_1$. Since $b_0+b_1+b_2 = 1$, $b_0$ is simply $1 - b_1 - b_2$.  Thus, assuming that correctly-scaled $\vec e_1$ and $\vec e_2$ are precomputed, we can compute the barycentric coordinates using just six multiplies and nine adds.</figcaption>
</figure>

in that image, $b_1 = \vec e_1 \cdot (\mathbf{p}-\mathbf{p_0})$ 
because $\vec e_1$ points directly away from the edge between $\mathbf{p_{i\ne1}}$.
Similarly, $b_2 = \vec e_2 \cdot (\mathbf{p}-\mathbf{p_0})$ and $b_0 = 1-b_1 - b_2$.
It thus suffices to find $\vec e_1$ and $\vec e_2$ in order to find the barycentric coordinates.
This may be done as
$$\begin{split}
\vec a_1 &= \overrightarrow{\mathbf{p_2}-\mathbf{p_0}} \times \vec n\\
\vec a_2 &= \overrightarrow{\mathbf{p_1}-\mathbf{p_0}} \times \vec n\\
\vec e_1 &= \frac{1}{\vec a_1 \cdot \overrightarrow{\mathbf{p_1}-\mathbf{p_0}}} \vec a_1 \\
\vec e_2 &= \frac{1}{\vec a_2 \cdot \overrightarrow{\mathbf{p_2}-\mathbf{p_0}}} \vec a_2
\end{split}$$
These two $\vec e_i$ vectors can be precomputed and stored along with the normal $\vec n$ in each triangle data structure to allow rapid ray-triangle intersections.  Note that this also suffices for the inside-outside test needed to turn a ray-plane intersection into a ray-triangle intersection; a point is inside a triangle if and only if all three barycentric coordinates are between zero and one.

Because $\mathbf{p} =  b_0\mathbf{p_0} + b_1\mathbf{p_1} + b_2\mathbf{p_2}$, 
we can use the barycentric coordinates to find all the information stored in each vertex
interpolated to any point on the interior of the triangle:
$\vec{p} =  b_0\vec{p_0} + b_1\vec{p_1} + b_2\vec{p_2}$.
You can then use that information just as you would interpolated fragment values during rasterization.


# Secondary Rays

Shadows, reflection, and transparency are easily achieved using secondary rays:
Once you find an intersection point $\mathbf p$ you then generate a new ray
with $\mathbf p$ as its origin and intersect that ray with the scene.

Care should be taken that roundoff errors in storing $\mathbf p$ 
do not cause the the secondary ray to intersect the object from which it originates.
This cannot be done simply by using more precise numbers;
instead you'll need to do one of the following:

- Bias the secondary rays away from the object that emits them.
    Effectively this means ignoring ray intersections with $t<\epsilon$ for some small positive $\epsilon$.
    If your $\epsilon$ is too small, you'll still get some self-intersections causing shadow acne or the like.
    If your $\epsilon$ is too large, opaque objects will render as invisible when seen from up close.

- Ignore intersections with the (part of the) object that emitted the ray.
    For sphere reflections and shadows this means ignoring the sphere.
    For sphere transparency it means ignoring the same entering/exiting intersection of the sphere.
    For triangle meshes is means ignoring the triangle and its immediate neighbors.

- Require particular directional interfacing.
    If all of your geometry is in the form of non-intersecting closed surface meshes
    then you can classify each ray as internal or external
    and each intersection as either entering or exiting
    and ignore intersections that don't match the ray type.
    The conditions on this make it unusual as-is,
    but a variant combining it with biasing can work well.


## Shadows

A point is in shadow relative to a particular light source
if the ray $(\mathbf p, \vec \ell)$ intersects anything closer than the light source itself.

## Reflection

A mirrored object's color is given by the ray tracing result
of the ray with origin $\mathbf p$ and direction $2(\vec n \cdot \vec e)\vec n - \vec e$.
A partially mirrored object mixes that color result with a standard lighting computation at $\mathbf p$.
One reflection ray might generate another;
a cutoff number of recursions is necessary to prevent infinite loops.

## Transparency

Transparency is somewhat more complicated, relying on Snell's Law.
For it to make sense, every surface needs to be a boundary between two materials,
which is not trivially true in the case of triangles nor intersecting objects.
However, assuming that we know that the ray is traveling 
from a material with index of refraction $n_1$ for index of refraction $n_2$,
we can derive a rule for finding the transmitted ray.

The cosine of the entering ray is $(\vec e \cdot \vec n)$,
meaning that it's sine is $\sqrt{1-(\vec e \cdot \vec n)^2}$, or $\|-\vec e -(\vec e \cdot \vec n)\vec n\|_2$.
The sine of the outgoing vector thus needs to be $\frac{n_1}{n_2}\sqrt{1-(\vec e \cdot \vec n)}$;
if that is greater than 1, we have total internal refraction and use the reflection equation instead;
otherwise, the cosine of the outgoing ray is $\sqrt{1-(\frac{n_1}{n_2})^2(1-(\vec e \cdot \vec n))}$.  Putting this all together, we have

:::algorithm
1. let $a = \vec e \cdot \vec n$ 
2. let $b = \frac{n_1}{n_2}\sqrt{1-(\vec e \cdot \vec n)}$
3. if $b \ge 1$, return $2(\vec n \cdot \vec e)\vec n - \vec e)$
4. let $c = \sqrt{1-\frac{n_1^2}{n_2^2}(1-(\vec e \cdot \vec n))}$
5. return $\frac{n_1}{n_2}(-\vec e -(\vec e \cdot \vec n)\vec n) - c \vec n$
:::

## Global Illumination

The standard lighting models pretend like the world is divided into a small number of light emitters
and a vast supply of things that emit no light.
This is obviously not true; if nothing but light sources gave off photons, we could only see the light sources themselves.
With global illumination, 
you try to discover the impact of light bouncing off of the wall, floor, and other objects 
by creating a number of secondary rays sampling the diffuse reflection of each object.  
Ideally, the distribution of rays should parallel 
the chosen model of diffuse lighting (see Section~\ref{diffusion}) 
and should be so dense as to be intractable for any reasonable scene.
Much of the research in photo-realistic rendering is devoted to finding shortcuts and techniques
that make this process require fewer rays for the same visual image quality.

# Photon Mapping and Caustics

Photon mapping is raytracing run backwards: instead of shooting rays from the eye,
you shoot them from the lights.
The quantity of light reaching each point in the scene is recorded 
and used when the scene is rendered, either by raytracing or rasterizing.
Since many photons leaving a light source never reach the eye, 
this is an inefficient way of creating a single picture;
however, it allows lens and mirror-bounced light (called caustics) to be rendered,
and it can be more efficient than viewer-centric global illumination 
if many images are to be made of the same static scene.

# Sub-, Super-, and Importance-Sampling

Sub-sampling is shooting fewer rays than you have pixels, interpolating the colors to neighboring pixels.
Super-sampling is shooting several rays per pixel, averaging colors to create an anti-aliased image.
Importance sampling shoots fewer rays per pixel into "boring" areas and more into "important" areas.
Image-space importance sampling shoots more rays into areas of the scene where neighboring pixels differ in color; 
scene-space importance sampling shoots more rays toward particular items.

