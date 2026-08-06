---
title: Barycentric coordinates
...

Barycentric coordinates are used by common implementations of all rasterizing and raytracing algorithms.

Given a triangle with vertices $(\mathbf v_1, \mathbf v_2, \mathbf v_3)$,
each point $\mathbf p$ in the triangle
has unique barycentric coordinates $(a_1, a_2, a_3)$ such that

- $\mathbf p = a_1 \mathbf v_1 + a_2 \mathbf v_2 + a_3 \mathbf v_3$,
- $a_1+a_2+a_3 = 1$, and
- $0 \le a_i$ for $i \in \{1,2,3\}$.

<details class="aside"><summary>The meaning of each of the three properties</summary>

The first property, $\mathbf p = a_1 \mathbf v_1 + a_2 \mathbf v_2 + a_3 \mathbf v_3$, explains how the point $\mathbf p$ can be created as a weighted sum of the three vertices of the triangle. It's what makes these be the barycentric coordinates of that specific point rather than a different point.

The second property, $a_1+a_2+a_3 = 1$, means that $\mathbf p$ is a weighted average of the three vertices, and geometrically ensures that $\mathbf p$ is in the same plane as the triangle.
If the triangle does not contain the origin $(0,0,0)$, violating this constraint can represent any point in 3D space.

The third constraint, $0 \le a_i$ for $i \in \{1,2,3\}$, ensures that $\mathbf p$ is inside the triangle.
If any of those was permitted to be negative, $\mathbf p$ could be farther away from the corresponding vertex than the oposite edge of the triangle and thus outside of the triangle.

Note that from the second and third properties combined we can derive $a_i \le 1$ for $i \in \{1,2,3\}$;
there are some cases where checking this on one or two Barycentric coordinates can speed up some computations.

</details>

Barycentric coordinates apply no matter the dimensionality of the points.
If each vertex has a position $(x,y,z)$
and a texture coordinate $(s,t)$
and a visual surface normal $(n_x, n_y, n_z)$
and a color $(r,g,b)$
and an opacity $(a)$,
we can define the vertices as 12-element vectors $(x,y,z, s,t ,n_x,n_y,n_z, r,g,b,a)$
and use barycentric coordinates to find all 12 values at any given point inside the triangle.

