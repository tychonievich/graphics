---
title: Quasi-random numbers
...

There are various needs for numerical integration in graphics,
generally over a 2D domain,
almost always using a Monte Carlo method.
Monte Carlo methods approximate
$$
\iint_A f(x,y) dx dy \approx \sum_{(x,y) \in B} \frac{f(x,y)}{|B|}
$$
where $B$ is an unbiased set of random points sampled from the area $A$.
Monte Carlo methods converge as $|B|$ gets large, but how quickly they converge depends on how $B$ is chosen.

Pseudorandom numbers work for Monte Carlo, but they are not very good in practice.
Instead, in graphics we almost always use quasi-random numbers which are pulled from a low-discrepancy sequence.
Pseudorandom sequences strive to be unpredictable: knowing past numbers gives no advantage in guessing the next number.
Quasirandom sequences strive to be well-distributed: the next number is likely to be far away from past numbers.
There are many quasirandom sequences, but there are two that I recommend.

# Hammersley

Many numerical integrations in graphics code use a Hammersley set^[John M. Hammersley. 1960. "Monte Carlo methods for solving mathematical problems." *Annals of the New York Academy of Sciences* 86(3): 844–874.].

The points in a Hammersley set depend on the size of the set, which must be known in advance.
If the set has $n$ elements, then point $i$ is
$\left(\frac{i}{n}, \operatorname{radinv}(i)\right)$,
where $\operatorname{radinv}(i)$ mirrors the bits in the binary expression of $i$ across the binary point.
The resulting 2D point has both $0 \le x < 1$ and $0 \le y < 1$.

<details class="example"><summary>How $\operatorname{radinv}(i)$ works</summary>
The following table shows the first several $\operatorname{radinv}(i)$ values:

| $i$ | Binary | Inverted | $\operatorname{radinv}(i)$ |
|----:|-------:|:---------|:---------------------------|
| 0   | 0.0    | 0.0      | 0.0   |
| 1   | 1.0    | 0.1      | 0.5   |
| 2   | 10.0   | 0.01     | 0.25  |
| 3   | 11.0   | 0.11     | 0.75  |
| 4   | 100.0  | 0.001    | 0.125 |
| 5   | 101.0  | 0.101    | 0.375 |
| 6   | 110.0  | 0.011    | 0.625 |
| 7   | 111.0  | 0.111    | 0.875 |
| 8   | 1000.0 | 0.0001   | 0.0625 |
| 9   | 1001.0 | 0.1001   | 0.5625 |

</details>

Computing the radical inverse can be done using several bitwise operators to reverse the bits in an integer,
then multiplying by 1 over the maximum integer.
Because that was done so often in graphics,
GPUs started supporting a bit-reverse operation directly in their hardware,
which WGSL exposes as `reverseBits`,
and we can precompute the 1-over-max number to get

```wgsl
fn radicalInverse(bits_in: u32) -> f32 {
    return f32(reverseBits(bits_in)) * 2.3283064365386963e-10;
}
```

Note that on older GPUs, `reverseBits` won't have hardware support
and will be implemented by WebGPU as 22 bitwise operations[^bitinvert] instead.

[^bitinvert]:
    ````wgsl
    bits = (bits << 16u) | (bits >> 16u);
    bits = ((bits & 0x55555555u) << 1u) | ((bits & 0xAAAAAAAAu) >> 1u);
    bits = ((bits & 0x33333333u) << 2u) | ((bits & 0xCCCCCCCCu) >> 2u);
    bits = ((bits & 0x0F0F0F0Fu) << 4u) | ((bits & 0xF0F0F0F0u) >> 4u);
    bits = ((bits & 0x00FF00FFu) << 8u) | ((bits & 0xFF00FF00u) >> 8u);
    ````

There are also 3D and higher versions of Hammersley sets,
but I've not seen them used in graphics.

# Roberts

In 2018, Martin Roberts proposed a new quasi-random distribution on his blog^[Martin Roberts. 2018. "The Unreasonable Effectiveness of Quasirandom Sequences." <https://extremelearning.com.au/unreasonable-effectiveness-of-quasirandom-sequences/>.].
They have slightly lower discrepancy than Hammersley sets,
do not need to know the set size in advance,
and are roughly as simple to compute.

The 2D Roberts sequence, often called R2, 
creates 2D points with both $0 \le x < 1$ and $0 \le y < 1$
by multiplying by a carefully-selected constant and discarding the integral part.
If created sequentially, this can be done with additions instead of multiplications
and results in increased numerical accuracy if more than a million points are needed.

The constants used are $\left(\frac{1}{x}, \frac{1}{x^2}\right)$
where $x$ is the unique real solution to $x^3 = x+1$,
which is 1.324717957244746....

Thus we have
```wgsl
fn R2(i: u32) -> f32 {
    const phi2 = vec2<f32>(0.7548776662466927, 0.5698402909980532);
    return fract(f32(i) * phi2);
}
```
or, if a sequence of points is wanted in a loop,
```wgsl
const phi2 = vec2<f32>(0.7548776662466927, 0.5698402909980532);
var r2 = vec2<f32>(0.0, 0.0);
for(var i = 0u; i < N; i+=1) {
    r2 = fract(r2 + phi2);
    // use r2 here
}
```

