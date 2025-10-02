---
title: Minimal WebGL
author:
    - Luther Tychonievich
license: CC-BY-SA
summary: What WebGL 2 accepts, what it requires, and how to get started.
...


At an absolute minimum, the GPU must be told

1. What GPU program to use
2. How many vertices there are
3. How the vertices are combined into primitives

# GPU Program

A program consists of a vertex shader and a fragment shader.

## Vertex Shader

A vertex shader has access to 

- Any inputs we sent the GPU
- `int gl_VertexID`: a 0-based index of the current vertex within the set of vertices created by the current drawing command
- `int gl_InstanceID`: a 0-based index that is always 0 unless we use one of the special "instanced" drawing commands

The vertex shader may set the following outputs:

- `vec4 gl_Position`: The homogeneous coordinate to use for rasterizing this vertex
- `float gl_PointSize`:  Only used for point primitives, the pixel width of the square to draw around this vertex
- Any `out` variables we define

An example using only built-in components might be

```glsl
#version 300 es
void main() {
  gl_Position = vec4(sin(float(gl_VertexID)),
                     cos(float(gl_VertexID)),
                     0,
                     1);
}
```

:::note
Most functions and operators in GLSL do *not* convert integers to floating-point numbers automatically. If you tried `sin(gl_VertexID)`{.glsl} you'd get the error message

    ERROR: 0:3: 'sin' : no matching overloaded function found

One of the few exceptions are the vector and matrix creation functions like `vec4`, which is why we could write `0` instead of `0.0` as an argument to `vec4`.
:::

## Fragment Shader

A fragment shader has access to

- the interpolated value of any outputs of the vertex shader
- `vec4 gl_FragCoord`, with window-space coordinates $(x,y,z,\frac{1}{w})$
- `bool gl_FrontFacing`, true for all lines and points, determined by handedness of triangles
- `vec2 gl_PointCoord`, only set for points if point sprites are enabled: where in the point this fragment is located; both `gl_PointCoord.x` and `gl_PointCoord.y` range from 0 to 1

The fragment shader may set the following outputs:

- `float gl_FragDepth`, which will be clamped to the 0--1 range; defaults to `gl_FragCoord.z` if not set
- one `out vec4` color output per layer (most programs have just one layer[^layers])

[^layers]:
    The most common use of multiple layers, more commonly called [multiple render targets](https://en.wikipedia.org/wiki/Multiple_Render_Targets), is to implement [deferred shading](https://en.wikipedia.org/wiki/Deferred_shading).

Fragment shaders also have a special keyword `discard` which, if executed, terminates processing for the current fragment and does not render the fragment.

An example using only built-in components and the required output might be

```glsl
#version 300 es
precision highp float;
out vec4 anyNameYouWant;
void main() {
    anyNameYouWant = vec4(1, 0, 0.5, 1);
}
```

:::note
GLSL offers three qualitative levels of precision for floating-point numbers (`lowp`, `mediump`, and `highp`), and requires the fragment shader to pick one.
:::

## Compiling, Linking, and Loading

### Compiling 

Each shader needs to be compiled in the browser that will use it before use.
Like all compilation, compiling will

- Checks for syntax and type errors in the source
- Create an executable binary format that can be run

Because the compilation happens in the browser on every page load, compiling will also

- Verify the shader uses only features the GPU can use
- Compile to a binary format specific to the host hardware

You *cannot* save the result of compilation as a file.
Instead, compilation returns an opaque JavaScript object you can use to refer to the compiled shader within the given browser session only.

Compiling in WebGL is performed four parts:

1. Allocate a shader object to hold the compiled results

    ````js
    let shader = gl.createShader(gl.VERTEX_SHADER)
    ````
    
    or

    ````js
    let shader = gl.createShader(gl.FRAGMENT_SHADER)
    ````

2. Assign GLSL source code to the shader object

    ````js
    gl.shaderSource(shader, sourceCode)
    ````
    
3. Compile the source code

    ````js
    gl.compileShader(shader)
    ````

4. Check for any compilation errors

    ````js
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(shader))
        throw Error("Shader compilation failed")
    }
    ````

### Linking 

A fragment and vertex shader needs to be linked into a program.
Linking verifies that the fragment shader inputs are matched by vertex shader outputs.

Linking in WebGL is performed in four parts:

1. Allocate a program object to hold the linked results

    ````js
    let program = gl.createProgram()
    ````

2. Tell it which shaders to use

    ````js
    gl.attachShader(program, compiledVertexShader)
    gl.attachShader(program, compiledFragmentShader)
    ````
    
3. Link

    ````js
    gl.linkProgram(program)
    ````

4. Check for any linking errors

    ````js
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
    ````

You may discard shaders after they are linked into a program.

If you plan to have several programs that share the same vertex shader with different fragment shaders (or vice versa) you should use the same compiled shader object for them all to avoid having duplicates of the code in the GPU.


### Loading

A linked shader program must be loaded as the active program before use.
This is done with a single invocation:

````js
gl.useProgram(linkedProgram)
````

You may have as many linked shader programs as you wish:
swapping between them can create different visual effects with the same source data.
Only one program can be active at a time---loading one unloads whatever was loaded before.

Note that linking a program does *not* automatically load the program.

If your WebGL app only has one GLSL program, you can discard the linked program after calling `useProgram`.
You may also keep programs around so that you can swap programs to get different visual effects.

Compiling and linking are relatively resource-intensive, and are generally done only during the setup stage of an app.
Loading much less expensive and can be done several times every frame if desired.


# HTML and JavaScript

WebGL is used to render parts of a webpage, to be viewed in a web browser.
Thus, to use it we need to embed it in a webpage.

Browsers expect web pages to be defined in HTML,
optionally styled with CSS,
and to have code written in JavaScript.

## HTML

You should use HTML5, indicated by starting your HTML file with `<!DOCTYPE html>`{.html}.

Every valid HTML document needs an outer `html` element
containing (1) a `head` containing a `title` and (2) a `body`.
WebGL renders into a `canvas` in the `body`,
which should be given a `width` and `height` (measured in pixels). 

We'll also need a `script` to store JavaScript in.
Technically that can go anywhere, but it is traditional to put it in the `head`.

```html
<!DOCTYPE html>
<html>
<head>
<title>Minimal HTML to support WebGL</title>
<script>
// to do: add JavaScript here
</script>
</head>
<body>
<canvas width="300" height="300"></canvas>
</body>
</html>
```

:::aside
Serving your HTML page

Your browser can open HTML pages on your hard drive
by using the `file://` scheme.
But there's a security risk inherent in that,
so many features of HTML are disabled if served as a `file://`.
For this minimal example it won't matter,
but for most WebGL programs you'll need to run a local webserver
in order to successfully view your WebGL program on your computer.
:::

## JavaScript

### Code structure

JavaScript may begin running before your webpage is fully loaded.
In particular, that means that the `canvas` element might not yet exist,
and thus that we might not be able to do any WebGL processing up front.

It is thus traditional to have the `script` define global variables functions,
and tell the browser to run any WebGL-specific initialization after the entire page loads.

```js
function compileAndLinkGLSL() {
    // to do: write me
}
function draw() {
    // to do: write me
}
window.addEventListener('load',(event)=>{
    window.gl = document.querySelector('canvas').getContext('webgl2')
    compileAndLinkGLSL()
    draw()
})
```

Note that the `window.` prefix on an the `gl` assignment makes the `gl` variable global.

### Setup

To `compileAndLinkGLSL` we'll need our shader code as strings;
there are many ways to do this, but one way is to use backtick-delimited strings.

```js
function compileAndLinkGLSL() {
    const vs_source = `#version 300 es
    void main() {
      gl_Position = vec4(sin(float(gl_VertexID)),
                         cos(float(gl_VertexID)),
                         0,
                         1);
    }`

    const fs_source = `#version 300 es
    precision highp float;
    out vec4 anyNameYouWant;
    void main() {
        anyNameYouWant = vec4(1, 0, 0.5, 1);
    }`
    // ...
```

and then the compiling and linking code from [above](#compiling-linking-and-loading):

```js
    // ...

    let vs = gl.createShader(gl.VERTEX_SHADER)
    gl.shaderSource(vs, vs_source)
    gl.compileShader(vs)
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
        consol.error(gl.getShaderInfoLog(vs))
        throw Error("Vertex shader compilation failed")
    }

    let fs = gl.createShader(gl.FRAGMENT_SHADER)
    gl.shaderSource(fs, fs_source)
    gl.compileShader(fs)
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
        consol.error(gl.getShaderInfoLog(fs))
        throw Error("Fragment shader compilation failed")
    }

    window.program = gl.createProgram()
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
}
```

Note the use of `window.program` to make the program global.
We don't technically need to do that here, but it is good practice for when we later have multiple GLSL programs in one WebGL application.

### Drawing a frame

To `draw` we tell WebGL which program to use
and what data to use when drawing.
For this simple example, the only data it needs 
is how many vertices to process
and which kind of primitive to use in connecting them:

```js
function draw() {
    const connection = gl.LINES // or gl.TRIANGLES or gl.POINTS
    const offset = 0            // unused here, but required
    const count = 12            // number of vertices to draw
    gl.drawArrays(gl.LINES, offset, count)
}
```

# Full example

<canvas id="example1" width="300" height="300" style="border: thin solid black; background:white; width:300; heiht:300;"></canvas>

~~~html
<!DOCTYPE html>
<html>
<head>
<title>Minimal HTML to support WebGL</title>
<script>
function compileAndLinkGLSL() {
    const vs_source = `#version 300 es
    void main() {
      gl_Position = vec4(sin(float(gl_VertexID)),
                         cos(float(gl_VertexID)),
                         0,
                         1);
    }`

    const fs_source = `#version 300 es
    precision highp float;
    out vec4 anyNameYouWant;
    void main() {
        anyNameYouWant = vec4(1, 0, 0.5, 1);
    }`

    let vs = gl.createShader(gl.VERTEX_SHADER)
    gl.shaderSource(vs, vs_source)
    gl.compileShader(vs)
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
        consol.error(gl.getShaderInfoLog(vs))
        throw Error("Vertex shader compilation failed")
    }

    let fs = gl.createShader(gl.FRAGMENT_SHADER)
    gl.shaderSource(fs, fs_source)
    gl.compileShader(fs)
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
        consol.error(gl.getShaderInfoLog(fs))
        throw Error("Fragment shader compilation failed")
    }

    window.program = gl.createProgram()
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
}

function draw() {
    gl.useProgram(program)
    const connection = gl.LINES // or gl.TRIANGLES or gl.POINTS
    const offset = 0            // unused here, but required
    const count = 12            // number of vertices to draw
    gl.drawArrays(gl.LINES, offset, count)
}

window.addEventListener('load',(event)=>{
    window.gl = document.querySelector('canvas').getContext('webgl2')
    compileAndLinkGLSL()
    draw()
})
</script>
</head>
<body>
<canvas width="300" height="300"></canvas>
</body>
</html>
~~~


<script>
function compileAndLinkGLSL() {
const vs_source = `#version 300 es
void main() {
gl_Position = vec4(sin(float(gl_VertexID)),
cos(float(gl_VertexID)),
0,
1);
}`
const fs_source = `#version 300 es
precision highp float;
out vec4 anyNameYouWant;
void main() {
anyNameYouWant = vec4(1, 0, 0.5, 1);
}`
let vs = gl.createShader(gl.VERTEX_SHADER)
gl.shaderSource(vs, vs_source)
gl.compileShader(vs)
if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
consol.error(gl.getShaderInfoLog(vs))
throw Error("Vertex shader compilation failed")
}
let fs = gl.createShader(gl.FRAGMENT_SHADER)
gl.shaderSource(fs, fs_source)
gl.compileShader(fs)
if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
consol.error(gl.getShaderInfoLog(fs))
throw Error("Fragment shader compilation failed")
}
window.program = gl.createProgram()
gl.attachShader(program, vs)
gl.attachShader(program, fs)
gl.linkProgram(program)
if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
console.error(gl.getProgramInfoLog(program))
throw Error("Linking failed")
}
}
function draw() {
gl.useProgram(program)
const connection = gl.LINES // or gl.TRIANGLES or gl.POINTS
const offset = 0            // unused here, but required
const count = 12            // number of vertices to draw
gl.drawArrays(gl.LINES, offset, count)
}
window.addEventListener('load',(event)=>{
window.gl = document.querySelector('canvas#example1').getContext('webgl2')
compileAndLinkGLSL()
draw()
})
</script>
