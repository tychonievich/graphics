---
title: Using video memory
summary: Achieving faster drawing through buffers of bytes.
...

High-end graphics cards have dedicated video memory that is distinct from main memory.
There are many reasons why this is desirable for graphics card performance,
but we need to know it because graphics APIs, including WebGL, are designed to make the two-memories model work.

This page discusses only **attributes**, which provide per-vertex information,
and their connectivity into primitives.
Uniforms and samplers are also stored in video memory, but are out of scope for this page.

 

Vertex attributes are values supplied per-vertex to the vertex shader.
In the vertex shader, they are specified with the `in` keyword.

Attributes are usually floating-point values
or vectors of up to four floating-point values.

The vertex shader can access up to 16 attributes.
These are provided in numbered "locations", 0 through 15.
When you provide a vertex shader you can either specify the location of each attribute directly by `in layout(location=3) vec4 p`{.glsl}
or leave the locations unspecified by `in vec4 n`{.glsl}
and let the shader compiler pick the location for you.
We do need locations, though, so if we let the compiler pick them
we later ask the compiler where they ended up
using `gl.getAttribLocation(program, 'n')`{.js}.
Letting the compiler pick them also makes it harder to use multiple shader programs with the same geometry, so we'll use direct location specification.

 

Attributes are sent to the GPU in arrays of bytes known as **buffers**.

CPU setup
:   1. Determine the per-vertex data.

    2. Store it in one or more arrays.
        
        Arrays need to be in the same order, but may be interleaved.
        For example, the following shows two ways to provide the same data:
        
        ````js
        pos = [ [-1,-1], [ 1,-1], [ 1, 1], [-1, 1] ]
        col = [ [0,0,0], [1,0,0], [0,1,0], [0,0,1] ]
        
        interleaved = [
            [-1,-1], [0,0,0],
            [ 1,-1], [1,0,0],
            [ 1, 1], [0,1,0],
            [-1, 1], [0,0,1],
        ]
        ````

    3. Flatten the arrays using the `.flat()` method.
        This removes all internal arrays and just keeps the values in order.
        
        ````js
        pflat = pos.flat() // = [-1,-1,1,-1,1,1,-1,1]
        cflat = col.flat() // = [0,0,0,1,0,0,0,1,0,0,0,1]
        
        iflat = interleaved.flat()
        // = [-1,-1,0,0,0, 1,-1,1,0,0, 1,1,0,1,0, -1,1,0,0,1]
        ````

    4. Encode the values in the arrays into bytes using the `new Float32Array` constructor.
        
        ````js
        pbytes = new Float32Array(pflat)
        // still looks like [-1,-1,1,-1,1,1,-1,1]
        // but now stored as bytes (little-endian on most CPUs):
        // 00 00 80 BF  00 00 80 BF  00 00 80 3F  00 00 80 BF
        // 00 00 80 3F  00 00 80 3F  00 00 80 BF  00 00 80 3F
        ````

Send data to a buffer in video memory
:   5. Allocate a buffer to store bytes in video memory.
        We'll need one buffer for each byte-encoded array.
    
        ````js
        buf = gl.createBuffer()
        ````
    
    6. Prepare a route to send data to that buffer.
    
        ````js
        gl.bindBuffer(gl.ARRAY_BUFFER, buf)
        ````

    7. Copy bytes into the buffer.
    
        ````js
        gl.bufferData(gl.ARRAY_BUFFER, pbytes, hint)
        ````
        
        The `hint` is either `gl.DYNAMIC_DRAW`{.js}
        which tells the GPU "I'm going to send new bytes into this buffer often so place it somewhere easy to modify and don't waste time optimizing it";
        of `gl.STATIC_DRAW`{.js}
        which tells the GPU "I'm going to draw this data many many times before I change it so place it somewhere easy to access and optimize it for faster reads."
    

Tell the GPU how to parse the buffer
:   8. Make a vertex array object to store some future setup in.
    
        ````js
        vao = gl.createVertexArray()
        ````

    9. Record the next parts into the vertex array object.
        This same function also reactivates what it's recorded later during drawing.
    
        ````js
        gl.bindVertexArray(voa)
        ````
    
    10. Make sure we have the vertex shader locations of the attributes.
        
        We might have these as constants due to using `in layout(location = 0) vec4 pos`{.glsl} or the like in the vertex shader,
        or we might retrieve them using `gl.getAttribLocation`{.js}.
    
    11. For each attribute, use `gl.vertexAttribPointer`{.js} with its six arguments that tell the GPU how to parse the bytes.
    
        12. Pick a buffer using `gl.bindBuffer(gl.ARRAY_BUFFER, buf)`{.js}.
            
            This example will assume the interleaved buffer.
        
        13. Pass in an attribute location
        
            ````js
            gl.vertexAttribPointer(pos_loc,
            ````
        
        14. Pass in how many number are used per vertex for that attribute.
            
            ````js
            gl.vertexAttribPointer(pos_loc,
                2, // because pos is a 2-vector
            ````
            
            Note that this is the number of values per vertex for the attribute *in the byte-serialized data*, which may be larger or smaller than the number in the vertex shader `in` variable type.

        15. Pass in the byte format used.
            Assuming we used a `Float32Array` in step 4, with is `gl.FLOAT`
            
            ````js
            gl.vertexAttribPointer(pos_loc,
                2,
                gl.FLOAT,
            ````

        16. Pass in a "normalization" argument that only applies to less-common integer-based byte formats and is ignored for floats.
            
            ````js
            gl.vertexAttribPointer(pos_loc,
                2,
                gl.FLOAT,
                false,
            ````
        
        17. Pass in how many bytes to skip between the end of one attribute and the start of the next.
            
            ````js
            gl.vertexAttribPointer(pos_loc,
                2,
                gl.FLOAT,
                false,
                0, // no gaps: one pos ends where next begins
            ````

        18. Pass in how many bytes to skip at the front of the buffer.
            
            ````js
            gl.vertexAttribPointer(pos_loc,
                2,
                gl.FLOAT,
                false,
                0,
                0) // the first pos starts on the first byte
            ````

        19. Activate the attribute.
        
            ````js
            gl.enableVertexAttribArray(pos_loc)
            ````

    <div class="note">
    The details specified as part of the `gl.vertexAttribPointer` and `gl.enableVertexAttribArray` are stored in the active VAO,
    along with prerequisite information like which buffer was bound to the `gl.ARRAY_BUFFER` when `gl.vertexAttritPointer` was called.
    None of the other information above is.
    </div>

:::example
The full non-interleaved example is

```js
pos = [ [-1,-1], [ 1,-1], [ 1, 1], [-1, 1] ]
col = [ [0,0,0], [1,0,0], [0,1,0], [0,0,1] ]
pflat = pos.flat()
cflat = col.flat()
pbytes = new Float32Array(pflat)
cbytes = new Float32Array(cflat)

pbuf = gl.createBuffer()
cbuf = gl.createBuffer()
gl.bindBuffer(gl.ARRAY_BUFFER, pbuf)
gl.bufferData(gl.ARRAY_BUFFER, pbytes, gl.STATIC_DRAW)
gl.bindBuffer(gl.ARRAY_BUFFER, cbuf)
gl.bufferData(gl.ARRAY_BUFFER, cbytes, gl.STATIC_DRAW)

vao = gl.createVertexArray()
gl.bindVertexArray(voa)
gl.bindBuffer(gl.ARRAY_BUFFER, pbuf)
gl.vertexAttribPointer(pos_loc, 2, gl.FLOAT, false, 0, 0)
gl.bindBuffer(gl.ARRAY_BUFFER, cbuf)
gl.vertexAttribPointer(col_loc, 2, gl.FLOAT, false, 0, 0)
gl.enableVertexAttribArray(pos_loc)
gl.enableVertexAttribArray(col_loc)
```
:::

:::example
The full interleaved example is

```js
interleaved = [
    [-1,-1], [0,0,0],
    [ 1,-1], [1,0,0],
    [ 1, 1], [0,1,0],
    [-1, 1], [0,0,1],
]
iflat = pos.flat()
ibytes = new Float32Array(iflat)

ibuf = gl.createBuffer()
gl.bindBuffer(gl.ARRAY_BUFFER, ibuf)
gl.bufferData(gl.ARRAY_BUFFER, ibytes, gl.STATIC_DRAW)

vao = gl.createVertexArray()
gl.bindVertexArray(voa)
// gl.bindBuffer(gl.ARRAY_BUFFER, ibuf) // not needed, still bound
gl.vertexAttribPointer(pos_loc, 2, gl.FLOAT, false, 4*3, 0)
gl.vertexAttribPointer(col_loc, 2, gl.FLOAT, false, 4*2, 4*3)
gl.enableVertexAttribArray(pos_loc)
gl.enableVertexAttribArray(col_loc)
```
:::




