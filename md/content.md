---
title: Content Outline
header-includes:
  - "<style>.container .row { max-width: 100%; } .container .row p { max-width: 60em; }</style>"
...

# Overview {-}

This page provides a list of videos and notes with the intent that following them in the order presented here will result in a cohesive approach to the subject of interactive computer graphics.

In general, the intent is that for a given topic the video and notes will provide equivalent explanations of the material; however, that intent is not always completely achieved.
The notes often have more formal definitions and more mentions of ancillary topics than the videos.
The videos often have additional commentary and exposition than the nodes.
When the video is using an interactive example or discussing or developing code samples, the notes often just have the example or code without commentary.

"How things appear" videos are included after each section but in generally have no direct correlation with the section itself, and are generally not tested by any of the course's assessments.
I include them because computer graphics is the process of trying to simulate how the world looks, so I assume you'll be interested in understanding how the world looks.
Feel free to message me with additional appearances you'd like me to describe, either general phenomena or specific images; there are more interesting visual phenomena than I have any hope of fully enumerating.

Videos are hosted in two places, in part so that if one site is down the other can be used:

- [ClassTranscribe](https://classtranscribe.illinois.edu/offering/c7e741f2-d482-496e-ba57-0285d39ccedb) allows collaborative editing of subtitles and transcripts.
- [MediaSpace](https://mediaspace.illinois.edu/channel/CS+418+online+2023-2025/379538012) has subtitles provided by DRES.

With a few exceptions, notes are written by Luther Tychonievich and hosted directly on this website, which is also hosted in two places:

- <https://cs418.cs.illinois.edu/website> also hosts the submission page
- <https://courses.grainger.illinois.edu/cs418/fa2025> also hosts many other courses

# Recommended Schedule {-}

A recommended weekly schedule follows.
MPs are listed in the week where the relevant content has been presented; it is expected most students will start them then and complete them a week or two later; that delay is why there are not MPs listed for the last two weeks.
Electives vary significantly in complexity and time required, as noted by their differing point values.
You only need to do some electives, and if 3cr only some core.
See the [MPs page](mp/) for more.

| Week | Content | Core MPs | Elective MPs |
|:-----|:--------|:---------|--------------|
| Aug 25–31     | [Preliminaries](#prelim)                         | [WebGL2 warmup](mp/warmup-webgl2.html) |
| Sep 01–07     | [DDA](#dda)                                      | [AnyLang warmup](mp/warmup-anylang.html) |
| Sep 08–14     | [Depth](#depth) and [related concepts](#rastetc) | [Rasterizer](mp/rasterizer.html) |
| Sep 15–21     | [Javascript](#js)                                | | Rasterizer electives |
| Sep 22–28     | [WebGL2](#webgl)                                 | | Psychedelic |
| Sep 29–Oct 05 | [3D Math](#math)                                 | [Logo](mp/logo.html) | GPU jitter, CPU jitter |
| Oct 06–12     | [GL example](#glcode) and [Lighting](#light)     | [Orbits](mp/orbits.html) | Lineograph |
| Oct 13–19     | [Fractals](#fract)                               | [Terrain](mp/terrain.html) | Cliffs, Weathering, Height map, Parametric |
| Oct 20–26     | [Animation](#anim) and [Code example](#geomcode) | [Flight](mp/flight.html) | |
| Oct 27–Nov 02 | [Textures](#texture)                             | [Textures](mp/textures.html) | Drive, Fog, OBJ, Subdivision |
| Nov 03–09     | [Raytracing](#ray)                               | [Raytracer](mp/raytracer.html) | |
| Nov 10–16     | [Raytracing](#ray)                               | | Raytracer electives |
| Nov 17–21     | [Dynamics](#dynamics)                            | [Spheres](mp/spheres.html) | Many Spheres, Goop |
| | Fall Break | | |
| Dec 01–07     | [Better rasterization](#pretty)                  | | |
| Dec 08–10     | Review and finish coding                         | | |

Experience has taught me that getting behind on lecture material or MPs is usually a sign that additional instructor/student interaction is needed. If you are more than a week behind the schedule given here, please contact me.






# Graphics Preliminaries {#prelim}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Rasters and pixels | [CT](https://classtranscribe.illinois.edu/video?id=66a4222b-ce30-426b-a2f7-393aeb9218e3) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_3dqc46vq) | [Aliasing](text/aliasing.html){title="Aliasing: two interpretations of rasters and the problems with both"} |
| Color in the eye | [CT](https://classtranscribe.illinois.edu/video?id=91fdc10c-a2bb-4c4f-a051-3d8bfa5f7cf7) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_bgova9go) | [Color](text/color.html){title="Color: as seen by eyes, projected on screens, and stored in sRGB and YCbCr"} |
| Color on the screen | [CT](https://classtranscribe.illinois.edu/video?id=9aae4a78-cd01-4b9c-b93b-59f697443cd5) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_aq0oi4h5) | [Color](text/color.html){title="Color: as seen by eyes, projected on screens, and stored in sRGB and YCbCr"} |
| Other color models | [CT](https://classtranscribe.illinois.edu/video?id=c39cf89e-7388-4f0c-9c72-6759a8c22218) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_q9wogvh9) | [Color](text/color.html){title="Color: as seen by eyes, projected on screens, and stored in sRGB and YCbCr"} |
| Dithering | [CT](https://classtranscribe.illinois.edu/video?id=5c4811a5-d6b6-4165-ae3d-a64c9a42944f) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_obkwnsra) | [Dithering](text/dither.html){title="Dithering: fooling the eye into thinking we have more colors displayed than we do"} |
| What is “interactive” computer graphics? | [CT](https://classtranscribe.illinois.edu/video?id=8395bdb8-5642-4bef-a5a3-72353f13857e) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_9qklpqdw) | [&quot;Interactive&quot; Graphics](text/interactive.html){title="&quot;Interactive&quot; Graphics: contrasting rasterization and raytracing, with a nod to other approaches"} |
| The GPU graphics pipeline | [CT](https://classtranscribe.illinois.edu/video?id=46cfa514-ec05-4179-9b32-7b57791c9807) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_1bbe15sr) | [WebGL's Graphics Pipeline](text/pipeline.html){title="WebGL's Graphics Pipeline: a collapsible top-down view of how 3D graphics with WebGL2 works"} |

How things appear: [*The Student, the Fish, and Agassiz* by The Student](text/fish.html) <small>and</small> Mirages and total internal reflection [CT](https://classtranscribe.illinois.edu/video?id=9debac49-d1a3-4a22-bc49-b288c59c351f) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_zy0k8pgn/1_rvyfle5g)

[Quiz](https://us.prairielearn.com/pl/course_instance/182443/assessment/2546495)

We also have recordings of a couple of in-class Q&A sessions from an older version of the course that might be of interest:

- [Q&A “Where is white in LMS?”](https://classtranscribe.illinois.edu/video?id=3eb33fbe-96a8-4f9c-8f8e-1f40531a26b6)
- [Q&A “Why dither and gamma?”](https://classtranscribe.illinois.edu/video?id=7ff135c6-7db9-49c3-9b4d-17dd4b721cfe)



# Rasterization

## DDA and related algorithms {#dda}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| DDA | [CT](https://classtranscribe.illinois.edu/video?id=2a7870c5-536e-4aee-be27-0a0d08cdeed4) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_caoo75kh/1_o8hamcmq) | [DDA (and Bresenham)](text/dda.html){title="DDA (and Bresenham): implementing the rasterization of lines and triangles"} |
| Scanline | [CT](https://classtranscribe.illinois.edu/video?id=aea3a3a4-45b9-4b83-9d1c-b878834f82f2) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_caoo75kh/1_ospwkh6i) | [DDA (and Bresenham)](text/dda.html){title="DDA (and Bresenham): implementing the rasterization of lines and triangles"} |
| Bresenham | [CT](https://classtranscribe.illinois.edu/video?id=ba1257bf-0d9d-43f9-a267-05797274004d) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_caoo75kh/1_ssjpki74) | [DDA (and Bresenham)](text/dda.html){title="DDA (and Bresenham): implementing the rasterization of lines and triangles"} |
| Interpolation | [CT](https://classtranscribe.illinois.edu/video?id=3f617daa-d28c-444d-91db-2ff4ae4f1f60) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_caoo75kh/1_62ehysuj) | [DDA (and Bresenham)](text/dda.html){title="DDA (and Bresenham): implementing the rasterization of lines and triangles"} |
| Rendering curves | [CT](https://classtranscribe.illinois.edu/video?id=b6b2ec58-81a4-43e6-8a1e-c29b9933331c) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_caoo75kh/1_0es7noxz) | [Bézier curves](text/bezier.html){title="Bézier curves: a brief introduction to how to evaluate them using de Casteljau's algorithm"} |

How things appear: Refraction [CT](https://classtranscribe.illinois.edu/video?id=a442b831-d7eb-485f-b759-b30183ffb86c) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_caoo75kh/1_2k4gh77g)

[Quiz](https://us.prairielearn.com/pl/course_instance/182443/assessment/2546833)

## Emulating 3D with depth {#depth}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Perspective via w | [CT](https://classtranscribe.illinois.edu/video?id=58eabb16-dcdf-438f-817b-8d63ec82cb03) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_tq1v0k0s/1_c792bz4z) | [Projection](text/projection.html){title="Projection: simulating depth and perspective using w and z"} |
| Frustum clipping | [CT](https://classtranscribe.illinois.edu/video?id=f7a7beb3-9399-4d20-b4cb-315219c161e2) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_tq1v0k0s/1_iggdnsj0) | [Clipping](text/clipping.html){title="Clipping: removing off-screen geometry, avoiding divide-by-zero, and using depth buffer bits well via frustum clipping"} |
| Hidden surface removal | [CT](https://classtranscribe.illinois.edu/video?id=77a8c192-3fd5-46cf-b4ac-da264971c764) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_tq1v0k0s/1_7gtzfs5b) |  |
| Z buffer | [CT](https://classtranscribe.illinois.edu/video?id=adf4ab97-d3ea-49b0-81fd-89f19b13a6d3) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_tq1v0k0s/1_w3780x4t) |  |


How things appear: Fresnel effect [CT](https://classtranscribe.illinois.edu/video?id=5b300c5a-2534-4115-b475-8ef2b10acc36) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_tq1v0k0s/1_w2dhqcxz)

(Quiz shared with [next section](#rastetc))


## Related concepts {#rastetc}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Viewport | [CT](https://classtranscribe.illinois.edu/video?id=9e629bb3-1d81-401a-ae09-c64d70efe3c6) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_7vst7d9z/1_3c80jgj3) | [Other parts of the rasterization process](text/other-rasterization.html){title="Other parts of the rasterization process: viewprts, blending, culling, and multisampling"} |
| Alpha blending | [CT](https://classtranscribe.illinois.edu/video?id=d991529f-2d3f-4c27-b6bc-6c28cab06056) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_7vst7d9z/1_8emkk80t) | [Other parts of the rasterization process](text/other-rasterization.html){title="Other parts of the rasterization process: viewprts, blending, culling, and multisampling"} |
| Back-face culling | [CT](https://classtranscribe.illinois.edu/video?id=af715562-41de-427d-8b3b-f89edc9ff7ff) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_7vst7d9z/1_jkhxm4r6) | [Other parts of the rasterization process](text/other-rasterization.html){title="Other parts of the rasterization process: viewprts, blending, culling, and multisampling"} |
| Full-scene anti-aliasing | [CT](https://classtranscribe.illinois.edu/video?id=27c24876-bdb9-4a44-b551-a62f6a5efe8c) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_7vst7d9z/1_fvjkaw40) | [Other parts of the rasterization process](text/other-rasterization.html){title="Other parts of the rasterization process: viewprts, blending, culling, and multisampling"} |
| What we covered on rasterization | [CT](https://classtranscribe.illinois.edu/video?id=efc2df45-1c35-4f10-9a92-e9a67a097d32) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_7vst7d9z/1_8ciqxksb) |  |


How things appear: Diffraction rainbows [CT](https://classtranscribe.illinois.edu/video?id=aedb1137-5a4f-4b4e-bd28-669fdbf5a06d) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_7vst7d9z/1_3f2r71e1)

[Quiz](https://us.prairielearn.com/pl/course_instance/182443/assessment/2547951)


# Using the GPU with WebGL2

## Enough JavaScript to get by {#js}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Running JavaScript | [CT](https://classtranscribe.illinois.edu/video?id=4d9dee1e-e8b5-4c6e-b138-424ae19423b3) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_sld426fk/1_2e8w4epc) | [Parts of JavaScript We'll Use](text/javascript.html){title="Parts of JavaScript We'll Use: assuming you know Java or C++ and are comfortable learning a language from examples on your own"} |
| JavaScript syntax and scoping | [CT](https://classtranscribe.illinois.edu/video?id=234b5675-757c-48c4-942e-eb8dfd81f4f7) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_sld426fk/1_6m8vcqsv) | [Parts of JavaScript We'll Use](text/javascript.html){title="Parts of JavaScript We'll Use: assuming you know Java or C++ and are comfortable learning a language from examples on your own"} |
| JavaScript values and types | [CT](https://classtranscribe.illinois.edu/video?id=ec2e91f4-25d2-4e1b-a9cf-9f9b05bf64b8) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_sld426fk/1_a6nw3id7) | [Parts of JavaScript We'll Use](text/javascript.html){title="Parts of JavaScript We'll Use: assuming you know Java or C++ and are comfortable learning a language from examples on your own"} |
| JavaScript functions | [CT](https://classtranscribe.illinois.edu/video?id=1ce5563f-ff44-4dd6-8fcb-7cbf583d49ff) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_sld426fk/1_xeqopxxo) | [Parts of JavaScript We'll Use](text/javascript.html){title="Parts of JavaScript We'll Use: assuming you know Java or C++ and are comfortable learning a language from examples on your own"} |
| HTML | [CT](https://classtranscribe.illinois.edu/video?id=bc0f940c-6133-44bb-96c4-622fceecd68c) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_sld426fk/1_exhk8gcl) | [Parts of JavaScript We'll Use](text/javascript.html){title="Parts of JavaScript We'll Use: assuming you know Java or C++ and are comfortable learning a language from examples on your own"} |
| In-class Q&A | [CT](https://classtranscribe.illinois.edu/video?id=18c48fcc-1918-4c2d-8a5a-9537b6d78a44) |  |


How things appear: Dispersion rainbow [CT](https://classtranscribe.illinois.edu/video?id=4d66e25a-62b0-46fb-9979-4de6a071693e) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_sld426fk/1_8fasrarm)

[Quiz](https://us.prairielearn.com/pl/course_instance/182443/assessment/2553128)


## Starting with WebGL2 coding {#webgl}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| First WebGL2 file | [CT](https://classtranscribe.illinois.edu/video?id=2c592135-6f96-45b6-85d2-e2bf2399f438) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_b71wxg8u/1_u9tbvbsb) | [Minimal WebGL](text/minimal-webgl.html){title="Minimal WebGL: what WebGL 2 accepts, what it requires, and how to get started"} |
| Using multiple files | [CT](https://classtranscribe.illinois.edu/video?id=ce4fca8a-7a87-463c-a853-0c395d6f22cb) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_b71wxg8u/1_ottrdx2k) | [ex02-fragment.glsl](code/2d-webgl/ex02-fragment.glsl)<br/>[ex02-split.html](code/2d-webgl/ex02-split.html)<br/>[ex02-vertex.glsl](code/2d-webgl/ex02-vertex.glsl)<br/>[ex02.js](code/2d-webgl/ex02.js) |
| Data paths on GPU | [CT](https://classtranscribe.illinois.edu/video?id=bc1ee9fc-bbb9-4e0c-adbd-91a8fbccaf81) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_b71wxg8u/1_z32gev7a) | [WebGL Geometry](text/webgl-goemetry.html){title="WebGL Geometry: several ways to tell WebGL what shapes we want to display"} |
| Loading a model | [CT](https://classtranscribe.illinois.edu/video?id=014ca247-33b5-4372-8a98-8352d9cfa1eb) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_b71wxg8u/1_br0axygs) | [ex03-fragment.glsl](code/2d-webgl/ex03-fragment.glsl)<br/>[ex03-geometry.json](code/2d-webgl/ex03-geometry.json)<br/>[ex03-model.html](code/2d-webgl/ex03-model.html)<br/>[ex03-vertex.glsl](code/2d-webgl/ex03-vertex.glsl)<br/>[ex03.js](code/2d-webgl/ex03.js) |
| Motion with uniforms | [CT](https://classtranscribe.illinois.edu/video?id=00bf3f38-6047-4c5b-a577-26cedfd2613a) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_b71wxg8u/1_wpe5ysoc) | [ex04-fragment.glsl](code/2d-webgl/ex04-fragment.glsl)<br/>[ex04-geometry.json](code/2d-webgl/ex04-geometry.json)<br/>[ex04-motion.html](code/2d-webgl/ex04-motion.html)<br/>[ex04-vertex.glsl](code/2d-webgl/ex04-vertex.glsl)<br/>[ex04.js](code/2d-webgl/ex04.js) |
| In-class Q&A | [CT](https://classtranscribe.illinois.edu/video?id=a929b4b7-52bf-4e46-8e0e-5e48d79e1b0a) |  |


How things appear: Exposure noise [CT](https://classtranscribe.illinois.edu/video?id=826f7d82-fc46-4cb0-8fde-6e4149015404) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_b71wxg8u/1_ocv927pj)

[Quiz](https://us.prairielearn.com/pl/course_instance/182443/assessment/2553689)


## Mathematics of interactive 3D graphics {#math}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Matrices and vectors | [CT](https://classtranscribe.illinois.edu/video?id=19e75f02-a239-4feb-9450-e4c2dfb054e7) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_1jw17f6z) | [Math Review](text/math1.html){title="Math Review: vectors and matrices"} |
| Rotation matrices | [CT](https://classtranscribe.illinois.edu/video?id=5f83d536-8740-4618-8296-c736344fb4ac) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_5tziljvv) | [Homogeneous Vectors and Transformations](text/math2.html){title="Homogeneous Vectors and Transformations: including definitions, terminology, and common operations"} |
| Scaling matrices | [CT](https://classtranscribe.illinois.edu/video?id=134fbe2a-e334-460d-8751-9c7ef5e16314) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_1haumnst) | [Homogeneous Vectors and Transformations](text/math2.html){title="Homogeneous Vectors and Transformations: including definitions, terminology, and common operations"} |
| Sheering | [CT](https://classtranscribe.illinois.edu/video?id=04b5401c-2eed-4346-a6ad-89c5194a1148) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_9si9fddw) | [Homogeneous Vectors and Transformations](text/math2.html){title="Homogeneous Vectors and Transformations: including definitions, terminology, and common operations"} |
| Homogeneous vectors, take 1: definition first | [CT](https://classtranscribe.illinois.edu/video?id=375b31ca-a76c-433b-b756-955b416f9576) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_1kh80r9i) | [Homogeneous Vectors and Transformations](text/math2.html){title="Homogeneous Vectors and Transformations: including definitions, terminology, and common operations"} |
| Homogeneous vectors, take 2: objective first | [CT](https://classtranscribe.illinois.edu/video?id=5d172845-f178-41d6-ad5f-7d88dd95107b) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_djq4qojt) | [Homogeneous Vectors and Transformations](text/math2.html){title="Homogeneous Vectors and Transformations: including definitions, terminology, and common operations"} |
| Visualizing 2D matrics | [CT](https://classtranscribe.illinois.edu/video?id=67875bd7-8763-4a6a-b7a8-2bc75948adee) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_8x4mjtly) | [matrixdemo.php](files/matrixdemo.php) |
| Visualizing order of matrics | [CT](https://classtranscribe.illinois.edu/video?id=c9572ae5-0ec9-4732-9d98-20becba656aa) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_z0dcg4fc) | [matrixdemo.php](files/matrixdemo.php) |
| Visualizing 3D matrices | [CT](https://classtranscribe.illinois.edu/video?id=48f6dcfc-4916-4a86-a2cf-b7d8bcbae513) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_g9a6rveb) | [matrixdemo2.php](files/matrixdemo2.php) |
| Standard matrix hierarchies | [CT](https://classtranscribe.illinois.edu/video?id=00586cf6-1e0d-4fb1-a39f-0766c772824d) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_p3tm1vfj)  |  |


How things appear: Lens bloom [CT](https://classtranscribe.illinois.edu/video?id=96aae7ab-9e5b-41de-8fac-81d0fb4d1a4e) [MS](https://mediaspace.illinois.edu/playlist/dedicated/379538012/1_m2wysuqj/1_sf367jd5)

[Quiz](https://us.prairielearn.com/pl/course_instance/182443/assessment/2554349)

We also have a recording of a previous semester's Q&A on matices: [CT](https://classtranscribe.illinois.edu/video?id=8bed82c1-d426-4d66-814b-ccf3bc097759)


## Multi-part coding example {#glcode}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| 3D WebGL2 code | [CT](https://classtranscribe.illinois.edu/video?id=d4106446-3a1a-4111-8a70-4f1fa68b9482) | [1-the-code.html](code/3d-webgl/1-the-code.html)<br/>[math.js](code/3d-webgl/math.js)<br/>[wrapWebGL2.js](code/3d-webgl/wrapWebGL2.js) |
| Adding perspective | [CT](https://classtranscribe.illinois.edu/video?id=7e151346-58cf-434b-b60f-6bf0a881a9cc) | [2-viewing.html](code/3d-webgl/2-viewing.html) |
| Coloring vertices and faces | [CT](https://classtranscribe.illinois.edu/video?id=b1dcc83d-3edd-4011-a723-edf0078ad52c) | [3-color.html](code/3d-webgl/3-color.html) |
| Multi-object scene | [CT](https://classtranscribe.illinois.edu/video?id=a854f636-e2d4-4353-be99-bbe88277821b) | [4-several.html](code/3d-webgl/4-several.html) |
| Choosing motion | [CT](https://classtranscribe.illinois.edu/video?id=e682edd1-0467-4462-bea1-256bd1448bde) | [5-scripted.html](code/3d-webgl/5-scripted.html) |
| Random procedural geometry | [CT](https://classtranscribe.illinois.edu/video?id=b2877f5e-7f06-401a-b625-efd9fdcd748d) | [6-makegeom.html](code/3d-webgl/6-makegeom.html) |
| Designing procedural geometry | [CT](https://classtranscribe.illinois.edu/video?id=dcad54b4-5cbf-45c4-8e81-e0d2fa31994a) | [7-starburst.html](code/3d-webgl/7-starburst.html) |


How things appear: [Subsurface scattering](https://classtranscribe.illinois.edu/video?id=de19c41f-3a59-4b8e-a090-c634ad566dda)

## Lighting on the GPU {#light}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Phong’s simple model of lighting | [CT](https://classtranscribe.illinois.edu/video?id=c34c4218-877e-4994-9f6b-412972416cfd) | [Lighting models](text/lighting.html){title="Lighting models: common BRDFs from trivial heuristics to intricate physically-based model"} |
| In-class Q&A re Halfway vector | [CT](https://classtranscribe.illinois.edu/video?id=a52c7a03-04b5-432a-9c5e-4ede0a2c214a) |  |
| Loading a monkey | [CT](https://classtranscribe.illinois.edu/video?id=3c8d73cd-821e-460d-8ce2-b09a4158123b) | [0-initial.html](code/simple-lighting/0-initial.html)<br/>[1-monkey.html](code/simple-lighting/1-monkey.html)<br/>[math.js](code/simple-lighting/math.js)<br/>[monkey.json](code/simple-lighting/monkey.json) |
| Computing surface normals | [CT](https://classtranscribe.illinois.edu/video?id=41023236-b36c-4742-80a3-4a8d73ab553b) | [2-normals.html](code/simple-lighting/2-normals.html) |
| Adding diffuse light | [CT](https://classtranscribe.illinois.edu/video?id=03494762-f902-4d4f-ae0b-640dcba674a8) | [3-lambert.html](code/simple-lighting/3-lambert.html) |
| Adding multiple light sources | [CT](https://classtranscribe.illinois.edu/video?id=61aec09a-7c3e-4c3f-a9d7-7bf9333c3cc8) | [4-two-lights.html](code/simple-lighting/4-two-lights.html) |
| Adding specular light | [CT](https://classtranscribe.illinois.edu/video?id=e294728c-49f6-4dec-b812-b65ca55ede9d) | [5-blinn-phong.html](code/simple-lighting/5-blinn-phong.html) |
| Physically-based lighting | [CT](https://classtranscribe.illinois.edu/video?id=0738d675-17fb-4929-a495-7d5592d1c7f9) | [the-pbr-guide-part-1](https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-1) |
| In-class Q&A re PBR | [CT](https://classtranscribe.illinois.edu/video?id=e603c410-9329-4bb2-a017-8cdaeb25a7ab) |  |


How things appear: [Rayleigh scattering](https://classtranscribe.illinois.edu/video?id=f44fdec8-983e-4357-b432-51704bf43cb2)

# Creating and animating geometry

## Fractals {#fract}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Fractional dimension | [CT](https://classtranscribe.illinois.edu/video?id=08892d01-184e-4e1d-aced-1e9d64772d94) | [Fractals](text/fractal.html){title="Fractals: a class of mathematically-defined geometries that look more &quot;natural&quot; than most others"} |
| In-class Q&A fractal overview | [CT](https://classtranscribe.illinois.edu/video?id=c77f8196-6cfc-464d-9d67-5f50cfb977db) |  |
| fBm noise | [CT](https://classtranscribe.illinois.edu/video?id=d84d8e39-1aea-4719-96af-aab626facf50) | [Fractals](text/fractal.html){title="Fractals: a class of mathematically-defined geometries that look more &quot;natural&quot; than most others"} |
| Subdivision noise | [CT](https://classtranscribe.illinois.edu/video?id=a89543f8-7312-48c5-b53f-ba72054e5a67) | [Fractals](text/fractal.html){title="Fractals: a class of mathematically-defined geometries that look more &quot;natural&quot; than most others"} |
| Fractal terrain via random faulting | [CT](https://classtranscribe.illinois.edu/video?id=59fac26e-c0c9-44cd-b1b3-3f80b8e89161) | [Terrain via the faulting method](text/faulting.html){title="Terrain via the faulting method: fault computation for simple fractals"} |
| Perlin noise | [CT](https://classtranscribe.illinois.edu/video?id=e009416c-19d5-4861-af16-39a73c407076) | [Fractals](text/fractal.html){title="Fractals: a class of mathematically-defined geometries that look more &quot;natural&quot; than most others"} |
| Weathering and erosion of terrain | [CT](https://classtranscribe.illinois.edu/video?id=c2c833f2-1de4-4706-ae1f-2c1002298a41) | [Hydraulic Erosion](text/erosion.html){title="Hydraulic Erosion: two methods for making weathered terrain"} |
| In-class Q&A re MP3 | [CT](https://classtranscribe.illinois.edu/video?id=ba7a3bfe-d7e3-42ce-ad42-85c12229dec1) |  |


How things appear: [Shiny hair](https://classtranscribe.illinois.edu/video?id=1447ec19-e169-4305-829f-5c7b0919df05)

## Animation {#anim}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| In-class Q&A on many topics | [CT](https://classtranscribe.illinois.edu/video?id=ec18b8b8-c1b6-47ff-90f7-c487cc07b2cb) |  |
| Key frames and tweening | [CT](https://classtranscribe.illinois.edu/video?id=6593af32-a355-4a58-9393-bc5ebd6d56f2) | [Keyframes, Bones, and Skinning](text/keyframe.html){title="Keyframes, Bones, and Skinning: an overview of how we animate articulated characters"} |
| Interpolating with lerps and Bezier curves | [CT](https://classtranscribe.illinois.edu/video?id=de78a9ac-1f58-47f0-a5e4-78612fe31dee) |  |
| Coding lerps of keyframes | [CT](https://classtranscribe.illinois.edu/video?id=77d59fbe-567b-494d-9a6c-0d7cdc238c44) | [3-lerp-code-1.html](code/simple-animation/3-lerp-code-1.html)<br/>[3-lerp-code-2.html](code/simple-animation/3-lerp-code-2.html)<br/>[math.js](code/simple-animation/math.js) |
| Lerping rotation matrices doesn’t work | [CT](https://classtranscribe.illinois.edu/video?id=dbbcef3c-70ec-4a75-a3b6-4d9b6c1bb876) | [4-rotation-problems-1.html](code/simple-animation/4-rotation-problems-1.html)<br/>[4-rotation-problems-2.html](code/simple-animation/4-rotation-problems-2.html) |
| Quaternions | [CT](https://classtranscribe.illinois.edu/video?id=5d40c672-2ecd-4340-b5d7-920eb5436893) | [Quaternions](text/quaternions.html){title="Quaternions: their definition and use in defining rotations in graphics"} |
| Interpolating quaternions | [CT](https://classtranscribe.illinois.edu/video?id=b2ba946e-07e8-4472-8b04-25eee03613b9) | [6-quaternion-interpolation.html](code/simple-animation/6-quaternion-interpolation.html) |
| In-class Q&A re Quaternions | [CT](https://classtranscribe.illinois.edu/video?id=0e94782b-f161-4179-a55f-343ae89ac549) |  |
| Skeletal animation with skinning | [CT](https://classtranscribe.illinois.edu/video?id=9e831deb-f0ee-41ed-af90-26fc7f054fa2) | [Keyframes, Bones, and Skinning](text/keyframe.html){title="Keyframes, Bones, and Skinning: an overview of how we animate articulated characters"} |


How things appear: [Brushed metal](https://classtranscribe.illinois.edu/video?id=cdb402bf-b4e2-4f55-8695-30554f1a5f85)

## Multi-part coding example {#geomcode}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Generating a leg | [CT](https://classtranscribe.illinois.edu/video?id=79b3b2e6-8a9d-490b-85f1-4bca383515e5) | [1-modeling.html](code/skeletal-animation/1-modeling.html)<br/>[math.js](code/skeletal-animation/math.js) |
| Coloring a leg | [CT](https://classtranscribe.illinois.edu/video?id=059286fc-a5ba-4089-96be-04945689bb74) | [2-colors.html](code/skeletal-animation/2-colors.html) |
| Joint locations | [CT](https://classtranscribe.illinois.edu/video?id=75cc999e-2455-4865-96b2-2036636763af) | [3-joints.html](code/skeletal-animation/3-joints.html) |
| Skeletal Animation | [CT](https://classtranscribe.illinois.edu/video?id=fe428697-f175-4868-bbe2-6b2078e218f7) | [4-rig-1.html](code/skeletal-animation/4-rig-1.html)<br/>[4-rig-2.html](code/skeletal-animation/4-rig-2.html) |
| Skinning | [CT](https://classtranscribe.illinois.edu/video?id=4bd4b0a4-2fb0-4a9a-a65b-5c4c3b41e7e9) | [5-skin.html](code/skeletal-animation/5-skin.html) |


How things appear: [Mirrors and one-way mirrors](https://classtranscribe.illinois.edu/video?id=098c186d-1a48-4ea3-80fc-936546f97339)

## Optional deep-dive content

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Stereoscopic 1 Concepts | [CT](https://classtranscribe.illinois.edu/video?id=749220a3-3d44-4115-aea3-c6fcca0c7ab5) |  |
| Stereoscopic 2 Calibration | [CT](https://classtranscribe.illinois.edu/video?id=c6eb2a3b-c6ba-4190-b530-53e120ad2eeb) | [stereoscopic.html](files/stereoscopic.html) |
| Stereoscopic 3 Implementation | [CT](https://classtranscribe.illinois.edu/video?id=958eee0d-62c2-4d08-8810-993ea068e130) |  |


# Texture mapping {#texture}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| In-class preview of texture content | [CT](https://classtranscribe.illinois.edu/video?id=72ae8911-6d83-47ab-82a4-87c4a7b699ce) |  |
| Texture concepts | [CT](https://classtranscribe.illinois.edu/video?id=48c9380f-d7d4-4ab5-9aaf-becb42db736f) | [Textures in WebGL](text/textures.html){title="Textures in WebGL: the mechanics of getting them set up and rendering"} |
| Texture code elements | [CT](https://classtranscribe.illinois.edu/video?id=5b80136e-895b-4580-8fc1-5e1b93b736e1) | [Textures in WebGL](text/textures.html){title="Textures in WebGL: the mechanics of getting them set up and rendering"} |
| Texture maps for all visual details | [CT](https://classtranscribe.illinois.edu/video?id=a2367b99-d91c-4bee-aa37-856c9e58fcee) | [Using Textures](text/textures2.html){title="Using Textures: classes of texture use common in rasterized 3D graphics"} |
| Parallax texture mapping | [CT](https://classtranscribe.illinois.edu/video?id=aceb5ebf-1032-45e9-8b83-6ad0e8af00f3) | [Using Textures](text/textures2.html){title="Using Textures: classes of texture use common in rasterized 3D graphics"} |
| In-class Q&A on camera movement in the MP | [CT](https://classtranscribe.illinois.edu/video?id=0e128e71-121e-485f-b9af-fc2dfee610ca) |  |
| In-class Q&A on textures beyond the MP | [CT](https://classtranscribe.illinois.edu/video?id=c5fe0756-ea25-4667-9f57-5509ae1cc3c4) |  |
| In-class Q&A on OBJ files in MP | [CT](https://classtranscribe.illinois.edu/video?id=4dd4f78d-83bc-4465-92a8-78a8892fea8e) |  |


How things appear: [Retroreflectors](https://classtranscribe.illinois.edu/video?id=886b37ba-4f1a-450b-837a-407ed9dc0348)

# Raytracing {#ray}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| In-class Q&A introducing raytracing | [CT](https://classtranscribe.illinois.edu/video?id=18dfdd86-2f6a-4d1d-9a4c-3e8e559cc600) |  |
| Why raytracing? | [CT](https://classtranscribe.illinois.edu/video?id=93e0449e-75d3-4640-a270-c04b9ab64e84) |  |
| Ray-plane intersection | [CT](https://classtranscribe.illinois.edu/video?id=7d99b7e2-badc-450f-8fd2-34f6022b6ca7) | [Raytracing](text/rays.html){title="Raytracing: basic theory and algorithms of ray intersections  and discussion of generating secondary rays"} |
| Barycentric coordinates and ray-triangle intersection | [CT](https://classtranscribe.illinois.edu/video?id=090462b2-7915-47c5-8e78-c6d758976066) | [Raytracing](text/rays.html){title="Raytracing: basic theory and algorithms of ray intersections  and discussion of generating secondary rays"} |
| Raytracer design | [CT](https://classtranscribe.illinois.edu/video?id=9376d7a0-609e-4cd2-9bfd-3f8cb58727a4) | [Raytracing](text/rays.html){title="Raytracing: basic theory and algorithms of ray intersections  and discussion of generating secondary rays"} |
| In-class Q&A raytracing code design | [CT](https://classtranscribe.illinois.edu/video?id=27ad91a1-f950-4a2e-b34f-92f6cddaaa2f) |  |
| Bounding volume hierachies | [CT](https://classtranscribe.illinois.edu/video?id=e25a1539-99ee-420a-b4a0-a8a4c1840f84) | [Bounding Volume Hierarchies](text/bvh.html) |
| Raytracing as integration | [CT](https://classtranscribe.illinois.edu/video?id=3ebc224f-c810-4a96-a880-6e28817b06c7) | [Integrating incident light](text/integration.html){title="Integrating incident light: including physically-based rendering, secondary ray generation as numerical integration, and importance sampling"} |
| In-class Q&A importance sampling | [CT](https://classtranscribe.illinois.edu/video?id=46922639-dcfa-4b38-84fd-3d29ba070c2a) |  |
| Raytracing many bounces | [CT](https://classtranscribe.illinois.edu/video?id=a0ebd5bc-611d-4230-9df0-36cb541ee4ba) | [Integrating incident light](text/integration.html){title="Integrating incident light: including physically-based rendering, secondary ray generation as numerical integration, and importance sampling"} |
| Raytracing acceleration | [CT](https://classtranscribe.illinois.edu/video?id=e9eb17aa-b625-47c3-b91d-c61a068e4b39) |  |
| In-class Q&A raytracing on GPU | [CT](https://classtranscribe.illinois.edu/video?id=f0422136-cff4-4496-bebf-fc4623c1637e) |  |
| In-class Q&A raytracing in context | [CT](https://classtranscribe.illinois.edu/video?id=8861de00-f283-43bc-bd78-10a00ffe5b30) |  |


How things appear: [Scale and depth of field](https://classtranscribe.illinois.edu/video?id=ec027823-5297-4760-b56e-af9df5abda7d) <small>and</small> [Peach fuzz](https://classtranscribe.illinois.edu/video?id=2af31613-9e57-46fd-b55d-d0b0e5e0bd4b)

# Simulating dynamics {#dynamics}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| Simulation-generated motion | [CT](https://classtranscribe.illinois.edu/video?id=20c33d3e-f8d4-4428-b4d5-d6ec0a9d3575) | [Visual Simulation](text/simulation.html){title="Visual Simulation: an overview good-enough simulation techniques, including Eulerian and Lagrangian methods"} |
| Particle dynamics | [CT](https://classtranscribe.illinois.edu/video?id=9b313d02-6308-4cca-8205-4298bfcd88c6) | [Euler, RK, and PBD](text/kinetics.html){title="Euler, RK, and PBD: common approaches to simulating kinetic motion of particles"} |
| Resolving collisions of rigid spheres | [CT](https://classtranscribe.illinois.edu/video?id=02349ea6-e8b8-4ab7-bc50-f3fa3313104d) | [Euler, RK, and PBD](text/kinetics.html){title="Euler, RK, and PBD: common approaches to simulating kinetic motion of particles"} |
| Rendering particles | [CT](https://classtranscribe.illinois.edu/video?id=1f2ecac5-2124-4d9e-afdd-afaef11bb6fc) | [Particle Effects](text/particles.html){title="Particle Effects: simple heuristic-based visual effects"} |
| Instability and the CFL conditions | [CT](https://classtranscribe.illinois.edu/video?id=0ba68e50-ab08-4c50-a23c-982df64d146c) | [The CFL Conditions](text/cfl.html){title="The CFL Conditions: why large time-steps can make simulations blow up"} |
| Particle-based soft bodies and fluids | [CT](https://classtranscribe.illinois.edu/video?id=651f2195-8c6b-457f-a653-779d3d21555b) | [Smoothed Particle Hydrodynamics](text/sph.html){title="Smoothed Particle Hydrodynamics: simplified to have as little math as I can get it"} |
| Divergence-free grid-based fluids  | [CT](https://classtranscribe.illinois.edu/video?id=c7220480-5da5-4ab5-90fd-95dc0bbb213e) | [Fluids on a Grid](text/grid-fluids.html){title="Fluids on a Grid: the core ideas behind Eulerian fluid simulation"} |
| Self-advecting grid-based fluids | [CT](https://classtranscribe.illinois.edu/video?id=246a9b39-fedd-4401-9871-fb0232454337) | [Fluids on a Grid](text/grid-fluids.html){title="Fluids on a Grid: the core ideas behind Eulerian fluid simulation"} |
| In-class Q&A on fluids | [CT](https://classtranscribe.illinois.edu/video?id=4bc19fdd-2c64-4b8a-8adf-01d2d6378a48) |  |
| In-class Q&A on graphics publication | [CT](https://classtranscribe.illinois.edu/video?id=7c23dc23-508f-4945-a1d1-6fe80611b92d) |  |


How things appear: [Optical illusions from relative color perception](https://classtranscribe.illinois.edu/video?id=bd83c5cf-bcf1-4f9f-ba1f-a9efc30fb3c7)

# Faster and prettier rasterization {#pretty}

| Topic | Video | Notes |
| ----- | ----- | ----- |
| In-class Q&A on MP5 | [CT](https://classtranscribe.illinois.edu/video?id=61fbc44b-52c0-4ca2-b390-2ab7519d7ea7) |  |
| In-class Q&A on shadows, deferred shading | [CT](https://classtranscribe.illinois.edu/video?id=51785f27-bb99-4e60-9d24-60940802b3cc) |  |
| Shadow maps and shadow acne | [CT](https://classtranscribe.illinois.edu/video?id=5d9b5f63-c590-433d-a43b-41d0798f11b2) | [Shadow maps](text/shadowmap.html){title="Shadow maps: implementation guides for the most common approach to adding shadows to interactive graphics"} |
| Visibility and occlusion culling | [CT](https://classtranscribe.illinois.edu/video?id=7ba59f77-6faa-4789-8b2e-f74eb54a4403) |  |
| Deferred shading | [CT](https://classtranscribe.illinois.edu/video?id=733edd7e-6510-4e24-a6f9-00086d40532c) | [Deferred Shading](text/deferred.html){title="Deferred Shading: using more memory to reduce time needed for fancy lighting effects"} |
| Inverse Kinematics | [CT](https://classtranscribe.illinois.edu/video?id=bf777d66-4024-4b7e-abf7-eeee9f5e78cb) | [IK_survey.pdf](http://andreasaristidou.com/publications/papers/IK_survey.pdf) |
| In-class Q&A on rasterized global illumination | [CT](https://classtranscribe.illinois.edu/video?id=598990a0-6d16-4be1-88dc-0b58cbf9a199) |  |


How things appear: [Sunbeams](https://classtranscribe.illinois.edu/video?id=ac3f38d4-cc6e-4516-be8a-3ca303fe7346)

## Optional deep-dive content

| Topic | Video | Notes |
| ----- | ----- | ----- |
| In-class Q&A setting up Nanite | [CT](https://classtranscribe.illinois.edu/video?id=772a45b0-d2a1-4945-a43f-e4de8137da20) |  |
| Nanite 1 Highly Detailed Scenes | [CT](https://classtranscribe.illinois.edu/video?id=52661a28-46ea-4251-8dd4-3d3ba9a563ff) | [Streaming, Level of Detail, and Occlusion](text/nanite.html){title="Streaming, Level of Detail, and Occlusion: the quest for complexity-independent render times with constant visual quality"} |
| Nanite 2 LOD | [CT](https://classtranscribe.illinois.edu/video?id=086ed16b-ed55-4813-8854-655b1bc0dc89) | [Streaming, Level of Detail, and Occlusion](text/nanite.html){title="Streaming, Level of Detail, and Occlusion: the quest for complexity-independent render times with constant visual quality"} |
| Nanite 3 Occlusion | [CT](https://classtranscribe.illinois.edu/video?id=7bca6faf-e9d5-4f5d-9046-7271bedb99e4) | [Streaming, Level of Detail, and Occlusion](text/nanite.html){title="Streaming, Level of Detail, and Occlusion: the quest for complexity-independent render times with constant visual quality"} |
| Nanite 4 Streaming | [CT](https://classtranscribe.illinois.edu/video?id=d9622985-0edc-4a15-8ef9-0be0585b5856) | [Streaming, Level of Detail, and Occlusion](text/nanite.html){title="Streaming, Level of Detail, and Occlusion: the quest for complexity-independent render times with constant visual quality"} |
| Nanite 5 Other | [CT](https://classtranscribe.illinois.edu/video?id=754c2612-e294-4041-a9e1-034aae4deb9a) | [Streaming, Level of Detail, and Occlusion](text/nanite.html){title="Streaming, Level of Detail, and Occlusion: the quest for complexity-independent render times with constant visual quality"} |
