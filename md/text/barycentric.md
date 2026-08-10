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
If any of those was permitted to be negative, $\mathbf p$ could be farther away from the corresponding vertex than the opposite edge of the triangle and thus outside of the triangle.

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



<figure>
<svg id="canvas" viewBox="0 0 500 500" style="border: thin solid black;">
<polygon id="triangle" points="100,250 400,450 400,50" fill="#0001" stroke="#000" />
<circle id="v1" cx="100" cy="250" r="6" fill="#f00" />
<text id="v1l" x="100" y="242" fill="#f00" text-anchor="middle">v₁</text>
<circle id="v2" cx="400" cy="450" r="6" fill="#080" />
<text id="v2l" x="400" y="442" fill="#080" text-anchor="middle">v₂</text>
<circle id="v3" cx="400" cy="50" r="6" fill="#04f" />
<text id="v3l" x="400" y="42" fill="#04f" text-anchor="middle">v₃</text>
<circle id="p" cx="300" cy="250" r="6" fill="#000" />
</svg>

:::{style="color:#f00"}
$a_1$ = <output id="a1">0.3333333333333333</output>
:::

:::{style="color:#080"}
$a_2$ = <output id="a2">0.3333333333333333</output>
:::

:::{style="color:#04f"}
$a_3$ = <output id="a3">0.3333333333333333</output>
:::

<script>
const svg = document.getElementById('canvas');
const triangle = document.getElementById('triangle');
const vertices = [
    document.getElementById('v1'),
    document.getElementById('v2'),
    document.getElementById('v3')
];
const labels = [
    document.getElementById('v11'),
    document.getElementById('v21'),
    document.getElementById('v31')
];
const outputs = [
    document.getElementById('a1'),
    document.getElementById('a2'),
    document.getElementById('a3')
];
const p = document.getElementById('p');

let activeVertex = null;
const svgWidth = svg.width.baseVal.value;
const svgHeight = svg.height.baseVal.value;
const padding = p.r.baseVal.value;

[p, ...vertices].forEach(vertex => {
    vertex.addEventListener('mousedown', (e) => {
        activeVertex = vertex;
        e.preventDefault();
    });
});

function findBarycentric() {
    const verts = vertices.map(v => [v.cx.baseVal.value, v.cy.baseVal.value]);
    const edges = verts.map((v,i) => [verts[i][0] - verts[(i+1)%3][0], verts[i][1] - verts[(i+1)%3][1]]);
    const ab_big = edges.map((e,i) => [edges[(i+1)%3][1], -edges[(i+1)%3][0]]);
    const ab_size = ab_big.map((vec,i) => vec[0]*edges[i][0] + vec[1]*edges[i][1]);
    const ab = ab_big.map((vec,i) => [vec[0]/ab_size[i], vec[1]/ab_size[i]]);
    const d = ab.map((vec, i) => -(vec[0]*verts[(i+1)%3][0] + vec[1]*verts[(i+1)%3][1]));
    const px = p.cx.baseVal.value, py = p.cy.baseVal.value;
    return [
        ab[0][0]*px + ab[0][1]*py + d[0],
        ab[1][0]*px + ab[1][1]*py + d[1],
        ab[2][0]*px + ab[2][1]*py + d[2],
    ];
}

window.addEventListener('mousemove', (e) => {
    if (!activeVertex) return;

    // Get mouse position relative to the SVG canvas viewport
    const rect = svg.getBoundingClientRect();
    let x = (e.clientX - rect.left)*(svg.viewBox.baseVal.width/rect.width);
    let y = (e.clientY - rect.top)*(svg.viewBox.baseVal.height/rect.height);

    // Constrain coordinates within the SVG bounds
    x = Math.max(padding, Math.min(svgWidth - padding, x));
    y = Math.max(padding, Math.min(svgHeight - padding, y));

    // Update the circle's center position
    activeVertex.setAttribute('cx', x);
    activeVertex.setAttribute('cy', y);
    const label = document.getElementById(activeVertex.id+'l');
    if (label) {
        label.setAttribute('x', x);
        label.setAttribute('y', y-padding-2);
    }

    // Update the triangle points dynamically
    triangle.setAttribute('points', vertices.map(v=>`${v.getAttribute('cx')},${v.getAttribute('cy')}`).join(' '));
    
    if (activeVertex === p ) {
        // Update the outputs
        const bary = findBarycentric();
        outputs.forEach((o,i) => o.textContent = String(bary[i]).replace('-','\u2012'));
    } else {
        // Update the interpolated point
        const a = outputs.map(o => Number(o.textContent.replace('\u2012', '-')));
        const verts = vertices.map(v => [v.cx.baseVal.value, v.cy.baseVal.value]);
        p.setAttribute('cx', verts[0][0]*a[0] + verts[1][0]*a[1] + verts[2][0] * a[2]);
        p.setAttribute('cy', verts[0][1]*a[0] + verts[1][1]*a[1] + verts[2][1] * a[2]);
    }
});

window.addEventListener('mouseup', () => {
    activeVertex = null;
});

</script>


<figcaption>
An interactive visualization of barycentric coordinates.
Drag the vertices to adjust the triangle.
Drag the free point to change which point's barycentric coordinates are displayed.
</figcaption>
</figure>
