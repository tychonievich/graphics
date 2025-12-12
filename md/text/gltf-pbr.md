---
title: Physically-based Rendering
summary: The most common parts of PBR models, circa 2020, as documented by Khronos in the glTF specification
...


On this page we introduce a few of the ideas of the 2010s and 2020s-era interactive-speed physically-based rendering (PBR) algorithms.

All physically-based rendering is developed roughly by

1. Understanding and mathematically describing how photons interact with matter in the real world.
2. Discarding details and approximating math until something sufficiently efficient to compute is developed.

This page focuses only on the simplest, most broadly-useful parts of these ideas.
In particular, it is limited to

- Opaque solids (no transparency, translucency, subsurface scattering)
- Within vacuum or optically-clear air (no crepuscular rays, varying air density, haze)
- With isotropic surface micro-geometry (no parallel grooves, brushed hairs)
- Illuminated externally (not glowing)
- Without detailed spectrum effects (no diffusion gratings, thin films, florescence)
- With zero-delay lighting (no phosphorescence)

# Light's behavior

We will model two phases of a light's interaction with a surface it contacts:

1. It will encounter the outer boundary of the solid, where light has to slow down to enter the object but some light bounces off instead as described by **Fresnel's equations**, resulting in **specular** reflections.

2. It will encounter the material itself, where some wavelengths of light will be **absorbed**; the light that is not absorbed will behave in one of two ways
    
    - If the material is a conductor (metal), light will be **reflected**.
    
    - If the material is a dielectric (not metal), light will be **diffused** (also called being scattered).

Specular, reflection, and diffusion are collectively all types of **reflectance**.

A key goal of PBR is to not break physical laws, in particular the conservation of energy.
Any light that is specularly reflected off the surface of an object (in any direction)
never reaches the material itself.

All reflectance is reversible: if you toggle the position
of a light source and a light detector,
the amount and color of light detected will never change.

# The metallic-roughness material model

**Fresnel**'s equations are complicated, with different behaviors for different wavelengths and polarization of light.
However, the biggest visual impact is, like with sheen, based on the viewing angle:
head-on most light makes it though the material surface
while at a glancing angle most is specularly reflected.

**Absorbtion** depends on wavelength, with some materials absorbing very specific wavelengths of light,
but to make the computation simple we usually represent it as an RGB color
suitable for sending to a 3-color display device.
For each R, G, and B channel, 0 means all light the eye would perceive as that color is absorbed
while 1 means none of it is.

**Reflection**, both specular and metallic, can be posed in several ways
but one of the most useful for graphics is based on the alignment of the surface normal
and the **halfway vector**, which is the vector half-way between the vector to the viewer and the vector to the light.
When those two align, light is reflected;
when they do not, light is not reflected.

**Diffuse** light is generally modeled as leaving the object in all directions equally,
meaning its intensity is dependent only on how much light reaches the object per unit surface area.
Equal intensity light hitting an object head-on hits a smaller area, and hence leads to more intense diffuse lighting,
than light that hits at a steep angle.
The relationship between incident angle and diffuse intensity is called **Lambert's Law**.

+------------+---------------------------------------------------------------------+
| Component  | Inputs                                                              |
+            +-------------------------+--------------------+----------------------+
|            | surface normal $\vec n$ | to viewer $\vec v$ | to light $\vec \ell$ |
+:===========+:=======================:+:==================:+:====================:+
| Fresnel    |  Yes                    | Yes                |                      |
+------------+-------------------------+--------------------+----------------------+
| Absorbtion |                         |                    |                      |
+------------+-------------------------+--------------------+----------------------+
| Reflection | Yes                     | Yes                | Yes                  |
+------------+-------------------------+--------------------+----------------------+
| Diffuse    | Yes                     |                    | Yes                  |
+------------+-------------------------+--------------------+----------------------+

## Roughness

When considering the surface normal,
it is common to model the "roughness" of the object,
representing sub-pixel-scale geometry.
In a very smooth object, all parts of the pixel have exactly the same surface normal
and $\vec n$ is a simple constant.
But most objects are at least a little rough,
meaning some parts of the pixel have a noticeably different normal than other parts,
and $\vec n$ is better treated as a distribution of normals over the area of the pixel.

The roughness of a material has more impact than just changing $\vec n$:
a tiny bump on one part of the material might cast a shadow over another part (called "self shadowing"),
and some light scattered off of a bump might hit another bump to add a kind of local light source called "multiscattering").

Roughness is traditionally represented in equations with the symbol $\alpha^2$
because early papers used a definition of roughness that was the square root of what was needed for the math.
In 2012, Brent Burley at Walt Disney Animation Studios published [a whitepaper](https://media.disneyanimation.com/uploads/production/publication_asset/48/asset/s2012_pbs_disney_brdf_notes_v3.pdf) which included the recommendation that artists preferred a roughness parameter
that was the square root of $\alpha$, and that has become mainstream since.
This means that $\alpha^2 = \text{roughness}^4$, where $\text{roughness}$ is the value provided by artists, materials, and roughness textures.


# Common approximations

## Fresnel

In 1994, Christophe Schlick published^[DOI [10.1111/1467-8659.1330233](https://doi.org/10.1111/1467-8659.1330233)] several computationally-efficient energy-preserving visually-close-enough approximations of PBR functions.
Some of these have become the standard implementation for PBR.

Schlick's equation for Fresnel reflectivity is 

$$\begin{split}
F_0 &= \left(1 - \text{ior} \over 1 + \text{ior}\right)^2 \\
F_r &= F_0 + (1 - F_0)\big(1 - |\vec v \cdot \vec h|\big)^5
\end{split}$$

where $\text{ior}$ is the index of refraction of the material^[Often assumed to be 1.5, a common value for organic material like wood and plastic, giving $F_0 = 0.04$]
and $\vec h$ is the halfway vector, $\vec \ell + \vec v$ normalized.

$F_r$ is a ratio of light that is specularly reflected:
when $F_r$ is 0, no light is reflected and all makes it into the material,
and when $F_r$ is 1, all light is reflected and none makes it into the material.

Note that roughness is not mentioned in this approximation.
While roughness does have some impact on Fresnel,
it is generally not considered to be visually important enough to be worth the extra computation.

To fully preserve energy, light that is specularly reflected due to Fresnel
should not be used to illuminate the material.
However, that lighting reduction is often omitted for efficiency,
meaning that objects may be a bit brighter than they should be.
In 2017 Christopher Kulla and Alejandro Conty presented^[In a SIGGRAPH course (DOI [10.1145/3084873.3084893](https://doi.org/10.1145/3084873.3084893), which does not publish course content; one author has the [slides](https://fpsunflower.github.io/ckulla/data/s2017_pbs_imageworks_slides_v2.pdf) on his personal page.] their finding that the lighting loss did not seem to have a simple equation
and when they wanted to add it they used an piecewise trilinear equation with 4096 terms.

## Reflection

There are *many* models of reflection,
in part because there are many micro-geometries that might make a material rough.

Since the 2010s, the most popular model has been the GGX model,
so named (with no explanation of why they picked that name)
by Bruce Walter, Stephen Marschner, Honsong Li, and Kenneth Torrance in 2007^[DOI [10.5555/2383847.2383874](httsP//doi.org/10.5555/2383847.2383874)].
The same model was also derived and published much earlier, but without getting much buy-in,
by T. S. Towbridge and Karl Reitz in 1975^[DOI [10.1364/JOSA.65.000531](https://doi.org/10.1364/JOSA.65.000531)].

The Towbridge-Reitz/GGX model is the product of two functions.
One is a microfacet distribution function:
$$
D = \frac{\alpha^2}{\big(1 + (\vec n \cdot \vec h)^2 (\alpha^2 - 1)\big)^2 \pi}
$$
The other is a self-shadowing/occluding function
or visibility function^[This page has the visibility function. The self-shadowing/occluding function has an extra factor $4 |\vec n \cdot \vec l| \, |\vec n \cdot \vec v|$ in the numerator and is traditionally given the letter $G$ instead of $V$.],
typically based on an derivation published by B. Smith in 1967^[DOI [10.1109/TAP.1967.1138991](https://doi.org/10.1109/TAP.1967.1138991)]:
$$
V = \frac{1}{
\left(|\vec n \cdot \vec \ell| + \sqrt{\alpha^2 + (1-\alpha^2)(\vec n \cdot \vec \ell)^2}\right)
\left(|\vec n \cdot \vec v| + \sqrt{\alpha^2 + (1-\alpha^2)(\vec n \cdot v)^2}\right)
}
$$

If any of $\vec n \cdot \vec h$, $\vec h \cdot \vec l$, or $\vec h \cdot \vec v$ is negative, no reflection occurs.

The product $V D$ gives the ratio of light that is reflected directly from the provided light source ($\vec \ell$) to the provided viewer ($\vec v$).
Any remaining light ($1 - V D$) is still reflected, but towards other viewers.

The common form of Towbridge-Reitz/GGX as given above
is not fully energy-conserving because it lacks a term for multiscattering,
meaning very rough surfaces come out darker than they should.
In 2017 Christopher Kulla and Alejandro Conty presented^[In a SIGGRAPH course (DOI [10.1145/3084873.3084893](https://doi.org/10.1145/3084873.3084893), which does not publish course content; one author has the [slides](https://fpsunflower.github.io/ckulla/data/s2017_pbs_imageworks_slides_v2.pdf) on his personal page.] an additional multiscattering term,
based not on a function of any kind but rather on precomputing the multiscattering energy loss of the above formula
on a grid of viewing angles and roughnesses
and looking up the energy to add back in via a texture lookup in that grid.

## Diffuse

Lambert's law is based on simple trigonometry:
a unit area of light
impacting a surface at angle $\theta$
is spread out over an area of $1 / \cos(\theta)$ of the surface
and thus reflects with intensity proportional to $\cos(\theta)$.
Integrating over all viewing angles shows $\cos(\theta)$ alone would diffuse
$\pi$ units of light for each unit of inbound light, which violates conservation of energy,
so we can derive the correct diffusion intensity as $\cos(\theta) / \pi$.
$\cos(\theta)$ is easy to compute: it's just $\vec n \cdot \vec \ell$, giving us
$$
\vec n \cdot \vec \ell \over \pi
$$

Note that roughness is not mentioned in this approximation.
While roughness does have some impact on diffuse lighting,
the normal distribution, self-shadowing, and multiscattering terms
come close to cancelling one another out,
leaving a minor enough visual effect that it is generally not considered to be worth the extra computation.

# Procedural and image lights

The approximations of lighting given above
(and also others not given here for sheen, refraction, anisotric reflections, and so on)
depend on $\vec \ell$, a unit vector pointing from the point being illuminated
toward the light source.

The simplest case is when all light comes from a finite set of mathematical points;
then we can simply run the equations with each light source
and add their contributions to find the light visible in a pixel.

More work is required if light comes from a finite set of finite areas.
Typically, this is handled by picking a sampling of points across the area
and treating each one as a point light, as noted above.
Often this is done using temporal antialiasing:
we pick a different point in the area each frame
and average the light found across multiple frames (unless the camera or object moves, in which case we reset).

Much better looking than even area lights
(and often combined with some point and area lights in practice)
is using an environment map
which indicates how much light comes from each direction across the entire surrounding sphere.

## Image-based lighting

Environment maps are generally provided as **high dynamic range** (HDR) images
with full 360°, $4\pi$ steradian coverage.
There are multiple HDR image formats
and multiple ways to project an entire surrounding sphere onto a rectangular image,
but these are not generally used as-is:
rather, they are first preprocessed into a few cubemaps.

A cubemap is an set of 6 square images that together cover the surface of a cube.
They are indexed by 3-vectors:
the face to use is chosen by finding which component of the vector is largest
and the texel on that face is chosen by dividing the other two components by that largest value.

:::example
The vector $(-0.36, -0.80, +0.48)$
uses the negative-y face of the cube
because its $y$ coordinate is the largest and is negative.

Within that face, it picks a texel
using $(-0.36, +0.48) / -0.80 = (+0.45, -0.6)$ in a ‒1-to-1 space,
or $(1+0.45, 1-0.6)/2$ in a 0-to-1 space,
meaning texel $(0.725 w, 0.2 h)$
on a $w×h$ texture map.
:::

The pre-processing converts the environment map into more than one cube map:
one for each major type of lighting.

For diffuse lighting, the cube map is indexed by surface normal.
To find the light intensity and color of a given diffuse cube map texel
we iterate over the environment map and apply the diffuse lighting equation
for the surface normal mapping to that cube map texel,
adding the effect of all such lightings.
An important consideration here is that in most environment maps,
not all pixels represent the same solid angle
and smaller pixels contribute less light to the diffuse cube map.

For reflective lighting, the cube map is indexed by the reflection of the view vector over the surface normal,
$\vec r = (2 \vec n \cdot \vec v) \vec n - \vec v$.
For zero-roughness materials, each texel of the cube map
is simply the environment map pixel.
For higher roughness, the cube map needs to be blurred
as specified in the Towbridge-Reitz/GGX distribution.
Such bluring is computationally expensive
and is done as part of the cube map creation,
with higher roughnesses stored as smaller mip maps.
Computing the blur needs to not only follow Towbridge-Reitz/GGX
but also the non-uniform solid angles of pixels,
and in practice is often done by using
a Monte Carlo quasirandom sampling of the Towbridge-Reitz/GGX distribution at a given roughness.

Once the cube maps are created, image-based lighting becomes

1. Compute [Fresnel] the same as with point lights.
2. For diffuse lighting, check the diffuse cube map instead of point light computation.
3. For reflection, check the reflection cube map at a mip map level based on roughness instead of the point light computation.
4. Combine those with absorbtion based on the fresnel, metalicity, and absorbtion color of the material.
5. If there are also point or area lights, compute and add their contribution too.

# Exposure Filtering

Physics-based rendering uses physical units.
In particular, light in each of the red, green, and blue channel is measured in nits^[1 nit = 1 candela / meter^2^<br/>1 candela = ${1 \over 683}$ watts of 550nm light per steradian ≈ the brightness of the flame of a wax candle.]
These are convenient units for computing lighting,
but are not very useful for sending to a display device.

Display devices and image formats
generally mimic analog photographs and other chemical imaging decides (like retnas)
by doing the following:

1. Optionally, filter the image to make very bright areas spill over into other regions,
    creating "glow"-type effects.
    
    There are many sources of glows:
    haze in the atmosphere,
    imperfections in lens surfaces,
    diffraction around lens aperture boundaries,
    and chemical bloom inside light receptors
    are some of the more common.
    
    Applying any of these filters requires non-local, and thus more expensive, computation,
    but without them very bright areas will appear flat and uninteresting.

2. Apply an exposure function that compressed bright colors and scales color overall.
    
    A simple exposure function is $\text{exposed} = c + k\log(\text{nits})$.
    This kind of function is easy to derive and implement, but can change saturation of colors if applied to R, G, and B separately
    and doesn't look as nice to many viewers as more complicated exposure functions do.

3. Apply [gamma correction](color.html#non-linear-storage-gamma) to compress data into the most visually-important brightnesses.

4. Digitize to just a few (often 8 or 10) bits per color channel.

5. Send the resulting bytes to the display.

6. Reverse the gamma correction and emit (backlit screens) or absorb (pigments) the corresponding amount of light.

:::note

Exposure ≠ gamma correction

Exposure models how light, which has no maximum brightness,
is perceived by eyes and cameras, which do max out at some brightness.

Gamma is used to compress light information in a way that minimizes viewer's perception of light transitions between adjacent discrete color values.

Both tend to expand darker colors and compress brighter ones,
but do so in different ways for different purposes.

A display capable of being as bright as the sun would not need exposure, but would still benefit in efficiency from gamma.

A display with unlimited storage and bandwidth would not need gamma, but would still benefit in human perception of light intensity from exposure.

:::
