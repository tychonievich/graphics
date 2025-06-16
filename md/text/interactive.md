---
title: '"Interactive" Graphics'
summary: Contrasting rasterization and raytracing, with a nod to other approaches.
...

This course is entitled "Interactive computer graphics".
While we will discuss some aspects of interactivity---that is, responding to user input---of a truth user interaction is more particularly covered in courses on user interface design and human-computer interaction.
Instead, this course will focus on an approach to computer graphics
that prioritizes being able to render an entire scene in a few milliseconds.

There are two common families of approaches to rendering a 3D scene:
Rasterization and Raytracing.

# Rasterize

Rasterizers render the scene one object at a time,
limiting the interaction between objects to just what what is in front of what.
Unlike the real world, light is not modeled bouncing between several objects before it reaches the eye.
That limits the visual accuracy of rasterizing, but also means

- Algorithms can can take advantage of the structure of the raster to find the pixels a given object covers very efficiently.
- Rasterizers can be run on all scene objects in parallel.
- Each thread of rasterization parallel execution runs the same instructions in the same order, just with different data.
- Rasterizers can be run in a "streaming" way, with scenes too large to fit in memory being loaded into memory in chunks, rendered, and then removed from memory to make room for the next chunk all as part of a single scene.

Graphics Processing Units (GPUs) are specialized devices optimized for very wide parallel single-instruction multiple-data (SIMD) execution.
GPUs also generally have fast hardware implementations of most of the rasterization process, meaning that they can render complex scenes at high resolution in mere milliseconds.
That speed allows GPU-accelerated rasterization to make 3D graphics applications that respond to user input at interactive speeds, meaning rasterization is often called "interactive computer graphics".

# Raytrace

Raytracers render the scene one light path through the scene at a time,
modeling the full interaction between objects with light bouncing and scattering multiple times on its path from light source to eye.

There are many possible paths light could take, the vast majority of which do not connect a light source and an eye and thus do not contribute to the appearance of the scene. A large part of raytracing is thus finding the visually-important light paths in a large search space.
Various data structures and algorithms make that process fairly fast, but the only ones that can compete with the speed of a rasterizer are those that mimic a rasterizer's no-interobject-lighting approach.
Those accerlating data structures make SIMD implementations of raytracing more involved than SIMD implementations of rasterization, with ongoing efforts to get GPU-accelerated raytracing to operate well.
Additionally, raytracers cannot take advantage of the structure of the raster because light paths are not limited to a simple grid, further slowing raytracing compared to rasterization.

As a result, raytracing is primarily used for what is called "production computer graphics", meaning non-interactive tasks like rendering the frames of a movie or static images used to visualize a scene.
However, as computers continue to get faster and GPU-accelerated raytracing becomes more capable, some raytracing is making it into the interactive application market.
