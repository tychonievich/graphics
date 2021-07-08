---
title: Color
...

Light is delivered in photons, each of which has a wavelength. Visible light wavelengths are roughly from 380nm to 750nm.

Your eye has 4 types of color receptors:
rods, L-cones, M-cones, and S-cones.^[Some women also have a fourth type of cone, but I have not yet seen studies showing women who have learned to articulate the extra color perception this gives them.]
All four operate on the same principle:

- When a photon hits the receptor, it has some chance of signaling the brain that it saw light.
- That chance is dependent on the wavelength of the light, with a roughly bell-shaped probability curve.
- After signaling, the receptor needs a short reset time before it can signal again. This varies, but something under 0.1 seconds is a reasonable estimate.
- Light intensity is perceived based on frequency of signaling.

Rods react to most of the visible spectrum and react very easily, so except in very dim-light situations they effectively signal as soon as their reset time elapses, providing no useful information to the brain. They're important for night vision, but not for color.

The simplest way to model color would thus be as three durations: the average time between two firings of an L-cone, of an M-cone, and of an S-cone. Thus, we might say the cone response is (0.1s, 2.4s, 0.4s) to mean the L-cone is firing almost immediately after reset, the M-cone is almost idle, and the S-cone is somewhere in between.

Seconds are awkward in this context in part because they are unbounded, approaching infinity in complete darkness; and because the difference in light intensity needed to go from 0.11 to 0.10 is much much larger than the difference needed to go from 11 to 10. But it's smooth and monotonic so three is some normalizing function that would convert these seconds into a some kind of nicely-behaved range where 0 means "never firing" and 1 means "firing as often as possible". We'll skip the math and assume we have access to that normalized cone signaling numbers.

Normalized cone signaling would form a cube, from (0,0,0) to (1,1,1).
But we don't perceive a cube of color.
There are various ways that (0.1, 0.2, 0.3) can change into (0.2, 0.4, 0.6) with no change in the outside world, including pupil dilation, clouds moving away from the sun, etc. We can perceive this overall intensity of light or "luminosity", but we our brain filters out overall luminosity and perceives only relative luminance^[Several related terms are technically distinct but sometimes used interchangeably in computer graphics:<br/>Luminosity = Joules of light per second.<br/>Luminance = Joules of light per second per unit area.<br/>Brightness = perception of luminance, generally relative to it surroundings.<br/>Lightness = perception of "how light it is", a non-linear scale as the eye is better at distinguishing between dark shades than light shades.<br/>Value = "distance from black"; if a white light and a red light have the same value, they are emitting equivalent numbers of long-wavelength photons, but the white light is also emitting short-wavelength photons and thus has higher luminosity.] of adjacent colors. So a better model of color is as 2D color vector $(l,m,s)$ where $l+m+s = 1$, coupled with a separate luminance level in the form of a scalar being multiplied by the whole vector.

Ignoring the luminance component for the time being, our color space is now a triangle:

<figure>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="-2 -2 204 177.20508075688772" style="max-width:24em">
<path d="M 200,173.20508075688772 100,0 0,173.20508075688772 Z" stroke-width="4" stroke="black" stroke-linejoin="round" fill="black"/>
<text x="195" y="173.20508075688772" fill="#ff8080" text-anchor="middle" font-family="arial" font-size="10px">L</text>
<text x="100" y="10" fill="#00ff00" text-anchor="middle" font-family="arial" font-size="10px">M</text>
<text x="5" y="173.20508075688772" fill="#8080ff" text-anchor="middle" font-family="arial" font-size="10px">S</text>
</svg>
<figcaption>Cone-based color triangle.</figcaption>
</figure>

In order for us to display the color represented by some point in this triangle, we have to find a combination of light of various wavelengths that triggers that ratio of response in the three cone types. The first step toward that goal is to find where each individual wavelength falls in this triangle.
Fortunately, others have done this work for us and published the results;
using the table from Stockman et al (1993)^[Andrew Stockman, Donald MacLeod, Nancy Johnson (1993) "Spectral sensitivity of the human cones." *Journal of the Optical Society of America A*, 10(12) pp. 2491--2521] we get

![Single-wavelength lights every 5nm from 390nm (on left) to 730nm (on right).](color-area.svg){style="max-width:24em"}

By combining multiple wavelengths we can get any point inside that curve. Points outside the curve represent cone responses that cannot be triggered by any combination of light.^[Presumably pharmaceuticals or surgery could cause the optic nerve to signal impossible ratios like (0,1,0). While I am unaware of studies that have attempted that, I postulate that the result would be painful rather than interesting, similar to the experience of other abnormal sensations like having your pupils artificially dialed so all cones are firing very quickly or the pins-and-needles feeling of having some pressure neurons firing at maximum levels while adjacent ones are not firing at all.]
In other words, only a subset of theoretical cone responses actually represent colors. 

It is worth noting that not every eye is the same. The exact ratios of pigments inside the cones vary by individual, meaning the exact same wavelengths of light might cause a response of (0.1, 0.4, 0.5) in one individual and (0.1, 0.45, 0.45) in another. The variations are typically fairly small, and when larger are called "color blindness" (a term that also refers to more extreme variations such as having only two types of working cones).

So, we want to make a display that can show a lot of colors. But creating arbitrary sets of wavelengths is quite expensive, so we want to pick just a few wavelengths that we can combine to make most colors. Because the curve is roughly triangular, picking three is a common choice. But getting a *single* wavelength is much harder than a narrow band of wavelengths and some wavelengths the eye hardly perceives at all so it would take too much energy to use them effectively in a display.

![Relative responsiveness of the S (blue), M (green), and R (red) cones to wavelengths from 390nm (on left) to 730nm (on right).](color-response.svg){style="max-width:24em"}

As a result, early color displays played with several different colors of light, but by 1993 had mostly settled on ITU-R Recommendation 709 which used colors made of several wavelengths, which can be plotted on our cone triangle as follows.

![Rec.709 color triangle and relative eye responsiveness to various pure wavelengths. The triangle shows all colors (luminance aside) that are representable  three dots are the Red, Green, and Blue primary color used by most RGB displays (as of 2021). The triangle does not extend to the L corner because it requires a lot of energy to get those wavelengths bright because none of the cones are very responsive there. It does not touch the curve anywhere because single-wavelength light sources are challenging to manufacture.](color-curve.svg){style="max-width:24em"}

You'll notice that there is space in the above image that is inside the visible-color curve but outside the colored-in triangle. Those colors exist in the real world, but cannot be replicated on this screen. Later ITU-R recommendations (Rec.2020 published in 2012 and Rec.2100 published in 2016) suggest single-wavelength lights to get a larger region, but while that makes the triangle bigger it still leaves out some colors. Most of the monitors I checked in 2021 still used Rec.709 colors instead, which is why I rendered the Rec.709 triangle above.

Note that some colors can be represented on a monitor but are not shown in the diagram because they differ from the diagrams colors only in luminance.
For example, yellow, is a higher-luminance version of the point halfway between the green and red corners
and forest green is a lower-luminance version of a point near the green corner of the triangle.

<!--






Color is more complicated than you think it is, and much of that complication will matter in computer graphics.

# Overview

- Perceptual light is comprised of many photons, each with a single wavelength.
- Three types of cones dominate our color vision. Rods are ineffective except in very dim situations.
- Each cone responds to photons with a range of wavelengths
    - The L cones respond to the longest wavelengths: roughly 470–655nm
    - The M cones respond to the medium wavelengths: roughly 455–620nm
    - The S cones respond to the shortest wavelengths: roughly 405–500nm
- Perceptually, color is split between chromaticity and luminosity
    - Luminosity is perceived overall brightness
        - This is relative to other nearby illumination
        - Some wavelengths look brighter than others: 560nm (yellowish-green) is the brightest-looking
        - The eye is better at distinguishing shades of darker luminosity than brighter luminosity
    - Chromaticity is perceived color
        - Chromaticity is defined by relative responsiveness of L, M, and S cones,
            which can be represented by a normalized vector like $\frac{(L,M,S)}{L+M+S}$
        - The set of all normalized 3-vectors makes up a triangle.
        - Because of responsiveness overlap, no light can cause the M cone to respond without also having L and/or S response. Thus, normalized vectors like $(0,1,0)$ cannot be created by any visual phenomenon.
        - Plotting all pure-wavelength light within the triangle shows a curved line, something like a lopsided horseshoe. Any point inside that horseshoe can be created by some combination of light, and except at the edges by many different combinations of light.
        - The perceived importance of color is not linear, so the most popular chromaticity diagrams (like CIE 1931s's $xy$ diagram) incorporate a nonlinear scaling factor
- Light-emitting displays (including most current screens) present a subset of chromaticities by mixing three colors of light
    - Single-wavelength lights are impractical to engineer at display scales, so the primary colors emit a narrow band of wavelengths instead, meaning their chromaticities are in the interior of the chromaticity diagram, not on its edges
    - The eye is not very sensitive to the most-blue and most-red visible wavelengths, so using them is energy-inefficient
    - The chromaticity diagram has a curved boundary, while three primary colors gives a triangle inside it. No finite number of primary colors can represent every chromaticity.
    - We generally call the light-emissive primary colors Red, Green, and Blue or RGB. Red mostly stimulates L cones, Blue mostly stimulates S cones, and Green is a compromise point in the curved region of the diagram stimulating M strongly, L less strongly, and S only a little.
- Light-absorbing displays (primarily color printers) present a subset of chromaticities by combining pigments that absorb different subsets of light.
    - The most popular pigments are
        - Cyan (C), which absorbs most wavelengths that primarily trigger the L cone 
        - Magenta (M), which absorbs most wavelengths that primarily trigger the M cone 
        - Yellow (Y), which absorbs most wavelengths that primarily trigger the S cone 
        - Black (K), which absorbs all of the visible spectrum
    - To be able to present bright colors, the absorbtion profiles should have minimal overlap. But because pigments do not have crisp wavelength boundaries, that means some wavelengths aren't fully absorbed even if CMY are applied at full strength. This is one reason that black is included (another reason is cost, as black is inexpensive to produce and popular in practice).
    - Because black absorbs some light that the other primaries don't, it can be thought of as a fourth print primary color that expands the set of representable chromaticities. However, it can only be used for that purpose if the color is not bright, and its contributions are relatively small.
    - $\displaystyle\begin{array}{l}R \approx 1-C-K\\G \approx 1-M-K\\B \approx 1-Y-K\end{array}$<br/> but these simulated RGB primaries each cover a much wider set of wavelengths than those used in light-emitting displays so the resulting representable chromaticities are a smaller subset of those possible in nature.
    - Using more pigments both allows a better approximation of the curved chromaticity diagram and allows narrower wavelength specificity, moving the covered region close to the edges of the diagram.
- Digital storage of color  ...
    - ...
- Digital presentation of color for artists  ...
    - ...

# Physics

Each photon has a wavelength and energy, which are different ways of measuring the same thing: high energy = short wavelength. Visible light has wavelengths between 380nm and 750nm.

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

![Graph of reactivity of three cones (from [wikimedia](https://commons.wikimedia.org/wiki/File:Cones_SMJ2_E.svg))](https://upload.wikimedia.org/wikipedia/commons/1/1e/Cones_SMJ2_E.svg)

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

![Single-wavelength lights within normalized cone response color triangle.^[Plotted based on data from Andrew Stockman, Donald MacLeod, Nancy Johnson (1993) "Spectral sensitivity of the human cones." *Journal of the Optical Society of America A*, 10(12) pp. 2491--2521]](color-curve.svg){style="max-width:24em"}

The two extremes of this curve are worth note.

At the long-wavelength extreme, even the L cone is not very receptive; so while the eye can distinguish between 700nm from 730nm, it requires a very strong red-only light source with virtually no ambient photons of other wavelengths to achieve that color perception. That lighting condition happens so rarely in nature that most people have no experience distinguishing "very red" from simply "red".

At the short-wavelength extreme, the curve hooks back toward red. Wavelengths shorter than about 430nm look similar to a mix of the 430nm "most blue" light and a little red light.
The size and strength of that hook varies by person, and can cause some people to see a hint of violet beyond the blue end of a rainbow.
Everyone can perceive that same violet if exposed to mix of a lot of blue and a little red light.

# Perceived Chromaticity

Our brain is far more sensitive to some colors than others. If you ask someone "which are more similar: this pair of colors or that pair of colors" their answers will not generally correlated to wavelength, number of distinct wavelengths needed, or any other simple function of light or cones.
The *Commission Internationale de l'éclairage* (CIE, known in English as the International Commission on Illumination) has performed human studies like this several times, starting in the 1920s, to produce various "chromaticity color spaces" by warping the light-possible part of the triangle so that distances in the color space are roughly equivalent to perceived differences of color.
The best known of these are CIE-1931 and CIELUV.

![A false-color picture of CIE-1931 (from [wikimedia](https://commons.wikimedia.org/wiki/File:CIE-1931_diagram_in_LAB_space.svg))](https://upload.wikimedia.org/wikipedia/commons/5/5f/CIE-1931_diagram_in_LAB_space.svg){style="max-width:30em"}

![A false-color picture of CIELUV (from [wikimedia](https://commons.wikimedia.org/wiki/File:CIE_1976_UCS.png))](https://upload.wikimedia.org/wikipedia/commons/8/83/CIE_1976_UCS.png){style="max-width:30em"}

Note that the above images have colors, but the colors used are *not* the colors represented by the corresponding regions of the chromaticity diagram.
You are viewing them on a screen or in print, neither of which are capable of representing all chromaticities.

Both diagrams have two axes;
$x$ and $y$ for CIE-1931 and $u'$ and $v'$ for CIELUV.
When it is important to model colors based on perceptual distance between them, computer graphics commonly works in one of these coordinate systems, with a third axis for *luminance*, the perceived brightness of a color.

Note that luminance is not simply the photonic energy of light nor the sum of cone responsiveness.
We perceive green light as being much brighter than red light, and red light as being much brighter than blue light.

:::aside
**CIE 1931**

Despite many issues having been identified and alternate chromaticity spaces being proposed since its creation, CIE 1931 remains the dominate way to defined chromaticity today. It can be derived from LMS responsiveness via the intermediate values XYZ (note: case maters, X and x are distinct).

XYZ values were part of the CIE-1931 specification and predate our current understanding of cone responsiveness, but a conversion between XYZ and cone responsiveness was published as the Hunt-Pointer-Estevez matrix in 1980^[Schanda, Jnos, ed. (2007). *Colorimetry*. p. 305. [doi:10.1002/9780470175637](https://doi.org/10.1002%2F9780470175637).]:
$$
\begin{bmatrix}X\\Y\\Z\end{bmatrix} =
\begin{bmatrix}1.9102&-1.11212&0.20191\\0.37095&0.62905&0\\0&0&1\end{bmatrix}
\begin{bmatrix}L\\M\\S\end{bmatrix}
$$

Given XYZ values, the defining formulae for CIE xy are
$$x = \frac{X}{X+Y+Z}$$
$$y = \frac{Y}{X+Y+Z}$$

Combing the matrix with the defining formulae we have
$$x = \frac{1.9102 L - 1.11212 M + 0.20191 S}{-0.48307 M + 1.20191 S + 2.28115 L}$$
$$y = \frac{0.37095 L + 0.62905 M}{-0.48307 M + 1.20191 S + 2.28115 L}$$
:::


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

![HDTV and UHDTV RGB coordinates in CIE-1931 (from [wikimedia](https://commons.wikimedia.org/wiki/File:CIExy1931_Rec_2020_and_Rec_709.svg))](https://upload.wikimedia.org/wikipedia/commons/2/27/CIExy1931_Rec_2020_and_Rec_709.svg){style="max-width:30em"}

Whatever the precise colors used, the hardware model for this is called RGB: the amount of illumination to be emitted by red, green, and blue emitters.

Display hardware needs to be given raw RGB data, but it is not space-efficient to store color data as raw RGB.
The perceptual difference between 10% and 20% illumination is much greater than the perceptual difference between 80% and 90%, so it is desirable to use more of the bits to store lower levels of light than are used for higher levels of light.

Early approaches to provide more storage for dimmer colors involved building nonlinearity into the dominant physical display device of the day, the cathode ray tube or CRT.
Because these were analog systems, the available functions were limited; the one used was typically called "gamma" and characterized by the following function:
$$V_{\text{display}} = {V_{\text{storage}}}^{\gamma}$$
$$V_{\text{storage}} = {V_{\text{display}}}^{1 / \gamma}$$
where we assume $V$ are in a normalized 0 (no light) to 1 (maximum light) range.
Empirically, $\gamma = 2.2$ is considered a useful value, but it was not standardized and some monitors allowed the display gamma to be adjusted by a physical knob.

This simple power-based gamma was not good for very dark colors, so the sRGB standard that dominates RGB-based file formats today defines the following piecewise function instead^[These formulae are given in the standard document IEC 61966-2-1, but are not quite inverses of one another because $0.0405/12.92 \ne 0.0031308$. I do not know why this discrepancy exists.]:
$$V_{\text{display}} = \begin{cases}
V_{\text{storage}}/12.92 &\text{if }V_{\text{storage}} \le 0.04045 \\
\displaystyle \left(\frac{V_{\text{storage}}+0.055}{1.055}\right)^{2.4} &\text{if }V_{\text{storage}} > 0.04045
\end{cases}$$
$$V_{\text{storage}} = \begin{cases}
12.92 V_{\text{display}} &\text{if }V_{\text{display}} \le 0.0031308 \\
1.055{V_{\text{display}}}^{1/2.4}-0.055 &\text{if }V_{\text{display}} > 0.0031308
\end{cases}$$

Despite the fact that sRGB cannot be expressed as a simple gamma exponent, it is still common to call any nonlinear storage favoring darker values a "gamma correction".

# Synthesis: what color is `#e3b021`?

Consider the web color string `#e3b021`.

This is an sRGB color value in hexadecimal:
`0xe3` = 227/255 = 0.89020 of the available red light,
`0xb0` = 176/255 = 0.69020 of the available green light, and
`0x21` = 33/255 = 0.12941 of the available blue light.

But that's in storage space; undoing the "gamma correction" we have
0.76815 red, 0.4342 green, and 0.0152 blue light ratios.

Depending on the specific colored light sources those might produce various photon wavelengths, but assuming we have a correctly calibrated HDTV display

:::example
finish this
:::

All of which produces this color:
<span style="width:5em; height:5em; background: #e3b021; display: inline-block; vertical-align:middle;"></span>

# Pigment

![Multiple color models graphed in CIE-1931, including the SWOP CMYK standard for color printers (from [wikimedia](https://commons.wikimedia.org/wiki/File:CIE1931xy_gamut_comparison.svg))](https://upload.wikimedia.org/wikipedia/commons/1/1e/CIE1931xy_gamut_comparison.svg){style="max-width:30em"}


-->
