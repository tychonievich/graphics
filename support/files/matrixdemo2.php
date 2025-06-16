<!DOCTYPE html>
<html>
<head>
<title>Matrix Demo 2</title>
<script src="math.js"></script>



<script id="frag" type="glsl">
#version 300 es
precision highp float;

uniform vec4 color;
in vec4 v_normal;
out vec4 fragColor;

void main() {
    float lambert = dot(normalize(v_normal), vec4(0.36,0.48,-0.80,0));
    fragColor = vec4(color.rgb * abs(lambert), color.a);
}
</script>



<script id="vert" type="glsl">
#version 300 es

in vec4 position;
in vec3 normal;
out vec4 v_normal;
<?php
$num = isset($_GET['n']) ? intval($_GET['n']) : 1;
for($i=0; $i<$num; $i+=1) {
    echo "uniform mat4 m$i;\n";
}
?>
uniform mat4 view;

void main() {
    gl_Position = view * <?php
for($i=0; $i<$num; $i+=1) {
    echo "m$i * ";
}
    ?>position;
    v_normal = <?php
for($i=0; $i<$num; $i+=1) {
    echo "m$i * ";
}
    ?>vec4(normal, 0);
}
</script>



<script>
const IlliniBlue = new Float32Array([0.075, 0.16, 0.292, 1])
const IlliniOrange = new Float32Array([1, 0.373, 0.02, 1])
const IdentityMatrix = new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])

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

    window.program = gl.createProgram()
    gl.attachShader(program, vs)
    gl.attachShader(program, fs)
    gl.linkProgram(program)
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.error(gl.getProgramInfoLog(program))
        throw Error("Linking failed")
    }
}

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

function setupGeomery(geom) {
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

function readInputs(i) {
    let ans = new Float32Array(16)
    var num;
    for(let row=0; row<4; row+=1) {
        for(let col=0; col<4; col+=1) {
            try {
                num = eval(document.querySelector('#m'+i+'_'+row+col).value) || 0
            } catch { num = 0 }
            ans[row+col*4] = num
        }
    }
    return ans
}

function draw() {
    gl.clearColor(0,0,0, 0) // transparent
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)
    gl.viewport(0,0,400,400); // front view
    draw_view(new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]));
    gl.viewport(404,204,196,196); // top view
    draw_view(new Float32Array([1,0,0,0, 0,0,-1,0, 0,1,0,0, 0,0,0,1]));
    gl.viewport(404,0,196,196); // side view
    draw_view(new Float32Array([0,0,-1,0, 0,1,0,0, 1,0,0,0, 0,0,0,1]));
}

function draw_view(lastM) {
    gl.useProgram(program)
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA)
    let matrixBindPoints = [<?php for($i=0; $i<$num; $i+=1) echo "$i,"; ?>].map(i => gl.getUniformLocation(program, 'm'+i))
    let colorBindPoint = gl.getUniformLocation(program, 'color')
    let viewBindPoint = gl.getUniformLocation(program, 'view')
    gl.uniformMatrix4fv(viewBindPoint, false, lastM)

    gl.bindVertexArray(geom.vao)

    gl.uniform4fv(colorBindPoint, IlliniOrange)
    matrixBindPoints.forEach((bp,i) => gl.uniformMatrix4fv(bp, false, readInputs(i)))
    gl.drawElements(geom.mode, geom.count, geom.type, 0)

    //gl.uniform4fv(colorBindPoint, IlliniBlue)
    //matrixBindPoints.forEach(bp => gl.uniformMatrix4fv(bp, false, IdentityMatrix))
    //gl.drawElements(geom.mode, geom.count, geom.type, 0)

}

function setm(idx, colmaj) {
    for(let r=0; r<4; r+=1) for(let c=0; c<4; c+=1)
        document.getElementById('m'+idx+'_'+r+c).value = colmaj[c*4+r].toString().substr(0,8);
    requestAnimationFrame(draw)
}


function dofunc(elem) {
    const idx = elem.id.substr(1)
    const text = elem.value
    elem.style.backgroundColor = 'rgba(0,0,0,0)'
    let args = null
    if ((args = /ident *\( *\)/i.exec(text)) != null) {
        setm(idx, [1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1])
    } else if ((args = /rotX *\( *([-+0-9.eE]+) *\)/i.exec(text)) != null) {
        setm(idx, m4rotX(Number(args[1])))
    } else if ((args = /rotY *\( *([-+0-9.eE]+) *\)/i.exec(text)) != null) {
        setm(idx, m4rotY(Number(args[1])))
    } else if ((args = /rotZ *\( *([-+0-9.eE]+) *\)/i.exec(text)) != null) {
        setm(idx, m4rotZ(Number(args[1])))
    } else if ((args = /axis *\( *\[ *([-+0-9.eE]+) *, *([-+0-9.eE]+) *, *([-+0-9.eE]+) *\] *, *\[ *([-+0-9.eE]+) *, *([-+0-9.eE]+) *, *([-+0-9.eE]+) *\] *\)/i.exec(text)) != null) {
        setm(idx, m4fixAxes([Number(args[1]),Number(args[2]),Number(args[3])], [Number(args[4]),Number(args[5]),Number(args[6])]))
    } else if ((args = /trans *\( *([-+0-9.eE]+) *, *([-+0-9.eE]+) *, *([-+0-9.eE]+) *\)/i.exec(text)) != null) {
        setm(idx, m4trans(Number(args[1]),Number(args[2]),Number(args[3])))
    } else if ((args = /scale *\( *([-+0-9.eE]+) *, *([-+0-9.eE]+) *, *([-+0-9.eE]+) *\)/i.exec(text)) != null) {
        setm(idx, m4scale(Number(args[1]),Number(args[2]),Number(args[3])))
    } else if ((args = /persp *\( *([-+0-9.eE]+) *, *([-+0-9.eE]+) *, *([-+0-9.eE]+) *, *([-+0-9.eE]+) *\)/i.exec(text)) != null) {
        setm(idx, m4perspNegZ(Number(args[1]),Number(args[2]),Number(args[3]),Number(args[4]), 1))
    } else {
        elem.style.backgroundColor = 'rgba(255,0,0,0.25)'
    }
    console.log(elem.id, elem.value)
}

async function setup(event) {
    window.gl = document.querySelector('canvas').getContext('webgl2')
    let vs = document.querySelector('#vert').textContent.trim()
    let fs = document.querySelector('#frag').textContent.trim()
    compileAndLinkGLSL(vs,fs)
    gl.enable(gl.DEPTH_TEST)
    let data = await fetch('smile-box.json').then(r=>r.json())
    window.geom = setupGeomery(data)
    requestAnimationFrame(draw)
    document.querySelectorAll('table input').forEach(elem => elem.addEventListener('input', event => requestAnimationFrame(draw)))
}

window.addEventListener('load',setup)
</script>


<style>
    input { width: 6em; font-size:1rem; text-align:center; }
    input.func { width: calc(100% - 1ex); }
    table, canvas { border: thin solid black; margin:1ex; display: inline-block; vertical-align: top; }
</style>
</head>
<body>
<?php
for($i=0; $i<$num; $i+=1) {
?>
<table><tbody>
<tr>
    <td><input id="m<?=$i?>_00"  step="any" value="1"></td>
    <td><input id="m<?=$i?>_01"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_02"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_03"  step="any" value="0"></td>
</tr><tr>
    <td><input id="m<?=$i?>_10"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_11"  step="any" value="1"></td>
    <td><input id="m<?=$i?>_12"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_13"  step="any" value="0"></td>
</tr><tr>
    <td><input id="m<?=$i?>_20"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_21"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_22"  step="any" value="1"></td>
    <td><input id="m<?=$i?>_23"  step="any" value="0"></td>
</tr><tr>
    <td><input id="m<?=$i?>_30"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_31"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_32"  step="any" value="0"></td>
    <td><input id="m<?=$i?>_33"  step="any" value="1"></td>
</tr>
<tr><td colspan="4"><input class="func" id="f<?=$i?>" type="text" list="funcs" onchange="dofunc(this)"/></td></tr>
</tbody></table>
<?php } ?>
<canvas width="600" height="400"></canvas>
<br/>Canvas shows views from front (left), top (top right, front = down), and left (bottom right, front = left).
<div><form method="GET">
    <label>How many matrices should we show? <input type="number" min="1" max="9" name="n" value="<?=$num?>">
    </label>
</form></div>
<datalist id="funcs">
    <option>ident()</option>
    <option>rotX(a)</option>
    <option>rotY(a)</option>
    <option>rotZ(a)</option>
    <option>axis([fx,fy,fz], [ux,uy,uz])</option>
    <option>trans(dx, dy, dz)</option>
    <option>scale(sx, sy, sz)</option>
    <option>persp(near, far, fovy, w_h)</option>
</datalist>
</body>
</html>
