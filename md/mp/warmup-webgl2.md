---
title: 'Warmup – HTML, Javascript, and WebGL'
header-includes: |
    <style>div > dl > dt  { clear: right; }</style>
...

The goal of this warmup is to ensure you can make a WebGL2 program,
run it on your own computer,
and run it on the submission server.
In theory this will mean just a little copy-paste of code we provide here;
in practice it will likely mean working around a few setup challenges.

# Overview

You will submit four files:

- One `.html` file
- One `.js` file
- Two `.glsl` files

You may also submit `.css` files if you wish.
Do not include spaces in file names as the submission server does not process them well.

If you need a specific directory structure, upload a `.zip` or `.tar` that contains those files.
The logic for handling submissions is

a. If you submitted a `zip` or `tar`, we extract it
    i. While it contains exactly one directory and no `.html` files, we remove the outer directory
a. If there's exactly one `.html` file, we use that
a. Otherwise, report an upload format error

Before submitting, you should verify that you can run your code on your development machine.
You'll likely need to [run a local server to bypass CORS limitations](../text/cors.html) to get that to work.

# Specification

You may diverge from this specification if you wish, as this warmup is not graded.
However, if you are unable to do what this specification says you are highly unlikely to be able to get any of the subsequent WebGL2 MPs to work.

## Fragment shader

In a file with a `.glsl` ending, put

```glsl
#version 300 es
precision highp float;
out vec4 color;
void main() {
    color = vec4(1, 0, 0.5, 1);
}
```

## Vertex shader

In a file with a `.glsl` ending, put

```glsl
#version 300 es
uniform float seconds;
uniform int count;
void main() {
    float rad = sqrt((float(gl_VertexID)+0.5)/float(count));
    float ang = 2.399963229728653 * float(gl_VertexID) + seconds;
    gl_Position = vec4(rad*cos(ang), rad*sin(ang), 0, 1);
    gl_PointSize = 4.0;
}
```

## Javascript driver

In a file with a `.js` ending, put four functions: setup, compile, tick, and draw

```js
/**
 * Fetches, reads, and compiles GLSL; sets two global variables; and begins
 * the animation
 */
async function setup() {
    window.gl = document.querySelector('canvas').getContext('webgl2')
    const vs = await fetch('path to your vertex shader file.glsl').then(res => res.text())
    const fs = await fetch('path to your fragment shader file.glsl').then(res => res.text())
    window.program = compile(vs,fs)
    tick(0) // <- ensure this function is called only once, at the end of setup
}
```


```js
/**
 * Compiles two shaders, links them together, looks up their uniform locations,
 * and returns the result. Reports any shader errors to the console.
 *
 * @param {string} vs_source - the source code of the vertex shader
 * @param {string} fs_source - the source code of the fragment shader
 * @return {WebGLProgram} the compiled and linked program
 */
function compile(vs_source, fs_source) {
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


```js
/**
 * Runs the animation using requestAnimationFrame. This is like a loop that
 * runs once per screen refresh, but a loop won't work because we need to let
 * the browser do other things between ticks. Instead, we have a function that
 * requests itself be queued to be run again as its last step.
 * 
 * @param {Number} milliseconds - milliseconds since web page loaded; 
 *        automatically provided by the browser when invoked with
 *        requestAnimationFrame
 */
function tick(milliseconds) {
    const seconds = milliseconds / 1000
    draw(seconds)
    requestAnimationFrame(tick) // <- only call this here, nowhere else
}
```


```js
/**
 * Clears the screen, sends two uniforms to the GPU, and asks the GPU to draw
 * several points. Note that no geometry is provided; the point locations are
 * computed based on the uniforms in the vertex shader.
 *
 * @param {Number} seconds - the number of seconds since the animation began
 */
function draw(seconds) {
    const count = 6+(seconds*10)%100          // number of vertices to draw

    gl.clear(gl.COLOR_BUFFER_BIT)
    gl.useProgram(program)
    gl.uniform1f(program.uniforms.seconds, seconds)
    gl.uniform1i(program.uniforms.count, count)

    const connection = gl.POINTS
    const offset = 0                          // unused here, but required
    gl.drawArrays(connection, offset, count)
}
```

In addition to these functions, put a call to get them started at the top level (outside of any function)

```js
window.addEventListener('load', setup)
```

## HTML file

Include the usual HTML boilerplate

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>WebGL Warmup</title>
    <script src="path to your javascript file.js"></script>
</head>
<body>
```
...
```html
</body>
</html>
```

In the body, create a square canvas:

```html
<canvas width="300" height="300" style="background:yellow"></canvas>
```

# Evaluating your results

On both your development machine
and when submitted to the submission server and then viewed by clicking the HTML link,
the resulting animation should look like this:

<figure>
<video controls autoplay loop>
<source src="vid/warmup-webgl2.webm" type="video/webm"/>
<source src="vid/warmup-webgl2.mp4" type="video/mp4"/>
</video>
<figcaption>
A video of an example result.
</figcaption>
</figure>

