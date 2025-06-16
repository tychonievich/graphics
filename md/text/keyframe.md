---
title: Keyframes, Bones, and Skinning
summary: An overview of how we animate articulated characters.
...

# Keyframes and Tweening

In production hand-drawn animation, the most respected artists draw the most important or *key* frames, the ones that define the motion overall. Less expensive artists then draw the in-between frames that make the motion progress smoothly from one keyframe to another, a process known as *tweening*.

In computer animiation, most often the keyframes are still supplied by an artist or motion capture suit and the computer is expected to do the tweening.

The simplest way to tween is to interpolate between keyframes.
Linear interpolation is the easiest, and [Bézier](bezier.html) interpolation is also common.
Recall that Bézier interpolation is simply linear interpolation of linear interpolations.

While tweening can be done on the GPU, it is more commonly done on the CPU:
we check the current time against the keyframe times,
pick the two adjacent keyframes,
and interpolate between them to find the matrices we send to the GPU this frame.

:::example
The following show how interpolation could be implemented in GLSL.
Linear interpolation is common in GPU code for skinning,
while Bézier interpolation is more common in CPU code for tweening.

```glsl
/**
 * Linear interpolation: returns A when t=0, B when t=1,
 * and intermediate values for t in between 0 and 1.
 */
mat4 linear_interpolation(float t, mat4 A, mat4 B) {
    return (1.0-t)*A + (t)*B;
}

/**
 * Cubic Bézier interpolation: returns A when t=0, D when t=1,
 * and intermediate values for t in between 0 and 1,
 * being tangent to the A->B path at t=0
 * and tangent to the C->D path at t=1.
 */
mat4 bezier_interpolation(float t, mat4 A, mat4 B, mat4 C, mat4 D) {
    mat4 AB = linear_interpolation(t, A,B);
    mat4 BC = linear_interpolation(t, B,C);
    mat4 CD = linear_interpolation(t, C,D);
    mat4 ABC = linear_interpolation(t, AB,BC);
    mat4 BCD = linear_interpolation(t, BC,CD);
    mat4 ABCD = linear_interpolation(t, ABC,BCD);
    return ABCD;
}
```
:::

## What to tween

Translation (either by vector or matrix) and uniform scaling tween as expected.
Rotation, however, is more complicated.

- Interpolating rotation matrices causes unwanted shrinkage mid-rotation
    because end-of-path vertices, not angles, are being interpolated by the matrices.
- Interpolating axis and angle causes strange hooked paths.
- Interpolating angles around several fixed perpendicular axes can make smooth rotations, but also suffers from [gimbal lock](https://en.wikipedia.org/wiki/Gimbal_lock).
- Thus, we usually interpolate [quaternions](quaternions.html) instead..

Quaternions have an interesting and rich mathematical basis, but from graphics perspective they are

- 4D vectors
- that represent rotations
- and interpolate reasonably well
    - especially if the keyframes are relatively similar
    - the more different the keyframe quaternions are, the more the interpolation will have slow rotation near the keyframes and faster rotation halfway between them
- and are converted to matrices after interpolation


# Bones and other scene graphs

Jointed characters are usually animated by imagining a set of bones inside the character.
Each can rotate and has an origin defined to be a specific offset from another bone.
Those offset rotations can be represented by a matrix hierarchy:
one matrix per bone, where each is part rotation and part translation.
The hierarchy defines something like
$$\vec w_{\text{toe}} = M_{\text{pelvis}} M_{\text{thigh}} M_{\text{calf}} M_{\text{foot}}\vec o_{\text{toe}}$$
where $\vec o_{\text{toe}}$ is the object-space position of a vertex and $\vec w_{\text{toe}}$ is the corresponding world-space position of that vertex.

This hierarchy of bones is an example of a "scene graph."
Almost all scene graphs are actually scene trees:
a set of objects or object parts (such as two thighs and a waist) defined as children of another part (such as the pelvis),
several layers deep.

When rendering scene graphs on a GPU
it is typical to iterate through the nodes on the graph in the CPU,
convert the interpolated positions and orientations into matrices,
then send the resulting matrices to the GPU along with the geometry that uses it.
Sending all of the matrices of a singe object and its geometry at once can also be done, provided that each vertex also has information identifying which matrices it should use.

# Skinning

When I bend my knee,
the skin on my calf moves in a fairly rigid way as if controlled by one matrix
and the skin on my thigh moves as if controlled by another matrix,
but the skin near my knee does something different.
At the top of my knee it moves mostly like by thigh, at the bottom mostly like my calf, and in between it moves in between.

This smooth variation in which vertices are controlled by which matrices is called "skinning".
A common approach to skinning is to

1. Define an integer for each matrix
2. Define a floating-point weight for each vertex.
    If a vertex has weight 3.2 it is controlled 80% by matrix 3 and 20% by matrix 4.
3. In the vertex shader, linearly interpolate where the vertex would be if controlled by each matrix based on its weight.

This does not create perfect results, but it does create the results that most graphics applications, both interactive and production, assume.
It falls to a special type of artist called a "rigger" to set up the bones and weights in such a way that this creates believable motion.
