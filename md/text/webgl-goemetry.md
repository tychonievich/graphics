---
title: WebGL Geometry
summary: Several ways to tell WebGL what shapes we want to display.
...

<style>
.threes td:nth-child(3n+1), .nines td:nth-child(3n+1) { border-right: thin solid rgba(0,0,0,0.25); }
.nines td:nth-child(9n+1) { border-right: thin solid rgba(0,0,0,1); }
</style>

# Data flow in WebGL2

The code of the vertex and fragment shaders are specified by the programmer.
The vertex shader has built-in inputs `gl_VertexID` and `gl_InstanceID` and built-in outputs `gl_Position` and `gl_PointSize`.
The fragment shader has built-in inputs `gl_FragCoord`, `gl_FrontFacing`, and `gl_PointCoord` and built-in output `gl_FragDepth`.
The fragment shader also has a single programmer-named color output which is used to display the frame buffer.
In between these two shaders the primitives are assembled, clipped, projected, and rasterized, with values interpolated to each resulting fragment.

<figure>
<img src="../files/shader-data.svg" class="wide"/>
<figcaption>
An illustration of the major parts of data flow in WebGL2, as described in the surrounding text.
</figcaption>
</figure>

The vertex shader may take additional programmer-specified inputs called "attributes."
The values of these attributes are pulled from special arrays in graphics memory called "buffers."
The set of values to run the vertex shade on, together with how sets of vertices are to be assembled into primitives, is specified by the specific draw command used as discussed [below](#attributes-and-connectivity).

The vertex shader may produce additional outputs called "varyings."
These are automatically interpolated by the rasterizer and their interpolated values (still called "varyings") are provided as additional inputs to the fragment shader.

Both shaders have access to global values called "uniforms" that are the same for all vertices and fragments in a given draw command.
Sending values to the buffers tends to be significantly slower than rendering from the buffers that are there, so there's a preference for making the buffers static, with values specified once and rendered many times;
changing the uniforms each frame can create per-frame motion with a static buffers.
Uniforms are also used for large data like textures.


# Attributes and Connectivity

To run a shader program, the GPU needs to know

- How many vertices to pass through the vertex shader
- The values of the per-vertex inputs or **attributes** each vertex has
- How to assembly vertices into primitives (points, lines, or triangles)

There are multiple ways to provide this data, each of which has multiple steps.
We illustrate the first two with an example based on the following simple three-triangle bowl object:

<figure>
<svg version="1.1" viewBox="-2 -1 64 57" xmlns="http://www.w3.org/2000/svg" style="max-width:22em">
 <defs>
  <marker id="Point" overflow="visible" markerHeight="8" markerWidth="8" orient="auto" preserveAspectRatio="xMidYMid" viewBox="0 0 5.4 5.4">
   <path transform="scale(.5)" d="m5 0c0 2.76-2.24 5-5 5s-5-2.24-5-5 2.3-5 5-5c2.76 0 5 2.24 5 5z" fill="white" stroke="#000" fill-rule="evenodd" stroke-width="2"/>
  </marker>
  <marker id="Arrow" overflow="visible" markerHeight="6.6094756" markerWidth="5.8874264" orient="auto-start-reverse" preserveAspectRatio="xMidYMid" viewBox="0 0 5.8874262 6.6094758">
   <path transform="scale(.5)" d="m6 0c-3 1-7 3-9 5 0 0 0-4 2-5-2-1-2-5-2-5 2 2 6 4 9 5z" fill="#000" fill-rule="evenodd" stroke="context-stroke" stroke-width="1pt"/>
  </marker>
 </defs>
 <g stroke="#000">
  <g fill="none" stroke-width=".5">
   <path d="m39.688 15.875-2.6458-10.583" marker-end="url(#Arrow)"/>
   <path d="m2.6458 26.458 10.583-13.229" marker-end="url(#Arrow)"/>
   <path d="m55.563 31.75-5.2917-13.229" marker-end="url(#Arrow)"/>
   <path d="m34.396 47.625v-17.198" fill="none" marker-end="url(#Arrow)" stroke-width=".5"/>
  </g>
  <g fill="#fff" fill-opacity=".8" stroke-width=".25">
    <path d="m2.6458 26.458 52.917 5.2917-15.875-15.875z"/>
    <path d="m39.688 15.875-5.2917 31.75" marker-start="url(#Point)"/>
    <path d="m2.6458 26.458 31.75 21.167 21.167-15.875z" marker-mid="url(#Point)" marker-start="url(#Point)"/>
  </g>
 </g>
 <g text-anchor="middle" font-size="3">
    <g stroke="#fff" stroke-width="2" stroke-opacity="0.75">
    <text x="34.4" y="52.6">(0,0,-1)</text>
    <text x="2.6" y="31.5">(-1,0,0)</text>
    <text x="55.7" y="36.7">(½,-1,0)</text>
    <text x="39.7" y="20.9">(½,1,0)</text>
    <text x="37" y="2.3">(-⅓,-⅔,⅔)</text>
    <text x="50.2" y="16.5">(-⅓,⅔,⅔)</text>
    <text x="13.2" y="11.2">(√5/3,0,⅔)</text>
    <text x="34.4" y="28.4">(0,0,1)</text>
    </g>
    <text x="34.4" y="52.6">(0,0,-1)</text>
    <text x="2.6" y="31.5">(-1,0,0)</text>
    <text x="55.7" y="36.7">(½,-1,0)</text>
    <text x="39.7" y="20.9">(½,1,0)</text>
    <text x="37" y="2.3">(-⅓,-⅔,⅔)</text>
    <text x="50.2" y="16.5">(-⅓,⅔,⅔)</text>
    <text x="13.2" y="11.2">(√5/3,0,⅔)</text>
    <text x="34.4" y="28.4">(0,0,1)</text>
 </g>
</svg>
<figcaption>
An illustration of a bowl with three triangles and four vertices;
each vertex has a normal in addition to a position.
</figcaption>
</figure>

Listed in rough order of likelihood to be what you want, from most likely to least likely, these are:

1.  <details><summary>For most polygonal approximations of smooth surfaces:</summary>

    Setup
    :   For each scene object,
    
        1. Many an array of attribute values for each vertex
        1. Make an array of primitive connectivity
        1. Make a vertex array object on the GPU to collect the next steps
        1. Send each attribute values array to the GPU as an array buffer
        1. Send the connectivity array to the GPU as an element array buffer

    Bowl example
    :   <div class="threes">
    
        |Array   | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|
        |--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
        |Position| 0| 0|-1| ½|-1| 0| ½| 1| 0|-1| 0| 0|
        |Normal  |0|0|1|-⅓|⅔|⅔|-⅓|-⅔|⅔|$\sqrt{5}/3$|0|⅔|
        |Index   |0 |1 | 2| 0| 2| 3| 0| 3| 1|  |  |  |
        
        </div>

    Drawing
    :   For each scene object,
        
        1. Bind that object's vertex array object
        2. call `gl.drawElements`
    
    This works well for almost any object type.
    It is a bit less efficient than the next option for drawing points
    or for drawing other primitives that do not share vertex attributes (such as flat-shaded polyhedra).
    
    </details>

1.  <details><summary>For most disconnected points or flat-shaded polygons:</summary>
    
    Setup
    :   For each scene object,
    
        1. Many an array of attribute values for each vertex of each primitive, in order.
            If the same vertex is used for multiple primitives, repeat its values in the array.
        1. Make a vertex array object on the GPU to collect the next steps
        1. Send each attribute values array to the GPU as an array buffer

    Bowl example
    :   <div class="nines">
    
        |Array   | 0| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|
        |--------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
        |Position| 0| 0|-1 | ½|-1| 0 | ½| 1| 0 | 0| 0|-1| ½| 1| 0 |-1| 0| 0 | 0| 0|-1|-1| 0| 0 | ½|-1| 0|
        |Normal  | 0| 0| 1 |-⅓|⅔|⅔|-⅓|-⅔|⅔| 0| 0| 1|-⅓|-⅔|⅔|$\sqrt{5}/3$|0|⅔| 0| 0| 1|$\sqrt{5}/3$|0|⅔ |-⅓|⅔|⅔|
        
        </div>

    Drawing
    :   For each scene object,
        
        1. Bind that object's vertex array object
        2. call `gl.drawArrays`
    
    This works well for objects that do not share vertex attributes,
    such as points or flat-shaded polyhedra.
    If vertices and their attributes are used for multiple primitives,
    as is the case for most virtually all polygonal approximations of smooth objects,
    the previous option is more efficient.
    
    </details>

1.  <details><summary>For many copies of the exact same object:</summary>

    If you have several multiple copies of the same scene object in the scene
    such that you can easily compute their placement using the same `uniform`s coupled with an integer telling you which copy you're drawing,
    then use one of the previous two options but use the `gl.drawElementsInstanced` or `gl.drawArraysInstanced` methods instead of the non-instanced options.
    
    This is generally *much* faster than using the non-instanced options repeatedly,
    but unless you have identical objects positioned in some kind of fixed grid or pseudo-random scattering it is unlikely to be useful.
    
    </details>

1.  <details><summary>For very many distinct objects:</summary>
    
    Setup
    :   For a set of scene objects that will have the same set of vertex attributes,
    
        1. Many an array of attribute values for each vertex of all scene objects, one after the other.
            
            For example, if you have a 12-vertex sphere and a 30-vertex knob you'd put the vertices of the sphere in indices $0$ though $12n-1$ and of the knob in indices $12n$ through $32n-1$, where $n$ is the number of values per vertex. Technically you can interleave vertices of different objects, but doing so has no advantage and might impeded cache performance.
        
        1. Make an array of primitive connectivity for all scene objects, one after the other.
        
            For example, if you have a 20-triangle sphere and a 50-triangle knob you'd put the vertices of the sphere in indices 0 though 59 and of the knob in indices 60 through 209. You cannot interleave the triangle indices: they have to be grouped by scene object.
        
        1. Make a vertex array object on the GPU to collect the next steps
        1. Send each attribute values array to the GPU as an array buffer
        1. Send the connectivity array to the GPU as an element array buffer

    Drawing
    :   1. Bind that vertex array object
        2. For each scene object, call `gl.drawElements` with `offset` of the index of the first entry in the index array and `count` of the number of index values.
            
            For example, the 50-triangle knob above would use `offset` of 60 and `count` of 150.
    
    This works well for almost any object type.
    It's a bit more confusing to the programmer and makes for harder-to-maintain code,
    but it uses fewer buffers on the GPU and can be marginally faster and use slightly less GPU memory.
    
    There's also a similar shared-array, offset-and-count option for `gl.drawArrays`, `gl.drawElementsInstanced`, and `gl.drawArraysInstanced`.
    
    </details>

1.  <details><summary>For saving GPU memory given several small attributes:</summary>
    
    WebGL assumes all attributes are 4-vectors and at least nominally expands smaller attributes to that size automatically.
    If you have multiple attributes that collectively take up less than 4 floats per vertex
    (for example, a 2D texture coordinate and a 1D shininess parameter)
    you can save some time and space by combining them into a larger vector when providing the buffer.
    
    </details>


