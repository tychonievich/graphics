---
title: Burley's Principled BRDF
summary: (unfinished) An empirically-backed artist-focussed material model with widespread adoption.
...

In 2012, Brent Burley at Walt Disney Animation Studios published [a whitepaper](https://media.disneyanimation.com/uploads/production/publication_asset/48/asset/s2012_pbs_disney_brdf_notes_v3.pdf) describing a BRDF used in Disney's 3D animation tools.
This paper has had significant impact for various reasons,
not the least of which is that it is the paper itself is reasonably readable and complete.

This model is a hybrid of physically-derived mathematics,
artist-friendly parameters,
and empirically-backed resulting appearances.
This page attempts to summarize the model from an implementer's point of view.
It also uses a simplified subset of the model,
ignoring many of the parameters.

# Variables

There are many variables used in the model.
These can be split into geometric variables
and material parameters.

: Geometric variables

| Symbol | GLSL type | Meaning |
|:------:|-----------|---------|
|$\vec n$|`vec3`|unit surface normal|
|$\vec l$|`vec3`|unit vector pointing towards light|
|$\vec v$|`vec3`|unit vector pointing toward viewer|
|$\vec h$|`vec3`|unit half-way vector between $\vec v$ and $\vec l$; that is, normalized $\vec v + \vec l$|
|$\theta_l$|`float`|angle between $\vec l$ and $\vec n$; $\cos(\theta_l) = \vec l \cdot \vec n$|
|$\theta_v$|`float`|angle between $\vec v$ and $\vec n$; $\cos(\theta_v) = \vec v \cdot \vec n$|
|$\theta_h$|`float`|angle between $\vec h$ and $\vec n$; $\cos(\theta_h) = \vec h \cdot \vec n$|
|$\theta_d$|`float`|angle between $\vec l$ and $\vec h$ = angle between $\vec v$ and $\vec h$; $\cos(\theta_d) = \vec l \cdot \vec h = \vec v \cdot \vec h$|

Note that we'll generally try to write formulas in terms of the cosines of angles instead of the angles themselves for efficiency.
Fortunately, many materials naturally have cosines of the angles in their fomulation.

: Parameters

| Name | GLSL type | Meaning |
|:-----|-----------|---------|
|*baseColor*|`vec3`|RGB color; generally should be dark (under 0.5 in all components)|
|*metalic*|`float`|0 means "use the dielectric BRDF"; 1 means "use the metalic BRDF"; intermediate values for sub-pixel mixing like slighly rusted metal|
|*specular*|`float`|artist-friendly measure of shininess if polished; correlated to optical density, with 0.5 being like plastics and other oils and 1 being like glass|
|*roughness*|`float`|0 for highly polished, 1 for matte and diffuse-looking|
|*sheen*|`float`|the pale halo seen with peach fuzz and some cloth; should be 0 for most substances|
|*sheenTing*|`float`|how much the sheen should match the base color; 0 for white sheen|

# Diffuse

$$
f_d = \mathit{baseColor}\frac{1}{\pi}\Big(1+(F_{90}-1)\big(1-\cos(\theta_l)\big)^5\Big)\Big(1+(F_{90}-1)\big(1-\cos(\theta_v)\big)^5\Big)
$$
where $F_{90}=0.5 + 2\mathit{roughness}\cos^2(\theta_d)$
