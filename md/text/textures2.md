---
title: Using Textures
summary: Classes of texture use common in rasterized 3D graphics.
...

A **texture** is a raster, a part of which is interpolated over a triangle.
There are many potential uses for this general idea.

Most of these techniques use an image as a collection of channels
rather than as a color image.
One channel of an image is a raster of numbers.
Those numbers have a fixed range, usually considered to be 0–1 regardless of the internal representation.
Common images have three or four channels,
often interpreted as Red, Green, Blue, and Alpha.
Inside the shaders of a WebGL application that interpretation is largely arbitrary:
the fragment shader's `out vec4` uses that interpretation,
but we can treat the a texture's channels any way we wish.

# "Standard" textures

The "standard" use of textures,
the thing people most often mean if they refer to textures without any additional qualifier,
uses the color retrieved from the texture as the diffuse color of the material.
This use dates back at almost to the very beginning of computer graphics^[<https://collections.lib.utah.edu/ark:/87278/s6cg2j21>]

# Decals

When the texture contains an alpha channel, it can be composited on top of another color using [the over operator](fixed-functionality.html#blending).
The color underneath can be fixed for the model, interpolated between vertices, or looked up in another texture.
Regardless of how the underlying color is selected, alpha-blended texture colors are commonly called "decals".
Decals also are often smaller than a full-object texture
and may be applied using different texture coordinates (either as additional attributes or computed separately from the same texture coordinate attributes in the vertex shader).

# BRDF parameters other than color

Other parameters of the BRDF being rendered can also be looked up in a texture:
secularity, roughness, anisotropy, and so on.

The more complicated the BRDF the more such parameters there are.
One popular model, often called "[physically based rendering](https://substance3d.adobe.com/tutorials/courses/the-pbr-guide-part-1)"
or "[principled BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)",
has upwards of 30 parameters.
On benefit of using a unified shader like that
is the ability to completely change material from one texel to the next,
having some texels represent metal, others wax, others stone, and so on.


# Displacement maps

Displacement maps use a single-channel image indicating a desired offset from the underlying geometry.
They are not used in the fragment shader, but instead during mesh generation,
typically as part of a subdivision-based mesh refinement.

The basic use of displacement maps runs as follows:

1. Create a low-polygon mesh with texture coordinates and a displacement map
2. Subdivide the mesh into smaller polygons; move each new vertex along its normal by an amount found by looking up its interpolated texture coordinate in the displacement map

Displacement maps are not overly common.
When used, they are generally part of the tesselation shader or geometry shader;
those shaders are parts of the GPU pipeline that are not exposed by WebGL, so we won't implement displacement maps.

# Bump and normal maps

Textures can also be used to modify surface normals.
There are multiple ways to achieve this, all collectively called "bump mapping",

The most intuitive way to store a bump map would be exactly like a displacement map.
However, that method does not allow us to modify normals in the fragment shader.
Instead, we compute the gradient of the displacement map and store the resulting "normal map" instead.

Normal maps^[James F. Blinn. 1978. "Simulation of wrinkled surfaces." *SIGGRAPH Comput. Graph.* 12, 3 (August 1978), 286–292. <https://doi.org/10.1145/965139.507101>] are 2-channel textures; one channel is how much to adjust the normal in the texture coordinate's $u$ direction and the other is how much to adjust it in the texture coordinate's $v$ direction.
Those directions vary across the model,
so we have to pass them in as vertex attributes and interpolate them to each fragment.
They will always be tangent to the surface of the model,
but not necessarily unit length (the texture might be stretched in one area of the model and squished in another) nor necessarily perpendicular (the texture might be sheered in some areas).
Because they are tangent and distinct we can use them to compute the surface normal if we wish to save some space.

Normal mapping thus runs as follows:

1. For each vertex, specify its position, normal, and texture coordinate.

2. For each vertex, compute its two tangents
    as vectors perpendicular to the normal
    and pointing in the direction of increasing $u$ and $v$, respectively.
    This computation can be performed during model loading
    or computed and stored during model creation.

3. At each fragment, light based on the interpolated normal
    plus the normal map's first channel's value times the first interpolated tangent
    plus the normal map's second channel's value times the second interpolated tangent.

# Parallax mapping

Parallax mapping is a type of bump mapping and an extension to normal mapping.
It requires three channels: the one used in displacement mapping and the two used in normal mapping.

The principle behind parallax mapping is to change the texture coordinate before texture lookup to simulate how light behaves at steeper angles.
Parallax mapping does this by one of several iterative approximations.

## Parallax mapping

Parallax mapping^[Kaneko, Tomomichi & Takahei, Toshiyuki & Inami, Masahiko & Kawakami, Naoki & Yanagida, Yasuyuki & Maeda, Taro & Tachi, Susumu. (2001). "Detailed shape representation with parallax mapping." In *Proceedings of the ICAT*. 2001.]
observes that if we had per-fragment displacement mapping (which we don't)
then as we looked at a polygon at an angle far from the normal
then we'd see a different position.

<figure>
<svg viewBox="0 40 200 100" font-size="6" style="width:32rem;">
<circle cx="10" cy="100" r="3" fill="blue"/>
<circle cx="190" cy="100" r="3" fill="blue"/>
<g fill="none" stroke="black">
<path d="M 10,100 190,100" stroke="blue"/>
<path d="M 10,110 S 40,100 70,120 100,125 130,125 160,130 190,100" stroke-width="0.5" stroke="#800"/>
<path d="m 100,100 -40,-40 -2,2 -2,-6 6,2 -2,2" stroke-width="0.5"/>
<path d="m 100,100 -0,30 30,0 -30,-30 m 30,0 0,30" stroke-width="0.5" stroke-dasharray="1 1"/>
</g>
<text x="15" y="95" fill="blue">Polygon</text>
<text x="50" y="137" fill="#800">Virtual displaced surface</text>
<text x="45" y="53">to eye</text>
<circle cx="100" cy="100" r="2"/>
<text x="98" y="107" text-anchor="end">Fragment</text>
<circle cx="130" cy="100" r="2" fill="green"/>
<text x="132" y="107" text-anchor="start" fill="green">Used u',v'</text>
</svg>
<figcaption>Concept behind parallax mapping</figcaption>
</figure>

1. Look up the displacement channel's value at this fragment;
    suppose that says to offset $h$ away from the surface of the object.

2. Figure out where the ray from the eye would have hit the plane if it had had that depth instead.
    This is done by
    
    a. Find $\Delta_u = \tan(\theta_u)$ where $\theta_u$ is the angle between the eye direction and the u tangent vector.
        
        Recall that $\tan(\theta) = \dfrac{\sqrt{1-\cos^2(\theta)}}{\cos(\theta)}$
        and that $\cos$ can be found via the dot product of two unit vectors.

    b. Set $u' = u + h \Delta_u$

    c. Repeat for $\Delta_v$

Parallax mapping says
"the fragment with coordinate $(u,v)$ should be colored as if it had coordinate $(u',v')$ instead".
This distance between $(u,v)$ and $(u',v')$ increases as the viewing angle becomes less head-on
and also increases as the displacement channel gets further from the geometry position.

We then use the color, normal, specularity, and other $(u',v')$ texel information to render the fragment

## Steep parallax mapping

Parallax mapping is better than normal mapping for some angles,
but as the viewing angle approaches the plane's tangent
and as the depth of displacement increases
it becomes less accurate.
Steep parallax mapping^[<https://casual-effects.com/research/McGuire2005Parallax/index.html>]
adds a linear search component on top of parallax mapping.

1. Iterate from closest to furthest possible depth the displacement map could have in several steps.

2. Update the $u,v$ for this new depth (similar to how we did for parallax mapping) and check if at that $(u,v)$ we've crossed into solid material yet.
    If so, use parallax mapping from there.
    If not, continue with the next depth step.

As depth steps approach single-pixel displacements, steep parallax approaches the appearance of high-resolution displacement mapping,
at the cost of significant work in the fragment shader.

## Parallax occlusion mapping

Steep parallax mapping has visible stair-stepping effects at steep viewing angles.
This happens because of the fixed iterations:
if one fragment stopped at iteration 2 and its neighbor at iteration 3 there'll be a visible discontinuity between them.

Parallax occlusion mapping^[Brawley, Z., and Tatarchuk, N. 2005. "Parallax Occlusion Mapping: Self-Shadowing, Perspective-Correct Bump Mapping Using Reverse Height Map Tracing." In *ShaderX3: Advanced Rendering with DirectX and OpenGL*, Engel, W., Ed., Charles River Media, pp. 135-154.]
fixes that by using a weighted average of two iterations of the steep parallax mapping process for each fragment.
Otherwise it's the same as steep parallax mapping.

# Baked lighting

"Baking" refers to computing something that is potentially dynamic (such as lighting, fluid motion, or organism growth) and storing the results for later use in rendering.

For a static scene with many objects, computing how much light falls on each point in the scene can be very time-intensive
but only need be done once as it does not change from frame to frame.
That makes it a prime candidate for baking, resulting in texture maps that express how brightly illuminated each texel is.

Baked lighting has many limitations.
For diffuse light a single channel is sufficient, but for specular light at least three are needed per specular highlight;
and if the lighting was complicated enough to need backed lighting it is unlikely that just a few specular highlights will be sufficient.
Also, real scenes are almost never *entirely* static;
they may be *largely* static with most geometry fixed in place and just a few moving parts,
but those few moving parts might have significant impact on lighting (e.g. if they occlude the primary light source).

Baked lighting is rarely used by itself.
Often a baked lighting map is used to compute the "ambient" light:
low-intensity light that reaches areas not directly visible from major light sources.
That baked ambient light is then combined with more traditional dynamic light sources to create final results.

# Environment maps

The other techniques on this page all assume that there is a texture coordinate interpolated to each fragment, but that is not the only way to use a texture.

Environment maps store a full $4 \pi$ [steradian](https://en.wikipedia.org/wiki/Steradian) view of the world from some fixed point.
As such, they are indexed not by a $(u,v)$ coordinate but by a direction represented as a unit vector.
Cube maps are the most common type of environment map, though others types are also sometimes used.

## Reflection

A reflective material can be emulated by using an environment map,
indexing it by the direction to the eye reflected across the normal:
$2(\vec e \cdot \vec n)\vec n - \vec e$.

If the cube map is mipmapped then intentionally using a higher level in the mipmap can simulate blurred reflections from a partially-reflective object.

## Refraction

A refractive transparent material can also be emulated using an environment map, though not as accurately as a reflective one.
Refraction depends on two angles: the entering angle, which we know,
and the exiting angle, which we don't.
Refraction simulation often assumes a simplified model such as "the exit surface is perpendicular to the eye" to obtain a generally refraction-like appearance.

Alternatively, depth peeling can be used to do multi-pass refraction.
Depth peeling works by rendering the scene normally into one frame buffer,
then rendering it again into another frame buffer but this time discarding any fragment that has a depth nearer than the first render's depth buffer.
Thus the first render will get the entering surface, the second render the exiting surface,
and the pair of them can make a slightly better estimate of refraction.

## Full BRDF

A high-dynamic-range environment map,
one in a light-linear color space instead of an exposed-image color space,
can be used to accurately compute an entire BSDF.
Each texel of this kind of environment map expresses the intensity and color of light coming from one direction,
and various mipmap levels average these for blurrier results.
Velveteen surfaces might look in this light map in one direction,
polished surfaces in another,
diffuse surface in several low-res directions together;
the BSDF can then combine these into a single illumination for the fragment.

## Dynamic environment maps

If the details of an environment map are both important enough to spend GPU time on and dynamic enough not to be easily pre-computed,
a cube map can be created by rendering the scene six times with six different view matrices.
This can allow effects like reflections of moving characters to appear on the surfrace of polished objects and the like.

# Shadow maps

Shadows are a complicated topic and have many solutions in graphics.
However, one of the most common to this day
is the basic shadow map first published in 1978^[Lance Williams. 1978. "Casting curved shadows on curved surfaces." *SIGGRAPH Comput. Graph.* 12, 3 (August 1978), 270–274. <https://doi.org/10.1145/965139.807402>].
It works as follows.

1. Load a view and projection matrix to view the scene from the perspective of the light.
2. Render a depth buffer (no color buffer) into a texture map called a shadow map.
3. Load a view and projection matrix to view the scene from the perspective of the viewer.
4. In the fragment shader
    a. find the distance to the light and position of the fragment from the light's perspective
    b. use the position to look up the maximum depth the camera can see in that direction
    c. if the maximum depth from the texture is closer than the fragment's depth, the fragment is in shadow

There are many nuances to get this exactly right.
The shadow map has finite precision;
the fragment likely lies between several texels;
geometry gets pixelated when rendered into the shadow buffer and that pixelation may not line up nicely with the pixels of the final scene;
and so on.

Common workarounds for these details include biassing the shadow map (i.e., pretending everything was just a bit further from the light than it actually was)
and checking several neighboring texels to blur the shadows and make single-texel errors less visible.


