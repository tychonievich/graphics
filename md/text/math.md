---
title: Graphics Math
...

There are several core mathematical tools that I have learned are difficult for students to master.
This page is an overview trying to provide context and the big ideas of each.
More detailed pages on each topic are provided in linked-to pages.

:::tldr

Major topics on this page

- A <dfn>vector</dfn> is a general mathematical construct that is used for many purposes in graphics.

- 3D vectors are used to represent <dfn>points</dfn>, which are locations in 3D space; <dfn>offsets</dfn> which have direction and magnitude but not location; and <dfn>directions</dfn> which lack magnitude.

- Homogeneous vectors use 4D vectors to represent 3D point or direction. They are of primary benefit for making matrices more powerful.

- 4×4 transformation matrices multiplied by homogeneous vectors can represent any combination of
    - Rotation
    - Scaling
    - Translation
    - Projection
    
    Rotation and scaling occupy the same part of the matrix (the top-left 3×3 submatrix)
    while translation and projection have their own matrix regions (the last column and last row, respectively).

- Quaternions use a 4D vector to represent a 3D rotation. They require slightly more computation to use than a 3×3 matrix, but they use less memory and can be interpolated much more naturally to create smooth animations of changing rotations.

- Typographically, we use

    | Example | Description | Use |
    |:-:|:--|:--|
    | $\vec x$ | arrow | a generic vector, or a direction |
    | $\mathbf x$ | boldface | a point or position |
    | $\hat x$ | circumflex | a direction or unit-length vector |
    | $\~x$ | tilde | a generic homogeneous vector |
    | $\frak x$ | fraktur | a quaternion |
    | $X$ | upper-case | a matrix |

- We often want to define functions with directions as input, or equivalently over the surface of a unit sphere.
    
    - Environment maps are a class of textures that sample the function on a regular grid, transform that grid into the surface of a sphere, and interpolate between samples to find values for all directions. Three environment map formats are particularly common in graphics:
    
        - Equirectangular projections are used to share environment maps between applications.
        - Cube maps have direct hardware support in many GPUs.
        - Tetrahedral maps are more efficient than cube maps, but are newer and distort pixels more.

    - Spherical harmonics are a special set of polynomial basis functions
        that are very good at storing very low-resolution smooth functions
        like diffuse illumination.

:::


# Points, directions, and offsets

A 3D point exists at a specific location in space.
We show them with bold-face variables like $\mathbf p$
and can store them as 3 numbers, $(p_x, p_y, p_z)$.

A 3D offset is the difference between two 2D points.
We show them with an arrow over the variable $\vec o$
and can store them as 3 numbers, $(o_x, o_y, o_z)$.

A 3D direction is an offset without the offset's length.
We show them with an circumflex over the variable $\hat d$
and can store them as 3 numbers, $(d_x, d_y, d_z)$,
where the Euclidean length of the numbers is $1$;
that is, $\sqrt{d_x^2 + d_y^2 + d_z^2} = 1$.

Note that all three can be stored as 3 numbers,
and hence all three are sometimes called "vectors",
but their meanings are distinct
and not all vector operations make sense on all of them.

# Homogeneous vectors and matrices

Homogeneous vectors are used to store 3D points and 3D directions
using 4, not 3, numbers.
In common or normalized form, 3 of those numbers are the same 3 numbers noted in the previous section;
the 4th is 1 for a point and 0 for a direction.
Typically, that four coordinate is called $w$.

Homogeneous vectors have a special property:
their meaning is not changed by multiplying them by a scalar.
By definition, $(1,2,3,4)$ and $(-3,-6,-9,-12)$ mean exactly the same thing as one another:
and both would be normalized to $(0.25, 0.5, 0.75, 1)$
and mean the point $(0.25, 0.5, 0.75)$.

If it is necessary to identify a variable as referring to a homogeneous vector,
we indicate that with a tilde over the variable, like $\~x$.
However, we'll usually use the point or direction style instead.

The extra coordinate allows homogeneous vectors to
distinguish between points and directions,
to implicitly include division by the magnitude of the $w$ coordinate,
and to encode more kinds of transformations inside a matrix.

In graphics, we often use 4×4 transformation matrices,
and almost always assume they are multiplied on the left side of a homogeneous vector to get a new homogeneous vector:
$$\begin{bmatrix}x'\\y'\\z'\\w'\end{bmatrix} =
\left[\begin{array}{ccc:c}
  a & b & c & t_x \\
  d & e & f & t_y \\
  g & h & i & t_z \\\hdashline
  w_x & w_y & w_z & w_w \\
\end{array}\right]
\begin{bmatrix}x\\y\\z\\w\end{bmatrix}$$

These 4×4 matrices can be divided into three parts:

- The bottom row sets the new $w$ coordinate and is usually $\begin{bmatrix}0&0&0&1\end{bmatrix}$.
    If it is anything else, we call this a <dfn>projection</dfn> matrix
    because after using the matrix we have to bring the resulting vector back to a normalized $w$ value
    by dividing by the $w$ it has;
    in 4D, this is projecting the point along a line through the origin onto the $w=1$ hyperplane.
    
    Projection matrices are used with points, but not with directions or offsets,
    and are generally the last step in any given set of transformations.

- The last column (without the last row) is called the <dfn>translation vector</dfn>.
    When the matrix is multiplied by a point ($w=1$),
    this column gets added to the resulting vector, effectively applying an offset to move the point.
    When the matrix is multiplied by a direction ($w=0$),
    this column has no impact on the result, which is consistent with how moving an object
    does not change the direction it is facing.
    The act of moving objects in this way is called <dfn>translating</dfn> them.

- The remaining 3×3 matrix does what 3×3 matrices would do to 3-vector representations of points and directions.
    By the singular value decomposition, this can always be broken into three actions:
    
    1. Rotate the point/direction about the origin.
    2. Scale the point/direction in each axis about the origin.
    3. Rotate the point/direction about the origin.
    
    Usually in 3D transformations we don't scale at all
    because most objects can't change size.
    If there's no scale, this 3×3 matrix is just a simple rotation.
    
    When we do scale, it's most often a uniform scale (the same in all 3 axes)
    in which case the two rotations combine into just one rotation.
    

<details class="aside"><summary>The so-called "sheering" transformation</summary>

It is common to see older graphics literature refer to "sheering" as if it were a primary transformation category
like rotation or translation is.
I have never seen sheering used in any real graphics context, but the term is used widely enough that knowing it might save you from some embarrassment later in life.

A sheer matrix looks like an identity matrix except that some of the zero elements in one column are replaced with non-zero values.
It causes the coordinates with non-zero values added to their row
to translate an amount based on the coordinate of that column.

This same result can be created with a rotation, non-uniform scaling, and a second rotation,
and in most 3D contexts they two cannot be distinguished because the cardinal axes that make sheering matrices look special do not generally have clear 3D meaning.

Translations are a 4D sheer using the $w$ column.
They're the only kind of sheer I've seen used in 3D graphics,
and I've never seen them referred to as sheering except in explanatory texts like this.

</details>

It is common to build transformation matrices out of a sequence of individual steps,
multiplying the individual matrices together to make a single matrix that does all the things.
It's worth remembering that because the vector is multiplied on the right,
the first matrix to apply is the right-most, not the left-most.

Sometimes we build two or three matrices instead of one.

- The projection matrix should be multiplied by points but not by directions, so it's usually kept separate.

- Matrices are often used both to position models in the 3D world
    and to position the world in front of a fixed camera viewpoint^[Moving the world in front of a fixed camera located at the origin and looking down one axis makes much of the math of rasterization much simpler. For raytracing, however, that movement doesn't add efficiency so raytracing often moves the camera instead of moving the scene.].
    If the 3D world coordinates are needed for lighting, the <dfn>model</dfn> and <dfn>view</dfn> matrices are kept separate;
    if not, they are combined into a single <dfn>model view</dfn>^[also spelled "model-view", "modelView", or "modelview", depending on the source] matrix.

We have special names for some classes of transformations:

| Name       | Rotate | Uniform Scale | Nonuniform scale | Translate | Project |
|------------|:-:|:-:|:-:|:-:|:-:|
| Projective | ✔ | ✔ | ✔ | ✔ | ✔ |
| Affine     | ✔ | ✔ | ✔ | ✔ |   |
| Similarity | ✔ | ✔ |   | ✔ |   |
| Linear     | ✔ | ✔ | ✔ |   |   |
| Rigid      | ✔ |   |   | ✔ |   |

Projective transformations keep straight lines straight.
Affine transformations keep parallel lines parallel.
Similarity transformations keep angles between lines and relative size of shapes unchanged.
Linear transformations keep the origin unchanged.
Rigid transformations keep shapes and sizes unchanged.



# Quaternions

Matrices can represent rotations, but they're not great at interpolating between two rotations to get a rotation halfway in between.
For that, we use a different 4-vector called a quaternion.

A <dfn>quaternion</dfn> is a generalization of complex numbers to 4D instead of 2D.
Most of the math of quaternions is irrelevant to graphics.
What is relevant is

- Quaternions are represented as 4-vectors: one real component (often denoted $w$) and three different imaginary ones (often denoted $(x, y, z)$).

- Each quaternion has a magnitude, which is the usual Euclidean length in 4D.

- Each quaternion has a complex conjugate, which has the same $w$ and the negation of the other coordinates $(-x, -y, -z)$.

- We can rotate a 3-vector $\vec x$ using a unit-magnitude quaternion by
    
    1. adding $w=0$ to $\vec x$ to make it into a quaternion $\frak x$
    2. using quaternion product $\frak q \frak x \frak q^*$ to get the rotated vector
    
    The rotation will rotate around the $(x,y,z)$ axis of the quaternion, with angle of the rotation being $2 \arctan\left(\frac{\sqrt{x^2+y^2+z^2}}{w}\right)$

All of this is to say, quaternions represent 3D rotations.
Quaternions are the preferred way to represent rotations
if you need to interpolate between them (e.g. for animation)
or need to save space.
Matrices are faster to compute with, and can be combined with other operations,
so they are preferred in other contexts.

<details class="note"><summary>Rotation matrix or quaternion?</summary>

Space
:   A rotation matrix is 9 numbers, a quaternion is only 4.

Time
:   Rotating a vector with a matrix is 3 dot products (3 `*+` and 3 `+-`).
    
    Rotating a vector with a quaternion is 2 cross products and 2 fused multiply-adds (6 `*+`).
    
    There are tricks whereby rotating 4 vectors by the same quaternion can be the same cost as rotating just one (6 `*+`), but I've rarely seen it used in graphics..

Combination
:   Combining two rotation matrices into one is 9 dot products (9 `*+` and 9 `+-`).
    
    Combining two quaternions into one is 4 dot-product-like operations (4 `*+` and 4 `+-`).

Affine combination
:   Rotation, translation, and scale can all be combined into a single 4×4 matrix.
    
    With quaternions, the three operations must be kept separate, with the order of operations preserved.

Interpolation
:   Linear interpolation of rotation matrices create scaling artifacts which are visually jarring and computaitonaly expensive to remove.
    
    Linear interpolation of quaternions works well.

Put together, there's not a single clear winner.
The most common approach I've seen is to
animate a model using quaternions and offsets,
then convert them to matrices before applying them to vertices as the first step in rendering.
</details>

If it is necessary to identify a variable as referring to a quaternion,
we indicate that with a fraktur variant of the variable, like $\frak q$.

# Approximating functions across spheres

It is often necessary to represent a sampled function defined over the surface of a sphere,
or equivalently with a direction as the function's input.
These are most often used to represent the light arriving at a point from each direction,
which is called an <dfn>environment map</dfn>, but can represent any kind of direction-dependent data.

There are two broad ways these sampled functions are commonly defined:

- <dfn>Textures</dfn> sample a function at a set of regularly-spaced points called <dfn>texels</dfn>
    and interpolates between the nearest texels to cover the rest of the surface.
    For the surface of a sphere, there are two ways of distrbuting the points in common use:
    cube maps and the octahedral maps.
    But data is usually provided in an equirectangular projection instead of either of those maps.

- <dfn>Spherical harmonics</dfn> approximate a function as the weighted sum of a set of simpler fenctions defined across the sphere.
    While conceptually more complicated than textures,
    these can represent smooth functions with many fewer numbers than textures
    and can be rotated arbitrarily with no loss of precision.


## Equirectangular projections

The challenges of representing the sufrace of a sphere in 2D has been long studied in cartography,
and many map projections are known.
The one most often used to provide environment map texture files
is called the "equirectangular" projection.

Equirectangular projections are $W×H$-pixel images
that are always twice as many pixels wide as they are tall, meaning $W = 2H$.
Each pixel coordinate represents a specific latitude and longitude on the sphere:
in particular, pixel $(x,y)$
is latitude $\frac{2y-H}{2H} \pi$ (or $\frac{2y-H}{2H} 180°$)
and longitude $\frac{2x-W}{W} \pi$ (or $\frac{2x-W}{W} 180°$).

Equirectangular projections do not have the same solid angle for each pixel^[Solid angle is the area of the unit sphere's surface covered by some patch on the sphere or group of directions. The solid angle of the entire unit sphere is its area, which is $4\pi$.]
In particular, the solid angle is proportional to the sine of the latitude.
That fact is needed if the projection will be used to integrate over some larger region,
such as is done when sampling from an equirectangular projection to create a spherical harmonic.



## Cube maps

A cube map texture stores six square grid of texels.
The grids are commonly named +X, ‒X, +Y, ‒Y, +Z, and ‒Z.
To find the value of the function at a given $(x,y,z)$ direction, we:

1. Find the coordinate of the direction with the largest absolute value.
    
    Let's assume for example that that was $y$.

2. Use the sign of that coordinate to pick one of the six squares.

    Let's assume that $y$ was negative, so we pick ‒Y.

3. Divide the other two coordinated by the largest coordinate to get a pair of numbers between ‒1 and +1.

    In our example, that would be $\left(\frac{x}{|y|}, \frac{z}{|y|}\right)$

4. Shift and scale those coordinates so that ‒1 to +1 becomes the full size of the square texture.
    
    If the ‒Y square was 16×16 texels, that would be achieved through $\left(8 + 8\frac{x}{|y|}, 8 + 8\frac{z}{|y|}\right)$

5. Collect and combine the nearest texel values to that point.

Cube maps are simple and efficient and are widely used.
They do have some complexity in how they handle the boundaries between cube faces, though,
which requires a nontrivial amount of extra work to get right.
Many GPUs have dedicated hardware just for computing those cube map edge and corner cases.

<figure>
```{=html}
<div>
<img src="earth.png"/><br/>
<img src="earth+x.png"/>
<img src="earth+y.png"/>
<img src="earth+z.png"/>
<img src="earth-x.png"/>
<img src="earth-z.png"/>
<img src="earth-y.png"/>
</div>
```
<figcaption>A visualization of cube map. In order the images are a scaled-down version of NASA's 2002 Blue Marble image of the earth and then the faces for $+x, +y, +z, -x, -z, -y$.</figcaption>
</figure>




## Octahedral maps

An octahedral map texture stores eight triangular faces in a single square texture.
Compared to cube maps, octahedral maps:

- Have more texel shape distortion, with each texel covering an elongated diamond-shaped patch of the sphere.
- Have more uniform texel sizes, with less different in covered area of the sphere between the face-corner texels and the face-center texels.
- Are less efficient to create dynamically with rasterization, requiring 8 instead of 6 rendering passes.
- Have much simpler edge-case handling logic.

It is that last point -- the simpler edge cases -- that have helped octahedral maps
gain significant ground over the older and better-established cube maps.
Notably, the result is a single grid of texels with no internal discontinuities,
meaning most algorithms designed for 2D textures work normally on them,
with the only special-case logic used for texels on the edges of the grid.

<figure id="octahedral-container">
<!-- The canvas will be injected here -->
<figcaption> A visualization of octahedral maps. The map morphs back and forth between being a square and a sphere, showing how the texels wrap around the sphere.
(Drag to Rotate)</figcaption>
</figure>

```{=html}
<script type="importmap">
    { 
        "imports": { 
            "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
            "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
        } 
    }
</script>

<script type="module">
    import * as THREE from 'three';
    import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

    const container = document.getElementById('octahedral-container');
    const width = container.clientWidth;
    const height = container.clientHeight;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    
    // 1. Enable Alpha for transparency
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    // 2. Set clear color to 0 alpha
    renderer.setClearColor(0x000000, 0); 
    container.insertAdjacentElement('afterbegin',renderer.domElement);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    const gridSize = 10.0;
    const segments = 24; 
    const geometry = new THREE.PlaneGeometry(gridSize, gridSize, segments, segments);

    const vertexShader = `
        uniform float uMorph;
        varying vec2 vUv;
        vec3 octToVec3(vec2 e) {
            vec3 v = vec3(e.xy, 1.0 - abs(e.x) - abs(e.y));
            if (v.z < 0.0) {
                v.xy = (1.0 - abs(v.yx)) * vec2(v.x >= 0.0 ? 1.0 : -1.0, v.y >= 0.0 ? 1.0 : -1.0);
            }
            return normalize(v);
        }
        void main() {
            vUv = uv;
            vec2 octCoord = uv * 2.0 - 1.0;
            vec3 posFlat = position;
            vec3 posSphere = octToVec3(octCoord) * (${gridSize.toFixed(1)} / 2.0);
            vec3 morphed = mix(posFlat, posSphere, uMorph);
            gl_Position = projectionMatrix * modelViewMatrix * vec4(morphed, 1.0);
        }
    `;

    const fragmentShader = `
        varying vec2 vUv;
        void main() {
            float freq = ${segments.toFixed(1)};
            vec2 grid = abs(fract(vUv * freq - 0.5) - 0.5) / fwidth(vUv * freq);
            float line = min(grid.x, grid.y);
            float mask = 1.0 - smoothstep(0.0, 1.2, line);
            float check = step(0.5, fract(vUv.x * freq)) == step(0.5, fract(vUv.y * freq)) ? 1.0 : 0.0;
            
            vec2 bigrid = vUv * 2.0 - 1.0;
            float rad = abs(bigrid.x) + abs(bigrid.y);
            float quadrant = bigrid.x * bigrid.y;
            float faceparity = (rad < 1.0 ? (quadrant < 0.0 ? 1.0 : 0.0) : (quadrant > 0.0 ? 1.0 : 0.0));
            
            // Vibrant blue/purple theme
            vec3 baseColor = mix(vec3(0.4 + faceparity * 0.2, 0.2, 0.9), vec3(0.4 + faceparity * 0.2, 0.05, 0.4), check);
            vec3 finalColor = mix(baseColor, vec3(1.0), mask * 0.4);
            
            gl_FragColor = vec4(finalColor, 1.0);
        }
    `;

    const material = new THREE.ShaderMaterial({
        vertexShader,
        fragmentShader,
        uniforms: { uMorph: { value: 0 } },
        side: THREE.DoubleSide
    });

    const mesh = new THREE.Mesh(geometry, material);
    scene.add(mesh);

    camera.position.z = 15;

    function animate(t) {
        material.uniforms.uMorph.value = (Math.sin(t * 0.0008) + 1.0) / 2.0;
        controls.update();
        renderer.render(scene, camera);
        window.animframe = requestAnimationFrame(animate);
    }

    // Observer to handle container resizing
    const resizeObserver = new ResizeObserver(() => {
        const w = container.clientWidth>>1;
        const h = container.clientHeight>>1;
        renderer.setSize(w, w);
        camera.aspect = w / w;
        camera.updateProjectionMatrix();
    });
    resizeObserver.observe(container);
    
    const viewObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) window.animframe = requestAnimationFrame(animate);
            else cancelAnimationFrame(window.animframe);
        });
    }, {threshold: 0.1} );
    viewObserver.observe(renderer.domElement);

</script>
```

To find the value of the function at a given $(x,y,z)$ direction, assuming the center of the square is the $+z$ axis, we:

1. Find the $L_1$ norm of the vector, which is $|x| + |y| + |z|$

2. Get a pair of numbers between ‒1 and +1 in one of two ways:

    If $z \ge 0$, use $(u,v) = \left(\frac{x}{L_1}, \frac{y}{L_1}\right)$
    
    If $z < 0$, use $(u,v) = \left(\frac{L_1-|y|}{\sgn(x)L_1}, \frac{L_1-|x|}{\sgn(y)L_1}\right)$ where $\sgn(a) = \begin{cases}1&\text{if }a \ge 0\\-1&\text{if }a<0\end{cases}$

3. Shift and scale those coordinates so that ‒1 to +1 becomes the full size of the square texture.
    
    If the octohedral map was 16×16 texels, that would be achieved through $\left(8 + 8u, 8 + 8v\right)$

4. Collect and combine the nearest texel values to that point.

There is some complexity at the edges of the texture map,
but it is much simpler than in the cube map case.
Texels on the left or right edge of the map are adjacent to their vertically-mirrored texel,
while texels on the top or bottom edge of the map are adjacent to their horizontally-mirrored texel.


<figure>
```{=html}
<div>
<img src="earth.png"/>
<img src="earth_oct.png"/>
</div>
```
<figcaption>A visualization of an octahedral map. In order the images are a scaled-down version of NASA's 2002 Blue Marble image of the earth and then the octohedral map.</figcaption>
</figure>


## Spherical harmonics

Spherical harmonics form an infinite set of orthogonal basis functions
with directions as inputs
which can be linearly combined to create any other function.
The term <dfn>spherical harmonics</dfn> is used broadly,
sometimes referring to the basis functions,
sometimes to the coefficients used to combine them into other functions on a sphere,
and sometimes to the broad idea of storing and using functions in this way.

The spherical harmonic basis functions are often described in terms of trignometry functions in spherical coordinates,
but can also be presented as polynomials of the coordinates of the unit-length direction vector.
That polynomial version is used almost exclusively in computer graphics
because it is much more efficient to compute.

The polynomials in the set are nontrivial to derive,
in part because of the need for them to be orthogonal^[Meaning the integral of the product of any two of them over the surface of the unit sphere is 0, and allowing many other operations to be simpler]
and in part because some obvious forms (like $x^2$, $y^2$, and $z^2$)
are redundant when applied to a unit sphere (because $x^2 + y^2 + z^2 = 1$).
In practive in graphics we don't derive them,
we simply look them up in a list created by mathematicians.

To represent arbitrary functions on the sphere, we'd need an infinite number of spherical harmonics basis functions.
But in practice we almost never go beyond polynomials of the 4^th^ power^[In spherical harmonics literature there are many names for this polynomial power. "Band" is often used in graphics context, with "multiplet", "subspace", and "shell" used more often in other domains. The power of polynomials in a given bad is denoted using the variable $\ell$, so the cubic polynomial basis functions are denoted as $\ell=3$.] (like $xy^2z$)
because the time complexity of computing higher-order polynomials makes them less arractive than environment maps if higher detail is needed.
For illumination, just using linear and quadratic terms is often sufficient.
Because the number of basis functions of order $n$ and below is $(n+1)^2$,
that means that a spherical harmonic terms in graphics vary between 9 (for quadratic functions)
and 25 (above which they become too slow for many applications).
For contrast, the smallest octahedral map I've seen in use was 8×8 = 64 terms
and many are at least an order of magnitude larger than that.

Low-order spherical harmonics are a great way to represent smooth and blurry functions of direction,
such as diffuse illumination as a function of surface normal.
Unlike low-resolution textures, they have no aliasing or other visual artefacts caused when some feature fails to align with any texel sample.
Indeed, spherical harmonics are closed under rotation,
though that is not widely used in graphics because it is often cheaper to rotate the input direction than it is to compute the rotated function's coefficients.

<figure>
```{=html}
<div>
<img src="earth.png"/>
<img src="earth-l0.png"/>
<img src="earth-l1.png"/>
<img src="earth-l2.png"/>
<img src="earth-l3.png"/>
<img src="earth-l4.png"/>
</div>
```
<figcaption>A visualization of spherical harmonics. In order the images are

1. A scaled-down version of NASA's 2002 Blue Marble image of the earth.

2. The 1-coordinate $\ell=0$ (constant) spherical harmonic, which is the constant value
    $\begin{bmatrix}0.57909678\\0.57939933\\0.79749238\end{bmatrix}$.
    This and other coefficients are 3D because the red, green, and blue are modeled as three separate functions.

3. The 4-coordinate $\ell\le 1$ (linear) spherical harmonics, which includes $\ell=0$ and three more coordinates
    $\begin{bmatrix}-0.14662046\\-0.12972639\\-0.05274042\end{bmatrix}$,
    $\begin{bmatrix} 0.13384709\\ 0.14422076\\-0.03082019\end{bmatrix}$, and
    $\begin{bmatrix}-0.21011754\\-0.19884235\\-0.05517153\end{bmatrix}$
.
4. The 9-coordinate $\ell\le 2$ (quadratic) spherical harmonics, which includes $\ell\le 1$ and five more coordinates
    $\begin{bmatrix}0.07791549\\0.05736443\\0.05600644\end{bmatrix}$,
    $\begin{bmatrix}-0.10744561\\-0.10649269\\-0.01958778\end{bmatrix}$,
    $\begin{bmatrix}0.10181003\\0.10915452\\0.08569074\end{bmatrix}$,
    $\begin{bmatrix}-0.14324432\\-0.12648681\\-0.06839883\end{bmatrix}$, and
    $\begin{bmatrix} 0.00308553\\-0.01250149\\ 0.03231016\end{bmatrix}$.

5. The 16-coordinate $\ell\le 3$ (cubic) spherical harmonics, which includes $\ell\le 2$ and seven more coordinates<!--
    $\begin{bmatrix}-0.12727887\\-0.12201173\\-0.01542337\end{bmatrix}$,
    $\begin{bmatrix}0.1899024 \\0.16527014\\0.05840684\end{bmatrix}$,
    $\begin{bmatrix}-0.04350075\\-0.04727148\\-0.00066759\end{bmatrix}$,
    $\begin{bmatrix}-0.1953883 \\-0.18476441\\-0.13657319\end{bmatrix}$,
    $\begin{bmatrix} 0.04187654\\ 0.04293499\\-0.01637099\end{bmatrix}$,
    $\begin{bmatrix}-0.03768123\\-0.04963935\\ 0.02489509\end{bmatrix}$, and
    $\begin{bmatrix}-0.0428035 \\-0.03651455\\-0.01439937\end{bmatrix}$-->.

6. The 25-coordinate $\ell\le 4$ (quartic) spherical harmonics, which includes $\ell\le 3$ and nine more coordinates<!--
    $\begin{bmatrix} 0.09721064\\ 0.1123593 \\-0.02001075\end{bmatrix}$,
    $\begin{bmatrix} 0.00177371\\-0.00903523\\-0.00192857\end{bmatrix}$,
    $\begin{bmatrix} 0.02825826\\ 0.03121304\\-0.00166604\end{bmatrix}$,
    $\begin{bmatrix}0.09962168\\0.09435509\\0.07428829\end{bmatrix}$,
    $\begin{bmatrix}0.05622194\\0.07245149\\0.07138553\end{bmatrix}$,
    $\begin{bmatrix}0.1275382 \\0.10674347\\0.05159074\end{bmatrix}$,
    $\begin{bmatrix}-0.11768658\\-0.11491717\\-0.01668319\end{bmatrix}$,
    $\begin{bmatrix}-0.0486706 \\-0.06039417\\ 0.00838498\end{bmatrix}$, and
    $\begin{bmatrix}-0.00857709\\-0.00179352\\ 0.01336876\end{bmatrix}$-->.

</figcaption>
</figure>


