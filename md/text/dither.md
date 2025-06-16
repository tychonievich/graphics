---
title: Dithering
summary: Fooling the eye into thinking we have more colors displayed than we do.
...

We have finite number of bits to store color with,
but want more color detail in the image.
Dithering solves this problem
but ensuring that if we blur the image we'll get more accurate colors.
There are three classes of ways to do this.

- Stochastic dithering uses randomized rounding.
    
    If a pixel's red channel is computed as 121.85, dithering will randomly pick wither 121 (15% chance) or 122 (85% chance) as the number to store.

- Error diffusion detects the error introduced by quantizing one pixel and distributes it to the neighboring pixels.
    
    If 121.85 is approximated as 122, an error of 0.15, we diffuse that error to the neighboring pixels by reducing their target brightness by a cumulative amount equal to the 0.15; for example, we might reduce three neighbors each by 0.05.
    If one of those neighbors was reduced from 85.52 to 85.47 we'd round it as 85 with an error of 0.47 to be diffused to its neighbors as well.

- Blue noise and optimal transport methods use various tricks to efficiently search through the possible pixel colors for a pattern that minimizes patterns in the error terms

Dithering is used to avoid the eye noticing transitions between the finite set of available colors
and is implemented automatically by most GPUs.
For very limited color pallettes dithering can also simulate more colors ar the cost of making the scene look noisy.

