---
title: GPU Lite
summary: What you should know about the GPU, aimed at those without prior computer architecture coursework
...


Graphics Processor Units (GPUs) have a variety of hardware design decisions that are aimed at making them very good at some tasks (including interactive computer graphics) but poor at others.
This page attempts to provide a mental model of the GPU
for students who have not studied CPU computer architecture^[Because CS 233 is not a prerequisite for CS 418.].
If you have studied CPU computer architecture some contents here will be familiar
and other parts may surprise you.

# Background: registers and logic

Digital logic consists of directed acyclic graphs of logic gates.
They have arrays of input wires and arrays of output wires.
When a given set of signals are provided to the input wires
the electricity flows through the gates
to make the output wires stabilize on the resulting answer.
The inputs must remain stable until all the gates resolve
or else the answers will be wrong.

Broadly speaking, "logic" can do anything you could write without using any loops or function calls in a programming language.
The more complicated that code, the longer the logic would take to stabilize to the right answer.

To keep inputs stable during computation and to ignore preliminary incorrect outputs,
both inputs and outputs of logic graphs are attached to registers.
Registers store and continuously output values,
ignoring their inputs most of the time.
They also have a special "clock" input:
at the moment that that input goes from 0 to 1,
the register grabs the inputs and puts them in its storage.

This leads to the following operation, where time increased down the table rows:

| Clock | Input Register | Logic | Output Register |
|-|-|-|-|
| 1 | provide first inputs | starts working | ignore input; output old values |
| 1-to-0 | provides first inputs | (instantaneous) | ignore input; output old values |
| 0 | provide first inputs | finish working | ignore input; output old values |
| 0-to-1 | accept second inputs | (instantaneous) | remember and output first results |

# Three Big Ideas

GPUs make heavy use of **pipelines**, **SIMD**, and avoiding **stalling** to achieve very high throughput at the expense of high latency.

**Throughput** measures how much work the processor accomplishes over an extended period of time.
**Latency** measures the time between a single work item being sent to the processor and it being completed.

CPUs try to keep latency fairly small because they often run code where later steps depend on the results of earlier steps:
if the earlier step hasn't finished than the later step has to wait for it,
meaning the latency of even a single instruction can slow down the entire processing significantly.

GPUs all-but ignore latency to get the highest throughput they can
under the assumption that graphics (and related tasks) have many independent tasks to complete
so they can always find work to do that doesn't depend on some high-latency operation completing first.

## Pipelines

Processors implement algorithms.
Algorithms do one step after another;
in hardware, that means there's hardware that does each step.
If we run a single instruction through all of the steps before starting on the next instruction
then most of that hardware will be idle most of the time,
which is not good for throughput.

Pipelines increase throughput by breaking algorithms into individual steps,
with registers between each step.
This lets each hardware component work most of the time
at the expense in latency of having to go through many registers to finish the task.

:::example
Consider an "add" instruction that needs to do the following:

1. Understand what parts of the instruction bits mean what
2. Retrieve the values of the variables used as arguments
3. Send those values across the chip to where the correct logic is found
4. Compute the sum of the values
5. Send the result back to where variables are stored
6. Store the result in the correct variable

If we do all 6 steps between a single pair of registers^[Technically, a pair of pipeline registers: registers are also used for other purposes, including storing variables and implementing stalling.]
then the time to complete this instruction is the time needed for electricity to go through the wires and gates that implement all 6 steps.
Our clock be set to run slow enough for all 6 to complete, plus a little buffer because timing can vary based on things like chip temperature and we never want to have the clock tick before the computation is done.

If we put a register between each step, then the clock will be set at the time of the slowest of the individual steps (plus a bit).
That means that at any given time, six different instructions will be in the processor.
For example, we might have an 8-instruction program where there's a moment in time that looks like the following:

| Instruction | Where | 
| ----------- | ----- |
| 1 | Finished, results back in variable storage |
| 2 | Being placed in variable storage |
| 3 | Traveling along the wire from computation to storage |
| 4 | Being computed |
| 5 | Traveling along the wire from storage to computation |
| 6 | Being retrieved from variable storage |
| 7 | Being broken apart and understood |
| 8 | Not yet begun |
:::

## SIMD

Single Instruction Multiple Data (SIMD) is one of several forms of parallelism.
In it, we have one copy of the parts of the processor that decide what actions to take
but many copies of the parts that read data and perform the computation.

In CPUs, SIMD is generally limited to single instructions:
you might have an instruction, for example, that performs `x[i] += y[i]` for `i`s between 0 and 3 all in one instruction,
intermingled with usual single-data instructions.

GPUs have SIMD instructions (for example, to multiple a 4×4 matrix by a 4-vector),
but also do SIMD at a much higher level.
Graphics tends to do the same operation on many inputs:
positioning many vertices,
rasterizing many triangles,
lighting many pixels,
and so on.
Thus, GPUs are designed to run entire program in SIMD mode,
executing the program in parallel on many inputs
by walking through the instructions in lock-step.

Program-level SIMD parallelism provides very high throughput,
but has a significant downside:
it cannot handle conditionals the way a CPU does.
On a CPU, if an `if` evaluates to false, we skip it entirely.
On a GPU, we can only skip it if it evaluates to false *for every thread*.

:::example
Consider the following code:

```glsl
float shine;
if (dot(n, l) > 0) {
    float ndh = dot(n, h);
    float term = (1 - ndh);
    term = term * term * term;
    shine = PI / term;
} else {
    float a = dot(n, l);
    float b = dot(n, h);
    float c = dot(h, l);
    shine = sqrt(b*b - 4*a*c);
}
```

On a CPU, that code would either execute the `if` or the `else`, not both,
with a runtime that matches just one of the two.
On a GPU, that code would execute both `if` and the `else`, one after the other,
with a runtime that is the sum of the two,
unless it just so happened to get lucky enough that `dot(n, l) > 0`{.glsl} had the same value for all threads.
:::

## Avoiding Stalling

Processors interact with other systems,
such as memory,
that operate very differently than processors do.
Where a processor might work on a few billion 64-bit values each second,
many other systems run much more slowly but work on much larger values.
For example, memory might be able to provide a few kilobytes of data as a single operation
but only run that operation a few million times a second^[If you took a CPU architecture course, this is probably not how you learned about memory working. CPUs don't have wide SIMD processors so they can't effectively operate on entire rows of memory and their cache hierarchies are designed to provide a more CPU-useful model instead. GPU caches are build from similar components, but with different designs for things like cache line size to better support common GPU workloads, making the large size of DRAM rows more visible to the GPU than it is to the CPU.].

If a program contains an instruction that requires interacting with a slow system,
the processor has to wait for the slow system to respond before it can continue.
There are broadly-speaking three ways to handle such a wait:

- Stall the pipeline: turn off the clock on the registers^[Or something fancier with a similar result] until the other system provides the requested data.
    
    Note that stalling does impact the entire pipeline.
    If stage 15 needs to wait for a thousand cycles
    then stage 14 also has to wait for stage 15 to be ready for its output,
    meaning stage 13 and so on back to stage 1 all have to wait as well.

- Pipeline more: add enough "just waiting" stages to the pipeline that stalls aren't needed.
    
    Suppose we realize that stage 15 sometimes talks to memory
    and memory takes a thousand cycles to respond.
    Then we can insert a thousand "wait" stages to the pipeline after stage 15:
    by the time we get to the last one, memory will have the answer for us.
    
    By pipelining instead of stalling, later instructions don't have to wait
    and throughput stays high.
    However, latency goes up significantly, with each instruction taking as long as the slowest case of the slowest external system.
    
    Pipelined waiting is known to be used in GPUs.

- Reorder instructions with task queues: if instructions are waiting on something, pull them out of the pipeline until that thing is available.
    
    There are several ways to implement this idea, but one is to break the pipeline into three parts:
    
    1. Pre-memory pipeline, ending with sending a request to memory.
    2. Memory waiting queue, storing the state of programs that are waiting on memory.
    3. Post-memory pipeline, starting when memory responds and the program waiting on it can be scheduled again.
    
    Modern CPUs have leaned heavily into these ideas and use fancier approaches (register renaming and reorder buffers) on every instruction.
    GPUs use it more selectively,
    picking specific parts of the overall graphics pipeline where the state of the computation can be easily stored in a waiting queue.


# Pipeline to draw triangles

## User-mode CPU code

Code you write for providing data, scheduling events, and so on runs in user mode on the CPU.

There are also user-mode drivers that help get data from your code in the format you provide
into formats and parts of memory that the GPU can handle.

There's also a scheduler that decides which app can use the GPU when.

## Kernel-mode CPU code

The kernel-mode driver handles mapping physical memory into appropriate process space,
managing display device hardware modes,
handling interrupts,
etc.

The kernel-mode driver also copies instructions from the user-mode command buffer (which is a generally-large block of GPU machine code)
to the GPU's internal command buffer (which is generally quite small)
to tell the GPU what to do next.

## Non-CPU non-GPU hardware

There's a bus that gets data between different components (CPU, GPU, screen).
Because graphics code often moves large amounts of data, bus technology matters for GPU performance,
but for the most part we can ignore how it works.

There's also a memory management unit that helps the GPU access memory conveniently.
This includes allowing both the CPU and the GPU to access the same CPU-visible memory,
allowing the GPU to read from and write to memory while the CPU does other work
and then to alert the CPU when it is done.

## GPU

The GPU does many things,
and different GPUs do different things in different ways.
GPUs also have more visible innovation that CPUs, with significantly-changed GPU designs coming out every few years.
This describes only a fairly simple triangle-drawing process.

You will have provided the GPU with four things

- Input data describing scene geometry, textures, etc.
- A vertex shader: GPU code that takes data about one vertex as input and produces data about that vertex as output.
- A fragment shader: GPU code that takes data about one fragment as input and produces data about that fragment as output.
- A pipeline setup, which includes such things as
    - how to connect vertices into primitives (triangles in our case),
    - how large and in what format the rendered image should be,
    - how to handle the depth buffer,
    - how to handle transparency,
    - ... and so on

With this, the GPU will do break the task into several pipelined steps with work queues between them.

### Vertex processing

For maximum efficiency, we want full SIMD perallelism,
meaning a group of vertices (call it 32) all using the same vertex shader.
Each will need it's own copy of each per-vertex input,
and for efficiency we put those inputs in hardware arrays indexed by thread id.
We might need to wait in the vertex processing work queue until memory gets us all those inputs.

Once a batch is ready, we step through the vertex shader instructions in SIMD lockstep.
Vertex shaders generally don't do much memory access so we probably won't have a deep wait-for-memory pipeline.

### Rasterizing

As vertex data is produced by vertex processing,
we group it into triangles to rasterize.

Most triangles will be off-screen and don't need rasterization.
If all the vertices are off the same side of the rendered region, we can skip the triangle altogether.

We'll need to scale triangles up from the normalized ‒1 to 1 coordinate system used by the vertex processing
to the pixel scale used for rendering.
Typically we also apply fixed-point representation so future work can be done on integers, not more computationally-expensive floating-point numbers.

There are several rasterization algorithms possible, with different trade-offs:

- [DDA](dda.html) is easy and efficient in floating-point CPU hardware.
    
- [Bresenham](dda.html#bresenham-hardware) is effective at drawing single-pixel-wide lines, and can also do triangles but does not parallelize well for SIMD parallelism.

    On GPUs, this is best for lines.

- [Defining linear equations](psc.html) for each triangle that detect where within a triangle a pixel is located in SIMD-friendly way.
    But for triangles which are long and thin (which often happens for cameras near large flat surfaces like floors and walls) these can be $O(n^2)$ instead of $O(n)$ in the area of the triangles.
    This leads to two variants:
    
    - Recursively use the algorithm, first in low resolution by checking corners of blocks of pixels (one sample per 16×16 block)
        and then only at full-resolution for the blocks that the low-resolution found the triangle touched.
        
        On GPUs, this is best for scenes with large triangles.
    
    - Use the algorithm directly at full resolution.
        
        On GPUs, this is best for scenes with many small triangles.
    
No matter which algorithm is used,
the end result is a set of **fragments**.
A fragment is the interpolated value of all the outputs of vertex processing
at a particular pixel coordinate.

### $z$ again and again

It is common for larger scenes to have many layers of content,
and it is desirable to avoid wasting time processing parts that are behind other parts.
To help achieve this, GPUs *recommend* that software

- Provide opaque geometry.
    
    Failure to do this must be handled by the programmer; the GPU will treat the depth buffer in a way that makes sense for opaque geometry, or will ignore it entirely.

- Render geometry in close-to-far order.

    Failure to do this reduces the benefit of early and hierarchical $z$, but has no other impact.

- Do not modify $z$ values in the fragment shader.

    Modifying $z$ in the fragment shader is allowed, but if the fragment shader has a code path that could do this then the GPU disables all of the optimizations listed here (both hierarchical $z$ and early z) entirely.

Graphics APIs define the^[They actually define several $z$-buffer modes, but the one described here is by far the most commonly used.] functionality of the $z$ buffer 
as if it was done by comparing the $z$ value of each fragment
with the $z$ value of the current pixel and then replacing the pixel with the fragment if the fragment is nearer (smaller $z$).

GPUs match API specifications but stop processing before making each fragment and comparing it individually
by making several conservative estimates:

#### Hierarchical depth

Hierarchical depth, often abbreviated **Hi-Z**, has a low-resolution copy of the full $z$ buffer.
Each low-res entry covers an $n\times n$ square of full-res $z$ buffer entries
and is stores the maximum value found in that square.

If a fragment has a larger $z$ value that the Hi-Z buffer has, it will be discarded by the full $z$ buffer.

If the minimum $z$ of a group of fragments has a larger $z$ value that the maximum Hi-Z buffer entry of that group, all of the fragemnts will be discarded by the full $z$ buffer.

Because the Hi-Z buffer is smaller than the full $z$ buffer, it requires fewer memory accesses and is thus faster to access.
It is also covers alarger area, making checking groups of fragments more efficient.

#### Early $z$

Early $z$ checks the $z$ buffer before producing final fragments.

Because there may be other fragments still in the pipeline that might change the $z$ buffer, this might fail to discard things that later will be behind those pending fragments.

The earliest $z$ check is done on entire triangles or even triangle clusters.
If all of the vertices are farther away than any of the pixels they might cover,
entire triangles can be discarded even before rasterization.
This requires checking all depths within the bounding box of the triangles,
which can be expensive if there are many pixels, but Hi-Z can help fix that.

If rasterization is done recursively, the low-rest rasterization can be compared to the Hi-Z buffer
and entire blocks of full-res pixels not rasterized.

Fragments can be checked against the $z$ buffer before they are sent to the fragment shader.
Again, because some other fragments may be added to the $z$ buffer before the fragment processing is completed
thost that are kept will also need to be checked against the $z$ buffer again after the fragment shader.

### Fragment processing

For maximum efficiency, we want full SIMD perallelism,
meaning a group of fragments (call it 32) all using the same vertex shader.
Each will need it's own copy of each per-fragment input,
and for efficiency we put those inputs in hardware arrays indexed by thread id.
We also prefer groups of fragments that are close to one another on the screen
and nearby in the 3D geometry
to maximize memory cahce locality for texture lookups, early- and Hi-Z checks, and eventual pixel operations.

Once a batch is ready, we step through the fragment shader instructions in SIMD lockstep.
Fragment shaders often involve texture lookups, with some estimates suggeting 1--2 texture cache misses per SIMD thread group,
so this pipeline often has a deep chain of wait-for-memory steps to avoid stalling.

### Pixel processing

Once the fragment shader is done with a fragment,
there's still several steps to take to get that fragment incorporated into the pixel:

- Do a (final) check of the $z$ buffer.
- If there's transparency or other blending, use it to combine the existing pixel color with the new fragment color.
- Update the $z$ and color buffers.

At some point, typically only after the entire image is rendered,
we also need to modify each pixel to

- Apply a gamma curve.
- Scale the computationally-friendly stored colors (0 to 1) to the final channel range (often 0 to 255).
- Apply dithering to help mask boundaries between large swaths of similar but not identical colors.
- Convert to the specific bytes (and byte order) expected by the image consumer.
- Send the image to the consumer (a display device, an on-GPU texture, or CPU memory).

## User-mode CPU code

If your GPU code returned values to the CPU (rather than sending them directly to the screen),
the schedule and user-mode drivers help it get to the right application in the requested format.

