---
title: Types of Graphics APIs
summary: Common API designs; with names for these designs, some common and some invented for the purpose of this text.
...

In order to teach a topic, it is necessary to impose structure on it, breaking it into small enough pieces that each can be individually comprehended and ordering them in some kind of linear order. Some fields have agreed on a common decomposition and ordering, while others have not. Computer Graphics is one of the ones that has not, so it falls on me, as an instructor of computer graphics, to either create a decomposition and ordering of my own or find one someone else has created to use. This text is a bit of each.

Computer Graphics deals with software that generates visual media, typically either images or animation.
This is distinct from Computer Vision, which deals with software that generates information from visual media.
As with all delineations between disciplines, that line is not crisp, the obvious middle ground being software that edits visual media, using them as both the input and output. This text deals only in computer graphics, not computer vision, and handles media editing at only the most superficial level.

One way of organizing computer graphics software is by the kind of API it provides.

# Canvas

Canvas APIs provide a set of "draw this shape" commands. While the software may provide some tools to assist in the creation of composite scenes with many shapes, it does not itself have any internal model of a "scene".

Canvas APIs deal with layering on a per-pixel basis.
Having the most recent draw command replace whatever was there before is the most common approach,
but many also support auxiliary per-pixel information (such as alpha, depth, or stencil buffers) that allow more advanced per-pixel decisions.

Because canvas APIs draw each shape individually, their runtime performance scales linearly with the number and size of objects in the scene.

Examples of products in this API family include Vulkan, Cairo, HTML5 Canvas, and the Java Graphics2D class.

# Scene Graph

Scene Graph APIs provide a set of commands to express the position of various objects in a scene, often in a hierarchical way, coupled with a single mostly-opaque "draw the scene" command.

Many scene graph systems draw the scene by making calls to an underlying canvas API;
examples include text layout (such as Pango and Harfbuzz),
vector graphics (such as SVG and PDF),
GUI toolkits (such as WxWidgets and GTK),
and game engines (such as Three.js and Unity),
among many others.
These inherit the linear runtime performance of their underlying canvas.
    
Some scene graph systems have their own drawing algorithms instead of using a canvas API;
by far the most common of these algorithms is raytracing.
Because they have the full scene data, full-scene algorithms can create visual phenomena that rely on the relative positioning of multiple scene components, such as shadows and reflections.
Modeling visual interactions between objects means full-scene drawing algorithms have nonlinear runtime performance in the number and size of objects in the scene.
Examples of raytracers include standalone systems like POVRay and LuxRender
and those integrated with design, editing, and animation software like Maya, Blender, and Houdini.


# Animation

Animation APIs add a time axis to the common spatial components of scene graphs. Because the goal is generally to provide more-or-less realistic-looking motion and because virtually all laws of physics treat time as a different kind of variable than space, the temporal part of these APIs generally have a quite different design from the spatial parts.

Most animation APIs express time as mathematical or geometric functions that move or otherwise change spatial data. Simple versions such as blinking cursors, mouse-over color change, and easing curves are present in many UIs. Mathematical descriptions are common in low-level APIs such as the SMIL animation layer for SVG and the `@keyframes` rule for CSS. Artist-friendly tools typically use time sliders, keyframes, and curve editors and are usually part of an animation tool with a primarily-visual interface like Maya, Blender, and Houdini.

Animation does not require an animation API.
Just as a scene can be rendered by user code repeatedly calling a canvas API, so to animation can be rendered by user code repeatedly rendering individual frames.
The most prevalent API support for animation without a full animation API
is an event loop with callbacks: once every frame and once after each user action a user-defined function is called and permitted to redraw the scene. Almost all windowing libraries and GUI systems provide this kind of animation API.


# Simulation

Simulation APIs generate portions of the content to be drawn using some approximation of real-world phenomena.

Simulation APIs can be roughly split into directable and undirectable APIs.
An undirectable API allows the user to set the initial conditions and manipulate external forces and then computes the resulting phenomena from that. A directable API allows the user to provide constraints on what the phenomena should look like and then tries to find something that looks believable within those constraints.

Simulation can be used both to create static content like landscapes, trees, cities, and skin and bark textures; and to create dynamic content like splashes, explosions, walking motion, and plant growth. Some simulations are purely phenomenological, like the classic 1989 boids algorithm that observed that birds seem to stay close, but not too close, and generally all fly the same direction and then turned that observation into code. Others try to incorporate the most up-to-date knowledge of their field, starting from the formulas and theorems current in another discipline's literature and then systematically simplifying it until they get to something that can be solved in reasonable time at the scale needed for good visual effects.

Virtually any discipline can be usefully simulated for graphics. I've read computer graphics papers simulating 
how plants react to pruning,
how crowds react to trauma,
how the elasticity of tendons changes with mood and age,
how light reacts to each layer of skin,
how drivers react to break lights,
how different historical cultures approached city planning,
how yarn material changes how knit fabric responds to pressure,
how different types of hair and hair product change the dynamics of hair movement,
how miscible and immiscible fluids of different densities mix,
how oxygen reaches fuel in a fire,
and dozens of other topics.

Because the scope of simulations is so broad, it is hard to generalize in how they are organized. However, they often have several of the following components:

- They make a discrete approximation of a continuous model.
- They solve a differential equation by making a linear approximation of it using a sparse matrix solver, often a conjugate gradient method.
- They split the simulation into two parts: the first applies several simple rules independently and the second tries to rectify the errors introduced by that simplistic approach.
- They pick an approximation that errs on the side of too-simple-looking results because erring on the side of too-complicated-looking-results is visually jarring or numerically unstable.
- They measure some global property that the science says is conserved, but their approximation failed to conserve and adjust it globally to "fix" that.

# Image-input

Like the other APIs discussed here, image-input APIs produce images, but unlike the others they also take in images as input. There are many operations that can be usefully applied on top of an existing image, including blurring, sharpening, outlining, resizing, removing, compositing, adding paint strokes, recoloring, and on and on. In general, each needs both the input image and some operation-specific parameters.

## Hybrid

Increasingly, image-input algorithms are being used in conjunction with canvas and scene graph APIs to create approximations of visual phenomena more quickly than could be done directly.
In these hybrid approaches, the image-input part is often identified with the qualifier "screen-space".

Screen-space additions to scene rendering APIs can often benefit from more information than could a purely image-input API. Rendering APIs can easily provide screen-space algorithms with per-pixel evaluations of all the information they knew about the objects being displayed there: object identifiers, depth, and surface normal, material type, instantaneous velocity, and so on. Some hybrid APIs even run extra rendering passes to provide the screen-space algorithm with information such as object thickness and other properties not immediately visible in a rendered scene.

Screen-space additions can allow canvas-based renders to add approximations of full-scene phenomena such as reflections, subsurface scattering, motion blur, and depth-of-field.
They can denoise raytracing, allowing better visual quality with fewer rays cast.
And they can add camera- and eye-based phenomena like bloom, lens flare, and spatially-adaptive exposure that are difficult or impossible to correctly simulate during rendering.
