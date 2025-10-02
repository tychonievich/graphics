---
title: Terrain via the faulting method
summary: Fault computation for simple fractals.
...


# Terrain Generation 

Many basic terrain modeling algorithms employ something called *Perlin noise* to create a highly detailed natural appearance. Invented by Ken Perlin in 1982 while working on the movie *Tron*, Perlin noise uses randomness and repetition to synthesize 2D and 3D textures. In 1997, Perlin won an Academy Award for Technical Achievement from the Academy of Motion Picture Arts and Sciences for this contribution to graphics. Perlin noise and techniques based off of it are still widely used in games and movies today.

Realistic terrain generation in modern games require tools that do more than just model the basic underlying terrain...these tools support operations like creation of vegetation and roads and erosion. See [this talk by Ubisoft developer Etienne Carrier](https://www.youtube.com/watch?v=NfizT369g60) if you are interested in seeing the tools technical artists use these days. 

![Example terrain created with Perlin noise and various additional steps afterward](https://illinois-cs418.github.io/img/perlin1.jpg)


# The Faulting Method

The same year (1982) that Ken Perlin crated Perlin Noise,
Benoit Mandelbrot proposed a less efficient but easier-to-implement method called _the faulting method_.

In addition to this page, you can find a summary of the faulting method in section 3.1.2 of the following survey paper on terrain generation algorithms:

_A Review of Digital Terrain Modeling_. Eric Galin, Eric Guérin, Adrien Peytavie, et al. [[PDF]](https://hal.archives-ouvertes.fr/hal-02097510/file/A%20Review%20of%20Digital%20Terrain%20Modeling.pdf)

The overall faulting method process runs as follows:

1. [Create a triangulated 2D grid](make-geom.html)
2. Repeatedly
    a. [Pick a random vertical plane, called a **fault plane**](#random-fault-planes)
    b. [Move points on one side of the fault plane up and points on the other side of the fault plane down by some small increment](#fault-plane-displacement)
3. [Compute the vertex normals](make-geom.html)


# Random fault planes

We will construct a fault plane cutting through the terrain by generating a random point $p$ and random direction vector $\vec{n}$ to define the plane.

1. First generate a random point $p$ in the $(x,y)$ bounds of the grid.
2. Generate a random normal vector $\vec{n}$ with $z = 0$ for the plane;
    in other words, $(x_n,y_n,0)$, where $x_n,y_n$ is a point uniformly sampled on the unit circle.
    If $\theta$ is a random angle between $0$ and $2\pi$ then an appropriate random normal would be $\vec{n}=(\cos{\theta},\sin{\theta},0)$.

<a id="fault-plane-displacement"></a>
Then for each vertex $b$,

1.  Test which side of the plane that vertex falls on by using the dot product test $(b-p) \cdot n \ge  0$.

    ![Faulting plane computation using dot products, by Eric Shaffer](https://illinois-cs418.github.io/img/dottest.jpg)

2.  If $b$ is in the negative half-space, **lower** the $z$ coordinate of by some amount $\Delta$.
    If $b$ is in the positive half-space, **raise** the $z$ coordinate of by some amount $\Delta$.

    **Optional** You may get better results with distance weighted displacements for $\Delta$, only moving vertices that are relatively close to the faulting plane.
    To do so compute the distance $r=\mathbf{d}(b,\Phi_i)$ from $b$ to the fault plane $\Phi_i$ and alter the $\Delta$ you use for each vertex by a coefficient function $g(r)=(1-(r/R)^2)^2$ for $r<R$ and $g(r)=0$ elsewhere.
    $R$ is a parameter you determine.

Once you're done, you might need to re-scale the vertical axis to get the desired ratio between vertical displacement and horizontal size.

