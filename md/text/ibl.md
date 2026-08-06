---
title: Image-based lighting
...

Image-based lighting (<abbr>IBL</abbr>) illuminates an object from every direction simultaneously,
taking the light from a panoramic image instead of from scene geometry.
It is not as accurate as [global illumination](gi.html),
but it is much faster and gives nicer-looking results than simple point light sources.

Implementing IBL requires several steps:

- [Obtain and parse an HDR environment map]
- [Preprocess the map for diffuse lighting]
- [Preprocess the map for specular lighting]
- [Apply the lighting]

# Obtain and parse an HDR environment map

There are two technical challenges in creating good image-based lighting images:
dynamic range
and environment mapping.

## Dynamic range

The <dfn>dynamic range</dfn> of an image is the ratio between the brightness of the brightest pixel it can represent
and the second-darkest pixel it can represent^[More generally, dynamic range is the ratio between the largest and smallest measurable values of some quantity. Because images almost universally use no light at all as their darkest pixel, the second-darkest indicates how much darkness can be measured.].

Almost all image formats are optimized for display technologies.
Light-emitting displays^[Print-based displays rarely exceed a contrast ratio of 50.] typically have contrast ratios^[Contrast ratio is roughly equivalent to dynamic range, but for a display instead of an image.]
between 500 and 5,000, and only achieve even those ranges under ideal viewing conditions (meaning being seen in a completely dark room).
Because of this, image formats are generally limited to 256 levels of light intensity
nonlinearly scaled to provide a dynamic range of about 3,300^[This dynamic range is what is provided by the sRGB gamma function on 8-bit encoded colors. The main exception to this is the rare but widely-supported 16-bit PNG, which has 65,536 levels of light intensity and a dynamic range of around 850,000].

In a common outdoor scene,
the sun is around $1.6×10^9 \frac{㏅}{m^2}$,
the sky is around $3×10^3 \frac{㏅}{m^2}$,
and dark-pigmented objects in shadow are at least 100× darker than that.
That's a dynamic range of over 500,000 just for the sky
and upwards of 50,000,000 overall,
which is *much* larger than any common image format can express.

There are three common solutions to this:

- Clip the sun out: store how bright everything else is and then add the sunlight back in as a separate (non-image-based) step. On a clear day outdoors this can work OK, but it fails to capture most lighting conditions correctly.
- Clip everything else out: store only the brightest parts of the environment. This works OK for rough objects, but makes reflections on smooth objects look wrong and fails to capture outdoor lighting.
- Use a special <dfn>high dynamic range (<abbr>HDR</abbr>)</dfn> image format.

As of 2026, there are two common HDR image formats^[There are also a handful of uncommon HDR image formats]:
OpenEXR (.exr) is a high-quality (but complicated) file format preferred in movie-quality rendering
and Radiance HDR (.hdr) is a much simpler (but uncompressed) file format preferred in lighter-weight applications.

Radiance HDR files are defined to allow for several variants, but I've only seen on variant in use.
These files consist of:

1. A header of ASCII text starting `#?RADIANCE\nFORMAT=32-bit_rle_rgbe` terminated by two newlines (`\n`, U+000A).

    There is also a `FORMAT=32-bit_rle_xyze` defined in the Radiance specification, but I've not seen it used.
    
    Radiance allows there to be additional newline-separated `key=value` pairs in addition to `FORMAT`, but I've not seen them used.

2. The dimensions of the image, expressed as something like `-Y 2048 +X 4096\n`, where
    - `-Y` means it starts with the top row (`+Y` would start with the bottom row)
    - `2048` means there are 2048 rows
    - `+X` means each row starts with the left pixel (`-X` would start with the right pixel)
    - `4096` means there are 4096 pixels per row

3. Binary data consisting of 4 bytes per pixel, in $(R,G,B,E)$ order.

    Treating those bytes as unsigned integers (0 through 255), 
    the meaning of the pixel is:
    
    - $(255, 255, 255, E)$ means $E$ additional copies of the previous color.
        
        I've never seen this used, and most HDR parsers I've looked at assume it will never happen.
    
    - $(R,G,B,0)$ means $(0,0,0)$ (black)
    
    - Any other $(R,G,B,E)$ means $(R,G,B) 2^{E-128-8}$
        
        The $-8$ above is intended to cheaply scale from 0--255 integers to 0--1 relative values,
        but actually divides by 256 instead of 255.
        
        If we instead treat the bytes as floats between 0 and 1,
        which is commonly how GPUs treat bytes,
        $(R,G,B,E)$ means $\frac{255}{256} (R,G,B) 2^{255 E - 128}$
        but the $\frac{255}{256}$ is close enough to $1$ that it can be ignored with only a 0.4% error.

## Environment mapping

The environment around an object is a light intensity and color for each direction.
While there are better ways of sampling such an environment from the perspective of graphics,
almost all environment map HDR images are provided in the [equirectangular projection](https://en.wikipedia.org/wiki/Equirectangular_projection).
This means

- They are twice as wide as they are tall

- Pixel coordinates correspond to spherical angles:
    $\theta = \frac{\pi}{2} - (y+0.5) \frac{\pi}{H}$ is the latitude
    and $\phi = \pi + (x+0.5) \frac{\pi}{H}$ is the longitude.

- Pixel solid angle is dependent on $y$ (but not $x$);
    in particular, it is $\frac{\pi^2}{H^2} \sin(\theta)$.

Texel lookup with an equirectangular projection requires use of trigonometry functions,
which are more expensive than we want to use;
that is one reason to preprocess the map before use in rendering.

# Preprocess the map for diffuse lighting

Diffuse lighting integrates incident illumination over half of all directions,
weighting each sample according to Lambert's law.

Because common environment maps have a small number of *very* bright pixels
that provide the majority of the illumination,
sampling the texture map to make a numerical approximation of the integral is tricky.
Generally, it is preferable to use every pixel.

The result of diffuse lighting is quite smooth, with no high-frequency information,
so it is effective to store the results using [spherical harmonics](sphericalharmonics.html).
Because spherical harmonics just have a few terms, each linearly independant from the others,
we can loop over each pixel in the map and add its contribution to each spherical harmonic
to get the final IBL diffuse lighting function.

To use this map, we evaluate the spherical harmonics at the surface normal;
the result is the total diffuse illumination received at that point.

The result is not 100% accurate.
Lambert's law is precisely accurate for perfectly smooth objects,
but slightly (almost imperceptibly) inaccurate for rough surfaces;
and spherical harmonics are approximate, not exact, representations of the correct diffuse lighting map.

# Preprocess the map for specular lighting

See [Specular lighting](specular.html)


# Apply the lighting
