---
title: WebGL's Graphics Pipeline
summary: A collapsible top-down view of how 3D graphics with WebGL2 works.
...


The following list provides a 2--3-level-deep outline of the interactive graphics pipeline.
It defaults to just an overview of the big steps;
clicking on a step will show you more about that step,
possibly including additional sub-steps.

1.  <details><summary>Specify 3D geometry</summary>
    
    This is done in the CPU, with the final results sent to the GPU for later drawing.
    
    Older systems use what's called "immediate mode" where each bit of geometry is rendered as soon as it is provided.
    Newer systems use "buffers" to store geometry data in video memory for much faster rendering.
    The buffer workflow works as follows:
    
    a. <details><summary>Define triangulated data</summary>
        
        Often this will come from artist-defined data we load from a file.
        Sometimes we'll construct it in the code
        either based on geometry (e.g. to make a sphere)
        or some kind of visual simulation (e.g. to make a mountain range).
        
        This data is usually specified in "model space" or "object space"
        with $(0,0,0)$ either in the middle of or at a corner of the data.
        
        </details>

    a. <details><summary>Convert to bytes and send to the GPU</summary>
        
        We want the GPU to be able to organize data in a way that facilitates fast drawing, so we have two copies:
        one we control in the CPU,
        and one we draw from in the GPU.
        
        i. Convert our model into one or more arrays of bytes.
            
        i. Allocate a buffer, a region of memory on the GPU.
        
        i. Send the bytes from the CPU to the GPU.
        
        </details>

    a. <details><summary>Tell the GPU how to interpret those bytes</summary>
        
        Bytes only have meaning if we know how to group and parse them.
        We need to tell the GPU
        
        i. What the bytes are for (vertex positions? triangle connectivity? other?)

        i. How they are encoded (bytes per element, in what format)

        i. If there's any bytes to ignore (e.g. because we have mixed several data in one byte stream)
        
        </details>

    a. <details><summary>Each frame, ask the GPU to render the geometry</summary>
        
        There are multiple ways to do this, but the most common sequence is
        
        i. Clear the screen
        i. Pick a shader program to run
        i. Send the GPU the current value of global values called **uniforms**
        i. For each model
            
            1. Send the GPU the current value of model-specific **uniforms**
            1. Tell the GPU which model to load (from the buffers it has in its memory)
            1. Ask the GPU to draw the model
        
        </details>
    
    </details>

1. <details><summary>Move vertices to view scene</summary>
    
    The GPU manages how data flows between steps here, but allows us to provide code for what happens at each step.
    
    a. <details><summary>Optionally, tesselation and geometry shaders make high-res geometry out of low-res input</summary>
        
        This is not supported by WebGL nor most embedded systems, so if we want to do it we either need to use a hardware-specific API (we won't in this course) or do it on the CPU as part of how we specify geometry.
        
        </details>

    a. <details><summary>Implement a vertex shader</summary>
    
        This step is fully programmable so we can do whatever we wish here, but we almost always do the following:
        
        i. <details><summary>Apply a model transformation to position and size the object in the scene</summary>
            
            This converts from *object coordinates* to *world coordinates*.

            </details>

        i. <details><summary>Apply a view transformation to position the scene in front of the camera</summary>
            
            We view the scene by assuming a fixed camera location:
            always at $(0,0,0)$ and pointing along the $z$ axis.
            To "move" the camera somewhere else we instead
            move *the entire scene* so that our desired camera location is at that fixed location and everything else located around it.
            
            This converts from *world coordinates* to *view coordinates*.
            
            </details>

        i. <details><summary>Compute aspect ratios and divisors for perspective projection</summary>
            
            
            1. <details><summary>Aspect ratio</summary>
            
                The GPU always called the left edge of the screen $x=-1$ and the right edge $x=1$;
                the bottom edge $y=-1$ and the top edge $y=1$.
                If the screen is non-square this will stretch or squish things.
                To counter that, we'll preemptively squish or stretch them so the subsequent stretch or squish undoes our preemptively
                we squish or stretch.
                
                </details>
                
            1. <details><summary>Divisors</summary>

                Things close to you look larger than things far from you.
                The GPU achieves that by allowing you to specify a $w$, representing depth into the scene, and dividing everything by $w$.

                </details>
            
            1. <details><summary>Depth</summary>

                The GPU clips off things that are too close or too far from the camera.
                The nearest visible point has $\frac{z}{w}=-1$ and the farthest $\frac{z}{w}=1$.
                We almost always have to change $z$ to make this work out.

                </details>

            </details>

        </details>

    </details>

1. <details><summary>Convert shapes to the pixels they cover</summary>
    
    All parts of this step are built in to the GPU hardware with just a few small areas we can influence via parameters.
    
    a. <details><summary>Primitive assembly</summary>
        
        When drawing triangles, each triangle is made up of three vertices.
        WebGL provides several ways to specify which three vertices makes up each triangle
        and also allows pairs of vertices to form lines
        and single vertices to be rendered as points.
        
        </details>

    a. <details><summary>Frustum clipping</summary>
        
        Both for efficiency and to prevent division-by-zero errors in the next step,
        each primitive is clipped to just the part that lies inside frustum, which is a truncated pyramid shape.
        
        Frustum clipping can be implemented as clipping against six independent planes.
        
        Clipping a triangle against a plane can leave it unchanged or dicard it entirely (when all vertices lie on the same side of the plane),
        replace it with a smaller triangle (when one vertex is inside and two outside the plane),
        or replace it with two smaller triangles (when one vertex is outside and two inside the plane).
        
        </details>

    a. <details><summary>Division by $w$</summary>
        
        Linear perspective projection is achieved by having a depth-based divisor for each vertex, provided by the vertex shader.
        Dividing $x$ and $y$ by this $w$ divisor term creates perspective projection.
        Dividing $z$ by $w$ creates a useful discretization of depth.
        Dividing everything else by $w$ helps interpolate values acros triangles correctly.
        
        </details>
    
    a. <details><summary>Culling</summary>
        
        If the three vertices of a triangle are in counter-clockwise order it is considerd to be front-facing;
        otherwise it is considered to be back-facing.
        Culling is diabled by default, but if enabled can be configured to discard either front or back faces.
        
        It is possible to pose the back/front property in homogeneous coordinates and do culling immediately after primitive assembly, resulting in faster overall computation. This is usually seen as an optimization, not as the definition of culling.
        
        </details>

    a. <details><summary>Viewport transformation</summary>
        
        At this point $x$, $y$, and $z$ are all between −1 and 1.
        We change that here,
        adjusting $x$ to be between 0 and raster width,
        $y$  to be between 0 and raster height,
        and $z$ to be between 0 and 1.
        
        </details>
    
    a. <details><summary>Rasterization and interpolation</summary>
        
        The scanline algorithm
        applies either the Bresenham or DDA algorithm
        in two dimensions
        to efficiently find the exact set of pixels that each triangles covers.
        We call the bit of a triangle that covers one pixel a "fragment".
        Scanline also interpolates each other per-vertex datum we provide to each fragment.
        
        </details>
    
    a. <details><summary>Division by $\frac{1}{w}$</summary>
        
        The $x$, $y$, and $z$ coordinates are found in the form we want them by the scanline algorithm,
        but the other interplated data has an unresolved division.
        We take care of that division here.
        
        </details>
    
    </details>

1. <details><summary>Color each pixel</summary>
    
    Broadly speaking, setting pixel colors is done by setting fragment colors (which is done by code we control) and then combining all the fragments (which is mostly built-in with a few parameters we control).
    
    a. <details><summary>Fragment discarding</summary>
        
        If it is known that some fragments will never be seen
        they will be discarded here.
        
        i. If rendering directly to a display, the operating system that owns the display can discard fragments.
        
            This is relatively uncommon.
        
        i. If a scissor region was set up, fragments are discarded based on that.

            This is relatively uncommon.
        
        i. <details><summary>Stencil test</summary>
        
            A stencil buffer is a raster the size of the frame buffer, typically set by special rendering calls.
            The stencil test compares each fragment with the corresponding pixel of the stencil buffer
            to decide if the fragment should be discarded.

            There are a small number of customizable comparisons that can be used for this test.
            
            </details>
        
        </details>

    a. <details><summary>Fragment Shader</summary>

        This step is fully programmable so we can do whatever we wish here, but the most common parts are:
        
        i. <details><summary>Interpolate some parameters</summary>
            
            The vertex shader can provide any number of **varying** values:
            `out` variables written by the vertex shader
            that are interpolated to each fragment
            and available as `in` variables in the fragment shader.
            
            </details>
        
        i. <details><summary>Look up some parameters</summary>
        
            Often a few of the varyings are used to look up other values in a large array, most often provided as an image called a "texture".
            
            </details>

        i. <details><summary>Compute some parameters</summary>
        
            Often the provided varyings care combined with some uniform or constant values to compute other values.
            
            A common example is using a varying position of the fragment in the scene and a uniform position of a light in the scene to compute a direction to the light.
            
            </details>

        i. <details><summary>Evaluate a BSDF</summary>
            
            The appearance of materials in light is modeled by a family of functions called Bidirectional Scattering Distribution Functions, or BSDFs.
            A versatile and simpler subset of BSDFs are the Bidirectional Reflectance Distribution Functions, or BRDFs.
            
            Fragment shaders use the various parameters available to them to compute the color of the fragment based on the BSDF.
            
            </details>

        i. <details><summary>Other adjustments</summary>
            
            Fragment shaders can modify fragment depth,
            discard unwanted fragments,
            and compute raster data other than colors.
            
            None of these is very common.
            
            </details>

        </details>

    a. <details><summary>Depth test</summary>
        
        A depth buffer is raster the size of the frame buffer
        which stores the $z$ value of each pixel.
        Fragments farther from the camera than that $z$ are discarded.
    
        There are a small number of customizable options for how the depth buffer is accessed and updated.
        
        </details>

    a. <details><summary>Blending</summary>
    
        If a fragment was not discarded, it is used to change the color at its pixel in the frame buffer.
        By default this is a simple replacement,
        but there are other options
        whereby the existing color and the new fragment's color are combined in various ways.
        Collectively, all of these are called "blending".
        
        If blending occurs, it often uses a "alpha" channel
        to model the opacity of the fragment and the pixel.
        Because of that, the entire blending process
        is sometimes called "alpha blending" or "alpha compositing."
        
        </details>

    </details>

1. <details><summary>Write frame buffer</summary>
    
    Once all the pixels are fully computed, the resulting values are placed as bytes in an image.
    
    a.  <details><summary>Multisample</summary>
        
        Full-screen anti-aliasing (FSAA) improves image quality
        by rendering at a much higher resolution that the final image,
        then averaging clusters of pixels.
        That averaging is taken care of here.
        
        </details>

    a.  <details><summary>Gamma</summary>
        
        The eye does not perceive light linearly,
        and every bit counts when it comes to images.
        Gamma encoding is a way of attempting distribute bits of an encoding
        in a way that matches visual acuity.
        In the ideal gamma encoding,
        encoded light intensities $i$ and $i + \epsilon$
        should look equally far apart regardless of $i$.
        
        Ideal gamma encoding depends on many things, including the specific viewer's eye and the background light in the room when viewing the screen.
        An accepted "good" gamma is the sRGB gamma function
        which uses roughly 50% of the available bit patterns
        to encode the darkest 20% of light.
        
        </details>

    a.  <details><summary>Dither</summary>
        
        We have finite number of bits to store color with,
        but want more color detail in the image.
        Dithering solves this problem
        but ensuring that if we blur the image we'll get more accurate colors.
        There are several ways to do this; two simple ones are
        
        - <details><summary>Stochastic</summary>

            Stochastic dithering uses is randomized rounding.
            If a pixel's red channel is computed as 121.85,
            dithering will randomly pick wither 121 (15% chance) or 122 (85% chance) as the number to store.
            
            </details>
        
        - <details><summary>Error diffusion</summary>

            Error diffusion uses detects the error introduced by quantizing one pixel
            and distributes it to the neighboring pixels.
            If 121.85 is approximated as 122,
            we reduce the target brightness of the neighboring pixels by a cumulative amount equal to the 0.15 we over-used;
            for example, we might reduce three neighbors each by 0.05.

            </details>
        
        
        

        Dithering is used to avoid the eye noticing transitions between the finite set of available colors.
        For very limited color pallettes it also simulates more colors ar the cost of making the scene look noisy.
        
        </details>
    
    </details>


Another view shows how the GPU-run parts operate

<figure>
<img src="../files/pipeline.svg"  class="wide"/>
<figcaption>
A shader program consists of a vertex shader and fragment shader linked together.
When a draw is requested the fixed functionality

1. accesses buffers of vertex data and sends it into the vertex shader
2. assembles primitives from vertex shader output, clips the primitives, divides by $w$, culls and applies viewport transformation, rasterizes into fragments, and undoes the division by $w$
3. sends the fragments with their interpolated values through the fragment shader to find the color of each fragment
4. discards invisible fragments via the depth buffer and related tests, blends new fragments onto old pixels, applies gamma, and converts into bits with dithering
</figcaption></figure>

