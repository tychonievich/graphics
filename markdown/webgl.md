---
title: Understanding WebGL (and beyond)
...

WebGL (and related technologies like OpenGL, OpenGL ES, Vulkan, Metal, and Direct X) is primarily a communication protocol:
it communicates from the CPU and RAM to the GPU and GPU memory (and, in some instances, back again).
This leads to the following observations

1. There are many things to communicate, including
    a. **shaders**, the code you want the GPU to run
    a. **buffers**, arrays of data you want the GPU to iterate over in parallel
    a. **attributes**,  explaining how to connect the shaders and the buffers
    a. **uniforms**, global read-only values the shaders can access
    a. textures or **samplers**, random-access memory your shaders can read
    a. **varyings**, explaining how shaders talk to one another
1. These all need to be communicated in some kind of common way that does not depend on the host language (i.e. not depending on JavaScript for WebGL)
1. Each GPU is unique, so there has to be some way of checking what features the running GPU has
1. The lower-level the API, both
    a. The simpler the implementation of the API, meaning the more easily it can be used on diverse platforms; and
    a. The more ability users have to customize behavior for speed and/or performance

In practice, the communication is generally not object-oriented; instead we see three common models:

1. Constants to direct traffic.
    For example, a buffer could be an `ARRAY_BUFFER` or an `ELEMENT_ARRAY_BUFFER` or ..., each of which is defined as a constant value known to the CPU and GPU.

1. Handles or identifiers.
    For example, when you create a buffer you get back an ID for that buffer
    which you can pass into later function calls to use or modify that buffer.
    These handles are similar in spirit to file handles in C or to cross-device addresses.

1. An implicit state machine.
    For example, instead of passing a buffer handle to each buffer-modifying function
    there's a `bindBuffer` command that sets the state so that all subsequent buffer-modifying commands will interact with that buffer.

# A basic example

Writing WebGL is initially mostly about wrestling with plumbing (Vulkan, DirectX, or Metal even more so). There are many wrapper libraries that provide ready-made plumbing for you, but there is learning to be done in understanding the plumbing itself.

## HTML and Javascript

HTML and Javascript are everywhere today, and notably not part of our required curriculum.


```html
<!DOCTYPE html> <!-- indicates that we are writing HTML5 -->
<html>
    <head><title>WebGL example</title></head>
    <body>
        <canvas style="position:fixed; left:0; top:0; width:100vw; height:100vh;"></canvas>
        
    </body>
</html>
```
