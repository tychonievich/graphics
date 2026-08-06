---
title: Specular lighting
...

Specular lighting occurs when photons bounce off of the surface of a material without entering it.

Mathematically, bouncing is simple:
the reflection of the incident direction across the surface normal is $\hat d - 2(\hat d \cdot \hat n) \hat n$,
or `reflect(v, n)`{.wgsl} in WGSL.

However, we need to consider the substance the light is bouncing off of, which changes how much light bounces in this way.
The impact of material and incident angle on reflectivity
is described by the Fresnel equations[^fresnel]
which are computationally too expensive for most interactive graphics applications.
In 1994, Schlick[^schlick] published a polynomial approximation that is much more widely used.

We also need to consider two consequences of materials being rough:
the normal seen at the scale of a photon (sometimes called the "micronormal" or "microfacet normal")
might not be the same as the normal seen at the scale of object shape and model (sometimes called the "macronormal"),
and microscopic hills and valleys across the surface of an object cast some shadows on other parts of the material (called "self shadowing").

There have been a variety of roughness models proposed over the years,
but since about 2015 the GGX model has dominated.
GGX was introduced to graphics in 2007 by Walters, Marschner, Li, and Torrence as they studied ground glass[^walters],
though it had previously been published 1975 by physicists Towbridge and Reitz[^towbridge]
and the self-shadowing part had been published in 1967 as part of Smith's study of naval radar[^smith].
The self-shadowing is computationally expensive,
but in 2013 Karis[^karis] published a modification of Schlick[^schlick]'s polynomial approximation of a different roughness model that made it much more appealing for interactive graphics,
incorporating an adjusted roughness parameter that Burley[^burley] shared that Disney artists preferred over the $\alpha$ paramter in the original GGX formulation.


[^fresnel]:
    Augusin-Jean Fresnel. 1831. "Mémoire sur la loi de la modification que la réflexion imprime à la lumière polarisée". *Mémoires de l'Académie Royale des Sciences de l'Institut de France*, Tom. XI, 393–489.

[^smith]:
    Bruce G. Smith. 1967. "Geometrical Shadowing of a Random Rough Surface." In *IEEE Transactions on Antennas and Propagation*, AP-15(5), 668–671.

[^walters]:
    Bruce Walter, Stephen R. Marschner, Hongsong Li, and Kenneth E. Torrance. 2007. "Microfacet models for refraction through rough surfaces." In *Proceedings of the 18th Eurographics conference on Rendering Techniques* (EGSR'07). Eurographics Association, Goslar, DEU, 195–206.

[^towbridge]:
    T. S. Trowbridge and K. P. Reitz. 1975. "Average irregularity representation of a rough surface for ray reflection." In *Journal of the Optical Society of America* volume 65, 531–536.

[^karis]:
    Brian Karis. 2013. "Real Shading in Unreal Engine 4." *SIGGRAPH Course: Physically Based Shading in Theory and Practice*, Epic Games.

[^schlick]:
    Christophe Schlick. 1994. "A fast alternative to Phong's specular model." *Graphics gems IV*. Academic Press Professional, Inc., USA, 385–387.

[^burley]:
    Brent Burley. 2012. "Physically Based Shading at Disney." *SIGGRAPH Course: Practical Physically Based Shading in Film and Game Production*, Disney.


# Determine how much light is reflected

For metals, all light that is not absorbed is reflected:
we first apply object color to absorb some light,
then reflect everything else.

For dielectric materials, how much is reflected is dependent on the object's index of refraction and the incident angle:
we first apply Schlick's approximation of the Fresnel equations,
and only the light that is not reflected in that way proceeds into the material and interacts with the objects' underlying color.

````wgsl
/**
 * cosTheta = the cosine of the incident angle and the surface normal;
 *            if those are unit vectors, this is the dot product of them.
 *
 * f0       = the reflectivity when cosTheta = 1;
 *            this equals ((1 - ior) / (1 + ior))^2 where ior = the index of refraction.
 *            f0 is 0.04 for most common solids, 0.02 for water, and 0.2 for some gemstones
 */
fn fresnelSchlick(cosTheta: f32, f0: vec3<f32>) -> vec3<f32> {
    return f0 + (vec3<f32>(1.0) - f0) * pow(1.0 - cosTheta, 5.0);
}    
````

# Determine how much light is blocked by self-shadowing

Rough surfaces have tiny hills and valleys;
the taller these are and the shallower the incident angle light travels in,
the more likely it is that the reflected light will bump into a hill before it escapes the surface.
In practice, this darkens the visual rim of rough objects a small but noticeable amount,
inspiring its "self shadowing" name and making modeling it in our rendering important.

Karis's modification of Schlick's approximation of self-shadowing to match the GGX distribution
is widely used today.
Note that we need to run it twice: a photon could be shadowed either when entering or when exiting the surface.

````wgsl
// Approximate self-shadowing for a given (normal dot direction) and roughness
fn geometrySchlickGGX(NdD: f32, roughness: f32) -> f32 {
    let r = (roughness + 1.0);
    let k = (r * r) / 8.0; 
    return NdD / (NdD * (1.0 - k) + k);
}
// Combine shadowing of view direction and light direction
fn geometrySmith(NdV: f32, NdL: f32, roughness: f32) -> f32 {
    return geometrySchlickGGX(NdV, roughness) * geometrySchlickGGX(NdL, roughness);
}
````

# Determine in which direction light is reflected

On a perfect smooth material, specular reflections are computed by reflecting the incident direction across the surface normal:
$\hat d - 2(\hat d \cdot \hat n) \hat n$,
or `reflect(v, n)`{.wgsl} in WGSL.

But materials are rough, so the visual normal (the one the photon encounters)
and the geometric normal (the one we use when modeling objects)
are generally not the same.

GGX describes one distribution of visual normals,
resulting in two functions with different purposes.

If we know both entering and exiting directions,
we can compute how much light is specularly reflected between them:
$$
D(\hat h) = \frac{\text{roughness}^4}{\pi\big((\hat n \cdot \hat h)^2(\text{roughness}^4-1) + 1\big)^2}
$$
where $\hat n$ is the surface normal
and $\hat h$ is the halfway vector )(halfway between the entering and exiting directions).
Note that this equation has a divide-by-0 error if $\text{roughness} = 0$ and $\hat n \cdot \hat h = 1$,
but when $\text{roughness} = 0$ all light is directly reflected and GGX isn't needed.

If we know only one direction,
we can sample a distribution over the other
by sampling a distribution over microfacet normals
and reflecting the vector we know over that sampled direction.
This is done in several steps:
we create 2 random numbers between 0 and 1,
turn them into spherical coordinate $\theta$ and $\phi$,
modify $\theta$ based on the GGX distribution and surface roughness,
compute the normal-space perturbed normal,
and convert that into world space to get the actual normal.

```WGSL
/**
 * normal       - the surface normal (a unit vector)
 * roughness    - the roughness of the material (between 0 and 1)
 * randomVal    - a quasirandom value between (0,0) and (1,1)
 * return value - the surface normal modified by the roughness of the material
 */
fn sampleGGX(normal: vec3<f32>, roughness: f32, randomVal: vec2<f32>) -> vec3<f32> {
    const PI = 3.14159265359;
    let alpha = roughness * roughness;
    let alpha2 = alpha * alpha;

    // In spherical coordinates, theta is angle away from the normal, which depends on roughness
    let cosTheta = sqrt((1.0 - randomVal.y) / (1.0 + (alpha2 - 1.0) * randomVal.y));
    let sinTheta = sqrt(max(0.0, 1.0 - cosTheta * cosTheta));
    // phi is angle around the normal, which depends on trig functions
    let phi = 2.0 * PI * randomVal.x;
    
    // In local coordinates, Z aligns with normal; X and Y should be perpendicular to that but otherwise arbitrary because GGX is isotropic.
    let H_local = vec3<f32>(
        cos(phi) * sinTheta,
        sin(phi) * sinTheta,
        cosTheta
    );

    // Local to global requires orthogonal basis vectors, one of which is the normal
    let up = select(vec3<f32>(1.0, 0.0, 0.0), vec3<f32>(0.0, 0.0, 1.0), abs(normal.z) < 0.999);
    let tangent = normalize(cross(up, normal));
    let bitangent = cross(normal, tangent);
    return = normalize(tangent * H_local.x + bitangent * H_local.y + normal * H_local.z);
}
```

For creating the `randomVal`s, see the page on [quasi-random numbers](quasi.html).

# Putting it together

In direct lighting
we know the view direction and the light direction
and what to know how much light makes it to the viewer.
That is the product of how much light is reflected specularly,
how much is not self-shadowed,
and how much is reflected between those directions:
`fresnelSchlick` × `geometrySmith` × $D(\hat h)$.

In ray tracing (and other importance sampling techniques)
we use `sampleGGX` to sample a reflection ray direction
and `fresnelSchlick` × `geometrySmith` to compute how much the light found in the reflected direction should influence the final color.

With a precomputed specularity environment map,
we use the reflection of the viewer direction over the normal
to look up an entry in the map,
and we multiply the result by `fresnelSchlick`.
But self-shadowing is more complicated and more expensive to compute,
so it is generally precomputed and stored as a look-up texture
with $\hat n \cdot \hat v$ as one axis
and $\text{roughness}$ as the other.

