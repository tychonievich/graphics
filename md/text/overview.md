---
title: The Real-time Graphics Pipeline
summary: An outline of how data flows from 3D model to rendered frame.
...

# Hardware-driven software design

Making code highly efficient always means writing software with the hardware it is running on in mind.^[
    Designing highly efficient hardware also means designing it with the software that will run on it in mind, a topic we'd say much more about if hardware design was our emphasis.
]
This is particularly true in interactive computer graphics
because the interaction is handled on one set of hardware
and the graphics are handled on another.

## CPUs and GPUs

<details class="tldr"><summary>Overview of this section</summary>

**CPUs** are good at branching and dependencies, and OK at repetition.

**GPUs** are great at repeating the same code on many independent data, but awful at branching and dependencies. They use many-part hardware-specified pipelines to bypass enough of those limitations to render graphics.

</details>

CPUs and their associated memory systems, buses, and peripherals are very efficient at running code involving millions of instructions, most running conditionally in response to some external input or some characteristic of data. When a better system for this kind of work come along, it replaces the current CPU as the next generation of CPU.

GPUs and their associated memory systems are very efficient at running the same few pieces of code millions of times a second with slightly different data each time. They can do this much faster than a CPU can, provided that the code runs without and branches and that each iteration is interdependent of other iterations.

Almost all interesting work involves some conditional behavior.
Some of that can be removed via clever coding tricks like masking.

:::example
Recall that the `<` operator produces either 0 or 1 as its result.
Thus conditional sorting code like

```js
if (x < y) { min = x; max = y; }
else       { min = y; max = x; }
```

can be written without conditionals like

```js
mask = (x < y);
min = mask*x + (1-mask)*y;
max = (1-mask)*x + mask*y;
```
:::

But there are limits to the effectiveness of these tricks.
For example, removing the conditional check in a while-loop requires (1) determining in advance the maximum number of times the loop could possibly run and (2) always running the loop exactly that many times, masking out all operations of the runs after it should have stopped so that they do nothing.
Generally, that kind of large-scale mask-based conditional removal isn't worthwhile compared to simply running the code on the CPU instead.

Common graphics algorithms are almost suited for condition-free independent operation, but they have a few key places where conditions and dependencies are unavoidable.
GPUs designers around this by identifying those places and adding special custom-designed hardware for handling those specific conditions and data dependencies.

The result is a pipeline-oriented architecture.
Data flows through a fixed sequence of hardware pipeline stages.
Some of these execute arbitrary branch-free code a programmer has provided.
Some do a single fixed task built into the hardware itself.
Most do a fixed task in one of fixed set of ways, with the specific way from that set chosen by a programmer-specified parameter.

The end result: there are many different pieces to understand, so many that you'll likely spend months forgetting some and feeling a bit confused.^[I've been programming GPUs for almost 20 years and I still sometimes feel that way, in part because many of the stages today didn't exist 20 years ago.]. There are too many pieces to hold in your mind all at once, so expect to occasionally consult a reference

## Main and Graphics Memory

<details class="tldr"><summary>Overview of this section</summary>
**Main memory** can have any organization but only a few accesses per cycle.

**Graphics memory** can support thousands of accesses per cycle, but has to be laid out carefully to support that.

APIs to move data from main memory to graphics memory use a state-machine model for efficiency and flexibility, but that also makes them verbose and picky.
</details>

Main memory and its associated cache hierarchy is designed to operate well with a CPU.
The number of memory accesses that arrive at any given moment is small, bounded by the number of cores in the CPU, and the main design goal is low latency: every nanosecond it takes to complete a memory access is several lost cycles of productivity on the CPU.

Graphics memory has a very different design space.
GPUs get much of their speed by running the same code on thousands of different input data in parallel, meaning when the code has a memory access the memory system gets thousands of addresses to handle all at the same time.
Throughput thus becomes a more important part of memory performance,
and is achieved in part through throughput-oriented memory access hardware
and in part through carefully controlled layout of data in memory.

The end result is that we need to move a lot of data the CPU (which has access to disks, networks, and user input and thus decides what we need to display) to the GPU (which does the displaying), reorganizing the data in the process.
We'll also need some way for the CPU to tell the GPU which data we want it to draw, which means we'll need some kind of identifier for that data, typically implemented as an integer but often wrapped in some kind of opaque datatype called a "handle" or "object".

We're also going to have to spend way more effort moving data from the CPU to the GPU than you might expect.
Depending on the data, the GPU may need to know what kind of data it is, how it will be accessed, how large it is, and how it is related to other data.
Because moving data between memories takes some time, communicating this information will be done by a series of API calls rather than all in one,
with the hope that you, the programmer, will be able to do most of them in a setup phase of your program with only a minimal subset repeated each frame,
while acknowledging that that minimal subset will vary depending on what your application is doing.
To minimize the need to send handles with every API call and to encourage temporal locality in your code, these calls will also operate in a state-machine way: instead of saying "the vertex positions for object *X* are ..." you say "I'm going to talk about object *X* now" and then in a separate call "the vertex positions are ...".

The end result: you'll write more code than you might expect to move data from CPU to GPU, and that code will require a specific order of API calls.
Adding perfectly valid code to a working application may cause existing code to fail because the added code changed some memory-communication state that the existing code depended on.
Most GPU-interfacing applications that I've seen use some kind of wrapper library to help keep these API calls organized, with the design of those libraries varying depending on what the applications they support expect to keep static from frame to frame and what they expect to change.


# Graphics Pipeline Overview

<details class="tldr"><summary>Overview of this section</summary>

On the GPU, data flows as follows:

1. a vertex shader you write moves vertices around
2. built-in hardware steps move them some more
3. built-in rasterizer hardware finds the pixels each triangle covers; one pixel of one triangle is called a fragment
4. a fragment shader you write picks a color for the fragment
5. a series of parameterizable hardware steps discards some fragments and combines others into a final color for each pixel

</details>

The central piece of fixed hardware in a GPU is the **rasterizer**, which takes as input the three *screen-space* *vertices* of a triangle and produces as output the set of *fragments* of that triangle.
Each **vertex** contains a position and may contain any number of other values representing information that may vary over the surface of the shape: texture coordinates, surface color and normals, etc.
A **screen-space** vertex (also called a vertex in **device coordinates**) has the $x$ and $y$ coordinates of its position in presented in units of pixels.
A **fragment** is a point on the triangle with integer $x$ and $y$;
or, put another way, it is the part of the triangle that covers one pixel.
Each fragment has all of the same information as each vertex, but interpolated from the three vertices to its particular location in the triangle.

## Before rasterization

The pipeline stages before the rasterizer convert from the information provided by the CPU---commonly 3D object geometry and positions and 3D viewpoint location and orientation---into the screen-space vertices needed by the rasterizer.
The most important of these are:

* A user-specified GPU-executed **vertex shader**
    
    input
    :   one vertex of the geometry to be drawn.
    
    output
    :   the corresponding vertex in **normalized coordinates**:
        i.e., moved to where it should appear on the screen,
        but in simplified coordinate system where the visible part of the screen is from $-1$ to $+1$ in $x$ and $y$, regardless of the number of pixels on the display.

    Both the input and output of a vertex shader are commonly called "vertices" even though they may have different datatypes and values.

* Fixed **frustum clipping** that removes and geometry that would be off-screen.

* Fixed **projection** that handles the math of common 3D perspective using a single number (the $w$ coordinate) provided by the vertex shader.

* Fixed **viewport transformation** that shifts and scales from the normalized $-1$ to $1$ coordinates to the screen-space coordinates needed by the rasterizer.

Some graphics applications will make use of a few additional pre-rasterization stages, mostly user-specified shaders for refining the object geometry before it gets to the vertex shader.

## After rasterization

The pipeline stages after the rasterizer convert the set of fragments that share a single $(x,y)$ coordinate into the color for that pixel.
There are many of these stages, but most either have a somewhat specialized purpose or just "do the right thing."
Three are of particular note:

* A user-specified GPU-executed **fragment shader**
    
    input
    :   one fragment produced by the rasterizer.
    
    output
    :   the corresponding color to display.
    
    Confusingly, both the input and output of a fragment shader are commonly called "fragments" even though they may have completely different datatypes and values (e.g., input a position, texture coordinate, and normal vector; output a color).

* Configurable **depth buffering** that discards fragments that are behind other fragments.

* Configurable **blending** that combines the fragment's color with the color already in the image at that pixel to create the new pixel color.
