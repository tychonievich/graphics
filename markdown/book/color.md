---
title: Color
...


Color is more complicated than you think it is, and much of that complication will matter in computer graphics.


# Physics

Each photon has a wavelength and energy, which are inversely proportional such that high energy = long wavelength. Visible light has wavelengths between 380nm and 750nm

Most sources of light include photons of many different wavelengths. The main exceptions are lasers, light-emitting diodes, and some types of florescence and phosphorescence.


# Biology

Your eye has four^[A small percentage of females have five: rods and four types of cones. I am unaware of any study showing these women have learned to distinguish the extra colors those extra cones theoretically allow them to perceive.] types of light receptors: rods and three types of cones. All four operate on the same general principle:

- When a photon hits the receptor, it has some chance of signalling the brain that it saw light.
- That chance is dependant on the wavelength of the light, with a roughly bell-shaped probability curve.
- After signaling, the receptor needs a short reset time before it can signal again.
- Light intensity is percieved based on frequency of signalling.

The rods react to most visible spectrum wavelenghts and have high proability of signaling; in any well-lit scenario they are more-or-less all continuously signalling; only in very dim-light situations do they provide useful visual information to the brain.

| Energy | Wavelength | Color | Peak | Approximate Range |
|:------:|:----------:|:-----:|:----:|:-----:|
| High (H) | Short (S) | Blue | 445nm | 400–520nm |
| Medium (M) | Medium (M) | Green | 535nm | 420–640nm |
| Low (L) | Long (L) | Red | 575nm | 450–680nm |

![Graph of reactivity of three cones; see [wikimedia](https://commons.wikimedia.org/wiki/File:Cones_SMJ2_E.svg) for image provenance](https://upload.wikimedia.org/wikipedia/commons/1/1e/Cones_SMJ2_E.svg)

Because of the overlap of cone sensitivity regions, there is no wavelength or combination of wavelengths of light that will cause the medium-sensitivity "green" cone to signal the brain without one of the other two cone types also signaling the brain.

You have many more red and green cones than blue cones, and the precise ratios vary by person and by region of the retina. This distribution effects only the resolution of perception in different colors, not the perceived color itself.

Pupils will dilate or contract to try to keep the number of photons entering the eye within optimal ranges: few enough photons that you can distinguish between light intensities, but enough photons that cones are providing frequent information to the brain. This means that absolute intensity of illumination is not a perfect predictor of perceived brightness of color: rather, brightness is perceived relative to the overall scene.

The optic center of the brain further removes perception of intensity and, to some degree, color. A region appears to be darker if surrounded by brighter things and brighter if surrounded by darker things. Similarly, after some time wearing rose-colored glasses the world stops looking rose-colored and starts to look normal again. Both of these phenomenon are cognitive, not physiological, but also both hard-wired into the brain.


# Modeling Cones

A straightforward way of modeling the perception of color is with three numbers: the signaling rate (in Hertz) of each of the three cone types. Perhaps for one region each red cone is signaling six times a second, each green cone once every four seconds, and each blue cone twice a second, for a cone response vector of (6, ¼, 2). This can be seen as the color data that travels along the optic nerve from retina to brain.

<figure>
<svg viewBox="0 15 200 220" style="max-width:30em; display:table; margin:auto; font-size:10px; font-family:Arial;">
<circle cx="40" cy="160" r="2"/>
<line x1="40" y1="160" x2="40" y2="40" stroke="black"/>
<path d="m 40,40 -2,0 2,-6 2,6 Z"/>
<text x="40" y="26" text-anchor="middle" fill="green">M</text>
<g transform="translate(40,160) rotate(80) translate(-40,-160)">
<line x1="40" x2="40" y1="160" y2="40" stroke="black"/>
<path d="m 40,40 -2,0 2,-6 2,6 Z"/>
</g>
<text x="170" y="138" text-anchor="start" fill="darkred">L</text>
<g transform="translate(40,160) rotate(130) translate(-40,-160)">
<line x1="40" x2="40" y1="160" y2="80" stroke="black"/>
<path d="m 40,80 -2,0 2,-6 2,6 Z"/>
</g>
<text x="108" y="222" text-anchor="start" fill="blue">S</text>
<text x="36" y="163" text-anchor="end">0 Hz</text>
<line x1="30" y1="60" x2="38" y2="60" stroke="black"/>
<text x="28" y="63" text-anchor="end">12 Hz</text>
<line x1="142" y1="145" x2="142" y2="153" stroke="black"/>
<text x="142" y="163" text-anchor="middle">12 Hz</text>
<line x1="86" y1="202" x2="86" y2="210" stroke="black"/>
<text x="86" y="220" text-anchor="middle">12 Hz</text>
</svg>
<figcaption>Three cone response rates.</figcaption>
</figure>

The cone response vector is not particularly useful representation for computer graphics; indeed, I've never seen it used in any code. One problem is its nonlinear scale: doubling the number of photons brings the Hz twice as close to their maximum value and that maximum, while *roughly* 12 Hz, varies by person and is a bit different each time each cone it signals. So we want to apply some kind of nonlinear rescaling of the axes to bring them into more perceptually-useful units.

<figure>
<svg viewBox="0 15 240 210" style="max-width:33em; display:table; margin:auto; font-size:10px; font-family:Arial;">
<circle cx="40" cy="160" r="2"/>
<line x1="40" y1="160" x2="40" y2="40" stroke="black"/>
<path d="m 40,40 -2,0 2,-6 2,6 Z"/>
<text x="40" y="26" text-anchor="middle" fill="green">M</text>
<g transform="translate(40,160) rotate(80) translate(-40,-160)">
<line x1="40" x2="40" y1="160" y2="40" stroke="black"/>
<path d="m 40,40 -2,0 2,-6 2,6 Z"/>
</g>
<text x="170" y="138" text-anchor="start" fill="darkred">L</text>
<g transform="translate(40,160) rotate(130) translate(-40,-160)">
<line x1="40" x2="40" y1="160" y2="80" stroke="black"/>
<path d="m 40,80 -2,0 2,-6 2,6 Z"/>
</g>
<text x="108" y="222" text-anchor="start" fill="blue">S</text>
<text x="36" y="163" text-anchor="end">0</text>
<line x1="30" y1="60" x2="38" y2="60" stroke="black"/>
<text x="28" y="63" text-anchor="end">1</text>
<line x1="142" y1="145" x2="142" y2="153" stroke="black"/>
<text x="142" y="163" text-anchor="middle">1</text>
<line x1="86" y1="202" x2="86" y2="210" stroke="black"/>
<text x="86" y="220" text-anchor="middle">1</text>
<g stroke-dasharray="2 2" fill="none" stroke="black">
<path d="m 40,60 102,-15 0,97 46,41 -102,15 0,-97 102,-15 0,97 M 40,60 l 46,41 M 40,60 m 102,-15 46,41"/>
</g>
</svg>
<figcaption>Volume of possible normalized cone response rates.</figcaption>
</figure>

However, a normalized volume is still not ideal because both the pupil and the optic center normalize overall brightness. Effectively that means we perceive *relative* response rates far more than we perceive *absolute* response rates. Conceptually, this projects a point in the volume onto a brightness-normalized plane, where (1, 1, 0) and (⅓, ⅓, 0) look like the same color (unless they are next to one another, in which case one looks darker than the other).

<figure>
<svg viewBox="0 15 240 210" style="max-width:33em; display:table; margin:auto; font-size:10px; font-family:Arial;">
<circle cx="40" cy="160" r="2"/>
<line x1="40" y1="160" x2="40" y2="40" stroke="black"/>
<path d="m 40,40 -2,0 2,-6 2,6 Z"/>
<text x="40" y="26" text-anchor="middle" fill="green">M</text>
<g transform="translate(40,160) rotate(80) translate(-40,-160)">
<line x1="40" x2="40" y1="160" y2="40" stroke="black"/>
<path d="m 40,40 -2,0 2,-6 2,6 Z"/>
</g>
<text x="170" y="138" text-anchor="start" fill="darkred">L</text>
<g transform="translate(40,160) rotate(130) translate(-40,-160)">
<line x1="40" x2="40" y1="160" y2="80" stroke="black"/>
<path d="m 40,80 -2,0 2,-6 2,6 Z"/>
</g>
<text x="108" y="222" text-anchor="start" fill="blue">S</text>
<text x="36" y="163" text-anchor="end">0</text>
<line x1="30" y1="60" x2="38" y2="60" stroke="black"/>
<text x="28" y="63" text-anchor="end">1</text>
<line x1="142" y1="145" x2="142" y2="153" stroke="black"/>
<text x="142" y="163" text-anchor="middle">1</text>
<line x1="86" y1="202" x2="86" y2="210" stroke="black"/>
<text x="86" y="220" text-anchor="middle">1</text>
<g stroke-dasharray="2 2" fill="none" stroke="black">
<path d="m 40,60 102,-15 0,97 46,41 -102,15 0,-97 102,-15 0,97 M 40,60 l 46,41 M 40,60 m 102,-15 46,41"/>
</g>
<path d="m 40,60 102,82 -56,56 z" fill="rgba(0,0,0,0.25)"/>
</svg>
<figcaption>Conceptual plane of color perception within normalized cone response volume.</figcaption>
</figure>


Conceptually, this gives us a triangle of possible colors,
to which relative brightness can be added as a third axis.
However, cone responsiveness overlaps so not all of this triangle of colors is achievable in practice.
Plotting single-wavelength light within this triangle shows a curved-boundary subregion; all colors that can be perceived (without artificial stimulation of cones via some input other than light^[I have never encountered studies where cones are stimulated artificially via surgery or drugs, but know of no intrinsic reason why they could not be. In theory, this could cause a person to perceive colors that are literally impossible in the real world.]) lie within this subregion.

![Single-wavelength lights within normalized cone response color triangle.^[Plotted based on data from Andrew Stockman, Donald MacLeod, Nancy Johnson (1993) "Spectral sensitivity of the human cones." *Journal of the Optical Society of America A*, 10(12) pp. 2491--2521]](color-curve.svg)

The two extremes of this curve are worth note.

At the long-wavelength extreme, even the L cone is not very receptive; so while the eye can distinguish between 700nm from 730nm, it requires a very strong red-only light source with virtually no ambient photons of other wavelengths to achieve that color perception. That lighting condition happens so rarely in nature that most people have no experience distinguishing "very red" from simply "red".

At the short-wavelength extreme, the curve hooks back toward red. Wavelengths shorter than about 430nm look similar to a mix of the 430nm "most blue" light and a little red light.
The size and strength of that hook varies by person, and can cause some people to see a hint of violet beyond the blue end of a rainbow.
Everyone can perceive that same violet if exposed to mix of a lot of blue and a little red light.

# Perceived Chromaticity

Our brain is far more sensitive to some colors than others. If you ask someone "which are more similar: this pair of colors or that pair of colors" their answers will not generally correlated to wavelength, number of distinct wavelengths needed, or any other simple function of light or cones.
The *Commission Internationale de l'éclairage* (CIE, known in English as the International Commission on Illumination) has performed human studies like this several times, starting in the 1920s, to produce various "chromaticity color spaces" by warping the light-possible part of the triangle so that distances in the color space are roughly equivalent to perceived differences of color.
The best known of these are CIE-1931 and CIELUV.

![A false-color picture of CIE-1931 from [wikimedia](https://commons.wikimedia.org/wiki/File:CIE-1931_diagram_in_LAB_space.svg)](https://upload.wikimedia.org/wikipedia/commons/5/5f/CIE-1931_diagram_in_LAB_space.svg)

![A false-color picture of CIELUV from [wikimedia](https://commons.wikimedia.org/wiki/File:CIE_1976_UCS.png)](https://upload.wikimedia.org/wikipedia/commons/8/83/CIE_1976_UCS.png)

Note that the above images have colors, but the colors used are *not* the colors represented by the corresponding regions of the chromaticity diagram.
You are viewing them on a screen or in print, neither of which are capable of representing all chromaticities.

Both diagrams have two axes;
$x$ and $y$ for CIE-1931 and $u'$ and $v'$ for CIELUV.
When it is important to model colors based on perceptual distance between them, computer graphics commonly works in one of these coordinate systems, with a third axis for *luminance*, the perceived brightness of a color.

Note that luminance is not simply the photonic energy of light nor the sum of cone responsiveness.
We perceive green light as being much brighter than red light, and red light as being much brighter than blue light.

# Light-emissive display coordinates

Light-emissive color displays include television, computer monitor, phone screen and other displays that are visible even in the dark.
Although the details vary, all of them work via the same basic principle:
a densely-packed space of very small components that each emit a narrow band of wavelengths.
Because the chromaticity diagram is roughly triangular, almost all such displays pick three wavelengths to emit.

Picking the exact wavelengths to emit is not as trivial as it may seem.

- Creating materials and assemblages that emit a desired narrow band of photons is challenging, and the more narrow the wavelength band the more challenging the engineering.
- There's an energy/quality trade-off: wavelengths that trigger the L cones much more strongly than the M cones require 10 to 100 times more power to produce than other colors because the L cones are not very sensitive in those wavelengths.

ITU-R Recommendation BT.2020 defines the light emitters for a UHDTV to be single-wavelength emitters of 467nm (blue), 532nm (green), and 630nm (red).
To the best of my knowledge, no current commodity hardware is capable of producing these wavelengths precisely.
The earlier ITU-R Recommendation BT.709 defines the light emitters for an HDTV to be wavelength-band emitters that can be achieved in various ways, such as with color filters over a white backlight or color LEDs which often have a 20nm spread in their emitted spectra.

![HDTV and UHDTV RGB coordinates in CIE-1931 (from [wikimedia](https://commons.wikimedia.org/wiki/File:CIExy1931_Rec_2020_and_Rec_709.svg)](https://upload.wikimedia.org/wikipedia/commons/2/27/CIExy1931_Rec_2020_and_Rec_709.svg)

Whatever the precise colors used, the hardware model for this is called RGB: the amount of illumination to be emitted by red, green, and blue emitters.

:::note
add gamma
:::


# Pigment

![Multiple color models graphed in CIE-1931, including the SWOP CMYK standard for color printers (from [wikimedia](https://commons.wikimedia.org/wiki/File:CIE1931xy_gamut_comparison.svg)](https://upload.wikimedia.org/wikipedia/commons/1/1e/CIE1931xy_gamut_comparison.svg)
