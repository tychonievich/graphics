---
title: Introduction to Computer Graphics
author: Luther Tychonievich
...

In order to teach a topic, it is necessary to impose structure on it, breaking it into small enough pieces that each can be individually comprehended and ordering them in some kind of linear order. Some fields have agreed on a common decomposition and ordering, while others have not. Computer Graphics is one of the ones that has not, so it falls on me, as an instructor of computer graphics, to either create an decomposition and ordering of my own or find one someone else has created to use. This text is a bit of each.

Computer Graphics deals with software that generates visual media, typically either images or animation.
This is distinct from Computer Vision, which deals with software that generates information from visual media.
As with all delineations between disciplines, that line is not crisp, the obvious middle ground being software that edits visual media, using them as both the input and output. This text deals only in computer graphics, not computer vision, and handles media editing at only the most superficial level.

One way of organizing computer graphics software is by the kind of API it provides. Roughly, these are

Canvas API
:   Provides a set of "draw this shape" commands. While the software may provide some tools to assist in the creation of composite scenes with many shapes, it does not itself have any internal model of a "scene".
    
    Examples of products in this API family include Vulkan, Cairo, HTML5 Canvas, and the Java Graphics2D class.
    

Scene Graph API
:   Provides a set of commands to express the position of various objects in a scene, often in a hierarchical way, coupled with a single mostly-opaque "draw the scene" command.
    
    Many scene graph systems draw the scene by making calls to an underlying canvas API;
    examples include text layout (such as Pango and Harfbuzz),
    vector graphics (such as SVG and PDF),
    GUI toolkits (such as WxWidgets and GTK),
    and game engines (such as Three.js and Unity),
    among many others.
    
    Some scene graph systems have their own drawing routines, most often ones rely on full scene information,
    typically to create visual phenomena like shadows and reflections that rely on the relative positioning of multiple scene components.
    Interactions of scene components implies non-linear performance scaling,
    so these methods are mostly limited to non-real-time rendering such as is used in the motion picture industry;
    examples include standalone systems like POVRay and LuxRender
    and those integrated with design, editing, and animation software like Maya, Blender, and Houdini.
    
Animation API
:   



Simulation API




# Things I might write up in the future

- Diffusion curves
- Paint strokes
- Parallax occlusion mapping (2005, texture maps with depth)
- Shadows
- Ambient Occlusion

