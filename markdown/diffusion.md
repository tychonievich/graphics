---
title: Diffusion
...

Diffusion (sometimes called smoothing) is a common operation on grids in computer graphics.
It is used to blur images, to add lens bloom, to detect feature size during edge detection, to simulate viscosity in Eulerian fluids, etc.

There are many ways to compute diffusion on a grid, but the most computationally efficient is to apply a separable discrete Gaussian convolution filter.

# Convolution

A convolution filter is an array that sums to 1.
It has a center cell.
To convolve an array by a filter,
replace each value in the array with a new value computed by
centering the filter on that cell,
multiplying each filter entry with the corresponding cell value, and summing.

Convolving requires us to pick edge conditions
to handle what happens when the filter overlaps with the edge of the array.
Three edge conditions are common:

- Wrap: if you go off one edge of the array, you arrive at the opposite edge.
- Clamp: assume that all cells past the edge of the array have the same value as the nearest cell in the array. This is a special case of the Neumman boundary condition.
- Constant: assume that all cells past the edge of the array have the same arbitrarily-selected value (most commonly 0). This is also called the Dirichlet boundary condition.

:::example
To convolve array $[1,2,3,4,3,2]$
with filter $[0.2,0.4,0.3,0.1]$ centered on the second filter value ($0.4$)
with clamped boundaries:

- replace the first entry with $0.2\cdot 1 + 0.4\cdot 1 + 0.3\cdot 2 + 0.1\cdot 3 = 1.5$
- replace the second entry with $0.2\cdot 1 + 0.4\cdot 2 + 0.3\cdot 3 + 0.1\cdot 4 = 2.3$
- replace the third entry with $0.2\cdot 2 + 0.4\cdot 3 + 0.3\cdot 4 + 0.1\cdot 3 = 3.1$
- replace the fourth entry with $0.2\cdot 3 + 0.4\cdot 4 + 0.3\cdot 3 + 0.1\cdot 2 = 3.3$
- replace the fifth entry with $0.2\cdot 4 + 0.4\cdot 3 + 0.3\cdot 2 + 0.1\cdot 2 = 2.8$
- replace the sixth entry with $0.2\cdot 3 + 0.4\cdot 2 + 0.3\cdot 2 + 0.1\cdot 2 = 2.2$

Result: $[1.5,2.3,3.1,3.3,2.8,2.2]$
:::


# Separable

Convolving works in any dimension:
a 2D array uses a 2D filter,
a 3D array a 3D filter, etc.
Separable filters have the special property that they can be applied one dimension at a time.

If a 5×7 filter $F$ is separable, there's a 5×1 filter $F_1$ and a 1×7 filter $F_2$
such that convolution by $F$ has the same result as convolution by $F_1$ then by $F_2$.


# Discrete Gaussian

The diffusion differential equation on a regular grid has a simple solution:
it is convolution by a particular bell-shaped filter named for a similar continuous solution
which in turn is named for Carl Gauss.

The discrete Guassian filter is separable and symmetric:
the 2D version is simply the 1D version applied once in each dimension.

The 1D discrete Gaussian has, as its entries, the values of the modified Bessel function of the first kind.
That's a fancy-sounding name, but for our purposes can be computed without too much work.
It has a single parameter, $t \ge 0$, which indicates how much smoothing is taking place.

Let $n$ be the number of cells away from the center of the filter, so the center has $n=0$, both its neighbors $n=1$, and so on.
The filter value in any cell is then
$$e^{-t} \sum_{m=0}^{\infty} \dfrac{(t/2)^{2m+n}}{m!(m+n)!}$$
This is an infinite sum, but you don't need to compute infinitely many terms:
each subsequent $m$ gives a smaller additional term until eventually they stop mattering (the factorials in the denominator eventually overtake the polynomial in the numerator).
You can compute it with something like

```c
/**
 * Returns the `n`th element of the discrete Gaussian filter
 * with strength `t`. That is, computes an exponential $e^{-t}$
 * times the the modified Bessel function of the first kind $I_n(t)$.
 *
 * Written by Luther Tychonievich based on the definition of
 * the Bessel function and released into the public domain.
 */
double filterElement(unsigned int n, double t) {
    double answer = 0;
    double term = 1;
    double scale = exp(-t);
    t /= 2;
    for(int i=1; i<=n; i+=1) term *= t/i;
    t *= t;
    int m = 0;
    while((answer + term) != answer) {
        answer += term;
        m += 1;
        term *= t / (m * (m+n));
    }
    return scale * answer;
}
```

This filter has infinite support: that is, it will give a filter with an infinite number of entries.
However, the values fall quickly with `n`.
Typically stopping once the elements get to $10^{-6}$ will result in no perceptible impact in the filtered data,
and sometimes $10^{-3}$ is a sufficient cut-off.
If using a cut-off, it is wise to use an explicit normalizing scale by dividing the entries by their sum
instead of using the $e^{-t}$ normalization in the infinite-support definition.

:::example
The discrete Gaussian filter with $t=1.5$ is (to 3 digits of precision)
$[\dots
0.00000634,
0.0000597,
0.000484,
0.00329,
0.018,
0.0754,
0.219,
0.367,
0.219,
0.0754,
0.018,
0.00329,
0.000484,
0.0000597,
0.00000634,
\dots]$
:::
