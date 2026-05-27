---
title: Spherical Harmonics
...

Spherical harmonics are one of two common ways of representing functions that have a direction as their argument
(the other being environment maps such as cube maps).
They have the advantages of representing perfectly smooth functions with very few bytes;
and of being closed under rotation, which means they have no directions that are better than others.

Spherical harmonics are usually presented in spherical coordinates with complex numbers and imaginary exponentials.
That presentation is useful for describing how they are derived and proving their properties,
but is not particularly valuable in describing how they are used in computing.
This page instead uses only the real-number Cartesian coordinates used by all other vectors in graphics.

# Concept

Polynomial functions of $(x,y,z)$ are perfectly smooth over the surface of a unit sphere.
This is true both because polynomials are generally smooth
and also because the sphere is smooth.
Thus, a function like $x^2$ is smooth where $|x| \ne 1$ because the function is smooth generally,
and also smooth at the poles where $|x| = 1$ because the sphere eases into these points gradually,
causing the discontinuity caused by the sphere ending to be smoothed out by the sphere's gradual arrival at those points.

Spherical harmonics^[There are technically multiple sets of spherical harmonics. In graphics, we always mean Laplace's spherical harmonics, and in particular the real-numbered versions of those.] are a set of basis functions of polynomials over a sphere.
This set is smaller than and different from the common power basis^[Or common-in-graphics Bernstein basis used in Bézier curves] of $\{1, x, y, z, x^2, xy, xz, y^2, yz, z^2, x^3, x^2y, ...\}$
because the unit sphere constraint means that set would contain duplicates.

:::example
By definition, the surface of a unit sphere are the points where
$x^2 + y^2 + z^2 = 1$.
That could let us express any polynomial that has $x$ using $\sqrt{1-y^2-z^2}$ instead,
or any polynomial that has $y$ using $\sqrt{1-x^2-z^2}$ instead,
or several other substutions as well.
:::

The specific set of basis functions we want should be orthogonal, meaning the integral of the product of any two of the functions over the entire sphere is 0.
Orthogonality will make several otherwise-complex mathematical operations much simpler.

It is common to refer to the basis functions as $Y_{\ell, m}$
where $\ell$ is the polynomial power (often called the <dfn>band<dfn>) of the function
and $m$ is an integer between $-\ell$ and $\ell$, inclusive, indicating which function this is.

The duplicates possible on a sphere
and the orthogonality constraint
lead to a set of functions that are perhaps non-intuitive,
but can be combined to create any polynomial function over the sphere's surface.
That combination is generally expressed as a vector of weights:
$[1, 3, -2, -4]$
would mean the function
$Y_{0,0} + 3Y_{1,-1} -2Y_{1,0} -4Y_{1,1}$.

Confusingly, the term <dfn>spherical harmonics</dfn>
is used *both* to describe the basis functions
*and* to describe the vector used to combine the basis functions into a polynomial.
Which one is meant can usually be determined from context,
but for novices the overloaded term can be confusing.
It's generally best to assume the vector is being referred to unless that interpretation doesn't make sense.

# Basis functions

The spherical harmonic basis functions
each consist of an irrational scalar times
a polynomial with a few terms and integer coefficients.
The scalar is important to maintain orthogonality and generally cannot be omitted.

$$\begin{align*}
Y_{0, 0} = \frac{1}{2}\sqrt{\frac{1}{\pi}}& \\
\\\hline\\
Y_{1,-1} = \frac{1}{2}\sqrt{\frac{3}{\pi}}& y \\
Y_{1, 0} = \frac{1}{2}\sqrt{\frac{3}{\pi}}& z \\
Y_{1, 1} = \frac{1}{2}\sqrt{\frac{3}{\pi}}& x \\
\\\hline\\
Y_{2,-2} = \frac{1}{2}\sqrt{\frac{15}{\pi}}& xy \\
Y_{2,-1} = \frac{1}{2}\sqrt{\frac{15}{\pi}}& yz \\
Y_{2, 0} = \frac{1}{4}\sqrt{\frac{5}{\pi}}& (3z^2 - 1) \\
Y_{2, 1} = \frac{1}{2}\sqrt{\frac{15}{\pi}}& xz \\
Y_{2, 2} = \frac{1}{4}\sqrt{\frac{15}{\pi}}& (x^2-y^2) \\
\\\hline\\
Y_{3,-3} = \frac{1}{4}\sqrt{\frac{35}{2\pi}}& y(3x^2-y^2) \\
Y_{3,-2} = \frac{1}{2}\sqrt{\frac{105}{\pi}}& xyz \\
Y_{3,-1} = \frac{1}{4}\sqrt{\frac{21}{2\pi}}& y(5z^2-1) \\
Y_{3, 0} = \frac{1}{4}\sqrt{\frac{7}{\pi}}& z(5z^2-3) \\
Y_{3, 1} = \frac{1}{4}\sqrt{\frac{21}{2\pi}}& x(5z^2-1) \\
Y_{3, 2} = \frac{1}{4}\sqrt{\frac{105}{\pi}}& z(x^2-y^2) \\
Y_{3, 3} = \frac{1}{4}\sqrt{\frac{35}{2\pi}}& x(x^2-3y^2) \\
\\\hline\\
Y_{4,-4} = \frac{3}{4}\sqrt{\frac{35}{\pi}}& xy(x^2-y^2) \\
Y_{4,-3} = \frac{3}{4}\sqrt{\frac{35}{2\pi}}& yz(3x^2-y^2) \\
Y_{4,-2} = \frac{3}{4}\sqrt{\frac{5}{\pi}}& xy(7z^2-1) \\
Y_{4,-1} = \frac{3}{4}\sqrt{\frac{5}{2\pi}}& yz(7z^2-3) \\
Y_{4, 0} = \frac{3}{16}\sqrt{\frac{1}{\pi}}& 35z^4 - 30z^2 + 3 \\
Y_{4, 1} = \frac{3}{4}\sqrt{\frac{5}{2\pi}}& xz(7z^2-3) \\
Y_{4, 2} = \frac{3}{8}\sqrt{\frac{5}{\pi}}& (x^2-y^2)(7z^2-1) \\
Y_{4, 3} = \frac{3}{4}\sqrt{\frac{35}{2\pi}}& xz(x^2-3y^3) \\
Y_{4, 4} = \frac{3}{16}\sqrt{\frac{35}{\pi}}& x^2(x^2-3y^2) - y^2(3x^3-y^2) \\
\end{align*}$$

If you're looking for patterns in the functions above and not finding them,
that is normal and expected.
While the patterns are a little clearer in polar coordinates,
spherical harmonic basis functions are nontrivial to derive.
Generally code that uses them has the basis functions it uses
written directly into the code, copied from some table of basis functions like this.

While there are larger $\ell$ values (indeed, there is no upper limit),
I've never seen more than $\ell=4$ used in graphics code.
If higher resolution is wanted, an environment texture map is generally used instead.

# Rotation

It is possible to rotate a set of spherical harmonics coefficients
by an arbitrary 3D rotation
and arrive at another set of spherical harmonics coefficients of the same order that exactly represents the rotated function.
The math for doing this is nontrivial, but computable if there is a need.

Rotating spherical harmonics is rarely done in graphics.
In most cases it is simpler and less computationally expensive
to rotate the direction vector before computing the function value instead.

That said, the *fact* that spherical harmonics can be rotated is an important and valuable reason for using them in graphics.
It means that there is no "best" coordinate system:
unlike texture maps, spherical harmonics can represent any oritentation of data equally well.

**TO DO**: explain the recursive Ivanic & Rudenberg matrix construction algorithm.

# Approximation

A common task for graphics is to take some densely-sampled scene,
such as an environment map,
and approximate its value used spherical harmonics with a much smaller $\ell$.

Because spherical harmonics form an orthogonal basis, this approximation is much simpler than it would be otherwise.
The basic process is:

1. Start all coefficients at $0$.
2. Loop through each sample and add the intensity of the sample times the solid angle it covers times $Y_{\ell,m}(\hat d)$ (where $\hat d$ is the direction of the sample) to the coefficient $C_{\ell,m}$.
3. Divide all coefficients by the surface area of a unit sphere, $4 \pi$.

The trickiest part is computing the solid angle covered by each sample.

- For raytracing, if ray directions are sampled uniformly each has an expected solid angle of $\frac{4\pi}{N}$ where $N$ is the number of rays cast.

- For a $W$-by-$H$ pixel latitude-longitude environment map, pixel solid angle depends on $y$ as $\sin{\pi \frac{y}{H}} \frac{2\pi^2}{W H}$ where $y$, $W$, and $H$ are all measured in pixels.

- For a $N$-by-$N$ cube map face, pixel solid angle is most easily described in terms of the unit vector that looks up a point on the sphere; in that framing, the solid angle of the texel is $\dfrac{4}{N^2 \max(|x|,|y|,|z|)^3}$.

- For a $N$-by-$N$ octahedral map, pixel solid angle is most easily described in terms of the unit vector that looks up a point on the sphere; in that framing, the solid angle of the texel is $\dfrac{16}{N^2 (|x| + |y| + |z|)^3}$.

