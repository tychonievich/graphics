---
title: Example WebGL2 traces explained
summary: Sequences of gl calls created by real programs, with commentary.
...

# ex01-standalone

[ex01-standalone.html](../code/2d-webgl/ex01-standalone.html) executes the following WebgGL2 library calls:

- Shader program setup
  - Create and compile a vertex shader and check for errors
    1. `Shader#1 = gl.createShader(gl.VERTEX_SHADER)`
    2. `gl.shaderSource(Shader#1, str)`
    3. `gl.compileShader(Shader#1)`
    4. `gl.getShaderParameter(Shader#1, gl.COMPILE_STATUS)`
  - Create and compile a fragment shader and check for errors
    5. `Shader#2 = gl.createShader(gl.FRAGMENT_SHADER)`
    6. `gl.shaderSource(Shader#2, str)`
    7. `gl.compileShader(Shader#2)`
    8. `gl.getShaderParameter(Shader#2, gl.COMPILE_STATUS)`
  - Create a shader program, link the two shaders together, and check for errors
    9. `Program#1 = gl.createProgram()`
    10. `gl.attachShader(Program#1, Shader#1)`
    11. `gl.attachShader(Program#1, Shader#2)`
    12. `gl.linkProgram(Program#1)`
    13. `gl.getProgramParameter(Program#1, gl.LINK_STATUS)`

- Draw (called once only)
  14. `gl.clear(gl.COLOR_BUFFER_BIT)`
      
      Normally we'd expect the depth buffer too, but this file doesn't use depth
  ​​15. `gl.useProgram(Program#1)`
  16. `gl.drawArrays(gl.TRIANGLES, 0, 6)`
      
      Note that we haven't provided *any* attributes.
      There will be no `in` variables supplied to the vertex shader,
      so it will have to compute its own positions based on `gl_VertexID` instead.

# ex04-motion

[ex04-motion.html](../code/2d-webgl/ex04-motion.html) executes the following WebgGL2 library calls:

- Shader program setup (see [ex01-standalone] for comments)
    1. `Shader#1 = gl.createShader(gl.VERTEX_SHADER)`
    2. `gl.shaderSource(Shader#1, str)`
    3. `gl.compileShader(Shader#1)`
    4. `gl.getShaderParameter(Shader#1, gl.COMPILE_STATUS)`
    6. `Shader#2 = gl.createShader(gl.FRAGMENT_SHADER)`
    7. `gl.shaderSource(Shader#2, str)`
    8. `gl.compileShader(Shader#2)`
    9. `gl.getShaderParameter(Shader#2, gl.COMPILE_STATUS)`
    10. `Program#1 = gl.createProgram()`
    11. `gl.attachShader(Program#1, Shader#1)`
    12. `gl.attachShader(Program#1, Shader#2)`
    13. `gl.linkProgram(Program#1)`
    14. `gl.getProgramParameter(Program#1, gl.LINK_STATUS)`
- Geometry setup
  - Set up a VAO to stores the various buffer bindings (but not buffer content, that's in GPU memory) for retrieval during drawing
    15. `VertexArray#1 = gl.createVertexArray()`
    16. `gl.bindVertexArray(VertexArray#1)`
  - Send data to the position attribute and enable it
    17. `Buffer#1 = gl.createBuffer()`

        Acts like a pointer to an array in GPU memory. Initially like a null pointer as we've not pointed it to anything.
    18. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#1)`

        The `gl.ARRAY_BUFFER` is like an input port to which we can send attribute data.
        We're specifying that data arriving through that port should end up pointed to by `Buffer#1`.
    19. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[8], gl.STATIC_DRAW)`

        And here we send in data, optimized for rare updates and frequent draws.
        `Buffer#1` is now no longer a null pointer, instead pointing to a 24-byte blob in GPU memory.
        
        The `Float32Array` type is a JavaScript-specific type and is lost in transit to the GPU,
        which only gets a blob of bytes.
        The GPU learns to parse them as floats on line 21.
    20. `Attrib#1 = gl.getAttribLocation(Program#1, "position")`
        
        This is just an integer.
        If we'd used `layout(location = 0) in vec4 position`{.glsl} in the GLSL we could just use 0 directly instead of needing this call.
        Using explicit layout locations is preferable in code that has more than one shader program.
    21. `gl.vertexAttribPointer(Attrib#1, 2, gl.FLOAT, false, 0, 0)`

        The "`2`" means 2 floats per attribute; coupled with the 8-element array on line 19, that means 4 total vertices.
        We also have to tell the GPU how to parse bytes into numbers,
        which is what `gl.FLOAT` and the arguments after it do.
    22. `gl.enableVertexAttribArray(Attrib#1)`
        
        It may seem strange that after picking an attribute and giving it data
        we also have to enable it.
        Having this separate enabling step allows a few special-case tricks we won't cover in this class.
  - Send data to the color attribute and enable it
    23. `Buffer#2 = gl.createBuffer()`
    24. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#2)`
    25. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[16], gl.STATIC_DRAW)`
    26. `Attrib#2 = gl.getAttribLocation(Program#1, "color")`
    27. `gl.vertexAttribPointer(Attrib#2, 4, gl.FLOAT, false, 0, 0)`

        The "`4`" means 4 floats per attribute; couples with the 16-element array on line 25, that means 4 total vertices
    28. `gl.enableVertexAttribArray(Attrib#2)`
  - Send data to the element array, identifying which vertices are connected into primitives nad how
    29. `Buffer#3 = gl.createBuffer()`
    30. `gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, Buffer#3)`
    31. `gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, Uint16Array[9], gl.STATIC_DRAW)`

        Note the 9-entry index buffer, which is provided without saying how many vertices are used per primitive.
        We need to specify that *per drawElements call*, as we see in step 37 below.
    
- Draw (called repeatedly)
    32. `gl.clear(gl.COLOR_BUFFER_BIT)`
        
        No depth buffer bit because this is a 2D animation
    33. `gl.useProgram(Program#1)`
    
        Because we only have one shader program, we could have done this once during setup.
        But generally we'll have several shader programs so it's good practice to specify which one we want every frame.
    34. `Program#1seconds = gl.getUniformLocation(Program#1, "seconds")`
        
        Note uniform locations are specific to a shader program, but don't change over the course of the program.
        We could have done this in the setup instead and remembered the return value for slightly faster operation.
    35. `gl.uniform1f(Program#1seconds, num)`
    36. `gl.bindVertexArray(VertexArray#1)`
    
        Because we only have one VAO and already bound it during setup, we could remove this call.
        But generally we'll have several VAO programs so it's good practice to specify which one we want every frame.
    37. `gl.drawElements(gl.TRIANGLES, 9, gl.UNSIGNED_SHORT, 0)`
        
        A lot is going on here.
        
        Because we say `drawElements`, it's going to look inside the currently-bound `ELEMENT_ARRAY_BUFFER` to find indices to connect into primitives;
        we bound that most recently in step 36: the VAO includes re-binding the `ELEMENT_ARRAY_BUFFER` it had during setup.
        
        Inside that buffer it will consider 3 indices at a time (that's what `gl.TRIANGLES` means).
        It will look at at most 9 total indices, meaning 3 triangles get drawn.
        
        As part of the draw, vertices are sent through the vertex shader of the currently bound program.
        Which vertices to send is determined by the indices stored inside the `ELEMENT_ARRAY_BUFFER`.
        The attributes for each are pulled from the currently enabled attribute arrays (lines 22 and 28),
        which are also re-enabled with the VAO (line 36).
        
        Like line 21, we also have to indicate how to parse the buffer's bytes into numbers.


# 5-scripted.html

[5-scripted.html](../code/3d-webgl/5-scripted.html) executes the following WebgGL2 library calls:

- Shader program setup (see [ex01-standalone] for comments)
    1. `Shader#1 = gl.createShader(gl.VERTEX_SHADER)`
    2. `gl.shaderSource(Shader#1, str)`
    3. `gl.compileShader(Shader#1)`
    4. `gl.getShaderParameter(Shader#1, gl.COMPILE_STATUS)`
    5. `Shader#2 = gl.createShader(gl.FRAGMENT_SHADER)`
    6. `gl.shaderSource(Shader#2, str)`
    7. `gl.compileShader(Shader#2)`
    8. `gl.getShaderParameter(Shader#2, gl.COMPILE_STATUS)`
    9. `Program#1 = gl.createProgram()`
    10. `gl.attachShader(Program#1, Shader#1)`
    11. `gl.attachShader(Program#1, Shader#2)`
    12. `gl.linkProgram(Program#1)`
    13. `gl.getProgramParameter(Program#1, gl.LINK_STATUS)`
- Render settings setup
    14. `gl.enable(gl.DEPTH_TEST)`
- Geometry setup (see [ex04-motion] for comments)
    15. `VertexArray#1 = gl.createVertexArray()`
    16. `gl.bindVertexArray(VertexArray#1)`
    17. `Buffer#1 = gl.createBuffer()`
    18. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#1)`
    19. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[21], gl.STATIC_DRAW)`
    20. `gl.getAttribLocation(Program#1, "position")`
    21. `gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0)`
    22. `gl.enableVertexAttribArray(0)`
    23. `Buffer#2 = gl.createBuffer()`
    24. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#2)`
    25. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[21], gl.STATIC_DRAW)`
    26. `gl.getAttribLocation(Program#1, "vcolor")`
    27. `gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 0, 0)`
    28. `gl.enableVertexAttribArray(1)`
    29. `Buffer#3 = gl.createBuffer()`
    30. `gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, Buffer#3)`
    31. `gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, Uint16Array[12], gl.STATIC_DRAW)`
- Render settings setup
    32. `gl.viewport(num, num, num, num)`
- Draw
  - Set up this frame
    33. `gl.clearColor(num, num, num, num)`
    34. `gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)`
    35. `gl.useProgram(Program#1)`
    36. `gl.bindVertexArray(VertexArray#1)`
    37. `gl.getUniformLocation(Program#1, "color")`
        
        This is in the code, but there's no uniform of this name so it returns `null`. We should probably remove this.
    38. `gl.uniform4fv(null, Float32Array[4])`

        This tries to send data to a non-existant uniform, an error we should remove.
  - Draw first copy of tetrahedron, and also complete general setup of projection matrix:
    39. `Program#1mv = gl.getUniformLocation(Program#1, "mv")`
    40. `gl.uniformMatrix4fv(Program#1mv, false, Float32Array[16])`
    41. `Program#1p = gl.getUniformLocation(Program#1, "p")`
    42. `gl.uniformMatrix4fv(Program#1p, false, Float32Array[16])`
    43. `gl.drawElements(gl.TRIANGLES, 12, gl.UNSIGNED_SHORT, 0)`
  - Draw second copy of tetrahedron:
    44. `Program#1mv = gl.getUniformLocation(Program#1, "mv")`
    45. `gl.uniformMatrix4fv(Program#1mv, false, Float32Array[16])`
    46. `gl.drawElements(gl.TRIANGLES, 12, gl.UNSIGNED_SHORT, 0)`
  - Draw third copy of tetrahedron:
    47. `Program#1mv = gl.getUniformLocation(Program#1, "mv")`
    48. `gl.uniformMatrix4fv(Program#1mv, false, Float32Array[16])`
    49. `gl.drawElements(gl.TRIANGLES, 12, gl.UNSIGNED_SHORT, 0)`

# 6-skinning

[6-skinning.html](../code/skeletal-animation/6-skinning.html) executes the following WebgGL2 library calls:

- Shader program setup (see [ex01-standalone] for comments)
    1. `Shader#1 = gl.createShader(gl.VERTEX_SHADER)`
    2. `gl.shaderSource(Shader#1, str)`
    3. `gl.compileShader(Shader#1)`
    4. `gl.getShaderParameter(Shader#1, gl.COMPILE_STATUS)`
    5. `Shader#2 = gl.createShader(gl.FRAGMENT_SHADER)`
    6. `gl.shaderSource(Shader#2, str)`
    7. `gl.compileShader(Shader#2)`
    8. `gl.getShaderParameter(Shader#2, gl.COMPILE_STATUS)`
    9. `Program#1 = gl.createProgram()`
    10. `gl.attachShader(Program#1, Shader#1)`
    11. `gl.attachShader(Program#1, Shader#2)`
    12. `gl.linkProgram(Program#1)`
    13. `gl.getProgramParameter(Program#1, gl.LINK_STATUS)`

- Render settings setup
    14. `gl.enable(gl.DEPTH_TEST)`

- Geometry setup (see [ex04-motion] for comments)
    15. `VertexArray#1 = gl.createVertexArray()`
    16. `gl.bindVertexArray(VertexArray#1)`
    17. `Buffer#1 = gl.createBuffer()`
    18. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#1)`
    19. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[6012], gl.STATIC_DRAW)`
    20. `gl.getAttribLocation(Program#1, "position")`
    21. `gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0)`
    22. `gl.enableVertexAttribArray(0)`
    23. `Buffer#2 = gl.createBuffer()`
    24. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#2)`
    25. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[6012], gl.STATIC_DRAW)`
    26. `gl.getAttribLocation(Program#1, "color")`
    27. `gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 0, 0)`
    28. `gl.enableVertexAttribArray(1)`
    29. `Buffer#3 = gl.createBuffer()`
    30. `gl.bindBuffer(gl.ARRAY_BUFFER, Buffer#3)`
    31. `gl.bufferData(gl.ARRAY_BUFFER, Float32Array[6012], gl.STATIC_DRAW)`
    32. `gl.getAttribLocation(Program#1, "weight")`
    33. `gl.vertexAttribPointer(2, 3, gl.FLOAT, false, 0, 0)`
    34. `gl.enableVertexAttribArray(2)`
    35. `Buffer#4 = gl.createBuffer()`
    36. `gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, Buffer#4)`
    37. `gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, Uint16Array[11880], gl.STATIC_DRAW)`
- Render settings setup
    38. `gl.viewport(num, num, num, num)`

- Draw
    39. `gl.clearColor(num, num, num, num)`
    40. `gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)`
    41. `gl.useProgram(Program#1)`
    42. `gl.bindVertexArray(VertexArray#1)`
    43. `gl.getUniformLocation(Program#1, "color")`
    44. `gl.uniform4fv(null, Float32Array[4])`
    45. `Program#1T = gl.getUniformLocation(Program#1, "T")`
    46. `gl.uniformMatrix4fv(Program#1T, false, Float32Array[16])`
    47. `Program#1C = gl.getUniformLocation(Program#1, "C")`
    48. `gl.uniformMatrix4fv(Program#1C, false, Float32Array[16])`
    49. `Program#1F = gl.getUniformLocation(Program#1, "F")`
    50. `gl.uniformMatrix4fv(Program#1F, false, Float32Array[16])`
    51. `Program#1p = gl.getUniformLocation(Program#1, "p")`
    52. `gl.uniformMatrix4fv(Program#1p, false, Float32Array[16])`
    53. `gl.drawElements(gl.TRIANGLES, 11880, gl.UNSIGNED_SHORT, 0)`
