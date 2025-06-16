---
title: Linear interpolation
summary: A common tool throughout graphics.
...

Linear interpolations are common throughout graphics.
They allow us to treat a finite set of points as if it was a continuous curve or surface at minimal cost.
It is so common that it is often abbreviated as "lerp", from **l**inear int**erp**olation.

# Basic lerp

Basic linear interpolation requires a pair of end points, $\vec p_0$ and $\vec p_1$
and how far to go between them, $t$, where we assume $0 \le t \le 1$.
The lerp is then computed as $$(1-t)\vec p_0 + (t)\vec p_1$$
This is a function with the following properties:

- If $t=0$, the lerp gives $\vec p_0$
- If $t=1$, the lerp gives $\vec p_1$
- For $0 < t < 1$, the lerp gives points along the line between $\vec p_0$ and $\vec p_1$
- The function is linear, meaning it is easy to compute and invertable

## Inverse lerp

An inverse lerp takes the interpolated points and endpoints and finds the parameter value.
This can be computed in several ways,
but one of them that finds the best possible parameter even for points that were not on the line is
$$t = \dfrac{(\vec p - \vec p_0)\cdot (\vec p_1 - \vec p_0)}{(\vec p_1 - \vec p_0)\cdot(\vec p_1 - \vec p_0)}$$


# Bilinear interpolation

Bilinear interpolation is a common 2D version of a lerp.

Given four points, $\vec p_{0\,0}$, $\vec p_{0\,1}$, $\vec p_{1\,0}$, and $\vec p_{1\,1}$;
and two parameters $s$ and $t$ both between 0 and 1,
then the bilinear interpolation
is equivalently any of the following:

$$(1-s)(1-t)\vec p_{0\,0} + (1-s)(t)\vec p_{0\,1} + (s)(1-t)\vec p_{1\,0} + (s)(t)\vec p_{1\,1}$$
or
$$\mathrm{lerp}\big(s, \mathrm{lerp}(t, \vec p_{0\,0}, \vec p_{0\,1}), \mathrm{lerp}(t, \vec p_{1\,0}, \vec p_{1\,1})\big)$$
or
$$\mathrm{lerp}\big(t, \mathrm{lerp}(s, \vec p_{0\,0}, \vec p_{1\,0}), \mathrm{lerp}(s, \vec p_{1\,0}, \vec p_{1\,1})\big)$$

Four points do not, in general, fall on a plane so this function is not linear in the strict mathematical sense,
though it is still often called "linear" in computer graphics because it retains most of the nice computational properties of linear functions.
Points found via bilinear interpolation technically lie on a hyperbolic paraboloid.

## Interpolating on a grid

One common use of bilinear interpolation is to look up points on a grid.
The basic process runs as follows:

1. Transform the point into the grid coordinate system.

    <div class="example">
    
    Consider a wrapping texture with a 256×256 sampler and the texture coordinate $(3.1, -7.25)$.
    Because it is wrapping we'd first wrap it into the 0–1 space for $(0.1, 0.75)$;
    then scale it up to the 256-space for $(25.6, 192)$
    
    </div>
    
2. Split the coordinates into integer and fractional parts.
    The integer parts are used to find the points, the fractional parts become the parameters.
  
    <div class="example">
    
    Continuing our example, the integer part is $(25,192)$ and the fractional part is $(0.6, 0)$.
    
    </div>

3. Look up four control points from the grid, using the integer parts and the integer parts +1.
    Bilinearly interpolate these using the fractional parts.
    
    <div class="example">
    
    Continuing our example, we have
    
    ````js
    lerp(0.6,
      lerp(0, grid[25][192], grid[25][193])
      lerp(0, grid[26][192], grid[26][193])
    )
    ````
    
    </div>


# Trilinear interpolation and beyond

Trilinear interpolation is a 3D version of a lerp,
with eight control points and three parameters.
One use of this is with mipmapping textures:
the `gl.LINEAR_MIPMAP_LINEAR` performs a trilinar interpolation
using the 2 nearest mipmap levels
along with the grid on each level.

# Simplex lerp

Lerps can also be extended to triangles, tetrahedra, and higher-dimensional simplices
in a way that fully preserves linearity.

Observe that the standard lerp uses two parameters, one for each input point,
selected so that they always sum to 1.
Simplex lerps continue this pattern for more than two input points.

For a triangle, we have three input points $\vec p_0$, $\vec p_1$, and $\vec p_2$;
and three parameters $w_0$, $w_1$, and $w_2$ such that $w_1 + w_2 + w_3 = 1$
giving us two degrees of freedom (we can solve for any one $w$ given the other two as $w_i = 1 - \sum_{j\ne i} w_j$).

For a tetrahedron, we have four input points and four parameters, again summing to  for 3 degrees of freedom.

When rasterizing a triangle we are finding the triangular simplex lerp at every pixel for every per-vertex attribute.
Finding the [barycentric coordinate](rays.html#inverse-mapping-and-barycentric-coordinates) of a ray-triangle intersection is computing an inverse simplex lerp and using the barycentric coordinate to interpolate per-vertex attributes to the intersection point is simplex lerping.


# Repeated lerp

The [Bézier curve](bezier.html) can be presented as repeated lerping.
They are widely used as animation control paths, in 2D illustration programs, and to define fonts.

Tensor product patches apply the Bézier curve repeated lerp technique to bilinear interpolation.
NURBS are a variant of tensor product patches that were popular in the '90s and '00s.
Catmull-Clark subdivision surfaces converge to tensor product patches.
Most 3D graphics programs I've used use one of these as their primary geometry definition technique.

Triangular patches apply the Bézier curve repeated lerp technique to simplex interpolation.
Despite theoretically being more versatile, these are not as common as tensor product patches
in part because they are not as good at representing the cylindrical shapes that are common in, creatures, plants, and manufactured objects.

# Slerp and friends

Various interpolations try to mimic the lerp in non-linear geometries.
For example, spherical linear interpolation or slerp can smoothly interpolate unit vectors.
A variant of slerps are common when animating with [quaternions](quaternions.html#slerp).
I've even seen research papers that used a variant of lerps for hyperbolic geometry, called hlerps, instead of Euclidean or spherical, but not yet seen that in common use.
