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
<svg viewBox="-2 -2 204 177.20508075688772">
<path d="M 0,0 100,173.20508075688772 200,0 Z" stroke-width="4" stroke="black" stroke-linejoin="round"/>
<line stroke-width="2" stroke="#5a5a5a" x1="154.14443604350782" y1="25.650252845401383" x2="153.34396324828137" y2="26.371349323575462" stroke-linecap="round"/>
<line stroke-width="2" stroke="#757575" x1="153.34396324828137" y1="26.371349323575462" x2="153.31831129392106" y2="26.140866513838755" stroke-linecap="round"/>
<line stroke-width="2" stroke="#9f9f9f" x1="153.31831129392106" y1="26.140866513838755" x2="153.5635847315145" y2="26.381745639793003" stroke-linecap="round"/>
<line stroke-width="2" stroke="#c9c9c9" x1="153.5635847315145" y1="26.381745639793003" x2="153.51707692154844" y2="26.781342115295168" stroke-linecap="round"/>
<line stroke-width="2" stroke="#f3f3f3" x1="153.51707692154844" y1="26.781342115295168" x2="155.3608131010375" y2="26.215435946355424" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="155.3608131010375" y1="26.215435946355424" x2="155.59364853952871" y2="26.908451006619" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="155.59364853952871" y1="26.908451006619" x2="156.6665728625659" y2="27.16146625792559" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="156.6665728625659" y1="27.16146625792559" x2="156.2698691812602" y2="28.306284248935608" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="156.2698691812602" y1="28.306284248935608" x2="155.47156163515643" y2="29.543538328979214" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="155.47156163515643" y1="29.543538328979214" x2="153.91760251532853" y2="31.149869190008886" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="153.91760251532853" y1="31.149869190008886" x2="152.6605572470301" y2="32.40933820570891" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="152.6605572470301" y1="32.40933820570891" x2="149.6898694127525" y2="34.80346578610497" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="149.6898694127525" y1="34.80346578610497" x2="145.65911450050672" y2="37.84687901348382" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="145.65911450050672" y1="37.84687901348382" x2="141.6980521141188" y2="40.77066519029226" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="141.6980521141188" y1="40.77066519029226" x2="135.37386200726286" y2="45.09704344465256" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="135.37386200726286" y1="45.09704344465256" x2="130.08957255643605" y2="48.52313576711739" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="130.08957255643605" y1="48.52313576711739" x2="122.82362726390626" y2="53.21554008037315" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="122.82362726390626" y1="53.21554008037315" x2="115.0186674231205" y2="58.130976343327085" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="115.0186674231205" y1="58.130976343327085" x2="107.6725328959745" y2="62.685923130171" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="107.6725328959745" y1="62.685923130171" x2="100.12331275828792" y2="67.1954100368279" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="100.12331275828792" y1="67.1954100368279" x2="92.98867043972787" y2="71.15076999468732" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="92.98867043972787" y1="71.15076999468732" x2="86.25574471229606" y2="74.72288683093966" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="86.25574471229606" y1="74.72288683093966" x2="80.27509338890506" y2="77.84965885195581" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="80.27509338890506" y1="77.84965885195581" x2="74.90849031738044" y2="80.42885353445095" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="74.90849031738044" y1="80.42885353445095" x2="70.17855511569992" y2="82.60176112302632" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="70.17855511569992" y1="82.60176112302632" x2="66.34425297004968" y2="84.23162843000651" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="66.34425297004968" y1="84.23162843000651" x2="63.13091675715597" y2="85.31135800028899" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="63.13091675715597" y1="85.31135800028899" x2="60.58303392251686" y2="85.90292882482967" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="60.58303392251686" y1="85.90292882482967" x2="58.56066689559034" y2="86.14968648962943" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="58.56066689559034" y1="86.14968648962943" x2="56.89734784432316" y2="86.1376353143158" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="56.89734784432316" y1="86.1376353143158" x2="55.44270503518306" y2="85.93787557919786" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="55.44270503518306" y1="85.93787557919786" x2="54.13333780403536" y2="85.50733245250557" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="54.13333780403536" y1="85.50733245250557" x2="52.89801830695768" y2="84.78602077960863" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="52.89801830695768" y1="84.78602077960863" x2="51.71488544814446" y2="83.84106513442524" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="51.71488544814446" y1="83.84106513442524" x2="50.51871178025865" y2="82.69261816559238" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="50.51871178025865" y1="82.69261816559238" x2="49.303061375717476" y2="81.3661609234507" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="49.303061375717476" y1="81.3661609234507" x2="47.96304823615571" y2="79.63843972793877" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="47.96304823615571" y1="79.63843972793877" x2="46.496801760011714" y2="77.56226410413043" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="46.496801760011714" y1="77.56226410413043" x2="45.05524098960621" y2="75.46160943946367" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="45.05524098960621" y1="75.46160943946367" x2="43.52287884970495" y2="73.13149488216527" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="43.52287884970495" y1="73.13149488216527" x2="41.77394016364061" y2="70.35708207087207" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="41.77394016364061" y1="70.35708207087207" x2="39.960891611899996" y2="67.42432118248728" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="39.960891611899996" y1="67.42432118248728" x2="38.15996469889689" y2="64.4762477858056" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="38.15996469889689" y1="64.4762477858056" x2="36.286542985613806" y2="61.368719980915316" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="36.286542985613806" y1="61.368719980915316" x2="34.35816325985357" y2="58.137354001731644" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="34.35816325985357" y1="58.137354001731644" x2="32.54627772715945" y2="55.086880449677324" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="32.54627772715945" y1="55.086880449677324" x2="30.86841289834176" y2="52.24998811115667" stroke-linecap="round"/>
<line stroke-width="2" stroke="#ffffff" x1="30.86841289834176" y1="52.24998811115667" x2="29.257676251657717" y2="49.51077167789227" stroke-linecap="round"/>
<line stroke-width="2" stroke="#e5e5e5" x1="29.257676251657717" y1="49.51077167789227" x2="27.71630250463546" y2="46.87654579368883" stroke-linecap="round"/>
<line stroke-width="2" stroke="#cdcdcd" x1="27.71630250463546" y1="46.87654579368883" x2="26.336836723811683" y2="44.51287513244963" stroke-linecap="round"/>
<line stroke-width="2" stroke="#b7b7b7" x1="26.336836723811683" y1="44.51287513244963" x2="25.19094854291849" y2="42.5436620782793" stroke-linecap="round"/>
<line stroke-width="2" stroke="#a2a2a2" x1="25.19094854291849" y1="42.5436620782793" x2="24.25181251700663" y2="40.9191786945716" stroke-linecap="round"/>
<line stroke-width="2" stroke="#8f8f8f" x1="24.25181251700663" y1="40.9191786945716" x2="23.506666008686373" y2="39.61684712380822" stroke-linecap="round"/>
<line stroke-width="2" stroke="#7e7e7e" x1="23.506666008686373" y1="39.61684712380822" x2="22.88568351050157" y2="38.518066297810954" stroke-linecap="round"/>
<line stroke-width="2" stroke="#6e6e6e" x1="22.88568351050157" y1="38.518066297810954" x2="22.375968447909933" y2="37.602472087677924" stroke-linecap="round"/>
<line stroke-width="2" stroke="#616161" x1="22.375968447909933" y1="37.602472087677924" x2="21.990639317645563" y2="36.895325126631334" stroke-linecap="round"/>
<line stroke-width="2" stroke="#565656" x1="21.990639317645563" y1="36.895325126631334" x2="21.73148474851851" y2="36.402076998767015" stroke-linecap="round"/>
<line stroke-width="2" stroke="#4c4c4c" x1="21.73148474851851" y1="36.402076998767015" x2="21.574627210652466" y2="36.08039377802475" stroke-linecap="round"/>
<line stroke-width="2" stroke="#444444" x1="21.574627210652466" y1="36.08039377802475" x2="21.4482990570896" y2="35.80231566358502" stroke-linecap="round"/>
<line stroke-width="2" stroke="#3d3d3d" x1="21.4482990570896" y1="35.80231566358502" x2="21.379789227618442" y2="35.61237595490764" stroke-linecap="round"/>
<line stroke-width="2" stroke="#373737" x1="21.379789227618442" y1="35.61237595490764" x2="21.406156804524574" y2="35.5672354258611" stroke-linecap="round"/>
<line stroke-width="2" stroke="#323232" x1="21.406156804524574" y1="35.5672354258611" x2="21.532186676816742" y2="35.67634987053586" stroke-linecap="round"/>
<line stroke-width="2" stroke="#2d2d2d" x1="21.532186676816742" y1="35.67634987053586" x2="21.679390009074222" y2="35.81425959653898" stroke-linecap="round"/>
<line stroke-width="2" stroke="#2a2a2a" x1="21.679390009074222" y1="35.81425959653898" x2="21.758380523005233" y2="35.842140621680485" stroke-linecap="round"/>
<line stroke-width="2" stroke="#272727" x1="21.758380523005233" y1="35.842140621680485" x2="21.82159985364461" y2="35.847662590741734" stroke-linecap="round"/>
<line stroke-width="2" stroke="#252525" x1="21.82159985364461" y1="35.847662590741734" x2="22.02879753792484" y2="36.07647700345857" stroke-linecap="round"/>
<line stroke-width="2" stroke="#232323" x1="22.02879753792484" y1="36.07647700345857" x2="22.232472148170174" y2="36.292404077753844" stroke-linecap="round"/>
<line stroke-width="2" stroke="#212121" x1="22.232472148170174" y1="36.292404077753844" x2="22.43478508120435" y2="36.49849745616402" stroke-linecap="round"/>
</svg>
<figcaption>Single-wavelength lights within normalized cone response color triangle.</figcaption>
</figure>

