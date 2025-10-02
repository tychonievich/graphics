---
title: Other parts of the rasterization process
summary: Viewports, blending, culling, and multisampling.
...

# Viewport

Graphics input is provided in a coordinate system that is independent of display size,
but eventually it needs to be mapped to specific pixels.
This mapping is called the "viewport transformation"
and is a simple offset-and-scale operation in $x$ and $y$:

$$\begin{split}
x_{\text{screen}} &= \dfrac{x_{\texttt{input}} + 1}{2}(\text{width in pixels})\\
y_{\text{screen}} &= \dfrac{y_{\texttt{input}} + 1}{2}(\text{height in pixels})\\
\end{split}$$

Note that this *always* maps the coordinate range $-1$ to $+1$ to the viewport in both dimensions, even if the viewport is rectangular instead of square.
It is common to apply a scaling to the scene data to make sure this does not squish content.

# Blending and Masking

After a fragment is shaded, a series of steps are used to decide if and how it should end up in the raster.

| Name | Parameterizable | Behavior |
|-----|:----:|----------------------|
| Ownership | No | Discards fragments occluded by other windows. |
| Scissor | `Scissor` | Discards fragments outside of a rectangular subregion of the rendered area. |
| Multisample coverage | several `enable`able options | Decides if this sample should be included in the final color averaging. |
| [Stencil](#stencil-buffer) | `StencilFunc`<br/>`StencilOp` | See below |
| [Depth](#depth-buffer) | `DepthFunc` | See below |
| Query | No | If any fragments make it to here, that fact is visible using an occlusion query API |
| [Blending] | `BlendEquation`<br/>`BlendFunc`<br/>`BlendColor` | See below |
| sRGB | No | Applies the piece-wise gamma encoding defined in the sRGB specification |
| Dithering | No | Reduces high-def color values to representable values either probabilistically (if dithering is enabled) or deterministically (otherwise) |
| Multisample combination | No | If there are multiple samples, they are averaged in an implementation-defined way to produce a final color. |

All of the above are disabled by default in OpenGL except the ownership test and sRGB conversion.
Dithering and blending technically happen even when disabled, just in a simple way.

## Stencil buffer

The stencil buffer allows some rendering actions to disable some future rendering actions for specific pixels. It can be used to make windows, mirrors, portals, and other rendered holes in the scenery.

Mechanically, the stencil buffer stores an integer (which doubles as a bit vector) for each pixel.

`StencilFunc` allows checking a formula of the form `(bufferValue & mask) [op] reference`
where `mask` and `reference` are constants and `[op]` is a comparison operator, all supplied to the `StencilFunc` call.
If this check yields false, the fragment is discarded.

`StencilOp` can define three different stencil value updates:
one for when the stencil test fails, one for when the depth test fails, and one for when the depth test succeeds.
The allowable operations are fairly limited but with a little creativity can create many interesting effects.

## Depth buffer

Each pixel has a depth value between $-1$ and $1$. This is compared to the $z$ value of the fragment using a comparison defined by the depth func; if it fails the fragment is discarded, otherwise the fragment is kept and the depth buffer value is changed to be the fragment's $z$.

Although the depth buffer is disabled by default, it is used in almost every 3D graphics program, and some 2D programs as well to control stacking.

## Blending

Blending is the process of deciding what color to make a pixel,
given three pieces of data:

- The new fragment's color (or "source color"), $(r_s, g_s, b_s, a_s)$
- The pixel's current color (or "destination color"), $(r_d, g_d, b_d, a_d)$
- A special constant color, $(r_c, g_c, b_c, a_c)$ (defined with `BlendColor`)

These are combined by applying one of several weighting functions selected with `BlendFunc` and one of several combining operations selected with `BlendEquation`.

:::example
The default blending is to just use the new fragment's color.
This is performed via $$1 (r_s, g_s, b_s, a_s) + 0 (r_d, g_d, b_d, a_d)$$
:::

:::example
One of the most common alternative blending modes treats alpha as an opacity channel
and performs what's known as the "over" operator:
$$\begin{split}
a' &= a_s + a_d(1-a_s)\\
(r',g',b') &= \dfrac{a_s}{a'} (r_s, g_s, b_s) + \dfrac{(1-a_s)a_d}{a'} (r_d, g_d, b_d)
\end{split}$$
This only works as expected if objects are sorted by distance from the camera and rendered farthest to nearest.
:::

Note that alpha blending involves combining colors, which must be done in a linear (not gamma-corrected) color space.
For 3D graphics it is common to store and alpha-blend linear colors, and only convert to gamma-corrected byte value after all alpha blending has been resolved.
For image composition, there is generally an sRGB-to-linear step, followed by the blending itself, followed by a linear-to-sRGB step.

It is common^[
    While premultiplied alpha is common, it is not universal,
    and in general could be specified differently
    for how WebGL stores its colors during blending,
    how the browser assumes the WebGL canvas's colors are represented,
    and how each imported image stores its colors.
    See [this StackOverflow post](https://stackoverflow.com/questions/39341564/webgl-how-to-correctly-blend-alpha-channel-png#answer-39354174) for an example of the complexities this can cause.
] to store $(ra, ga, ba, a)$ instead of $(r,g,b,a)$.
This is called "premultiplied alpha" and makes some operations more efficient.
However, premultiplied alpha restricts alpha blending to a few operators and is not generally available in graphics APIs like WebGL.
