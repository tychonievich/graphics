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

<figure>
<svg viewBox="-2 -2 202 175.20508075688772">
<path d="M 0,0 100,173.20508075688772 200,0 Z"/>
<line stroke-width="2" stroke="#222222" x1="195.67669453447348" y1="7.488020173267583" x2="186.1707254861938" y2="7.650914313451111" stroke-linecap="round"/>
<line stroke-width="2" stroke="#2a2a2a" x1="186.1707254861938" y1="7.650914313451111" x2="186.16781845384153" y2="7.509338195137789" stroke-linecap="round"/>
<line stroke-width="2" stroke="#3e3e3e" x1="186.16781845384153" y1="7.509338195137789" x2="186.33161198071744" y2="7.640331255779599" stroke-linecap="round"/>
<line stroke-width="2" stroke="#595959" x1="186.33161198071744" y1="7.640331255779599" x2="186.26693002180528" y2="7.895963678163971" stroke-linecap="round"/>
<line stroke-width="2" stroke="#7d7d7d" x1="186.26693002180528" y1="7.895963678163971" x2="187.61176831591263" y2="7.399245103395551" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ababab" x1="187.61176831591263" y1="7.399245103395551" x2="187.7075138097319" y2="7.808267772296031" stroke-linecap="round"/>
<line stroke-width="2" stroke="#d7d7d7" x1="187.7075138097319" y1="7.808267772296031" x2="188.3796701965656" y2="7.878604094565553" stroke-linecap="round"/>
<line stroke-width="2" stroke="#f7f7f7" x1="188.3796701965656" y1="7.878604094565553" x2="187.99666756493934" y2="8.647513902238638" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="187.99666756493934" y1="8.647513902238638" x2="187.3173660490685" y2="9.563452948338265" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="187.3173660490685" y1="9.563452948338265" x2="186.02822613485642" y2="10.898473649192164" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="186.02822613485642" y1="10.898473649192164" x2="184.92439825130336" y2="12.030892077856445" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="184.92439825130336" y1="12.030892077856445" x2="182.19190486900035" y2="14.47654818464735" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="182.19190486900035" y1="14.47654818464735" x2="178.01976846589343" y2="18.082261274480537" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="178.01976846589343" y1="18.082261274480537" x2="173.3511849658829" y2="22.07934072112996" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="173.3511849658829" y1="22.07934072112996" x2="164.7799711789866" y2="29.072209300029876" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="164.7799711789866" y1="29.072209300029876" x2="156.57642835790665" y2="35.506973696548336" stroke-linecap="round"/>
<line stroke-width="2" stroke="#eeeeee" x1="156.57642835790665" y1="35.506973696548336" x2="143.87145331528927" y2="45.36604430812036" stroke-linecap="round"/>
<line stroke-width="2" stroke="#dbdbdb" x1="143.87145331528927" y1="45.36604430812036" x2="128.95402321842946" y2="56.61286698295019" stroke-linecap="round"/>
<line stroke-width="2" stroke="#d0d0d0" x1="128.95402321842946" y1="56.61286698295019" x2="114.50570943661052" y2="67.22064885384687" stroke-linecap="round"/>
<line stroke-width="2" stroke="#d2d2d2" x1="114.50570943661052" y1="67.22064885384687" x2="100.22341977395533" y2="77.16979154492591" stroke-linecap="round"/>
<line stroke-width="2" stroke="#e2e2e2" x1="100.22341977395533" y1="77.16979154492591" x2="88.01836819714967" y2="84.77024594139891" stroke-linecap="round"/>
<line stroke-width="2" stroke="#fcfcfc" x1="88.01836819714967" y1="84.77024594139891" x2="78.12252436130092" y2="90.24550192588464" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="78.12252436130092" y1="90.24550192588464" x2="70.8880518813883" y2="93.80464590461402" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="70.8880518813883" y1="93.80464590461402" x2="65.58785385951232" y2="95.62512474803638" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="65.58785385951232" y1="95.62512474803638" x2="61.832872306758276" y2="96.38185923837415" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="61.832872306758276" y1="96.38185923837415" x2="59.32793232379389" y2="96.36669581413241" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="59.32793232379389" y1="96.36669581413241" x2="57.41309051458663" y2="95.64662203487433" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="57.41309051458663" y1="95.64662203487433" x2="55.91713071399071" y2="94.53174051989703" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="55.91713071399071" y1="94.53174051989703" x2="54.678746137357" y2="93.23970159870957" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="54.678746137357" y1="93.23970159870957" x2="53.56012519521181" y2="91.81573909108974" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="53.56012519521181" y1="91.81573909108974" x2="52.47457209089298" y2="90.2662453315395" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="52.47457209089298" y1="90.2662453315395" x2="51.322489837611805" y2="88.48089210072447" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="51.322489837611805" y1="88.48089210072447" x2="49.99494155559433" y2="86.3132307719841" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="49.99494155559433" y1="86.3132307719841" x2="48.52623720797161" y2="83.85395460984334" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="48.52623720797161" y1="83.85395460984334" x2="46.89304645088957" y2="81.08406169057473" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="46.89304645088957" y1="81.08406169057473" x2="45.1140532849109" y2="78.04414159873436" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="45.1140532849109" y1="78.04414159873436" x2="42.94709326734163" y2="74.31737716329455" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="42.94709326734163" y1="74.31737716329455" x2="40.44946168468929" y2="70.00910840387156" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="40.44946168468929" y1="70.00910840387156" x2="37.98582037129614" y2="65.75504788601877" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="37.98582037129614" y1="65.75504788601877" x2="35.34164915197486" y2="61.18451368510467" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="35.34164915197486" y1="61.18451368510467" x2="32.31525346576447" y2="55.94911207464969" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="32.31525346576447" y1="55.94911207464969" x2="29.249295391342386" y2="50.64341920508567" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="29.249295391342386" y1="50.64341920508567" x2="26.31218695506197" y2="45.55968610998445" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="26.31218695506197" y1="45.55968610998445" x2="23.385918137554988" y2="40.49380012046272" stroke-linecap="round"/>
<line stroke-width="2" stroke="#e8e8e8" x1="23.385918137554988" y1="40.49380012046272" x2="20.535671298269015" y2="35.55891366386622" stroke-linecap="round"/>
<line stroke-width="2" stroke="#c9c9c9" x1="20.535671298269015" y1="35.55891366386622" x2="18.029670808634364" y2="31.219812900574453" stroke-linecap="round"/>
<line stroke-width="2" stroke="#adadad" x1="18.029670808634364" y1="31.219812900574453" x2="15.863931473354123" y2="27.469700269247834" stroke-linecap="round"/>
<line stroke-width="2" stroke="#929292" x1="15.863931473354123" y1="27.469700269247834" x2="13.925324675052776" y2="24.112694472991564" stroke-linecap="round"/>
<line stroke-width="2" stroke="#7b7b7b" x1="13.925324675052776" y1="24.112694472991564" x2="12.20171416274459" y2="21.127855693447252" stroke-linecap="round"/>
<line stroke-width="2" stroke="#676767" x1="12.20171416274459" y1="21.127855693447252" x2="10.770813614980085" y2="18.64986178721449" stroke-linecap="round"/>
<line stroke-width="2" stroke="#565656" x1="10.770813614980085" y1="18.64986178721449" x2="9.66105780043949" y2="16.727969363163506" stroke-linecap="round"/>
<line stroke-width="2" stroke="#484848" x1="9.66105780043949" y1="16.727969363163506" x2="8.801340379427476" y2="15.23899979773346" stroke-linecap="round"/>
<line stroke-width="2" stroke="#3c3c3c" x1="8.801340379427476" y1="15.23899979773346" x2="8.148202100689478" y2="14.10768269390589" stroke-linecap="round"/>
<line stroke-width="2" stroke="#333333" x1="8.148202100689478" y1="14.10768269390589" x2="7.621855932530574" y2="13.195852294145705" stroke-linecap="round"/>
<line stroke-width="2" stroke="#2c2c2c" x1="7.621855932530574" y1="13.195852294145705" x2="7.200428066103161" y2="12.465638511400579" stroke-linecap="round"/>
<line stroke-width="2" stroke="#262626" x1="7.200428066103161" y1="12.465638511400579" x2="6.8857572784932275" y2="11.920243889182885" stroke-linecap="round"/>
<line stroke-width="2" stroke="#232323" x1="6.8857572784932275" y1="11.920243889182885" x2="6.672228834775585" y2="11.549960356232464" stroke-linecap="round"/>
<line stroke-width="2" stroke="#202020" x1="6.672228834775585" y1="11.549960356232464" x2="6.536261696646917" y2="11.313928874440723" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1e1e1e" x1="6.536261696646917" y1="11.313928874440723" x2="6.420912014726125" y2="11.113477557424053" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1c1c1c" x1="6.420912014726125" y1="11.113477557424053" x2="6.3443895626596145" y2="10.98009470599985" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1b1b1b" x1="6.3443895626596145" y1="10.98009470599985" x2="6.330011858796187" y2="10.954039259693673" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1b1b1b" x1="6.330011858796187" y1="10.954039259693673" x2="6.381510933288389" y2="11.041738833735517" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1a1a1a" x1="6.381510933288389" y1="11.041738833735517" x2="6.445989469579491" y2="11.151687319342837" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1a1a1a" x1="6.445989469579491" y1="11.151687319342837" x2="6.463609774708708" y2="11.180496121225813" stroke-linecap="round"/>
<line stroke-width="2" stroke="#1a1a1a" x1="6.463609774708708" y1="11.180496121225813" x2="6.471531047787224" y2="11.192487389327773" stroke-linecap="round"/>
<line stroke-width="2" stroke="#191919" x1="6.471531047787224" y1="11.192487389327773" x2="6.576596747204064" y2="11.372125373111356" stroke-linecap="round"/>
<line stroke-width="2" stroke="#191919" x1="6.576596747204064" y1="11.372125373111356" x2="6.6776396295137115" y2="11.544502855261007" stroke-linecap="round"/>
<line stroke-width="2" stroke="#191919" x1="6.6776396295137115" y1="11.544502855261007" x2="6.775911943563094" y2="11.711747120521347" stroke-linecap="round"/>
</svg>
<figcaption>Single-wavelength lights within normalized cone response color triangle.</figcaption>
</figure>

