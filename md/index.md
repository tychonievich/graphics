---
title: WebGPU
...

In this course, you will submit assignments using WebGPU. There are several caveats and general points to know about that.


:::tldr
- WebGPU may require manual enabling on some browser+OS pairs.
- WebGPU apps involve 4 languages: HTML and CSS for non-graphics structure, JavaScript for CPU code, and WGSL for GPU code.
- WebGPU has several steps to get access to a GPU that meets application needs.
- Data is sent to the GPU in a two-step process, with a staging buffer separating the memory the CPU uses and the memory the GPU uses.
- GPU buffers have distinct roles. These interact with the built-in parts of the hardware rendering process.
- GPU code is 
    - written in shaders
    - compiled into modules
    - combined into pipelines
    - sequenced with data moves in passes
    - encoded into command buffers
- Code is executed when a command buffer is submitted to the GPU's queue.
:::

# Running WebGPU

WebGPU's purpose is to let a website supply code that will run on the site user's GPU.
While all browsers have had implementations since mid 2024
and the API this has been stable since December 19, 2024,
WebGPU use is still not part of the web baseline.

The main holdup is the fact that WebGPU lets webpages
send data and instructions through a graphics driver to the GPU.
If the driver is fully secure, that process is safe,
but security was not the primary goal of most graphics driver writers
and many drivers are not as secure as web browsers prefer.
As of May 2026, the overall status depends on both the browser and the operating system.

|        | Windows | MacOS | iOS | Android | Linux |
|--------|:-------:|:-----:|:---:|:-------:|:-----:|
| Blink  | ✔       | ✔     | N/A | ✔       | ⚐     |
| Gecko  | ✔       | ✔     | N/A | ✗       | ⚐     |
| WebKit | N/A     | v26+  | v26+| N/A     | ✗     |

Key
:   ✔
    :   WebGPU enabled by default

    ⚐
    :   WebGPU disabled by default, enableable through a configuration flag

    ✗
    :   WebGPU not supported

    v26+
    :   Prior to OS version 26, enableable through a configuration flag; since version 26, enabled by default

    N/A 
    :   This engine+OS pair is not supported
    

This table was last updated May 2026;
you can find more regularly-updated content
on <https://caniuse.com/webgpu>.


Blink is the engine used by Chrome and Edge and many newer smaller browsers.
Gecko is the engine used by Firefox and a few smaller browsers.
WebKit is the engine used by Safari, and by all iOS browsers, and by some old smaller no-longer-supported browsers.

Microsoft has an extensive driver validation process,
so Windows drivers are generally considered to be safe.

Apple has a policy of only supporting a small number of hardware configurations with each OS version.
Safe use with WebGPU was a criteria for the drivers included with
version 26 of both of their operating systems (macOS 26 "Tahoe" and iOS 26).

Android's official version from Google
supports a limited number of hardware configurations
and has generally trusted drivers.
Other hardware platforms typically roll their own fork of Android
and may have lower security overall,
including potentially having insecure graphics drivers.

Linux supports more hardware than any other OS,
and has a wide ecosystem of drivers.
Many of these are secure and safe to use with WebGPU,
but not all are so many browsers require Linux users to opt-in to WebGPU
through a browser settings flag^[Flags are accessed with special URLs; Chrome uses `chrome://flags`, Firefox uses `about:config`].
If you have an off-brand GPU or graphics driver,
you might consider doing that in a browser that you don't usually use for browsing the web
to avoid the security risk the flag was in place to protect against.

:::note
```{=html}
<p id="status"></p>

<script type="module">
async function init() {
  // 1. Check if the API exists in the browser
  if (!navigator.gpu) {
    document.getElementById('status').innerText = "❌ The browser you are viewing this page in does not support WebGPU.";
    return;
  }

  // 2. Try to access the GPU hardware
  const adapter = await navigator.gpu.requestAdapter();
  if (!adapter) {
    document.getElementById('status').innerText = "❌ The browser you are viewing this page in has WebGPU enabled, but can't find a compatible GPU to run on.";
    return;
  }

  // 3. Try to initialize the device
  const device = await adapter.requestDevice();
  
  if (device) {
    document.getElementById('status').innerText = "✅ The browser you are viewing this page in has WebGPU enabled and working.";
  } else {
    document.getElementById('status').innerText = "❌ The browser you are viewing this page in has WebGPU enabled and identified a suitable GPU, but was denied access to that GPU by your operating system or browser security settings.";
  }
}
init();
</script>
```
:::


# Languages

To make a WebGPU app,
you need to provide content in 4 computer languages.

- HTML provides a logical structure to the content that appears on the page.
- CSS provides a declarative description of how that content will be displayed.
- JavaScript provides the code for the part of the app that runs on the CPU.
- WGSL provides the code for the part of the app that runs on the GPU.

We'll basically ignore HTML and CSS in this course;
while some will be needed to provide specific app features,
it will be provided for you as learning these languages is not a goal of this course.

You'll create many JavaScript and WGSL programs in this course.
The details of these languages is not really a learning goal of the course,
but using them effectively will be necessary
so we will cover some of the language ideas.

# Hardware access

WebGPU is designed to work effectively
even on computers that have multiple GPUs each with multiple operating modes.
This leads to a three-step API access model.

1. `navigator.gpu`{.js} represents the browser's WebGPU understanding.
    If it is absent, WebGPU is not enabled on that browser.

2. A GPUAdapter represents a specific GPU.

    A GPUAdapter is obtained with `navigator.gpu.requestAdapter()`{.js}
    and can be queried to see what features it supports
    (how many textures, bit-depth of depth buffer, etc).
    
    You can pass options to the `requestAdapter` call; the most important is `powerPreference`:
    
    - `navigator.gpu.requestAdapter({powerPreference:"low-power"})`{.js} asks for the GPU that uses the least energy.
    - `navigator.gpu.requestAdapter({powerPreference:"high-performance"})`{.js} asks for the GPU that works the fastest and/or has the most features.
    - `navigator.gpu.requestAdapter()`{.js} lets the browser pick; for example it might pick low power if you're on battery and high performance if you're plugged in.
    
3. A GPUDevice represents the webpage's access to a given GPU.
    
    A GPUDevice is obtained with the `.requestDevice()`{.js} method of a GPUAdapter.
    It is what is used to send data, code, and action requests to the GPU.
    
    You can pass options to the `requestDevice` call, but they're rarely needed.
    The most common use case I've seen is to add `requiredFeatures` and `requiredLimits`
    to cause `requestDevice` to reject with an `OperationError` if the specific GPU features needed are not present.

# Bytes and buffers

The fundamental job of WebGPU
is to share work between a GPU and a CPU.
That requires sharing data between them,
either by sharing access to some regions of memory
or by sending data across wires between the two chips.
And if they share data, they must agree on how the data is formatted.

Older graphics APIs like WebGL
hid the data format agreement behind API calls.
That was nice for programmers, but not good for performance.
Newer APIs like WebGPU instead communicate directly in bytes,
with explicit messaging from CPU to GPU to tell the GPU how to interpret those bytes.
That makes the code longer and less clear,
but it also allows more efficient programs.

Because the communication happens in bytes,
the JavaScript will need to use special datatypes with defined byte-level layout,
most often [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray) subclasses like `Float32Array` and `Uint16Array`.

The GPU stores data in <dfn>buffers</dfn>.
Within the context of WebGPU, whenever we say "buffer" we mean data on the GPU, not the CPU.
Because some GPUs have optimized handling of some kinds of data,
WebGPU requires each buffer to have a clear purpose.


## Mapping and copying

WebGPU is designed to support hardware where the GPU is a discrete piece of silicon from the CPU
and each have their own dedicated memory.
That means that getting data between the CPU and GPU is generally a slow process
involving sending the data a few bytes at a time over a wire.
The GPU should neither be blocked from working during this data transfer,
nor should it work on half-sent data.

These considerations have led to a design where the GPU has two kinds of buffers.
There are buffers that the GPU can use during computation,
and there are buffers that are used in CPU/GPU communication.
Both kinds live on the GPU.
A common way these buffers are used is:

1. The CPU sends data to a staging buffer on the GPU.
2. The GPU copies the data from the staging buffer to a working input buffer.
3. The GPU does work, filling up a working output buffer.
4. The GPU copies the data from the working input buffer to a staging buffer.
5. The CPU retrieves data from the staging buffer on the GPU.

The actual copying here might be optimized as an index swap
(e.g. we just swap the base address used by each operation
instead of copying all of the bytes)
or involve some data being modified into a more cache- or processor-friendly format.
The WebGPU API is designed so that these kinds of optimizations are left to the discretion of the GPU designer.

When you create a buffer in WebGPU, you specify how it will be used
with a bitvector representing a set of flags.^[If bitvector sets of flags are new to you, you might want to consult a course that covers bitwise operations, such as the text page I created for [CS 340](https://courses.grainger.illinois.edu/cs340/sp2025/text/bitwise.html#flags-and-bitvectors-as-sets)]
Not all combinations are allowed.

`MAP_WRITE | COPY_SRC`
:   These flags create a staging buffer the CPU sends data to.
    They cannot be combined with other flags.

`MAP_READ | COPY_DST`
:   These flags create a staging buffer the CPU receives data from.
    They cannot be combined with other flags.

Anything with neither `MAP_READ` nor `MAP_WRITE`
:   Creates a buffer that can be used inside GPU computations.
    Each will also a role within the GPU indicated,
    and may also contain `COPY_SRC` and/or `COPY_DST` if they will be used as the source and/or destination of GPU buffer copy operations.

The use of "map" in the flags is based on how WebGPU ensures that data in a staging buffer
is not changed or accessed by the GPU mid-communication.
Each such buffer is in one of two states:
it is either <dfn>mapped</dfn> and can be accessed by the CPU,
it is is <dfn>unmapped</dfn> and it can be accessed by the GPU.

Mapped buffers are exposed to JavaScript as an [ArrayBuffer](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ArrayBuffer),
meaning communication looks like byte-level memory access.
Most often, that ArrayBuffer is accessed through a [TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray)
like `Float32Array` or `Uin16Array`.

There are two special cases with buffer mapping and copying:

If a buffer will have data sent from CPU to GPU exactly once,
the GPU-accessible buffer can be created with `{mappedAtCreation: true}`{.js}.
It will then start as a write-mapped buffer,
but the first time it is unmapped it will be permanently changed to a computation-ready buffer.
This saves the need to make two buffers when the data will never be changed,
as is often the case for the largest data in graphics which was provided by an artist.

If a buffer is small and is being updated by the CPU,
it can be bandwidth-effective to send the new contents of the buffer as part of the copy command
instead of first providing the data and then sending a separate copy command.
Buffers created with `COPY_DST` can use this combined command
though the `device.queue.writeBuffer()`{.js} function.
Note that this is faster than having two buffers for small buffers (a few dozen bytes)
but can be much slower for larger buffers (a kilobyte or more).

## GPU roles of buffers

- <dfn>`UNIFORM`</dfn> buffers
    store data that all GPU threads read from
    and that are immutable during a single GPU run.
    
    Each uniform has two indexes
    which together identify the specific uniform buffer in both the CPU and GPU.
    The first index, called the <dfn>group</dfn>, should be the same for all uniforms that change at the same time;
    the second, called <dfn>binding</dfn>, should distinguish each uniform within the group.

- <dfn>`VERTEX`</dfn> buffers
    store data about a single vertex.
    Vertex shaders run one for each such vertex.

- <dfn>`INDEX`</dfn> buffers
    describe which vertexes are connected into triangles and rasterized.

- <dfn>`STORAGE`</dfn> buffers
    store data to be accessed by compute shaders.
    They can also be used to give vertex or fragment shaders compute-like access to arrays of data.

- <dfn>`INDIRECT`</dfn> buffers
    store data that can parameterize other operations,
    such as the number of vertexes in a vertex buffer.
    
    Indirect buffers are primarily used by WebGPU
    to allow a compute shader to prepare data for a subsequent vertex shader.

- <dnf>`QUERY_RESOLVE`</dfn> buffers
    store the results of certain queries the CPU might ask the GPU to answer
    such as how long some operation took
    or whether a given point is occlused by some geometry.
    
:::example
Simple graphics scenes have multiple artist-created objects
animated by matrices that vary each frame
with lighting that doesn't change.
We might expect:

- Vertex locations and texture coordinates in `VERTEX` buffers, set once and never changed.
- Vertex connectivity in `INDEX` buffers, set once and never changed.
- Matrices and lighting in `UNIFORM` buffers, changed each frame.

If one of the objects was melting with CPU-computed new vertex positions each frame,
that would still be in a `VETEX` buffer (now also `COPY_DST`)
but may lead to CPU-to-GPU bandwidth being a limiting factor.

If one of the objects was melting with GPU-computed new vertex positions each frame,
they'd be computed in a `STORAGE` buffer (also `COPY_SRC`)
and then copied to the `VETEX` buffer (also `COPY_DST`).
If the number of vertices changed frame-to-frame, that would be in an `INDIRECT` buffer.
:::



## Textures are slightly different

Conceptually, a texture is just a 2D (usually) array of floats or vectors,
and could be handled through a buffer.
But textures are used so often that GPUs have dedicated hardware that handled their common usage patterns
more efficiently than more general buffers.

In practice, this means

- Textures are treated as a different kind of GPU object than buffers in the WebGPU API.
- You can copy from a staging buffer to texture, like you would to a GPU buffer.
- There's also a `device.queue.writeTexture()`{.js} function that handles the staging buffer invisibly for you.
- There's also a `device.queue.copyExternalImageToTexture()`{.js} function that has the browser handle all of decoding an image codec, sending the pixels to the GPU, and copying it into a texture.

Textures have special hardware dedicated to accessing them efficiently,
with several access patterns exposed in WebGPU as <dfn>sampler</dfn> objects.

Textures can also have a `STORAGE_BINDING` role
which lets compute shaders access them by pixel index,
much like they can access `STORAGE` buffers by index.

The frame buffer which rendering fills with the new image each frame
is also a texture,
though typically created in WebGPU with a Canvas method
that hooks the canvas into the browser's rendering engine
and handles displaying each new frame automatically.


# Giving the GPU instructions

To use a GPU, we need to tell it what to do.
This is done in several steps.

## Shaders and pipelines

GPU code is called a "shader"^[This name dates from the first shaders, which were limited to just computing the lighting (or shade) of each pixel -- a subset of what fragment shaders do now. Modern shaders can do much more than that, but the name "shader" is still used.];
there are several shader languages; WebGPU uses WGSL, which uses Rust-like syntax.

Shaders are compiled by a combination of the browser and the graphics driver,
using the `device.createShaderModule()`{.js} method.
The compiled code lives on the GPU;
an identifier or handle to this compiled code^[similar in some ways to an open file descriptor]
is returned as a `GPUShaderModule` object.

For common graphics purposes, shaders are then combined into a render pipeline^[There are also compute pipelines, with are similar with less graphics-oriented structure.].
The pipeline is created using `device.createRenderPipeline()`{.js}
passed an object describing which shader functions to call for each step of the rendering
and how to store the results.

## Passes and command buffers and encoders

The code and configuration represented by a shader module, render pipleine, and pass descriptor
still need to be executed,
and generally executed along with several other activities
like providing the vertex positions of geometry
and the values of uniforms.

A sequence of executions is described as a command buffer,
which is created using a command encoder.
The command buffer contains a sequence of passes,
each of which contains several actions to take.
The general structure is

1. `encoder = device.createCommandEncoder()`{.js} gives an encoder to be used.

2. One or more pass is created, each as something like

    a. `pass = encoder.beginRenderPass(pass_descriptor)`{.js}
        
        The `pass_descriptor` contains options for the fixed hardware part of the graphics pipeline,
        such as how new pixels should be placed in the frame buffer.
    
    b. `pass.setPipeline(pipeline)`{.js}
    c. Any needed data provision
    d. `pass.draw(vertex_count)`{.js}
    e. `pass.end()`{.js} 
    
    Command passes have different specifics, but follow a similar overall design.

3. `buffer = encoder.finish()`{.js} tells the encoder the command buffer is complete and returns a message that can be sent to the GPU to run the commands in that command buffer.

The resulting command buffer can be used once or many times;
it works like a function or program that runs on the GPU
as often as we care to invoke it.

## Command queue

Commands are run on the GPU by submitting a command buffer to queue.
This is a simple function:
`device.queue.submit([command_buffer, /*... another command buffer, ...*/])`{.js}

In most cases, the queue is fire-and-forget:
you tell the queue what commands to run
and then move on to other things.
If you need to wait for it to complete
(for example to retrieve data from a `MAP_READ` buffer),
the queue has an `onSubmittedWorkDone()` method that can insert that wait.

The queue also has several convenience methods
for sending data to the GPU,
as noted in the buffers and textures sections above.
