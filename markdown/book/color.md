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
<svg viewBox="0 0 200 174">
<path d="M 0,0 100,173.20508075688772 200,0 Z"/>
<circle r="2" fill="#5e5e5e" cx="163.94129109830422" cy="62.45551587307319"/>
<circle r="2" fill="#929292" cx="116.31932986419596" cy="47.91003338006867"/>
<circle r="2" fill="#a2a2a2" cx="114.60184046284907" cy="48.78519033527619"/>
<circle r="2" fill="#b2b2b2" cx="113.26659349902044" cy="49.82801739600207"/>
<circle r="2" fill="#bebebe" cx="112.38137065821381" cy="50.55687266225793"/>
<circle r="2" fill="#c7c7c7" cx="112.33183652278464" cy="50.84977696268302"/>
<circle r="2" fill="#cfcfcf" cx="111.95100063601595" cy="51.476965897165414"/>
<circle r="2" fill="#d5d5d5" cx="112.00329159455698" cy="51.876593845413154"/>
<circle r="2" fill="#d9d9d9" cx="111.78364080980819" cy="52.40697704900191"/>
<circle r="2" fill="#dcdcdc" cx="111.48168129873953" cy="52.88153551972271"/>
<circle r="2" fill="#e0e0e0" cx="111.01795154450872" cy="53.366771154762624"/>
<circle r="2" fill="#e2e2e2" cx="110.67993657218898" cy="53.71004026179943"/>
<circle r="2" fill="#e3e3e3" cx="110.03077362351485" cy="54.212275359758415"/>
<circle r="2" fill="#e4e4e4" cx="109.16122012945544" cy="54.789989318810505"/>
<circle r="2" fill="#e6e6e6" cx="108.28590141438083" cy="55.32261085974633"/>
<circle r="2" fill="#e8e8e8" cx="106.99743185123302" cy="56.02007206756854"/>
<circle r="2" fill="#eaeaea" cx="105.91863125435194" cy="56.548863222879405"/>
<circle r="2" fill="#ebebeb" cx="104.5282127841082" cy="57.25788883926697"/>
<circle r="2" fill="#ebebeb" cx="103.04515145742046" cy="58.01396772343293"/>
<circle r="2" fill="#ebebeb" cx="101.6023267708421" cy="58.75621104815054"/>
<circle r="2" fill="#ebebeb" cx="100.02669086638552" cy="59.54944186228676"/>
<circle r="2" fill="#ececec" cx="98.42281114739158" cy="60.32124397261098"/>
<circle r="2" fill="#ededed" cx="96.75938183166033" cy="61.12758264342305"/>
<circle r="2" fill="#eeeeee" cx="95.09356355089496" cy="61.958681821708055"/>
<circle r="2" fill="#eeeeee" cx="93.35546672087087" cy="62.825650608273726"/>
<circle r="2" fill="#eeeeee" cx="91.51098569445283" cy="63.76789638688609"/>
<circle r="2" fill="#ededed" cx="89.67701364528324" cy="64.7168415268676"/>
<circle r="2" fill="#ebebeb" cx="87.7770141275296" cy="65.68963062779743"/>
<circle r="2" fill="#e9e9e9" cx="85.92798211118821" cy="66.62699567275514"/>
<circle r="2" fill="#e6e6e6" cx="84.13790413790413" cy="67.52978403052168"/>
<circle r="2" fill="#e3e3e3" cx="82.382081061863" cy="68.40759091377151"/>
<circle r="2" fill="#e1e1e1" cx="80.6053381124588" cy="69.28729824274033"/>
<circle r="2" fill="#dedede" cx="78.82177479492917" cy="70.14853504116536"/>
<circle r="2" fill="#dbdbdb" cx="77.04692909241915" cy="70.96609916858692"/>
<circle r="2" fill="#d8d8d8" cx="75.27672194143938" cy="71.74760565064982"/>
<circle r="2" fill="#d5d5d5" cx="73.46031476689433" cy="72.51791732228308"/>
<circle r="2" fill="#d2d2d2" cx="71.59441258030623" cy="73.2807937393374"/>
<circle r="2" fill="#cecece" cx="69.71813091973259" cy="73.96473548754672"/>
<circle r="2" fill="#cbcbcb" cx="67.8135355538287" cy="74.58104927005942"/>
<circle r="2" fill="#c7c7c7" cx="65.86318684320761" cy="75.20211489798797"/>
<circle r="2" fill="#c3c3c3" cx="63.86216384543165" cy="75.78054357329573"/>
<circle r="2" fill="#bfbfbf" cx="61.790891450747644" cy="76.26611876876544"/>
<circle r="2" fill="#bbbbbb" cx="59.65168889929011" cy="76.70867811272647"/>
<circle r="2" fill="#b6b6b6" cx="57.44227033305961" cy="77.13247427789904"/>
<circle r="2" fill="#b1b1b1" cx="55.13067683901232" cy="77.50344775514657"/>
<circle r="2" fill="#acacac" cx="52.69948054159926" cy="77.81912680518944"/>
<circle r="2" fill="#a7a7a7" cx="50.15424617689833" cy="78.14494796389044"/>
<circle r="2" fill="#a1a1a1" cx="47.475729265531555" cy="78.49101039891437"/>
<circle r="2" fill="#9c9c9c" cx="45.30912799108307" cy="78.47771172719705"/>
<circle r="2" fill="#989898" cx="44.772023127027886" cy="77.5474188136611"/>
<circle r="2" fill="#939393" cx="44.22636859707798" cy="76.60231744440775"/>
<circle r="2" fill="#8f8f8f" cx="43.6948051948052" cy="75.68162262422712"/>
<circle r="2" fill="#8b8b8b" cx="43.16756814940394" cy="74.76842127395965"/>
<circle r="2" fill="#868686" cx="42.64175221684523" cy="73.85768136333873"/>
<circle r="2" fill="#818181" cx="42.09612719714098" cy="72.91263110733023"/>
<circle r="2" fill="#7c7c7c" cx="41.52806176946318" cy="71.92871292456891"/>
<circle r="2" fill="#767676" cx="40.948006849205456" cy="70.92402833150223"/>
<circle r="2" fill="#717171" cx="40.36456581690994" cy="69.91347882034596"/>
<circle r="2" fill="#6c6c6c" cx="39.76548108261301" cy="68.87583362250479"/>
<circle r="2" fill="#676767" cx="39.099814568544076" cy="67.72286539924012"/>
<circle r="2" fill="#626262" cx="38.364804902799605" cy="66.4497913141165"/>
<circle r="2" fill="#5c5c5c" cx="37.5468085106383" cy="65.03298000248506"/>
<circle r="2" fill="#565656" cx="36.63742757025399" cy="63.45788601030467"/>
<circle r="2" fill="#515151" cx="35.60262603740865" cy="61.66555717966638"/>
<circle r="2" fill="#4c4c4c" cx="34.405973837599724" cy="59.592894770608254"/>
<circle r="2" fill="#464646" cx="33.04505346812365" cy="57.23571154562029"/>
<circle r="2" fill="#414141" cx="31.47172236503856" cy="54.51062213794854"/>
<circle r="2" fill="#3c3c3c" cx="29.570084129473845" cy="51.21688809633481"/>
<circle r="2" fill="#373737" cx="27.230947528273987" cy="47.165384657212684"/>
</svg>
<figcaption>Single-wavelength lights within normalized cone response color triangle.</figcaption>
</figure>

