---
title: Parsing OBJ Files
summary: How to parse one of the most common simple 3D model formats.
---

OBJ file format (also called [Wavefront .obj](https://en.wikipedia.org/wiki/Wavefront_.obj_file)) is a simple format to represent 3D objects. Geometry is represented by vertices (V), faces (F), texture coordinates, normals, etc. For a bit more information on OBJ format you can look [here]([https://en.wikipedia.org/wiki/Wavefront_.obj_file](https://en.wikipedia.org/wiki/Wavefront_.obj_file)). 

# Line-based file

The OBJ format is a line-based text format.
Each line is either blank (ignore blank lines)
or consists of several space-separated tokens.
The first token is an indicator of what kind of line it is.

Number in OBJ are stored in any format most programming languages can handle,
such as `-2`, `3.45`, or `7.8849e-05`.
In JavaScript, these can be parsed using the built-in `Number` function.

## Line types

A `#` line is a comment; ignore it. Also ignore any lines that begin with a character we haven't documented here.

A `v` line is a vertex.
After the `v` come 3 numbers giving the position,
optionally followed by 3 more giving the vertex color.

A `vn` line is a normal.
After the `vn` come three numbers giving the normal direction.

A `vt` line is a texture coordinate.
After the `vt` come two numbers giving the coordinate.

An `f` line is a face.
After it comes three or more index specifiers.
If there are more than 3, the triangles are the first and each pair of adjacent others

:::example
`f 2 3 5 7 11` defines 3 triangles: `f 2 3 5`, `f 2 5 7`, and `f 2 7 11`
:::

An index specifier in general has **three integers separated by slashes**.

1. The first integer tells which `v` line the position (and color) come from:
this is a **1-based index** (not 0-based like WebGL wants) from the beginning of the file, so `2` refers to the second `v` line.
2. The second integer tells which `vt` line the texture coordinate comes from, again with 1-based indexing.
3. The third integer tells which `vn` line the normal comes from, again with 1-based indexing.

The second and third integers may be omitted if the file doesn't have `vt` or `vn` lines,
and trailing slashes may be removed; `1//` will usually be stored as just `1`, `1/1/` as `1/1`, and `1//1` as itself.

`f` lines always come after the `v`, `vt`, and `vn` lines they reference.

# From OBJ to VAO

The vertex array objects we've been using (option 1 from [the geometry page](webgl-goemetry.html)) are similar to OBJ:
they have arrays of per-vertex values and an array of indices making up faces.

## Just `v` and `f`

In the absence of `vn` and `vt`, we can convert one to the other directly:
convert the `v` lines directly into the arrays of per-vertex values,
split the `f` lines into triangles,
subtract 1 from all `f` indices, and make the result our index buffer.

## Also `vn` and/or `vt`

With `vn` and `vt` things are less straightforward because OBJ lets each attribute has its own indexes.
Broadly speaking, we have two options:

### No indices

1. Load the `v`, `vt`, and `vn` lines into separate temporary arrays
2. For each `f`, look up the indices in the temporary arrays and push the resulting values into data buffers
3. Use `drawArrays` instead of `drawElements` on the resulting data buffers (option 2 from [the geometry page](webgl-goemetry.html))

:::example
Given this OBJ

```obj
v 1 1 0
v -1 1 0
v -1 -1 0
v 1 -1 0
vn 0 0 1
f 1//1 2//1 3//1
f 1//1 3//1 4//1
```

we'd make 

position buffer
:   `[1,1,0, -1,1,0, -1,-1,0, 1,1,0, -1,-1,0, 1,-1,0]`{.js}

normal buffer
:   `[0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1, 0,0,1]`{.js}

and then call `drawArrays`
:::

### Make new indices

1. Load the `v`, `vt`, and `vn` lines into separate temporary arrays
2. Make a map from `f` index value to new corrected index number
3. For each index value of each `f`
    - If we've seen the index value before, use the corrected index number
    - Otherwise, add its looked-up attributes into the data buffers and add a new entry into the corrected index number map

:::example
Given this OBJ

```obj
v 1 1 0
v -1 1 0
v -1 -1 0
v 1 -1 0
vn 0 0 1
f 1//1 2//1 3//1
f 1//1 3//1 4//1
```

we'd make 

position buffer
:   `[1,1,0, -1,1,0, -1,-1,0, 1,-1,0]`{.js}

normal buffer
:   `[0,0,1, 0,0,1, 0,0,1, 0,0,1]`{.js}

index buffer
:   `[0,1,2, 0,2,3]`{.js}

corrected index mapping
:   `{"1//1":0, "2//1":1, "3//1":2, "4//1":3}`{.js}

and then call `drawElements`
:::


# Scale, centering, and orientation

OBJ files contain coordinates with no units
and axes with no defined interpretation.

## Orientation

It is common to find OBJ where

- $+z$ is up and $+y$ is forward
- $+y$ is up and $-z$ is forward
- $+y$ is up and $+z$ is forward

Other orientations are also possible.

There is no easy way to tell what orientation a given file has
except by having a user to look at the data rendered in one orientation and say "that's not right."

## Scaling

OBJ files have no notion of absolute scale.
Files created for 3D printing often use 1 unit = 1 millimeter,
those created for architectural visualization often use 1 unit = 1 meter,
and most other uses don't have dominant patterns.
It is common to find 1000-fold differences in intended scale between different OBJ files.

Fortunately you can re-scale data automatically:
find the maximum separation of points $s$ in the data
and then multiply every point by $t/s$ where $t$ is your desired maximum separation.

## Centering

Vertex positions may be any number, and there is no requirement that they be centered around any particular point.
It is relatively common to find

- All coordinates positive, putting the model in the first octant
- The "up" coordinate positive, the other two centered around 0
- All three coordinates centered around 0

But sometimes you'll also find files where the data is centered very far from the origin.

Fortunately you can re-center data automatically:
find the average point $p$ in the data
and then add $c-p$ to every point, where $c$ is your desired center location.

