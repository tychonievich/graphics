---
title: Understanding hardware performance
...

Graphics does a *very large* amount of computation,
and needs to do it quickly.
It runs on GPUs, chips designed to support this computation.
But performance of GPU hardware and software is not something most students enter CS 418 already knowing.

This is not a full computer architecture course,
nor does it have a computer architecture course as a prerequisite.
Because of that, this page necessarily makes some generalizations and simplifications,
sacrificing full technical precision for hopefully increased understanding.


# Functional units

Inside a computer chip are collections of transistors known as functional units.
Each functional unit takes a few inputs and produces an output
by performing either just one or a family of closely-related operations.
These inputs must be physically provided on specific wires,
and there are other parts of the chip that take care of putting them there.

We'll consider just four functional units
which might be considered typical of how GPUs do most of their work.
I introduce two-character abbreviations for each;
these abbreviations are not standard outside of this class,
but I hope they will help remind you of the details of these operations.

`+-`
:   Addition and subtraction of floating-point numbers differ only in a single bit
    and are both done by a functional unit commonly called an <dfn>adder</dfn>.
    
    Addition is much faster than the other operations a GPU does,
    so much so that it is common to have a functional unit that does several additions in a single clock cycle.
    Commonly this functional unit takes a list of 4 numbers and computes their sum all in one go,
    optionally flipping the sign of any subset of the numbers along the way to cover subtraction too.
    To compute `x + y`, this unit instead computes `x + y + 0 + 0`.

`*+`
:   Multiplication is implemented in a way that allows a number to be added to the product with no extra work,
    creating functional units commonly called <dfn>fused multiply-adders (<abbr>fma</abbr>)</dfn>.
    To compute `x * y`, this unit instead computes `(x * y) + 0`.

`1/`
:   In GPUs, it is common for the same denominator to be used in many divisions.
    Because division is much more time consuming than multiplication,
    the functional unit of interest is actually a single-argument <dfn>inversion</dfn>
    which computes `1/x` for its given `x`.

    Inversion is slow, often taking multiple cycles to complete.
    In CPUs it is common to use fancy approaches that take fewer cycles for smaller arguments,
    but in GPUs runtime predictability is important for effective parallelization.
    The exact time does vary by GPU and by the number of bits used to represent the number,
    but 10 cycles per inversion (compared to 1 for a `+-` or `*+`) is a good rule of thumb.

`?:`
:   GPUs are very bad a branching.
    While they do support control constructs like `if` and `while`,
    using them in ways that do not impose a massive performance penalty is tricky,
    as is described more in the section on [SIMT].
    
    What GPUs can do fairly efficiently is selecting between readily-available values.
    This can be selecting one of two values, like `i ? x : y` does in C-like languages;
    or one of a small, fixed set of values, like `v[i]` does when `v` is a small fixed-length array stored in registers.

GPUs often have hardware implementations of common math functions,
most notably square roots (i.e. $x^{1/2}$) and inverse square roots (i.e. $x^{-1/2}$).
Sometimes these are functional units, other times they are optimized implementations of some heuristic followed by a few steps of Newton's method
or the like. 
Details vary, but thinking of (inverse) square roots as costing twice as much as an inversion and other math functions as costing several times more still is reasonable.

    
# SIMD and SIMT

GPUs use two forms of parallelism extensively.

## SIMD

<dfn>Single Instruction, Multiple Data (<abbr>SIMD</abbr>)</dfn>
is implemented in hardware by lining up several identical functional units
and having them operate in lockstep on lists of inputs to produce list of outputs.
SIMD is primarily exposed by GPUs' graphics APIs in the form of operations of 4-element vectors and 4×4 matrices,
with similar operations with more but smaller arguments being common in more approximate computations used in machine learning.
For example,

- A dot product of 4-vectors is 4 `*+` operating in parallel followed by one `+-`: `a*x + b*y + c*z + d*w`.
- A matrix-vector multiply is 4 dot products operating in parallel: entry $i$ = matrix row $i$ dot the vector.
- A matrix-matrix multiply is 4 matrix-vector multiplies operating in parallel: resulting column $j$ = matrix times column $j$.

Because of SIMD, for common operations the interesting aspect for runtime
is how deep, rather than how wide, the operation is.
A matrix-matrix multiply takes the same time as a dot product,
which we might generalize as 2 cycles: one that does 64 `*+` operations in parallel
and one that does 16 `+-` operations in parallel.

However, the SIMD parallelism comes at the cost of hardware being created for each common operation.
A GPU that can do 64 `*+` operations in parallel is larger than one that only does 16 at a time
and creates the columns of the matrix one after another;
and that extra size means extra manufacturing cost and extra time spent moving information around the larger chip.

How much SIMD is happening is hidden from programmer.
We use the `mat4x4` data type and the *` operator
and trust the compiler that shipped from our GPU's supplier
as part of the GPU's device driver
to know whether there's one 64-wide 2-cycle matrix multiply
or a sequence of four 2-cycle vector-matrix multiplies
or a sequence of sixteen 2-cycle dot products.

:::example
A dot $\vec p \cdot vec q$ product of 4-vectors is one vectorized `*+` and one `+-`.

A cross-product of 3-vectors is two vectorized `*+`.

A division of a 4-vector by its largest value is one `?:`, one `1/`, and one vectorized `*+`.
:::

## SIMT

<dfn>Single Instruction, Multiple Threads (<abbr>SIMT</abbr>)</dfn>
is implemented in hardware by lining up several identical complete sets of functional units
and attaching them all to just one control unit
that reads instructions in the software we provide it and decides what all of the different functional units should do at once.

A reasonable way of thinking about SIMT is to imagine your code was being run inside of a `for` loop,
but instead of the loop running your code once, then running it again, then again,
it instead runs it many times all at once.

We call each of these parallel runs a <dfn>thread</dfn> (NVIDIA) or <dfn>work item</dfn> (AMD and Intel).
They are somewhat like threads in a CPU,
in that they can run in parallel and have their own register values,
but unlike threads they are not individually scheduled.
Instead, they are grouped together into large sets^[The group of threads sharing a control unit are called "wavefronts" by AMD, "sub-groups" by Intel, and "warps" by NVIDIA. There are some differences between these three implementations, but not ones that are important to this class.]
that work through the same code at the same time,
just with different inputs.

SIMT significantly changes how we write code.
If an `if` condition depends on an input that might change between the instances running with a shared control unit,
then the control unit has to run *both* branches of the `if`,
<dfn>masking</dfn> the threads so they each ignore the operations on one branch but not the other.
Similarly, if a `for` or `while` loop's iteration count depends on a varying input
then all threads stay in the loop until all are ready to leave it,
with those that would finish early masking out the later iterations.

To help both programmers and GPUs understand which branches and loops are efficient
and which are problematic,
GPU-oriented programming languages distinguish between
two kinds of inputs:

- <dfn>Varying</dfn> inputs may be different for different threads.

- <dfn>Uniform</dfn> inputs are guaranteed by the language structure to be the same for all threads running concurrently.
    They can still change, but only between invocations of the GPU, not between threads of a single invocation.

While there are advanced cases where putting a varying input (or a value derived from it) in the condition of a loop or branch can be correct,
doing so is so often the wrong thing to do that we simply ban it entirely in this course.
If you submit GPU code with a varying involved in an `if`, `for`, or `while`'s condition,
we'll return the code to be fixed instead of grading it.

# Memory

Memory access is slow and complicated.
That is true with CPUs and GPUs, though in different ways.
Rather than try to explain the details of multi-level caching
and why some memory access is slower than others,
this section gives just a few broad principles for GPU memory use.

When the control unit managing a group of threads reaches a memory access instruction,
it sends the requests from all of its threads to memory
and then sets those threads aside.
They sit in an out-of-the-way place^[If you're familiar with reservation stations from out-of-order processor architecture, threads waiting for memory to respond are stored in a similar structure. If you are familair with pipelined processors, you can think of these waiting threads as moving through a long sequence of pipeline registers with no work between them. If you don't know what either of those are, don't worry, this class is not about that level of hardware design.] in the GPU
for a few hundred cycles, doing nothing while they wait for memory to repond.
Only once data is retreived from memory for every thread in the group do they re-enter the rest of the GPU's work.

While one group of threads are waiting for memory,
the processor starts working on another group of threads.
It is quite likely that that next group will also access memory
and also be routed into the memory waiting area.
If all of the threads access memory as their first operation,
it is quite possible to have the waiting area entirely full,
forcing the GPU to pause operatation until at least one of them gets its results from memory.

This design may seem strange, but it is based on a property of how memory works.
Memory (especially memory designed specifically for a GPU)
has high <dfn>throughput</dfn>, meaning it can deliver a large number of bytes per second,
but also high <dfn>latency</dfn>, meaning it takes hundreds of cycles to respond to a single request.
Having a many groups of threads each issue their requests to memory
and then each wait for the result
can take advantage of that high throughput without sitting idle while waiting on the long latency.

Part of how memory gets such high throughput is by providing large blocks of contiguous memory addresses in a single operation.
Because of this, memory accesses where all of the threads in a group
requested addresses that were close together get handled much more quickly than those that scatter their addresses across memory may need several rounds
to give memory time to collect all the relevant data together.

This leads to two guiding principles:

- Smaller data is faster, because more of it can be grabbed with a single memory access.

- Try to access memory densely. Skipping large parts of memory makes memory accesses slower.

A common use of memory in graphics is a texture map,
where a 2D array of data is mapped over the 2D surface of an object.
That useage pattern means that nearby pixels often access nearby regions of memory,
but in a 2D instead of the 1D way memory addresses typically work.
To make 2D-adjacent memory access work well with the 1D layout of memory addresses,
GPUs often reorder texture maps, converting from how they are stored row by row in CPU memory
into a more block-based order.
If you use built-in texture operations this works automatically behind the scenes,
but if you decide you want to directly manage the details of memory it becomes something you need to manage yourself.




