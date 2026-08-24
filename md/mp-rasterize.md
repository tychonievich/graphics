---
title: Coding the GPU's fixed functionality
...

The most direct way of doing 3D rendering with the GPU is a pipeline containing two parts software and three parts fixed functionality embedded in the hardware design:

1. **HW** Primitive assembly
    
    Input: Buffers of bytes
    
    Input: Information about how geometry is stored in those buffers
    
    Output: Triangles

2. **SW** Vertex shader, which moves vertices around to model the camera and positioning of objects in the scene

3. **HW** Rasterization

    Input: Coordinates of a triangle's vertices
    
    Input: Viewport rectangle
    
    Output: Single-pixel fragments of the triangle, with all vertex attributes interpolated to them.

4. **SW** Fragment shader, which computes a color for each fragment

5. **HW** Compositing

    Input: Colored fragments
    
    Output: A complete image


Most of the MPs in this class will have you focus on writing the software parts above and on creating the inputs used, but this MP has you implement the hardware parts as software.
The goal is not to have a particularly effective or performant implementation,
but rather to understand what is happening by coding it.

# Primitive assembly

It is unusual for geometry to be rendered to be provided to the GPU in the exact format it will use for rendering.
This is the case because of two considerations:

- GPUs want to be able to change their internal formats without requiring graphics code to change.
    This gives them more freedom to innovate and improve their hardware.

- GPU memory is limited, so storing data in a more compact format than is used to compute can allow rendering larger scenes.

The common way that this is exposed to the programmer
is by having the CPU first copy a large array of bytes into GPU memory,
and then telling the GPU how to parse those bytes to find individual triangles.
That information typically consists of

- Information about vertices:
    - A byte offset into the array: "starting at byte 1024..."
    - A description of data types stored there: "...are 4-element vectors with 32-bit floating-point elements..."
    - A stride, the number of bytes between the start of consecutive elements: "...every 20 bytes..."
    - A purpose, where "position" is special: "...representing vertex positions."
- Information about triangles, indicating which vertices are connected into a triangle:
    - Whether vertices should be read in order or via an index buffer.
    - How sequential vertices are connected.

For this MP, the input will be a [glTF file](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.html)
and the output will be text, consisting of











