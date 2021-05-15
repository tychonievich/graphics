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

You have many more red and green cones than blue cones, and the precise ratios vary by person and by region of the retina. This distribution effects only the resolution of perception in different colors, not the perceived color itself.

Pupils will dilate or contract to try to keep the number of photons entering the eye within optimal ranges: few enough photons that you can distinguish between light intensities, but enough photons that cones are providing frequent information to the brain. This means that absolute intensity of illumination is not a perfect predictor of perceived brightness of color: rather, brightness is perceived relative to the overall scene.

The optic center of the brain further removes perception of intensity and, to some degree, color. A region appears to be darker if surrounded by brighter things and brighter if surrounded by darker things. Similarly, after some time wearing rose-colored glasses the world stops looking rose-colored and starts to look normal again. Both of these phenomenon are cognitive, not physiological, but also both hard-wired into the brain.


# Modeling Perception

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
Plotting single-wavelength light within this triangle shows a curved-boundary subregion; and at the extreme edges the cones are so dimly responsive that only very intense single-wavelength light courses can ever cause them to be perceived.

<svg viewBox="0 0 200 174">
<path d="M 200,0 100,173.20508075688772 200,0 Z" fill="black"/>
<circle r="2" fill="#0f0f0f" cx="195.67678953726664" cy="7.488020173267583"/>
<circle r="2" fill="#151515" cx="195.58274256158222" cy="7.650914313451111"/>
<circle r="2" fill="#1e1e1e" cx="195.66448157160127" cy="7.509338195137789"/>
<circle r="2" fill="#313131" cx="195.58885269277772" cy="7.640331255779599"/>
<circle r="2" fill="#4c4c4c" cx="195.44126324490054" cy="7.895963678163971"/>
<circle r="2" fill="#707070" cx="195.72804384775455" cy="7.399245103395551"/>
<circle r="2" fill="#9e9e9e" cx="195.4918944997602" cy="7.808267772296031"/>
<circle r="2" fill="#cacaca" cx="195.45128580516408" cy="7.878604094565553"/>
<circle r="2" fill="#eaeaea" cx="195.00735552072152" cy="8.647513902238638"/>
<circle r="2" fill="#ffffff" cx="194.4785378658946" cy="9.563452948338265"/>
<circle r="2" fill="#ffffff" cx="193.70776330488286" cy="10.898473649192164"/>
<circle r="2" fill="#ffffff" cx="193.05396122025823" cy="12.030892077856445"/>
<circle r="2" fill="#ffffff" cx="191.6419610086573" cy="14.47654818464735"/>
<circle r="2" fill="#ffffff" cx="189.56020158562154" cy="18.082261274480537"/>
<circle r="2" fill="#ffffff" cx="187.25248669112614" cy="22.07934072112996"/>
<circle r="2" fill="#f3f3f3" cx="183.2151521346906" cy="29.072209300029876"/>
<circle r="2" fill="#f2f2f2" cx="179.50003917818884" cy="35.506973696548336"/>
<circle r="2" fill="#e1e1e1" cx="173.80790210663818" cy="45.36604430812036"/>
<circle r="2" fill="#cecece" cx="167.31454600779722" cy="56.61286698295019"/>
<circle r="2" fill="#c3c3c3" cx="161.19014028913017" cy="67.22064885384687"/>
<circle r="2" fill="#c5c5c5" cx="155.4460000782297" cy="77.16979154492591"/>
<circle r="2" fill="#d5d5d5" cx="151.05787568646252" cy="84.77024594139891"/>
<circle r="2" fill="#efefef" cx="147.8967351699376" cy="90.24550192588464"/>
<circle r="2" fill="#ffffff" cx="145.84186243573356" cy="93.80464590461402"/>
<circle r="2" fill="#ffffff" cx="144.79080848542964" cy="95.62512474803638"/>
<circle r="2" fill="#ffffff" cx="144.3539076237281" cy="96.38185923837415"/>
<circle r="2" fill="#ffffff" cx="144.36266223079588" cy="96.36669581413241"/>
<circle r="2" fill="#ffffff" cx="144.77839702108693" cy="95.64662203487433"/>
<circle r="2" fill="#ffffff" cx="145.42207416387362" cy="94.53174051989703"/>
<circle r="2" fill="#ffffff" cx="146.16803318282467" cy="93.23970159870957"/>
<circle r="2" fill="#ffffff" cx="146.99015831991485" cy="91.81573909108974"/>
<circle r="2" fill="#ffffff" cx="147.8847589590989" cy="90.2662453315395"/>
<circle r="2" fill="#ffffff" cx="148.9155331275085" cy="88.48089210072447"/>
<circle r="2" fill="#ffffff" cx="150.1670329791687" cy="86.3132307719841"/>
<circle r="2" fill="#ffffff" cx="151.58689673339228" cy="83.85395460984334"/>
<circle r="2" fill="#ffffff" cx="153.18609515595847" cy="81.08406169057473"/>
<circle r="2" fill="#ffffff" cx="154.94119383929743" cy="78.04414159873436"/>
<circle r="2" fill="#ffffff" cx="157.09284228930494" cy="74.31737716329455"/>
<circle r="2" fill="#ffffff" cx="159.5802224172991" cy="70.00910840387156"/>
<circle r="2" fill="#ffffff" cx="162.03630540243034" cy="65.75504788601877"/>
<circle r="2" fill="#ffffff" cx="164.6751045536685" cy="61.18451368510467"/>
<circle r="2" fill="#ffffff" cx="167.69776508278045" cy="55.94911207464969"/>
<circle r="2" fill="#ffffff" cx="170.7610082892607" cy="50.64341920508567"/>
<circle r="2" fill="#ffffff" cx="173.69610296020568" cy="45.55968610998445"/>
<circle r="2" fill="#fbfbfb" cx="176.62089359993996" cy="40.49380012046272"/>
<circle r="2" fill="#dbdbdb" cx="179.47005162407618" cy="35.55891366386622"/>
<circle r="2" fill="#bcbcbc" cx="181.97523261780356" cy="31.219812900574453"/>
<circle r="2" fill="#a0a0a0" cx="184.14036115499144" cy="27.469700269247834"/>
<circle r="2" fill="#868686" cx="186.07852935513114" cy="24.112694472991564"/>
<circle r="2" fill="#6e6e6e" cx="187.80182682798866" cy="21.127855693447252"/>
<circle r="2" fill="#5a5a5a" cx="189.2324972768024" cy="18.64986178721449"/>
<circle r="2" fill="#494949" cx="190.3421023851817" cy="16.727969363163506"/>
<circle r="2" fill="#3b3b3b" cx="191.20175936459796" cy="15.23899979773346"/>
<circle r="2" fill="#2f2f2f" cx="191.8549255990316" cy="14.10768269390589"/>
<circle r="2" fill="#262626" cx="192.38137112578846" cy="13.195852294145705"/>
<circle r="2" fill="#1f1f1f" cx="192.80296024982235" cy="12.465638511400579"/>
<circle r="2" fill="#1a1a1a" cx="193.11784398177426" cy="11.920243889182885"/>
<circle r="2" fill="#161616" cx="193.33162727919967" cy="11.549960356232464"/>
<circle r="2" fill="#131313" cx="193.46790011874933" cy="11.313928874440723"/>
<circle r="2" fill="#111111" cx="193.58363074058838" cy="11.113477557424053"/>
<circle r="2" fill="#101010" cx="193.66063936576342" cy="10.98009470599985"/>
<circle r="2" fill="#0f0f0f" cx="193.67568248470212" cy="10.954039259693673"/>
<circle r="2" fill="#0e0e0e" cx="193.62504911202123" cy="11.041738833735517"/>
<circle r="2" fill="#0d0d0d" cx="193.56157032425887" cy="11.151687319342837"/>
<circle r="2" fill="#0d0d0d" cx="193.54493755473666" cy="11.180496121225813"/>
<circle r="2" fill="#0d0d0d" cx="193.53801439287014" cy="11.192487389327773"/>
<circle r="2" fill="#0d0d0d" cx="193.43430035457598" cy="11.372125373111356"/>
<circle r="2" fill="#0d0d0d" cx="193.33477816885468" cy="11.544502855261007"/>
<circle r="2" fill="#0c0c0c" cx="193.23821964728614" cy="11.711747120521347"/>
</svg>
<figcaption>Single-wavelength lights within normalized cone response color triangle.</figcaption>
</figure>

