const IlliniBlue = new Float32Array([0.075, 0.16, 0.292, 1])
const IlliniOrange = new Float32Array([1, 0.373, 0.02, 1])

/**
 * Given the source code of a vertex and fragment shader, compiles them,
 * and returns the linked program.
 */
function compileAndLinkGLSL(vs_source, fs_source) {
    let vs = gl.createShader(gl.VERTEX_SHADER)
    gl.shaderSource(vs, vs_source)
    gl.compileShader(vs)
    if (!gl.getShaderParameter(vs, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(vs))
        throw Error("Vertex shader compilation failed")
    }

    let fs = gl.createShader(gl.FRAGMENT_SHADER)
    gl.shaderSource(fs, fs_source)
    gl.compileShader(fs)
    if (!gl.getShaderParameter(fs, gl.COMPILE_STATUS)) {
        console.error(gl.getShaderInfoLog(fs))
        throw Error("Fragment shader compilation failed")
    }

    let program = gl.createProgram()
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
    
    return program
}

/**
 * Sends per-vertex data to the GPU and connects it to a VS input
 * 
 * @param data    a 2D array of per-vertex data (e.g. [[x,y,z,w],[x,y,z,w],...])
 * @param program a compiled and linked GLSL program
 * @param vsIn    the name of the vertex shader's `in` attribute
 * @param mode    (optional) gl.STATIC_DRAW, gl.DYNAMIC_DRAW, etc
 * 
 * @returns the ID of the buffer in GPU memory; useful for changing data later
 */
function supplyDataBuffer(data, program, vsIn, mode) {
    if (mode === undefined) mode = gl.STATIC_DRAW
    
    let buf = gl.createBuffer()
    gl.bindBuffer(gl.ARRAY_BUFFER, buf)
    let f32 = new Float32Array(data.flat())
    gl.bufferData(gl.ARRAY_BUFFER, f32, mode)
    
    let loc = gl.getAttribLocation(program, vsIn)
    gl.vertexAttribPointer(loc, data[0].length, gl.FLOAT, false, 0, 0)
    gl.enableVertexAttribArray(loc)
    
    return buf;
}

/**
 * Creates a Vertex Array Object and puts into it all of the data in the given
 * JSON structure, which should have the following form:
 * 
 * @param geom    an object structured like this:
 * ````
 * {"triangles": a list of of indices of vertices
 * ,"attributes":
 *  {name_of_vs_input_1: a list of 1-, 2-, 3-, or 4-vectors, one per vertex
 *  ,name_of_vs_input_2: a list of 1-, 2-, 3-, or 4-vectors, one per vertex
 *  }
 * }
 * ````
 *
 * @param program a compiled and linked GLSL program
 *
 * @param mode    (optional) gl.STATIC_DRAW, gl.DYNAMIC_DRAW, etc
 * 
 * 
 * @returns an object with four keys:
 *  - mode = the 1st argument for gl.drawElements
 *  - count = the 2nd argument for gl.drawElements
 *  - type = the 3rd argument for gl.drawElements
 *  - vao = the vertex array object for use with gl.bindVertexArray
 */
function setupGeomery(geom, program, mode) {
    if (mode === undefined) mode = gl.STATIC_DRAW
    var triangleArray = gl.createVertexArray()
    gl.bindVertexArray(triangleArray)

    for(let name in geom.attributes) {
        let data = geom.attributes[name]
        supplyDataBuffer(data, program, name)
    }

    var indices = new Uint16Array(geom.triangles.flat())
    var indexBuffer = gl.createBuffer()
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer)
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW)

    return {
        mode: gl.TRIANGLES,
        count: indices.length,
        type: gl.UNSIGNED_SHORT,
        vao: triangleArray
    }
}


/**
 * Resizes the first canvas on the page to completely fill the screen.
 * Can optionally be given either of the following, in any order:
 * 
 * - A configuration object with any subset of the following keys:
 *   - "canvas": an element or query selector (defaults to "canvas")
 *   - "width": a CSS-style target width (defaults to "100vw")
 *   - "height": a CSS-style target height (defaults to "100vh")
 * 
 * - A function to be invoked with the new width and height values
 */
function fillScreen() {
    config={}
    for(let i=0; i<arguments.length; i+=1)
        if ('object' == typeof(arguments[i])) Object.assign(config, arguments[i])
    
    let canvas = document.querySelector(config.canvas || 'canvas')
    canvas.style.width = config.width || '100vw'
    canvas.style.height = config.height || '100vh'
    canvas.width = canvas.clientWidth
    canvas.height = canvas.clientHeight
    canvas.style.width = ''
    canvas.style.height = ''
    for(let i=0; i<arguments.length; i+=1)
        if ('function' == typeof(arguments[i]))
            arguments[i](canvas.width, canvas.height)
}



/** Normalize a (prefix of a) vector */
function m4normalized(vec, len) {
    vec = Array.from(vec)
    if (len && len < vec.length) vec = vec.slice(0,len)
    let mag = Math.sqrt(vec.map(x=>x*x).reduce((x,y)=>x+y))
    return vec.map(x=>x/mag)
}
/** Helper function to normalize a (prefix of a) vector and return the old length */
function m4normalized2_(vec, len) {
    vec = Array.from(vec)
    if (len && len < vec.length) vec = vec.slice(0,len)
    let mag = Math.sqrt(vec.map(x=>x*x).reduce((x,y)=>x+y))
    return [vec.map(x=>x/mag), mag]
}
/** Find the cross product of two 3-vectors */
function m4cross(x,y) {
    return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
}
/** Find the dot product of (a prefix of) two vectors */
function m4dot(x,y,len) {
    len = len ? Math.min(x.length, y.length, len) : Math.min(x.length, y.length)
    return Array.from(x).slice(0,len).map((v,i)=>v*y[i]).reduce((a,b)=>a+b)
}
/** Find the difference of (a prefix of) two vectors */
function m4sub(x,y,len) {
    len = len ? Math.min(x.length, y.length, len) : Math.min(x.length, y.length)
    return Array.from(x).slice(0,len).map((v,i)=>v-y[i])
}
/** Find the sum of (a prefix of) two vectors */
function m4add(x,y,len) {
    len = len ? Math.min(x.length, y.length, len) : Math.min(x.length, y.length)
    return Array.from(x).slice(0,len).map((v,i)=>v+y[i])
}

/**
 * Multiply two matrices. Helper function; generally call m4mult instead.
 */
function m4mult_(m1,m2) {
    let ans = new Float32Array(16)
    for(let outRow = 0; outRow < 4; outRow += 1) {
        for(let outCol = 0; outCol < 4; outCol += 1) {
            for(let i = 0; i < 4; i += 1) {
                ans[outRow+outCol*4] += m1[outRow+i*4] * m2[i+outCol*4]
            }
        }
    }
    return ans
}
/**
 * Multiplies any number of matrices and returns the result.
 * Call as m4mult(A, B, C, D) to evaluate $A B C D$.
 */
function m4mult() {
    if (arguments.length == 1) return arguments[0]
    return Array.prototype.reduce.apply(arguments, [m4mult_])
}

/**
 * Returns the transpose of the given matrix
 */
function m4transpose(m) {
    return new Float32Array([m[0],m[4],m[8],m[12], m[1],m[5],m[9],m[13], m[2],m[6],m[10],m[14], m[3],m[7],m[11],m[15]]);
}

/**
 * Creates and returns a new identity matrix
 */
function m4ident() {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]);
}

/**
 * Creates and returns a new translation matrix
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#translation>
 */
function m4translate(x,y,z) {
    return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, x,y,z,1]);
}

/**
 * Creates and returns a new scaling matrix
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#scaling>
 */
function m4scale(x,y,z) {
    if (y == undefined && z == undefined) z = y = x
    return new Float32Array([x,0,0,0, 0,y,0,0, 0,0,z,0, 0,0,0,1]);
}

/**
 * Creates and returns a new perspective projection matrix
 * where "forward" is the +z axis.
 * 
 * - `m4perspPosZ(near, far)` assumes 90° FoV in X and Y
 * - `m4perspPosZ(near, far, PI/4, 16/9)` has FoV in Y and 16:9 aspect ratio
 * - `m4perspPosZ(near, far, PI/3, 16, 9)` has FoV in Y and 16:9 aspect ratio
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#division>
 */
function m4perspPosZ(near, far, fovy, width, height) {
    if (fovy === undefined) {
        var sx = 1, sy = 1;
    } else {
        let aspect = (height === undefined) ? width : width / height
        var sy = 1/Math.tan(fovy/2);
        var sx = sy/aspect;
    }
    return new Float32Array([sx,0,0,0, 0,sy,0,0, 0,0,1, 0,0,(far+near)/(far-near),(2*far*near)/(near-far),0]);
}
/// Like {m4perspPosZ} but -z, not +z, is in front of camera.
function m4perspNegZ(near, far, fovy, width, height) {
    if (fovy === undefined) {
        var sx = 1, sy = 1;
    } else {
        let aspect = (height === undefined) ? width : width / height
        var sy = 1/Math.tan(fovy/2);
        var sx = sy/aspect;
    }
    return new Float32Array([sx,0,0,0, 0,sy,0,0, 0,0,-1, 0,0,-(far+near)/(far-near),(2*far*near)/(near-far),0]);
}


/**
 * Creates and returns a new yz-plane rotation.
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#rotation>
 */
function m4rotX(ang) {
    let c = Math.cos(ang), s = Math.sin(ang);
    return new Float32Array([1,0,0,0, 0,c,s,0, 0,-s,c,0, 0,0,0,1]);
}
/**
 * Creates and returns a new zx-plane rotation.
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#rotation>
 */
function m4rotY(ang) {
    let c = Math.cos(ang), s = Math.sin(ang);
    return new Float32Array([c,0,-s,0, 0,1,0,0, s,0,c,0, 0,0,0,1]);
}
/**
 * Creates and returns a new xy-plane rotation.
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#rotation>
 */
function m4rotZ(ang) {
    let c = Math.cos(ang), s = Math.sin(ang);
    return new Float32Array([c,s,0,0, -s,c,0,0, 0,0,1,0, 0,0,0,1]);
}

/** Helper function for rotations */
function m4rotAxis_(r,c,s) {
    omc = 1-c
    let xy = r[0]*r[1]*omc, yz = r[1]*r[2]*omc, zx = r[2]*r[0]*omc
    return new Float32Array([
        r[0]*r[0]*omc + c, xy + r[2]*s, zx - r[1]*s, 0,
        xy - r[2]*s, r[1]*r[1]*omc + c, yz + r[0]*s, 0,
        zx + r[1]*s, yz - r[0]*s, r[2]*r[2]*omc + c, 0,
        0,0,0,1]);
}

/**
 * Creates and returns a new axis + angle rotation.
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#rotation>
 */
function m4rotAxis(axis, ang) {
    let r = m4normalized(axis, 3)
    let c = Math.cos(ang), s = Math.sin(ang);
    return m4rotAxis_(r,c,s)
}
/**
 * Creates and returns a rotation that results in a pointing towards b
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#rotation>
 */
function m4rotAtoB(a,b) {
    a = m4normalized(a,3)
    b = m4normalized(b,3)
    let [r, s] = m4normalized2_(m4cross(a,b))
    let c = m4dot(a,b)
    return m4rotAxis_(r,c,s)
}

/**
 * Creates and returns a rotation that puts (center-eye) on -z and up near +y,
 * combined with a translation that puts eye at 0,0,0
 * 
 * See <https://cs418.cs.illinois.edu/website/text/math2.html#rotation>
 */
function m4view(eye, center, up) {
    let f = m4normalized(m4sub(center,eye,3))
    let r = m4normalized(m4cross(f,up))
    let u = m4cross(r,f)
    return m4mult(new Float32Array([
        r[0],u[0],-f[0],0,
        r[1],u[1],-f[1],0,
        r[2],u[2],-f[2],0,
        0,0,0,1
    ]), m4translate(-eye[0],-eye[1],-eye[2]))
}

/**
 * Creates and returns a rotation from a quaternion.
 * Assumes quaternion in (x,y,z;w) order.
 * 
 * See <https://cs418.cs.illinois.edu/website/text/quaternions.html#rotation-matrix>
 */
function m4quatToRot(q) {
    let n = m4dot(q,q)
    let [x,y,z,w] = q
    let s = n && 2/n
    return new Float32Array([
        1-s*(y*y+z*z), s*(x*y+z*w), s*(x*y-y*w), 0,
        s*(x*y-z*w), 1-s*(x*x+z*z), s*(y*z+x*w), 0,
        s*(x*z+y*w), s*(y*z-x*w), 1-s*(x*x+y*y), 0,
        0, 0, 0, 1,
    ])
}
