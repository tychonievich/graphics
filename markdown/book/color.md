---
title: Color
...


Color is more complicated than you think it is, and much of that complication will matter in computer graphics.


# Physics

Each photon has a wavelength and energy, which are inversely proportional. For most graphics purposes, it is sufficient to know that high energy = low wavelength. Visible light has wavelengths between 380nm and 750nm

Most sources of light include photons of many different wavelengths. The main exceptions are lasers, LEDs, and some types of florescence.


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

You have many more red and green cones than blue cones, and the percise ratios vary by person and by region of the retna. This distriction effects only the resolution of perception in different colors, not the perceived color itself.

Pupils will dilate or contract to try to keep the number of photons entering the eye within idea ranges: few enough photons that you can distinguish between light intensities, but enough photons that cones areproviding frequent information to the brain. This means that absolute intensity of illumination is not a perfect predictor of perceived brightness of color: rather, brightness is percieved relative to the overall scene.

The optic center of the brain further removes perception of intensity and, to some degree, color. A region appears to be darker if surrounded by brighter things and brighter if surrounded by darker things. Similarly, after some time wearing rose-colored glasses the world stops looking rose-colored and starts to look normal again. Both of these phenomenon are cognitive, but also both hard-wired into the brain.


# Modeling Perception

A straightforward way of modeling the perception of color is as a vector of 3 numbers, one for each cone type.
Simple numbers might be 1 ÷ (time between signals); given cones rest for about 1/12 of a second between signals that would give a range of 0–12Hz per cone.



