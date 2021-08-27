---
title: Introduction to Computer Graphics
author: Luther Tychonievich
...

In order to teach a topic, it is necessary to impose structure on it, breaking it into small enough pieces that each can be individually comprehended and ordering them in some kind of linear order. Some fields have agreed on a common decomposition and ordering, while others have not. Computer Graphics is one of the ones that has not, so it falls on me, as an instructor of computer graphics, to either create an decomposition and ordering of my own or find one someone else has created to use. This text is a bit of each.

Computer Graphics deals with software that generates visual media, typically either images or animation.
This is distinct from Computer Vision, which deals with software that generates information from visual media.
As with all delineations between disciplines, that line is not crisp, the obvious middle ground being software that edits visual media, using them as both the input and output. This text deals only in computer graphics, not computer vision, and handles media editing at only the most superficial level.

One way of organizing computer graphics software is by the kind of API it provides.

# Canvas
Provides a set of "draw this shape" commands. While the software may provide some tools to assist in the creation of composite scenes with many shapes, it does not itself have any internal model of a "scene".
    
Examples of products in this API family include Vulkan, Cairo, HTML5 Canvas, and the Java Graphics2D class.

In this class, you'll implement a 2D canvas API in HW1 and a 3D canvas API in HW2.

# Scene Graph
Provides a set of commands to express the position of various objects in a scene, often in a hierarchical way, coupled with a single mostly-opaque "draw the scene" command.

Many scene graph systems draw the scene by making calls to an underlying canvas API;
examples include text layout (such as Pango and Harfbuzz),
vector graphics (such as SVG and PDF),
GUI toolkits (such as WxWidgets and GTK),
and game engines (such as Three.js and Unity),
among many others.
    
Some scene graph systems have their own drawing routines, most often ones rely on full scene information,
typically to create visual phenomena like shadows and reflections that rely on the relative positioning of multiple scene components.
Visual interactions of scene components implies non-linear performance scaling,
so these methods are mostly limited to non-real-time rendering such as is used in the motion picture industry;
examples include standalone systems like POVRay and LuxRender
and those integrated with design, editing, and animation software like Maya, Blender, and Houdini.

In this class, you'll implement a full-scene raytracer in HW3.
Currently, hierarchical positioning is not planned as a homework assignment.

# Animation
Provides a spatiotemporal data model and command system with the goal of allowing artists to easily implement a function that, given any time, can produce the scene graph at that time. Because the goal is generally to provide more-or-less realistic-looking motion and because virtually all laws of physics treat time as a different kind of variable than space, the time part of these APIs generally have a quite different design from the scene graph parts.

The simplest and most prevalent form a animation API is an event loop with callbacks: once every frame, and (if interactive) whenever the user does something, a function is called whose purpose is to adjust the scene graph. Almost all windowing libraries and GUI systems provide this kind of animation API.

Some animation APIs also provide a way to express changes over time as a mathematical or geometric function. Simple versions of these, such as blinking cursors, mouse-over color change, and easing curves are present in many UIs. More complicated versions include a few progamatic APIs like the SMIL animation layer for SVG, the `@keyframes` rule for CSS, but are more often part of an animation tool with a primarily-visual interface like Maya, Blender, and Houdini.

In this class, you'll implement an animated scene graph in HW4.

# Simulation
Generates portions of the content to be drawn using some approximation of real-world phenomena.

Simulation APIs can be roughly split into directable and undirectable. An undirectable API allows the user to set the initial conditions and manipulate external forces and then computes the resulting phenomena from that. A directable API allows the user to provide constraints on what the phenomena should look like and then tries to find something that looks believable within those constraints.

Simulation can be used both to create static content like landscapes, trees, cities, and skin and bark textures; and to create dynamic content like splashes, explosions, walking motion, and plant growth. Some are purely phenomenological, like the classic 1989 boids algorithm that just observed that birds seem to stay close, but not too close, and generally all fly the same direction and then turned that observation into code. Others try to incorporate the most up-to-date knowledge of their field, bringing in formulas and theorems from another discipline's literature and then systematically simplifying it until they get to something that can be solved in reasonable time at the scale needed for good visual effects.

Virtually any discipline can be usefully simulated for graphics. I've read computer graphics papers simulating how plants react to pruning, how crowds react to trauma, how the elasticity of tendons changes with mood and age, how light reacts to each layer of skin, how drivers react to break lights, how different historical cultures approached city planning, how yarn material changes how knit fabric responds to pressure, how different types of hair and hair product change the dynamics of hair movement, how miscible and immiscible fluids of different densities mix, how oxygen reaches fuel in a fire, and dozens of other topics.

Because the scope of simulations is so broad, it is hard to generalize in how they are organized. However, they often have several of the following components:

- They make a discrete approximation of a continuous model.
- They solve a differential equation by making a linear approximation of it an using a sparse matrix solver, often a conjugate gradient method.
- They split the simulation into two parts: the first applies simple rules independently and the second tries to rectify the errors introduced by that simplistic approach.
- They pick an approximation that errs on the side of too-simple-looking results because erring on the side of too-complicated-looking-results is visually jarring or numerically unstable.
- They measure some global property that the science says is conserved but their approximation failed to conserve and adjust it globally to "fix" that.

I hope to have a HW5 option that implements a few simple simulations, but have not yet planned how to fit that into the semester.

# Image-space
Like the other APIs discussed here, image-space APIs produce images, but unlike the others they also take in images as input. There are many operations that can be usefully applied on top of an existing image, including blurring, sharpening, outlining, resizing, removing, compositing, adding paint strokes, recoloring, and on and on. In general, each needs both the input image and some operation-specific parameters.

The current plan is to only mention image-space operations briefly and not implement them.
However, I have a ready-made and properly-scoped image-space HW5 that I might swap in if the simulation HW5 doesn't come together well.

