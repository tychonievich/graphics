---
title: Simplified PBR
summary: An efficiently-computable approximation of physically-based rendering from Unreal Engine 4 and Disney.
...

This page documents a subset of the current physically-based rendering (PBR) models; in particular, it is the subset selected by Unreal Engine team^[Brian Karis, 2013. "Real shading in Unreal Engine 4" <https://cdn2.unrealengine.com/Resources/files/2013SiggraphPresentationsNotes-26915738.pdf>] of the model popularized by Disney^[Brent Burley, 2012. "Physically Based Shading at Disney" <https://media.disneyanimation.com/uploads/production/publication_asset/48/asset/s2012_pbs_disney_brdf_notes_v3.pdf>].

# Diffuse

The Unreal Engine 4 team determined that for diffuse lighting, using Lambert's law was visually adequate. This leaves out three terms included by the Disney team led by Brent Burley:

- Because surfaces have microscopic bumps, normals are randomized causing more uniform lighting that Lambert's law would otherwise suggest and a brightening near the edges of the lit area.
- Because surfaces have microscopic bumps, one bump might shadow another, causing more uniform lighting that Lambert's law would otherwise suggest, causing a darkening near the edges of the lit area.
- Because many surfaces are not fully transparent, light that enters one spot might emerge from a slightly different spot, causing light to bleed over light-dark boundaries.

While these are all important for the appearance of some materials, many materials are smooth enough that the two effects of bumps nearly cancel out and opaque enough that light entering the material does not travel far enough to have a strong visual appearance.

# Specular

The specular model got much more attention. Lambert's law is based on an actual physical property, but Blinn and Phong's models are not based on anything physical and need to be fully replaced. In particular, most PBR models replace it with what is called the Microfacet Model, which consists of three optical terms (plus a normalization factor to make it energy-preserving) as well as change in how we define scenes:

- $D$, the microfacet distribution function. This asks a variant of "how bumpy is the surface": in particular, it asks "if we sampled an entire pixel at this normal, what percentage of the sampled normals in that area would reflect the light source?". Because "reflects the light source" is handled by the halfway vector, this is often written as $D(\theta_h)$ where $\theta_h$ is the angle between the halfway vector and the surface normal.
    
    There are two main parameters we consider when defining $D$.
    
    One is "what shape are the bumps?" which will be hard-coded into the math we use to define $D$; we will use the GGX distribution ("ground glass unknown", named in a 2007 paper that re-derived it^[Bruce Walter, Stephen Marschner, Honsong Li, Kenneth Torrance, 2007. "Microfacet Models for Refraction through Rough Surfaces." <https://www.cs.cornell.edu/~srm/publications/EGSR07-btdf.pdf>] but first defined without a catchy name in 1975^[T. S. Trowbridge, K. P. Reitz, 1975. "Average irregularity representation of a rough surface for ray reflection." <https://opg.optica.org/josa/fulltext.cfm?uri=josa-65-5-531&id=55682>]); GGX models the surface as a bunch of little segments of spheres. That's a bit of work to compute, so we'll use various approximations to make it more efficient.
    
    The other parameter is "how bumpy is it?" which will be a material property, roughness.

- $F$, the Fresnel reflection coefficient. August-Jean Fresnel defined the math of light passing a material boundary which has many nuances, but the one we are interested in here is that at a glancing angle everything is shiny. Because this depends on the angle we look at the material from, it depends on the vector to the viewer; because it is specular, it depends on the halfway vector; thus it is often written $F(\theta_d)$ where $\theta_d$ is the angle between the vector to the viewer and the halfway vector.

    There is only one parameter needed to handle $F$: the shininess to a ray coming directly into the surface along its normal (when $\theta_d = 0$), or $F_0$. While there is some real-world variation in $F_0$, it's a reasonable simplification to say that there are just two values: metals have $1.0$, non-metals (i.e. "dielectrics") have $0.04$. There are some non-metals that have a bit higher (maybe as high as $0.6$) or a bit lower (maybe as low as $0.2$) but they're uncommon and giving that flexibility to artists doesn't have much positive impact on visual appearance.

- $G$, the geometric attenuation factor or shadowing factor. More bumps means more of the material that is shadowed by other bumps. This depends on both the viewing angle (head-on we see all the shadows there are, but from the side we might only see a few of them) and the lighting angle (head-on lighting has no shadows, but lighting from the side has many) so we write it as $G(\theta_l, \theta_v)$ where $\theta_l$ is the angle between the surface normal and the light and $\theta_v$ is the angle between the surface normal and the viewer.
    
    $G$ should theoretically depend on the exact same parameters as $D$, since it is a different aspect of the same geometrical property. However, if we try to directly derive $G$ from the GGX distribution we get something we do not want to compute and no one "best" approximation has been identified. We present here the same approximation discussed chosen by Unreal Engine 4.

In addition to these three physical reflectence terms, we also need to handle another aspects of Blinn and Phong's models. Real light sources are not tiny mathematical points; they have area, which makes their shine spots bigger. If we start using physically-based specular computation with dimensionless lights the shine spots will become far too small to be believable, so we'll need a separate way of making lights look bigger, preferably without the overhead of sampling many light points. Karis defined several ways to do this, but we'll use just one: a representative point method for spherical light sources.

# Implementation

1. The lighting models we showed in class used "direction to light" as an uniform parameter. Replace that with "position of light" and compute "direction to light" as "position of light" &minus; "position of fragment."
    
    If you put the light far from the model this will have little visual impact, but move it closer and most of the model will become darker.

2. Add a "radius of light" parameter and use Karis's representative point computation^[Note: Karis had a sign error in the formula for closestPoint, which is corrected below]:
    
    a. $\vec r$ = reflection of vectorToEye over surfaceNormal
    a. centerToRay = directionToLight &minus; (vectorToEye dot $\vec r$) $\vec r$
    a. closestPoint = directionToLight &minus; centerToRay clamp01(lightRadius / distanceToLight)
    a. newDirectionToLight = normalized(closestPoint)
    a. use the newDirectionToLight for specular but not for diffuse lighting
    
    If you make the light radius only a bit smaller than the distance from the model to the light, the shines should get very large.

3. Change parameters to be more believable.
    
    - Most things you see absorb most of the light that hits them. Only have a color parameter above 0.5 if you want the object to look intensely bright in that spectrum.
    - Increase light intensity until the colors no longer look muted.

4. Add a "roughness" material parameter, and a constant $F_0 = 0.04$. For roughness we'll use Disney's $\alpha$, the square of the roughness parameter in the GGX definition of roughness, because that scaling is more intuitive to artists. It will always be between 0 and 1.
    
    For now this has no visual impact because we're not using it for anything.

5. Add functions to compute $D$, $G$, and $F$, which use $\vec n$ the normal vector, $\vec h$ the halfway vector, $\vec l$ the direction to the light and $\vec v$ the direction to the eye:
    
    $$\begin{align}
    D &= \dfrac{\alpha^2}{\big((\vec n \cdot \vec h)^2(\alpha^2-1) + 1\big)^2\pi} \\
    k &= \dfrac{(\sqrt{\alpha}+1)^2}{8}\\
    G_1(\vec x) &= \frac{\vec n \cdot \vec x}{(\vec n \cdot vec v)(1 - k) + k}\\
    G &= G_1(\vec l) G_1(\vec v)\\
    c &= \vec v \cdot \vec h\\
    F &= F_0 + (1-F_0)2^{(-5.55473c - 6.98316)c}
    \end{align}$$



