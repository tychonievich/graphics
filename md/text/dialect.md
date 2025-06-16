---
title: Our Dialect of WebGL2
summary: Some choices CS 418 makes for you, and why they are not always the right ones.
header-includes:
  - |
    <style>
      .bad { background: rgba(0,0,0,0.0625); border-color: rgba(0,0,0,0.1225); }
      .bad > :first-child:before { color:inherit; content:"Out-of-dialect example \2014\00A0 "; }
    </style>
...

Over time, graphics APIs have become more flexible and more complicated.
What was a 10-line program in OpenGL1 might take 500 lines in Vulkan,
but OpenGL1 was limited to just a few kind s of images
while Vulkan can create myriad visual effects and do considerable computation too.

WebGL2 is somewhere in the middle of this spectrum.
It is designed to render images only, with little to no support for non-graphics computation,
but within that limitation is has considerable flexibility.

In any sufficiently complicated language, programmers naturally pick a dialect to program in,
intentionally picking a subset of its options to keep the code readable and maintainable.
For example, C++ can allocate memory using `new`, `malloc`, `mmap`, `shm_open`, or several other methods
but it would be quite unusual to try to use more than one or two of these in a single programming project.
The remainder of this page describes several dialect choices CS 418 requires.

Most of this dialect is checked for by [wrapWebGL2.js](../code/wrapWebGL2.js),
with warnings about violations displayed in the console.

# Attribute locations

An *attribute* provides per-vertex data and is sent to the GPU via a *buffer*.
The GPU identifies buffers by indices (which WebGL2 calls "locations"), typically 0 through 15,
and all CPU-GPU communication uses those indices.
But source code uses variable names instead.

WebGL2 offers two ways to pair attribute names with attribute locations.

One way is to let the GLSL compiler assign attribute locations and query the compiler state to determine their locations.

:::{.example .bad}
Compiler-assigned attribute locations can be created with a vertex shader like
```glsl
#version 300 es
in vec4 position;
main {
  gl_Position = position;
}
```
and corresponding JavaScript code
```js
const positionLoc = gl.getAttribLocation(program, "position")
gl.vertexAttribPointer(positionLoc, data[0].length, gl.FLOAT, false, 0, 0)
gl.enableVertexAttribArray(positionLoc)
```
We will not use this pattern in CS 418.
:::

The compiler-assigned technique makes for more readable code,
but it also means that locations are shader-program specific.
When I started teaching WebGL2 I assumed this would be the right choice because readability aids learning;
however, it caused significant headaches once we switched to more involved scenes with multiple programs.
It is no longer the CS 418 dialect.

The other way is to assign the locations manually in the GLSL source and use those same locations manually.

:::example
Manually-assigned attribute locations can be created with a vertex shader like
```glsl
#version 300 es
layout(location=0) in vec4 position;
main {
  gl_Position = position;
}
```
and corresponding JavaScript code
```js
const positionLoc = 0;
gl.vertexAttribPointer(positionLoc, data[0].length, gl.FLOAT, false, 0, 0)
gl.enableVertexAttribArray(positionLoc)
```
:::

The manual technique makes for less readable code, with stray numbers in the JavaScript that have no obvious meaning, though that can be partially mitigated with good named constants.
However, it also makes attributes, and hence vertex array objects and scene geometry generally,
work the same for all shader programs your application might use,
allowing much easier implementation of multi-material scenes.
Thus, the manual technique is the designated CS 418 dialect.

# Uniform structure and location

Like [attributes](#attribute-locations), *uniforms* are identified by the GPU using locations.
However, unlike attributes, WebGL2 does not support manual location specification for uniforms.
To help communicate that uniform locations may differ for the same uniform name between different shader programs,
CS 418 dialect stores the locations in the compiled program object right after it is compiled
and only accesses the locations thereafter from that compiled source.

:::example
Immediately after compiling a shader program, we retrieve all uniform locations as
```js
const uniforms = {}
for(let i=0; i<gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS); i+=1) {
    let info = gl.getActiveUniform(program, i)
    uniforms[info.name] = gl.getUniformLocation(program, info.name)
}
program.uniforms = uniforms
```
and thereafter access uniforms using that stored location
```js
gl.uniformMatrix4fv(program.uniforms.p, false, projectionMatrix)
```
:::

WebGL2 also supports something called *uniform buffers*,
which are a way to collect several uniforms into a a struct- or array-like collection.
These can help organize your code,
can reduce the number of calls needed to send uniform values to the GPU,
and can provide more uniform values that the available set of locations would permit.
We will not need those features in this class, so we will not use uniform buffers in the CS 418 dialect.

# Compiling shaders

In WebGL2, a shader program consists of a compiled vertex shader
and compiled fragment shader
linked together.
The compiling and linking are broken into several steps,
which can allow various features such as

- Having a fancy shader that some browsers can't compile and a fallback shader to use if compilation of the fancy one fails.
- Compiling a vertex shader once and then linking it with several different fragment shaders to efficiently render multiple materials.
- Providing custom error messages when compilation or linking fails, possibly including guidance to the user on how to resolve those issues.

We won't use any of these features, so the flexibility of the compilation and linking process will not be needed.
Instead, we'll always use the same compilation function,
which will also handle [collecting uniform locations](#uniform-structure-and-location)

```js
/**
 * Compiles two shaders, links them together, looks up their uniform locations,
 * and returns the result. Reports any shader errors to the console.
 *
 * @param vs_source - the source code of the vertex shader
 * @param fs_source - the source code of the fragment shader
 * @throws {Error} if compilation or linking fails
 * @return the compiled and linked program, with additional field `.uniforms`
 *         storing all uniform locations in the program
 */
function compileShader(vs_source, fs_source) {
    const vs = gl.createShader(gl.VERTEX_SHADER)
    gl.shaderSource(vs, vs_source)
    gl.compileShader(vs)
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(vs))
        throw Error("Vertex shader compilation failed")
    }

    const fs = gl.createShader(gl.FRAGMENT_SHADER)
    gl.shaderSource(fs, fs_source)
    gl.compileShader(fs)
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(fs))
        throw Error("Fragment shader compilation failed")
    }

    const program = gl.createProgram()
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
    
    const uniforms = {}
    for(let i=0; i<gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS); i+=1) {
        let info = gl.getActiveUniform(program, i)
        uniforms[info.name] = gl.getUniformLocation(program, info.name)
    }
    program.uniforms = uniforms

    return program
}
```

# GLSL languages

WebGL2 supports two different shader languages:
GLSL 2.0 ES and GLSL 3.0 ES.
These have a variety of syntactic differences, such as what GLSL 3.0 ES calls an "`in`"
being called an "`attribute`" or "`varying`" in GLSL 2.0 ES.

We will only use GLSL 3.0 ES in CS 418.
That means that every shader [must]{style="font-variant:small-caps"}
begin with the exact string "`#version 300 es`{.glsl}".

GLSL also allows C-style macros. The CS 418 dialect does not use these.

# Warp parallelism

GPUs are more efficient than CPUs because they are very highly parallel.
That high degree of parallelism comes in part by having dozens of threads move through the exact some code in lock-step,
differing only in what attribute values they are given.
A group of lock-step threads is sometimes called a *warp*.

Some control constructs can break a warp, forcing the GPU to run every branch of the code instead of just some.
Occasionally breaking a warp can be the right thing to do, but it very rarely is.
In CS 418 we forbid warp-breaking code.

In particular, we define an *input-dependent expression* as follows:

input-dependent expression
:   - Any expression containing an `in` variable.
    - Any expression containing a local variable that was computed using an input-dependent expression.

We forbid using input-dependent expressions in the following places

- The guard of an `if`; e.g. `if (here)`{.glsl}
- The guard of a `while`; e.g. `while (here)`{.glsl}
- The guard of a `for`; e.g. `for (...; here; ...)`{.glsl}

We allow using input-dependent expressions everywhere else, notably including expression-level conditionals such as

- The first term of a short-circuit logical operation such as `here && ...`{.js} and `here || ...`{.glsl}
- The guard of the trinary operator `here ? ... : ...`{.glsl}

# Null on failures

Various WebGL2 functions return `null` when they fail to operate correctly
rather than throwing any kind of error.
This can allow graceful failures when a given browser is not able to handle certain calls appropriately,
but it can also mean that programmer errors go undetected.

To help catch the programmer errors, the CS 418 dialect forbids
writing code that provides `null` arguments to WebGL2 functions
or invokes WebGL2 functions in ways that produce a `null` return value.

# requestAnimationFrame

Not really WebGL but related to creating animations:
Javascript provides multiple animation-creating functions,
including `setTimeout`, `setInterval`, and `requestAnimationFrame`.
Each of these has different properties, and each can be used in several ways to create various animated and time-delayed behaviors.

In CS 418, we only use `requestAnimationFrame` to create animated or time-delayed behavior;
`setTimeout` and `setInterval` are not permitted.

Each invocation of `requestAnimationFrame` queues a function to be invoked once on the next screen refresh.
If it is invoked ten times in a given frame, ten function invocations will be attempted on the next screen refresh.
Having multiple queued functions is a useful technique for organizing complicated pages with multiple animated elements,
but in the context of CS 418 it usually results from coding errors and can cause browsers to freeze or in some rare cases even entire computers to crash.
Because of this, we require that at most one `requestAnimationFrame` is pending at any given time.

We recommend achieving this by the following:

1. Define a single function that `requestAnimationFrame`s itself as its last operation.
    Keep this function as simple as possible, deferring all interesting per-frame work to other functions.
    
    <div class="example">
    
    ````js
    function tick(milliseconds) {
        const seconds = milliseconds / 1000
        const dt = seconds - (window.lastSeconds || 0)
        window.lastSeconds = seconds
        
        updateState(dt)
        draw(seconds)
   
        requestAnimationFrame(tick)
    }
    ````
    
    </div>

2. Request that that function be invoked once, after getting a WebGL2 rendering context
    and doing any other needed scene setup
    in a window load callback
    
    <div class="example">
    
    ````js
    window.addEventListener('load', async (event) => {
        window.gl = document.querySelector('canvas').getContext(
            'webgl2',
            {antialias: false, depth:true, preserveDrawingBuffer:true}
        )
        
        // ... other setup here
        
        requestAnimationFrame(tick)
    })
    ````
    
    </div>
