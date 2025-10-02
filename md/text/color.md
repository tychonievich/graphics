---
title: Color
summary: As seen by eyes, projected on screens, and stored in sRGB and YCbCr.
...

# Cones: LMS

Light is delivered in photons, each of which has a wavelength. Visible light wavelengths are roughly from 380nm to 750nm.

Your eye has 4 types of color receptors:
rods, L-cones, M-cones, and S-cones.^[Some women also have a fourth type of cone (see e.g. [wikipedia](https://en.wikipedia.org/wiki/Tetrachromacy#Humans)), but I have not yet seen studies convincingly showing women who have learned to articulate the extra color perception this gives them.]
All four operate on the same principle:

- When a photon hits the receptor, it has some chance of signaling the brain that it saw light.
- That chance is dependent on the wavelength of the light, with a roughly bell-shaped probability curve.
- After signaling, the receptor needs a short reset time before it can signal again. This varies, but something under 0.1 seconds is a reasonable estimate.
- Light intensity is perceived based on frequency of signaling.

Rods react to most of the visible spectrum and react very easily, so except in very dim-light situations they effectively signal as soon as their reset time elapses, providing no useful information to the brain. They're important for night vision, but not for color.

The most direct way to model color perception would thus be as three durations: the average time between two firings of an L-cone, of an M-cone, and of an S-cone. Thus, we might say the cone response is (0.1s, 2.4s, 0.4s) to mean the L-cone is firing almost immediately after reset, the M-cone is almost idle, and the S-cone is somewhere in between.

Seconds are awkward in this context in part because they are unbounded, approaching infinity in complete darkness; and because the difference in light intensity needed to go from 0.11s to 0.10s is much much larger than the difference needed to go from 11s to 10s. But the relationship between seconds and light intensity is a smooth and monotonic function, so there is some normalizing function that would convert these seconds into a some kind of nicely-behaved range where 0 means "never firing" and 1 means "firing as often as possible". We'll skip the math and assume we have access to that normalized cone signaling numbers.

# Cone chromaticity

Normalized cone signaling would form a cube, from (0,0,0) to (1,1,1).
But we don't perceive a cube of color.
There are various ways that (0.1, 0.2, 0.3) can change into (0.2, 0.4, 0.6) with no change in the color of the object being observed, including pupil dilation, clouds moving away from the sun, etc. We can perceive this overall intensity of light or "luminosity", but our brain filters out overall luminosity and perceives only relative luminance[^bright] of adjacent colors. So a better model of color is as 2D chromaticity vector $(l,m,s)$ where $l+m+s = 1$, coupled with a separate luminance level in the form of a scalar being multiplied by the whole vector.

[^bright]:
    Several related terms are technically distinct but sometimes used interchangeably in computer graphics:
    
    **Luminosity** = Watts of photon radiation (either overall or in the visual range).
    
    **Luminance** = Luminosity per unit area.<br/>**Brightness** = perception of luminance, generally relative to its surroundings.
    
    **Lightness** = perception of "how light it is", a non-linear scale as the eye is better at distinguishing between darkish shades than light shades or very dark shades.
    
    **Value** = "distance from black"; if a white light and a red light have the same value, they are emitting equivalent numbers of long-wavelength photons, but the white light is also emitting short-wavelength photons and thus has higher luminosity.

Ignoring the luminance component for the time being, our cone-based chromaticity space is now a triangle:

<figure>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="-2 -2 204 177.20508075688772" style="max-width:24em">
<path d="M 200,173.20508075688772 100,0 0,173.20508075688772 Z" stroke-width="4" stroke="black" stroke-linejoin="round" fill="black"/>
<text x="195" y="173.20508075688772" fill="#ff8080" text-anchor="middle" font-family="arial" font-size="10px">L</text>
<text x="100" y="10" fill="#00ff00" text-anchor="middle" font-family="arial" font-size="10px">M</text>
<text x="5" y="173.20508075688772" fill="#8080ff" text-anchor="middle" font-family="arial" font-size="10px">S</text>
</svg>
<figcaption>Cone-based chromaticity triangle.</figcaption>
</figure>

# Achieving chromaticities with light: RGB

In order for us to display the color represented by some point in this triangle, we have to find a combination of light of various wavelengths that triggers that ratio of response in the three cone types. The first step toward that goal is to find where each individual wavelength falls in this triangle.
Fortunately, others have done this work for us and published the results;
using the table from Stockman, McLeod and Johnson (1993)^[Andrew Stockman, Donald MacLeod, Nancy Johnson (1993) "Spectral sensitivity of the human cones." *Journal of the Optical Society of America A*, 10(12) pp. 2491--2521] we get

![Single-wavelength lights every 5nm from 390nm (on left) to 730nm (on right).^[Notice the little hook on the short-wavelength end of the curve? While neither is very sensitive there, the L cone is more sensitive than the M cone in those wavelengths, causing them to look indigo, a color more often created with a combination of blue and a little red light. But the sensitivities are small enough, even slight individual variations mean some people see much more indigo in those wavelengths than do others.]](color-area.svg){style="max-width:24em"}

By combining multiple wavelengths we can get any point inside that curve. Points outside the curve represent cone responses that cannot be triggered by any combination of light.^[In 2025, researchers caused the optic nerve to signal the impossible ratio $(L,M,S)=(0,1,0)$ by targeting microscopic lasers directly at M cones and only M cones. The subjects report seeing a very saturate color that was sort of bluish-green, which they named "[Olo](https://en.wikipedia.org/wiki/Olo_(color))".]
In other words, only a subset of theoretical cone responses actually represent colors. 

It is worth noting that not every eye is the same. The exact ratios of pigments inside the cones vary by individual, meaning the exact same wavelengths of light might cause a response of (0.1, 0.4, 0.5) in one individual and (0.1, 0.45, 0.45) in another. The variations are typically fairly small, and when larger are called "color blindness" (a term that also refers to more extreme variations such as having only two types of working cones).

Computer screens want to be able to show a lot of colors. But creating arbitrary sets of wavelengths is quite expensive, so we want to pick just a few wavelengths that we can combine to make most colors. Because the curve is roughly triangular, picking three such primary colors is a common choice. But getting a *single* wavelength is much harder than getting a narrow band of wavelengths and some wavelengths the eye hardly perceives at all so it would take too much energy to use them effectively in a display.

![Relative responsiveness of the S (blue), M (green), and L (red) cones to wavelengths from 390nm (on left) to 730nm (on right).](color-response.svg){style="max-width:24em"}

As a result, early color displays played with several different colors of light, but by 1993 had mostly settled on ITU-R Recommendation 709 which used colors made of several wavelengths, which can be plotted on our cone triangle as follows.

![Rec.709 color triangle and relative eye responsiveness to various pure wavelengths. The triangle shows all colors (luminance aside) that are representable using the Red, Green, and Blue primary color used by most RGB displays (as of 2025). The triangle does not extend to the L corner because it requires a lot of energy to get those wavelengths to appear bright because none of the cones are very responsive there. It does not touch the curve anywhere because single-wavelength light sources are challenging to manufacture.](color-curve.svg){style="max-width:24em"}

You'll notice that there is space in the above image that is inside the visible-color curve but outside the colored-in triangle. Those colors exist in the real world, but cannot be replicated on this screen. Later ITU-R recommendations (Rec.2020 published in 2012 and Rec.2100 published in 2016) suggest single-wavelength lights to get a larger region, but while that makes the triangle bigger it still leaves out some colors. Most of the monitors I checked in 2025 still used Rec.709 colors instead, which is why I rendered the Rec.709 triangle above.

Note that some colors can be represented on a monitor but are not shown in the diagram because they differ from the diagram's colors only in luminance.
For example, yellow, is a higher-luminance version of the point halfway between the green and red corners
and forest green is a lower-luminance version of a point near the green corner of the triangle.

# Non-linear storage: Gamma

Let's review where we stand:

- The eye has three color receptors, L, M, and S (named after the long, medium, and short-wavelength light they perceive).
- Because their sensitivities overlap, some combinations of LMS response are impossible in the visual world. The achievable subregion is curved.
- Because the curve is roughly triangular, mixing three light colors (called primary colors) can give a pretty good approximation of the visible light spectrum. More primary colors would do a better job, but is generally not seen to be worth the cost.
- We call the three primaries "Red", "Green", and "Blue" as by themselves they (roughly) correspond to colors with those names.

We've almost reached how color is actually stored in a computer; the missing component is "gamma".

Let's assume we have two colors that differ only in luminance.
The formal term for this is having the same "chromaticity".
The eye roughly distinguishes the two by the relative luminance,
so 1.0 and 0.9 are seen as much more similar than are 0.2 and 0.1.
The formal term for this relative perception is "lightness".

Given that we want to store a grid of millions of colors for every picture we store, we want the storage to be small, so we have an incentive to represent colors on a logarithmic scale instead of a linear scale to handle this relative comparison.
But a pure logarithmic scale is not ideal:
while the eye is better at distinguishing dark colors than bright colors,
that breaks down for the very darkest colors,
making a logarithm not quite right.

In exploring efficient ways of encoding lightness, early efforts developed a simple-to-implement-in-analog-electronics system known as "gamma", from the generic equation $r = s^{\gamma}$ where $s$ is the stored lightness and $r$ is the real luminosity. A gamma of $\gamma = 2.2$ was found to be a good value, and many CRT displays were manufactured that applied that equation automatically in their circuitry. Some also featured an adjustable gamma knob so that, by moving physical wire coils and so on, the $\gamma$ in $r = s^{\gamma}$ could be adjusted.

As digital display technologies became prevalent and a simple formula was no longer needed, the name gamma stuck, as did most of the implementation. However, because the eye is not good at distinguishing very dim colors people found that a raw gamma scale resulted in 3--5% of all color signals being perceived as indistinguishably "black". So modern "gamma correction" is generally a piecewise equation, linear for dim colors and polynomial for brighter colors. The most common version is the sRGB gamma function, defined for a color range of 0--1 (not the 0--255 range sometimes used to encode in bytes), is

$$L_{\text{linear}} = \begin{cases}
L_{\text{sRGB}}/12.92 &\text{if }L_{\text{sRGB}} \le 0.04045 \\
\displaystyle \left(\frac{L_{\text{sRGB}}+0.055}{1.055}\right)^{2.4} &\text{if }L_{\text{sRGB}} > 0.04045
\end{cases}$$
$$L_{\text{sRGB}} = \begin{cases}
12.92 L_{\text{linear}} &\text{if }L_{\text{linear}} \le 0.0031308 \\
1.055{L_{\text{linear}}}^{1/2.4}-0.055 &\text{if }L_{\text{linear}} > 0.0031308
\end{cases}$$

The above functions assume each color channel is stored between 0 (black) and 1 (as bright as the screen can manage).
To store that channel in $b$ bits we use a factor of $2^b-1$ in addition to the sRGB gamma function.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" viewBox="-20 -10 150 120" style="max-width:26em; display:table; margin:auto">
<text x="0" y="-3" text-anchor="middle" font-size="6">Linear</text>
<text x="103" y="102" text-anchor="start" font-size="6">sRGB</text>
<path fill="none" stroke="#000" d="M 0,2 -1,2 0,0 1,2 0,2 0,100 98,100 98,99 100,100 98,101 98,100"/>
<path fill="none" stroke="#000" d="M 0,100 C 48,100 77,50 100,0"/>
<path fill="none" stroke="#000" stroke-width="0.5" stroke-dasharray="1 1" d="M 50,100 50,78.6 0,78.6"/>
<path fill="none" stroke="#000" stroke-width="0.5" stroke-dasharray="1 1" d="M 73.5,100 73.5,50 0,50"/>
<text x="50" y="108" text-anchor="middle" font-size="6">0.5</text>
<text x="-2" y="80.6" text-anchor="end" font-size="6">0.212</text>
<text x="73.5" y="108" text-anchor="middle" font-size="6">0.735</text>
<text x="-2" y="52" text-anchor="end" font-size="6">0.5</text>
</svg>
<figcaption>
An illustration of a gamma curve.
Because the eye is better at distinguishing darker colors than brighter colors (vertical axis)
we want the majority of possible bit patterns (horizontal axis) to be used for darker colors
with a relatively small set of values for bright colors.
</figcaption>
</figure>

There are many names and uses of each of the two encodings gamma creates:

Display
:   In this space, light intensity (i.e. luminosity or watts of light energy) is directly proportional to numbers, making it what we want our **display output** to be.
    That make it a **linear** space which is what we need for any type of **interpolation** (such as by DDA/Bresneham) or **lighting** computation (such as we do often in 3D graphics).
    As such it is the space assumed in most 3D graphics APIs like **WebGL**.
    
    Because 3D standards like WebGL use linear coordinates, the WebGL color `0.5` is given on the vertical axis and hence 0.735 on the horizontal axis of the above figure.

Storage
:   In this space, binary encodings are optimally efficient (assuming 1 is "the brightest light in view":
    **sRGB** is calibrated assuming it is used in a dark room, not in a bright space).
    That makes it a **nonlinear** space good to **storage** in image files and over-the-wire transmission to as **display input** sent to screens and other display devices.
    Because it is what screens process and files store, it is used in standards that intend to **enumerate** all representable colors such as **CSS** and other non-3D web standards.
    
    Because web standards like CSS use sRGB, the CSS color `#7F7F7F` is around 0.5 on the horizontal axis and hence 0.212 on the vertical axis of the above figure.



# Bytes

While higher-range images are starting to gain popularity, most displays and image formats use 8 bits each for Red, Green, and Blue.
Web standards have popularized representing the result as three hexadecimal bytes, RGB, each written with two hex digits in a row with a hashtag in front, like `#e3b021` for this color: <span style="width:5em; height:5em; background: #e3b021; display: inline-block; vertical-align:middle;"></span>. Unless otherwise noted, it is safe to assume these are in the sRGB color space and stored post-gamma-correction, which means that most monitors can display them as-is but that arithmetic on the colors requires conversion to linear display intensities before it is accurate.

Systems interested in optimal compression of information, ranging from the earliest color television broadcast signals to the most recent compression/decompression algorithms (also known as "codecs"), have observed that the eye perceives chromaticity at a coarser resolution than it perceives luminance. It is thus advantageous to decompose color using a different set of axes than RGB, using one axis for some form of brightness, lightness, luminance, or luminosity, so that we can easily transmit more bits of luminance than bit of chromaticity.

[HSL](https://en.wikipedia.org/wiki/HSL_and_HSV) dates back to 1938, was designed for color television, and was the first separate-lightness model to be widely implemented in hardware. In it, <b>H</b>ue is an angle around the color wheel and <b>S</b>aturation is intensity of color (i.e., non-gray-ness).

HSL has an angular coordinate (H) which makes it awkward for use in digital computation.
As digital replaced analog in displays, [YCbCr](https://en.wikipedia.org/wiki/YCbCr) became more popular than HSL.
In YCbCr, Y represents luminance (or Y' represents luma, a gamma-corrected version of luminance; both YCbCr and Y'CbCr are used),
Cb is how much of that luminosity comes from blue
and Cr is how much of that luminosity comes from red.
Along with a few variants like YUV and YcCbcCrc that replace Cb and Cr with similar numbers computed in slightly different ways, YCbCr is the dominant way color is stored for lossy compression of digital media, including JPEG, H264, HEVC, VP9, and so on.

YCbCr and its relatives are capable of expressing nonsensical colors: ones with negative or more-than-100% levels of some primary colors. Thus, YCbCr encodings never contain those particular color expressions^[Sometimes impossible YCbCr values are permitted for computational simplicity of encoding and are clamped to the nearest possible value during decoding.].

<figure>
<div>Y': <input type="range" id="y"
    min="0" max="255" value="80" step="0"
    aria-valuemin="0" aria-valuemax="255" aria-valuenow="80"
    oninput="fillPlane(Number(value))"></div>
<output for="y" id="colors">
    <br/>
    Y'CbCr colors at Y' = <span id="y_val">0</span>:
    <br/>
    <canvas id="plane" width="256" height="256"></canvas>
</output>
<script type="text/javascript" style="display:none">
function YCbCr_to_sRGB(y,cb,cr) {
    let r = y + 1.402*(cr-128);
    let g = y - 0.344136*(cb-128)-0.71436*(cr-128);
    let b = y + 1.773*(cb-128);
    return [r,g,b];
}
function fillPlane(y) {
    document.getElementById('y_val').innerHTML = y
    let ctx = document.getElementById('plane').getContext('2d');
    var id = ctx.getImageData(0,0,256, 256)
    function pixel(x,y,color) {
        let [r,g,b] = color
        id.data[4*(x+256*(y)) + 0] = (r+0.5)|0;
        id.data[4*(x+256*(y)) + 1] = (g+0.5)|0;
        id.data[4*(x+256*(y)) + 2] = (b+0.5)|0;
        id.data[4*(x+256*(y)) + 3] = 255;
    }
    for(cb = 0; cb < 256; cb += 1) {
        for (cr = 0; cr < 256; cr += 1) {
            let color = YCbCr_to_sRGB(y,cr,cb)
            if (color[0] < 0 || color[1] < 0 || color[2] < 0
            || color[0] > 255 || color[1] > 255 || color[2] > 255)
                color = [127,127,127]
            pixel(cr,cb,color);
        }
    }
    ctx.putImageData(id,0,0);
    document.getElementById('plane').setAttribute('alt','YCbCr colors for Y = '+y)
}
fillPlane(Number(document.getElementById('y').value))
</script>
<figcaption>Interactive demonstration of the 0--255 Y'CbCr color space defined in the JFIF standard for JPEG images. Use the slider to pick a Y' value; colors with that Y' value are shown with Cb=0 on the left and Cr=0 on the top. Gray background represents CrCb values that are not defined for the chosen Y'.</figcaption>
</figure>

# Representations for more displays

By design, HSL and YCbCr represent the same chromaticities as RGB.
Sometimes it is desirable to use a model that allows representing *all* chromaticities, not just those a computer can display.
[CIE 1931](https://en.wikipedia.org/wiki/CIE_1931_color_space) (also called CIEXYZ), [CIELAB](https://en.wikipedia.org/wiki/CIELAB_color_space), and [CIELUV](https://en.wikipedia.org/wiki/CIELUV) were designed by international standards bodies and both roughly approximate a warped version of the LMS triangle discussed earlier so that the curve comes close to filling a square and is stretched to make distance in the warped space roughly approximate human perceived difference of colors.
While not designed for digital display, the CIE models (and several related variants) are used to describe calibrations of display components and the interrelationship of different color models and different kinds of displays.

Since the mid-2010s, manufacturers have started producing displays that use narrower and more widely-spaced primaries than the sRGB standard supports,
though not all use the same primaries.
This has encouraged some image files to be encoded in CIE color spaces, allowing each device to determine how best to represent or approximate the color using the primaries the device has available.
Unfortunately, CIEXYZ is not perceptually uniform, meaning distance in the XYZ space is not a good predictor of quality of approximation; and CIELUV and related color spaces have various computational and perceptual challenges that make them suboptimal for this purpose.

In 2020, Björn Ottosson use numerical optimization to find a mathematically-simple function that best fit several different CIELUV-like color models and posted the result [on his blog](https://bottosson.github.io/posts/oklab/).
This model, which he called "Oklab" because it was an "OK" version inspired by CIELAB, rapidly gained traction, especially in 2D graphics applications such as computing color gradients and modelling perception, as well as as a convenient way to represent device-independent full-gamut colors.
By 2023 Oklab was implemented by all major web browsers along with a variety of other applications.

Overall, Oklab has a similar feel to Y'CbCr:
one axis is luminance, others approximate "blueness" and "redness",
and many (L,a,b) triples have no mapping to RGB (or even any possible color).
However, where Y'CbCr is a single matrix multiply from sRGB,
Oklab handles gamma, a matrix multiply, raises each channel to a power, and then does another matrix multiply;
the extra steps allow it to more accurately reflect human perception, at the expense of more computational work.

<figure>
<div>L: <input type="range" id="l"
    min="0" max="1" value="0.7" step="0.001"
    aria-valuemin="0" aria-valuemax="1" aria-valuenow="0.7"
    oninput="fillPlaneOK(Number(value))"></div>
<output for="l" id="colors">
<br/> Oklab L = <span id="l_val">0</span>: <br/>
<canvas id="planeOK" width="512" height="512">
</canvas>
</output>
<script type="text/javascript" style="display:none">
function lab_to_sRGB(L,a,b) {
    let l_ = L + 0.3963377774 * a + 0.2158037573 * b;
    let m_ = L - 0.1055613458 * a - 0.0638541728 * b;
    let s_ = L - 0.0894841775 * a - 1.2914855480 * b;
    let l = l_*l_*l_;
    let m = m_*m_*m_;
    let s = s_*s_*s_;
    let rgb = [
		+4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
		-1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
		-0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    ];
    return rgb.map(c => 255*(c < 0.0031308 ? 12.92*c : (1.055*(c**(1/2.4))-0.055)));
}
function fillPlaneOK(l) {
    document.getElementById('l_val').innerHTML = l
    let ctx = document.getElementById('planeOK').getContext('2d');
    var id = ctx.getImageData(0,0,512, 512)
    function pixel(x,y,color) {
        let [r,g,b] = color
        id.data[4*(x+512*(y)) + 0] = (r+0.5)|0;
        id.data[4*(x+512*(y)) + 1] = (g+0.5)|0;
        id.data[4*(x+512*(y)) + 2] = (b+0.5)|0;
        id.data[4*(x+512*(y)) + 3] = 255;
    }
    for(ca = 0; ca < 512; ca += 1) {
        for (cb = 0; cb < 512; cb += 1) {
            let a = (ca-256)/(3*256)
            let b = (cb-256)/(3*256)
            let color = lab_to_sRGB(l,a,b)
            if (color[0] < 0 || color[1] < 0 || color[2] < 0
            || color[0] > 255 || color[1] > 255 || color[2] > 255)
                color = (ca==256||cb==256) ? lab_to_sRGB(l,0,0) : [127,127,127]
            pixel(ca,cb,color);
        }
    }
    ctx.putImageData(id,0,0);
    document.getElementById('planeOK').setAttribute('alt','Oklab colors for L = '+l)
}
fillPlaneOK(Number(document.getElementById('l').value))
</script>
<figcaption>
Interactive demonstration of the portion of the Oklab color space that can be represented by an sRGB display. Use the slider to pick an L value; colors with that L value are shown with a = −⅓ on the left and b = −⅓ on the top.
Gray background represents Oklab colors that cannot be represented in sRGB for the chosen L.
Crosshairs indicate the origin, where the grey pixel at the given L can be found, and is drawn in that shade of grey.
Colors to the right should be perceptually red, to the left perceptually green; colors to the bottom should be perceptually yellow, to the top perceptually blue;
and the further a color is from the origin the more intense its chroma (more vivid color, less grey).
</figcaption>
</figure>


# Why print is more complicated

The above discussion applies to light-emitting displays: laptops, desktops, phones, etc. Print media has additional constraints.

The basic function of colored ink is to absorb some wavelengths and not others. Cyan ink, for example, absorbs most wavelengths that we'd see as being orange or red. Picking the best inks is tricky: if they absorb too many wavelengths then they overlap and some bright colors become unpresentable; if they absorb too few then some wavelengths cannot be absorbed and some dark colors become unpresentable.

The most common compromise is to have a CMYK printer: <b>C</b>yan, <b>M</b>agenta, and <b>Y</b>ellow ink that each remove a bit shy of a third of the visible spectrum and blac<b>K</b> ink that absorbs the entire visible spectrum and can help approximate those darker colors that the gaps between the CMY absorptions make hard by themselves. Common CMYK inks together cover a smaller and somewhat different region of possible colors than RGB.

Higher-end printing systems use many more inks covering many narrow bands of photons to give a higher degree of color fidelity. The [Pantone system](https://en.wikipedia.org/wiki/Pantone#Pantone_Color_Matching_System) is probably the best known with 14 base pigments instead of CMYK's 4.

Even with many pigments, print and light colors have different coverage than one another. In an RGB display, white is (1,1,1) meaning that roughly ⅓ of light energy is coming from wavelengths that look purely red. But on paper, white is a mix of all the visible spectrum, and to filter out all but the red light will result in a darker red (relative to white) than would result if we turned off the G and B components of an RGB display. With enough pigments the chromaticities could be made to match, but not the luminances. Unless, that is, you print with florescent pigments that absorb photons of one wavelength and release that energy as photons of a different wavelength, or are viewing the printed medium under RGB-based lights, which some florescent and LED lights are, or...

Beyond noting that these complexities exist, we'll mostly ignore pigment-based color in this class.
