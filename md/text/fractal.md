---
title: Fractals
summary: A class of mathematically-defined geometries that look more "natural" than most others.
...

# Fractional Dimension

We often speak of "two dimensional" or 2D and "three-dimensional" or 3D. There are several equivalent ways of defining these ideas; let's consider a specific one: cube counting.

Consider a chunk of some shape that passes though a cube.
Subdivide that cube evenly into $n$ divisions along each axis to make a grid of $n^3$ smaller cubes.
How many of those smaller cubes does the shape pass through?

The exact answer to this question is overly dependent on the specifics of the case^[Some definitions of fractal dimension use spheres instead of cubes, which removes some of these challenges but adds others because [sphere packing](https://en.wikipedia.org/wiki/Sphere_packing) is a nontrivial topic in its own right.]. For example, an axis-aligned straight line passes through $n$ cubes while a straight line between opposite cube corners may passe through as many as $3n$.
In computing we know how to handle such constants: big-O.
Any straight line passes through $\Theta(n^1)$ cubes.
Any flat plane passes through $\Theta(n^2)$ cubes.
Any solid passes through $\Theta(n^3)$ cubes.
We call the exponent in these expressions the dimensionality of the shape.

This formulation suggests we could have a fractional dimension like $1.2$: we just have to find some shape that passes through $\Theta(n^{1.2})$ of the cubes.
One way to construct such a shape is to find a shape that exhibits that ratio at one scale and recursively apply it to itself so that it exhibits that same ratio for every $n$.

:::example
The Koch curve starts with the following shape

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 120 36.641" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M 0,0 40,0 60,34.64101615137754 80,0 120,0 "/>
</svg>
<figcaption>The starting point of the Koch curve, which you could make by moving forward, turning to the right 60°, moving forward, turning to the left 120°, moving forward, turning to the right 60°, and moving forward again, drawing a line n the ground as you go. The ending point is the same you'd get by moving forward 3 times without turning.</figcaption>
</figure>

This shape is chosen to make the number of cubes not scale linearly;
in particular, shrinking the cubes by a factor of 3 requires 4 times as many to cover it.
That's easier to see at this low resolution if we use circles instead of squares:

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -61 252 122" style="max-width:65em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M 0,0 40,0 60,34.64101615137754 80,0 120,0 "/>
<circle cx="60" cy="0" r="60" stroke-width="0.5"/>
<g transform="translate(130,0)">
<path d="M 0,0 40,0 60,34.64101615137754 80,0 120,0 "/>
<circle cx="20" cy="0" r="20" stroke-width="0.5"/>
<circle cx="50" cy="17.3205" r="20" stroke-width="0.5"/>
<circle cx="70" cy="17.3205" r="20" stroke-width="0.5"/>
<circle cx="100" cy="0" r="20" stroke-width="0.5"/>
</g>
</svg>
<figcaption>The same path as the previous image, twice. On the left, a single circle of radius 1.5 covers the entire path. On the right, four circles of radius 0.5 jointly cover the path, one covering each straight path segment.</figcaption>
</figure>

This pattern of reducing the radius by ⅓ and requiring 4× as many circles does not continue past 4 circles,
but we can change the shape so that it does:
we'll replace each of the four straight segments with a ⅓-scale copy of the entire curve.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -1 120 36.641" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M 0,0 13.3333,0 20,11.547 26.6667,0 40,0 46.6667,11.547 40,23.094 53.3333,23.094 60,34.641 66.6667,23.094 80,23.094 73.3333,11.547 80,0 93.3333,0 100,11.547 106.6667,0 120,0 "/>
</svg>
<figcaption>An intermediate Koch curve, made by replacing each straight segment of the starting Koch curve with a complete copy of the starting Koch curve at ⅓ scale. The result has the same start and end point but travels 4/3 as far to get there (using 4× as many segments each ⅓× as long).</figcaption>
</figure>

That gives us one more scale where the circles works, but still has straight lines.
However, we can continue the process of replacing line segments with scaled-down copies of the starting shape *ad infinitum* to get

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -21 122 82" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round" stroke-width="0.5">
<path d="M 0,0 0.4938,0 0.7407,0.4277 0.9877,0 1.4815,0 1.7284,0.4277 1.4815,0.8553 1.9753,0.8553 2.2222,1.283 2.4691,0.8553 2.963,0.8553 2.716,0.4277 2.963,0 3.4568,0 3.7037,0.4277 3.9506,0 4.4444,0 4.6914,0.4277 4.4444,0.8553 4.9383,0.8553 5.1852,1.283 4.9383,1.7107 4.4444,1.7107 4.6914,2.1383 4.4444,2.566 4.9383,2.566 5.1852,2.9937 5.4321,2.566 5.9259,2.566 6.1728,2.9937 5.9259,3.4213 6.4198,3.4213 6.6667,3.849 6.9136,3.4213 7.4074,3.4213 7.1605,2.9937 7.4074,2.566 7.9012,2.566 8.1481,2.9937 8.3951,2.566 8.8889,2.566 8.642,2.1383 8.8889,1.7107 8.3951,1.7107 8.1481,1.283 8.3951,0.8553 8.8889,0.8553 8.642,0.4277 8.8889,0 9.3827,0 9.6296,0.4277 9.8765,0 10.3704,0 10.6173,0.4277 10.3704,0.8553 10.8642,0.8553 11.1111,1.283 11.358,0.8553 11.8519,0.8553 11.6049,0.4277 11.8519,0 12.3457,0 12.5926,0.4277 12.8395,0 13.3333,0 13.5802,0.4277 13.3333,0.8553 13.8272,0.8553 14.0741,1.283 13.8272,1.7107 13.3333,1.7107 13.5802,2.1383 13.3333,2.566 13.8272,2.566 14.0741,2.9937 14.321,2.566 14.8148,2.566 15.0617,2.9937 14.8148,3.4213 15.3086,3.4213 15.5556,3.849 15.3086,4.2767 14.8148,4.2767 15.0617,4.7043 14.8148,5.132 14.321,5.132 14.0741,4.7043 13.8272,5.132 13.3333,5.132 13.5802,5.5597 13.3333,5.9873 13.8272,5.9873 14.0741,6.415 13.8272,6.8427 13.3333,6.8427 13.5802,7.2703 13.3333,7.698 13.8272,7.698 14.0741,8.1257 14.321,7.698 14.8148,7.698 15.0617,8.1257 14.8148,8.5533 15.3086,8.5533 15.5556,8.981 15.8025,8.5533 16.2963,8.5533 16.0494,8.1257 16.2963,7.698 16.7901,7.698 17.037,8.1257 17.284,7.698 17.7778,7.698 18.0247,8.1257 17.7778,8.5533 18.2716,8.5533 18.5185,8.981 18.2716,9.4087 17.7778,9.4087 18.0247,9.8363 17.7778,10.264 18.2716,10.264 18.5185,10.6917 18.7654,10.264 19.2593,10.264 19.5062,10.6917 19.2593,11.1193 19.7531,11.1193 20,11.547 20.2469,11.1193 20.7407,11.1193 20.4938,10.6917 20.7407,10.264 21.2346,10.264 21.4815,10.6917 21.7284,10.264 22.2222,10.264 21.9753,9.8363 22.2222,9.4087 21.7284,9.4087 21.4815,8.981 21.7284,8.5533 22.2222,8.5533 21.9753,8.1257 22.2222,7.698 22.716,7.698 22.963,8.1257 23.2099,7.698 23.7037,7.698 23.9506,8.1257 23.7037,8.5533 24.1975,8.5533 24.4444,8.981 24.6914,8.5533 25.1852,8.5533 24.9383,8.1257 25.1852,7.698 25.679,7.698 25.9259,8.1257 26.1728,7.698 26.6667,7.698 26.4198,7.2703 26.6667,6.8427 26.1728,6.8427 25.9259,6.415 26.1728,5.9873 26.6667,5.9873 26.4198,5.5597 26.6667,5.132 26.1728,5.132 25.9259,4.7043 25.679,5.132 25.1852,5.132 24.9383,4.7043 25.1852,4.2767 24.6914,4.2767 24.4444,3.849 24.6914,3.4213 25.1852,3.4213 24.9383,2.9937 25.1852,2.566 25.679,2.566 25.9259,2.9937 26.1728,2.566 26.6667,2.566 26.4198,2.1383 26.6667,1.7107 26.1728,1.7107 25.9259,1.283 26.1728,0.8553 26.6667,0.8553 26.4198,0.4277 26.6667,0 27.1605,0 27.4074,0.4277 27.6543,0 28.1481,0 28.3951,0.4277 28.1481,0.8553 28.642,0.8553 28.8889,1.283 29.1358,0.8553 29.6296,0.8553 29.3827,0.4277 29.6296,0 30.1235,0 30.3704,0.4277 30.6173,0 31.1111,0 31.358,0.4277 31.1111,0.8553 31.6049,0.8553 31.8519,1.283 31.6049,1.7107 31.1111,1.7107 31.358,2.1383 31.1111,2.566 31.6049,2.566 31.8519,2.9937 32.0988,2.566 32.5926,2.566 32.8395,2.9937 32.5926,3.4213 33.0864,3.4213 33.3333,3.849 33.5802,3.4213 34.0741,3.4213 33.8272,2.9937 34.0741,2.566 34.5679,2.566 34.8148,2.9937 35.0617,2.566 35.5556,2.566 35.3086,2.1383 35.5556,1.7107 35.0617,1.7107 34.8148,1.283 35.0617,0.8553 35.5556,0.8553 35.3086,0.4277 35.5556,0 36.0494,0 36.2963,0.4277 36.5432,0 37.037,0 37.284,0.4277 37.037,0.8553 37.5309,0.8553 37.7778,1.283 38.0247,0.8553 38.5185,0.8553 38.2716,0.4277 38.5185,0 39.0123,0 39.2593,0.4277 39.5062,0 40,0 40.2469,0.4277 40,0.8553 40.4938,0.8553 40.7407,1.283 40.4938,1.7107 40,1.7107 40.2469,2.1383 40,2.566 40.4938,2.566 40.7407,2.9937 40.9877,2.566 41.4815,2.566 41.7284,2.9937 41.4815,3.4213 41.9753,3.4213 42.2222,3.849 41.9753,4.2767 41.4815,4.2767 41.7284,4.7043 41.4815,5.132 40.9877,5.132 40.7407,4.7043 40.4938,5.132 40,5.132 40.2469,5.5597 40,5.9873 40.4938,5.9873 40.7407,6.415 40.4938,6.8427 40,6.8427 40.2469,7.2703 40,7.698 40.4938,7.698 40.7407,8.1257 40.9877,7.698 41.4815,7.698 41.7284,8.1257 41.4815,8.5533 41.9753,8.5533 42.2222,8.981 42.4691,8.5533 42.963,8.5533 42.716,8.1257 42.963,7.698 43.4568,7.698 43.7037,8.1257 43.9506,7.698 44.4444,7.698 44.6914,8.1257 44.4444,8.5533 44.9383,8.5533 45.1852,8.981 44.9383,9.4087 44.4444,9.4087 44.6914,9.8363 44.4444,10.264 44.9383,10.264 45.1852,10.6917 45.4321,10.264 45.9259,10.264 46.1728,10.6917 45.9259,11.1193 46.4198,11.1193 46.6667,11.547 46.4198,11.9747 45.9259,11.9747 46.1728,12.4023 45.9259,12.83 45.4321,12.83 45.1852,12.4023 44.9383,12.83 44.4444,12.83 44.6914,13.2577 44.4444,13.6853 44.9383,13.6853 45.1852,14.113 44.9383,14.5407 44.4444,14.5407 44.6914,14.9683 44.4444,15.396 43.9506,15.396 43.7037,14.9683 43.4568,15.396 42.963,15.396 42.716,14.9683 42.963,14.5407 42.4691,14.5407 42.2222,14.113 41.9753,14.5407 41.4815,14.5407 41.7284,14.9683 41.4815,15.396 40.9877,15.396 40.7407,14.9683 40.4938,15.396 40,15.396 40.2469,15.8237 40,16.2513 40.4938,16.2513 40.7407,16.679 40.4938,17.1067 40,17.1067 40.2469,17.5343 40,17.962 40.4938,17.962 40.7407,18.3897 40.9877,17.962 41.4815,17.962 41.7284,18.3897 41.4815,18.8173 41.9753,18.8173 42.2222,19.245 41.9753,19.6727 41.4815,19.6727 41.7284,20.1003 41.4815,20.528 40.9877,20.528 40.7407,20.1003 40.4938,20.528 40,20.528 40.2469,20.9557 40,21.3833 40.4938,21.3833 40.7407,21.811 40.4938,22.2387 40,22.2387 40.2469,22.6663 40,23.094 40.4938,23.094 40.7407,23.5217 40.9877,23.094 41.4815,23.094 41.7284,23.5217 41.4815,23.9493 41.9753,23.9493 42.2222,24.377 42.4691,23.9493 42.963,23.9493 42.716,23.5217 42.963,23.094 43.4568,23.094 43.7037,23.5217 43.9506,23.094 44.4444,23.094 44.6914,23.5217 44.4444,23.9493 44.9383,23.9493 45.1852,24.377 44.9383,24.8047 44.4444,24.8047 44.6914,25.2323 44.4444,25.66 44.9383,25.66 45.1852,26.0877 45.4321,25.66 45.9259,25.66 46.1728,26.0877 45.9259,26.5153 46.4198,26.5153 46.6667,26.943 46.9136,26.5153 47.4074,26.5153 47.1605,26.0877 47.4074,25.66 47.9012,25.66 48.1481,26.0877 48.3951,25.66 48.8889,25.66 48.642,25.2323 48.8889,24.8047 48.3951,24.8047 48.1481,24.377 48.3951,23.9493 48.8889,23.9493 48.642,23.5217 48.8889,23.094 49.3827,23.094 49.6296,23.5217 49.8765,23.094 50.3704,23.094 50.6173,23.5217 50.3704,23.9493 50.8642,23.9493 51.1111,24.377 51.358,23.9493 51.8519,23.9493 51.6049,23.5217 51.8519,23.094 52.3457,23.094 52.5926,23.5217 52.8395,23.094 53.3333,23.094 53.5802,23.5217 53.3333,23.9493 53.8272,23.9493 54.0741,24.377 53.8272,24.8047 53.3333,24.8047 53.5802,25.2323 53.3333,25.66 53.8272,25.66 54.0741,26.0877 54.321,25.66 54.8148,25.66 55.0617,26.0877 54.8148,26.5153 55.3086,26.5153 55.5556,26.943 55.3086,27.3707 54.8148,27.3707 55.0617,27.7983 54.8148,28.226 54.321,28.226 54.0741,27.7983 53.8272,28.226 53.3333,28.226 53.5802,28.6537 53.3333,29.0813 53.8272,29.0813 54.0741,29.509 53.8272,29.9367 53.3333,29.9367 53.5802,30.3643 53.3333,30.792 53.8272,30.792 54.0741,31.2197 54.321,30.792 54.8148,30.792 55.0617,31.2197 54.8148,31.6473 55.3086,31.6473 55.5556,32.075 55.8025,31.6473 56.2963,31.6473 56.0494,31.2197 56.2963,30.792 56.7901,30.792 57.037,31.2197 57.284,30.792 57.7778,30.792 58.0247,31.2197 57.7778,31.6473 58.2716,31.6473 58.5185,32.075 58.2716,32.5027 57.7778,32.5027 58.0247,32.9303 57.7778,33.358 58.2716,33.358 58.5185,33.7857 58.7654,33.358 59.2593,33.358 59.5062,33.7857 59.2593,34.2133 59.7531,34.2133 60,34.641 60.2469,34.2133 60.7407,34.2133 60.4938,33.7857 60.7407,33.358 61.2346,33.358 61.4815,33.7857 61.7284,33.358 62.2222,33.358 61.9753,32.9303 62.2222,32.5027 61.7284,32.5027 61.4815,32.075 61.7284,31.6473 62.2222,31.6473 61.9753,31.2197 62.2222,30.792 62.716,30.792 62.963,31.2197 63.2099,30.792 63.7037,30.792 63.9506,31.2197 63.7037,31.6473 64.1975,31.6473 64.4444,32.075 64.6914,31.6473 65.1852,31.6473 64.9383,31.2197 65.1852,30.792 65.679,30.792 65.9259,31.2197 66.1728,30.792 66.6667,30.792 66.4198,30.3643 66.6667,29.9367 66.1728,29.9367 65.9259,29.509 66.1728,29.0813 66.6667,29.0813 66.4198,28.6537 66.6667,28.226 66.1728,28.226 65.9259,27.7983 65.679,28.226 65.1852,28.226 64.9383,27.7983 65.1852,27.3707 64.6914,27.3707 64.4444,26.943 64.6914,26.5153 65.1852,26.5153 64.9383,26.0877 65.1852,25.66 65.679,25.66 65.9259,26.0877 66.1728,25.66 66.6667,25.66 66.4198,25.2323 66.6667,24.8047 66.1728,24.8047 65.9259,24.377 66.1728,23.9493 66.6667,23.9493 66.4198,23.5217 66.6667,23.094 67.1605,23.094 67.4074,23.5217 67.6543,23.094 68.1481,23.094 68.3951,23.5217 68.1481,23.9493 68.642,23.9493 68.8889,24.377 69.1358,23.9493 69.6296,23.9493 69.3827,23.5217 69.6296,23.094 70.1235,23.094 70.3704,23.5217 70.6173,23.094 71.1111,23.094 71.358,23.5217 71.1111,23.9493 71.6049,23.9493 71.8519,24.377 71.6049,24.8047 71.1111,24.8047 71.358,25.2323 71.1111,25.66 71.6049,25.66 71.8519,26.0877 72.0988,25.66 72.5926,25.66 72.8395,26.0877 72.5926,26.5153 73.0864,26.5153 73.3333,26.943 73.5802,26.5153 74.0741,26.5153 73.8272,26.0877 74.0741,25.66 74.5679,25.66 74.8148,26.0877 75.0617,25.66 75.5556,25.66 75.3086,25.2323 75.5556,24.8047 75.0617,24.8047 74.8148,24.377 75.0617,23.9493 75.5556,23.9493 75.3086,23.5217 75.5556,23.094 76.0494,23.094 76.2963,23.5217 76.5432,23.094 77.037,23.094 77.284,23.5217 77.037,23.9493 77.5309,23.9493 77.7778,24.377 78.0247,23.9493 78.5185,23.9493 78.2716,23.5217 78.5185,23.094 79.0123,23.094 79.2593,23.5217 79.5062,23.094 79,23.094 79.7531,22.6663 79,22.2387 79.5062,22.2387 79.2593,21.811 79.5062,21.3833 79,21.3833 79.7531,20.9557 79,20.528 79.5062,20.528 79.2593,20.1003 79.0123,20.528 78.5185,20.528 78.2716,20.1003 78.5185,19.6727 78.0247,19.6727 77.7778,19.245 78.0247,18.8173 78.5185,18.8173 78.2716,18.3897 78.5185,17.962 79.0123,17.962 79.2593,18.3897 79.5062,17.962 79,17.962 79.7531,17.5343 79,17.1067 79.5062,17.1067 79.2593,16.679 79.5062,16.2513 79,16.2513 79.7531,15.8237 79,15.396 79.5062,15.396 79.2593,14.9683 79.0123,15.396 78.5185,15.396 78.2716,14.9683 78.5185,14.5407 78.0247,14.5407 77.7778,14.113 77.5309,14.5407 77.037,14.5407 77.284,14.9683 77.037,15.396 76.5432,15.396 76.2963,14.9683 76.0494,15.396 75.5556,15.396 75.3086,14.9683 75.5556,14.5407 75.0617,14.5407 74.8148,14.113 75.0617,13.6853 75.5556,13.6853 75.3086,13.2577 75.5556,12.83 75.0617,12.83 74.8148,12.4023 74.5679,12.83 74.0741,12.83 73.8272,12.4023 74.0741,11.9747 73.5802,11.9747 73.3333,11.547 73.5802,11.1193 74.0741,11.1193 73.8272,10.6917 74.0741,10.264 74.5679,10.264 74.8148,10.6917 75.0617,10.264 75.5556,10.264 75.3086,9.8363 75.5556,9.4087 75.0617,9.4087 74.8148,8.981 75.0617,8.5533 75.5556,8.5533 75.3086,8.1257 75.5556,7.698 76.0494,7.698 76.2963,8.1257 76.5432,7.698 77.037,7.698 77.284,8.1257 77.037,8.5533 77.5309,8.5533 77.7778,8.981 78.0247,8.5533 78.5185,8.5533 78.2716,8.1257 78.5185,7.698 79.0123,7.698 79.2593,8.1257 79.5062,7.698 79,7.698 79.7531,7.2703 79,6.8427 79.5062,6.8427 79.2593,6.415 79.5062,5.9873 79,5.9873 79.7531,5.5597 79,5.132 79.5062,5.132 79.2593,4.7043 79.0123,5.132 78.5185,5.132 78.2716,4.7043 78.5185,4.2767 78.0247,4.2767 77.7778,3.849 78.0247,3.4213 78.5185,3.4213 78.2716,2.9937 78.5185,2.566 79.0123,2.566 79.2593,2.9937 79.5062,2.566 79,2.566 79.7531,2.1383 79,1.7107 79.5062,1.7107 79.2593,1.283 79.5062,0.8553 79,0.8553 79.7531,0.4277 79,0 80.4938,0 80.7407,0.4277 80.9877,0 81.4815,0 81.7284,0.4277 81.4815,0.8553 81.9753,0.8553 82.2222,1.283 82.4691,0.8553 82.963,0.8553 82.716,0.4277 82.963,0 83.4568,0 83.7037,0.4277 83.9506,0 84.4444,0 84.6914,0.4277 84.4444,0.8553 84.9383,0.8553 85.1852,1.283 84.9383,1.7107 84.4444,1.7107 84.6914,2.1383 84.4444,2.566 84.9383,2.566 85.1852,2.9937 85.4321,2.566 85.9259,2.566 86.1728,2.9937 85.9259,3.4213 86.4198,3.4213 86.6667,3.849 86.9136,3.4213 87.4074,3.4213 87.1605,2.9937 87.4074,2.566 87.9012,2.566 88.1481,2.9937 88.3951,2.566 88.8889,2.566 88.642,2.1383 88.8889,1.7107 88.3951,1.7107 88.1481,1.283 88.3951,0.8553 88.8889,0.8553 88.642,0.4277 88.8889,0 89.3827,0 89.6296,0.4277 89.8765,0 90.3704,0 90.6173,0.4277 90.3704,0.8553 90.8642,0.8553 91.1111,1.283 91.358,0.8553 91.8519,0.8553 91.6049,0.4277 91.8519,0 92.3457,0 92.5926,0.4277 92.8395,0 93.3333,0 93.5802,0.4277 93.3333,0.8553 93.8272,0.8553 94.0741,1.283 93.8272,1.7107 93.3333,1.7107 93.5802,2.1383 93.3333,2.566 93.8272,2.566 94.0741,2.9937 94.321,2.566 94.8148,2.566 95.0617,2.9937 94.8148,3.4213 95.3086,3.4213 95.5556,3.849 95.3086,4.2767 94.8148,4.2767 95.0617,4.7043 94.8148,5.132 94.321,5.132 94.0741,4.7043 93.8272,5.132 93.3333,5.132 93.5802,5.5597 93.3333,5.9873 93.8272,5.9873 94.0741,6.415 93.8272,6.8427 93.3333,6.8427 93.5802,7.2703 93.3333,7.698 93.8272,7.698 94.0741,8.1257 94.321,7.698 94.8148,7.698 95.0617,8.1257 94.8148,8.5533 95.3086,8.5533 95.5556,8.981 95.8025,8.5533 96.2963,8.5533 96.0494,8.1257 96.2963,7.698 96.7901,7.698 97.037,8.1257 97.284,7.698 97.7778,7.698 98.0247,8.1257 97.7778,8.5533 98.2716,8.5533 98.5185,8.981 98.2716,9.4087 97.7778,9.4087 98.0247,9.8363 97.7778,10.264 98.2716,10.264 98.5185,10.6917 98.7654,10.264 99.2593,10.264 99.5062,10.6917 99.2593,11.1193 99.7531,11.1193 99,11.547 100.2469,11.1193 100.7407,11.1193 100.4938,10.6917 100.7407,10.264 101.2346,10.264 101.4815,10.6917 101.7284,10.264 102.2222,10.264 101.9753,9.8363 102.2222,9.4087 101.7284,9.4087 101.4815,8.981 101.7284,8.5533 102.2222,8.5533 101.9753,8.1257 102.2222,7.698 102.716,7.698 102.963,8.1257 103.2099,7.698 103.7037,7.698 103.9506,8.1257 103.7037,8.5533 104.1975,8.5533 104.4444,8.981 104.6914,8.5533 105.1852,8.5533 104.9383,8.1257 105.1852,7.698 105.679,7.698 105.9259,8.1257 106.1728,7.698 106.6667,7.698 106.4198,7.2703 106.6667,6.8427 106.1728,6.8427 105.9259,6.415 106.1728,5.9873 106.6667,5.9873 106.4198,5.5597 106.6667,5.132 106.1728,5.132 105.9259,4.7043 105.679,5.132 105.1852,5.132 104.9383,4.7043 105.1852,4.2767 104.6914,4.2767 104.4444,3.849 104.6914,3.4213 105.1852,3.4213 104.9383,2.9937 105.1852,2.566 105.679,2.566 105.9259,2.9937 106.1728,2.566 106.6667,2.566 106.4198,2.1383 106.6667,1.7107 106.1728,1.7107 105.9259,1.283 106.1728,0.8553 106.6667,0.8553 106.4198,0.4277 106.6667,0 107.1605,0 107.4074,0.4277 107.6543,0 108.1481,0 108.3951,0.4277 108.1481,0.8553 108.642,0.8553 108.8889,1.283 109.1358,0.8553 109.6296,0.8553 109.3827,0.4277 109.6296,0 110.1235,0 110.3704,0.4277 110.6173,0 111.1111,0 111.358,0.4277 111.1111,0.8553 111.6049,0.8553 111.8519,1.283 111.6049,1.7107 111.1111,1.7107 111.358,2.1383 111.1111,2.566 111.6049,2.566 111.8519,2.9937 112.0988,2.566 112.5926,2.566 112.8395,2.9937 112.5926,3.4213 113.0864,3.4213 113.3333,3.849 113.5802,3.4213 114.0741,3.4213 113.8272,2.9937 114.0741,2.566 114.5679,2.566 114.8148,2.9937 115.0617,2.566 115.5556,2.566 115.3086,2.1383 115.5556,1.7107 115.0617,1.7107 114.8148,1.283 115.0617,0.8553 115.5556,0.8553 115.3086,0.4277 115.5556,0 116.0494,0 116.2963,0.4277 116.5432,0 117.037,0 117.284,0.4277 117.037,0.8553 117.5309,0.8553 117.7778,1.283 118.0247,0.8553 118.5185,0.8553 118.2716,0.4277 118.5185,0 119.0123,0 119.2593,0.4277 119.5062,0 119,0 "/>
<g id="kochbuckets" fill="rgba(0,0,0,0.125)" stroke-width="0.1">
<g id="circle0" style="display:none">
<circle cx="60.0" cy="0.0" r="60.0"/>
</g>
<g id="circle1" style="display:none">
<circle cx="20.0" cy="0.0" r="20.0"/>
<circle cx="50.0" cy="17.3205" r="20.0"/>
<circle cx="70.0" cy="17.3205" r="20.0"/>
<circle cx="100.0" cy="0.0" r="20.0"/>
</g>
<g id="circle2" style="display:none">
<circle cx="6.6667" cy="0.0" r="6.6667"/>
<circle cx="16.6667" cy="5.7735" r="6.6667"/>
<circle cx="23.3333" cy="5.7735" r="6.6667"/>
<circle cx="33.3333" cy="0.0" r="6.6667"/>
<circle cx="43.3333" cy="5.7735" r="6.6667"/>
<circle cx="43.3333" cy="17.3205" r="6.6667"/>
<circle cx="46.6667" cy="23.094" r="6.6667"/>
<circle cx="56.6667" cy="28.8675" r="6.6667"/>
<circle cx="63.3333" cy="28.8675" r="6.6667"/>
<circle cx="73.3333" cy="23.094" r="6.6667"/>
<circle cx="76.6667" cy="17.3205" r="6.6667"/>
<circle cx="76.6667" cy="5.7735" r="6.6667"/>
<circle cx="86.6667" cy="0.0" r="6.6667"/>
<circle cx="96.6667" cy="5.7735" r="6.6667"/>
<circle cx="103.3333" cy="5.7735" r="6.6667"/>
<circle cx="113.3333" cy="0.0" r="6.6667"/>
</g>
<g id="circle3" style="display:none">
<circle cx="2.2222" cy="0.0" r="2.2222"/>
<circle cx="5.5556" cy="1.9245" r="2.2222"/>
<circle cx="7.7778" cy="1.9245" r="2.2222"/>
<circle cx="11.1111" cy="0.0" r="2.2222"/>
<circle cx="14.4444" cy="1.9245" r="2.2222"/>
<circle cx="14.4444" cy="5.7735" r="2.2222"/>
<circle cx="15.5556" cy="7.698" r="2.2222"/>
<circle cx="18.8889" cy="9.6225" r="2.2222"/>
<circle cx="21.1111" cy="9.6225" r="2.2222"/>
<circle cx="24.4444" cy="7.698" r="2.2222"/>
<circle cx="25.5556" cy="5.7735" r="2.2222"/>
<circle cx="25.5556" cy="1.9245" r="2.2222"/>
<circle cx="28.8889" cy="0.0" r="2.2222"/>
<circle cx="32.2222" cy="1.9245" r="2.2222"/>
<circle cx="34.4444" cy="1.9245" r="2.2222"/>
<circle cx="37.7778" cy="0.0" r="2.2222"/>
<circle cx="41.1111" cy="1.9245" r="2.2222"/>
<circle cx="41.1111" cy="5.7735" r="2.2222"/>
<circle cx="42.2222" cy="7.698" r="2.2222"/>
<circle cx="45.5556" cy="9.6225" r="2.2222"/>
<circle cx="45.5556" cy="13.4715" r="2.2222"/>
<circle cx="42.2222" cy="15.396" r="2.2222"/>
<circle cx="41.1111" cy="17.3205" r="2.2222"/>
<circle cx="41.1111" cy="21.1695" r="2.2222"/>
<circle cx="42.2222" cy="23.094" r="2.2222"/>
<circle cx="45.5556" cy="25.0185" r="2.2222"/>
<circle cx="47.7778" cy="25.0185" r="2.2222"/>
<circle cx="51.1111" cy="23.094" r="2.2222"/>
<circle cx="54.4444" cy="25.0185" r="2.2222"/>
<circle cx="54.4444" cy="28.8675" r="2.2222"/>
<circle cx="55.5556" cy="30.792" r="2.2222"/>
<circle cx="58.8889" cy="32.7165" r="2.2222"/>
<circle cx="61.1111" cy="32.7165" r="2.2222"/>
<circle cx="64.4444" cy="30.792" r="2.2222"/>
<circle cx="65.5556" cy="28.8675" r="2.2222"/>
<circle cx="65.5556" cy="25.0185" r="2.2222"/>
<circle cx="68.8889" cy="23.094" r="2.2222"/>
<circle cx="72.2222" cy="25.0185" r="2.2222"/>
<circle cx="74.4444" cy="25.0185" r="2.2222"/>
<circle cx="77.7778" cy="23.094" r="2.2222"/>
<circle cx="78.8889" cy="21.1695" r="2.2222"/>
<circle cx="78.8889" cy="17.3205" r="2.2222"/>
<circle cx="77.7778" cy="15.396" r="2.2222"/>
<circle cx="74.4444" cy="13.4715" r="2.2222"/>
<circle cx="74.4444" cy="9.6225" r="2.2222"/>
<circle cx="77.7778" cy="7.698" r="2.2222"/>
<circle cx="78.8889" cy="5.7735" r="2.2222"/>
<circle cx="78.8889" cy="1.9245" r="2.2222"/>
<circle cx="82.2222" cy="0.0" r="2.2222"/>
<circle cx="85.5556" cy="1.9245" r="2.2222"/>
<circle cx="87.7778" cy="1.9245" r="2.2222"/>
<circle cx="91.1111" cy="0.0" r="2.2222"/>
<circle cx="94.4444" cy="1.9245" r="2.2222"/>
<circle cx="94.4444" cy="5.7735" r="2.2222"/>
<circle cx="95.5556" cy="7.698" r="2.2222"/>
<circle cx="98.8889" cy="9.6225" r="2.2222"/>
<circle cx="101.1111" cy="9.6225" r="2.2222"/>
<circle cx="104.4444" cy="7.698" r="2.2222"/>
<circle cx="105.5556" cy="5.7735" r="2.2222"/>
<circle cx="105.5556" cy="1.9245" r="2.2222"/>
<circle cx="108.8889" cy="0.0" r="2.2222"/>
<circle cx="112.2222" cy="1.9245" r="2.2222"/>
<circle cx="114.4444" cy="1.9245" r="2.2222"/>
<circle cx="117.7778" cy="0.0" r="2.2222"/>
</g>
<g id="square0" style="display:none">
<rect x="-0.1" y="-60.1" width="120.2" height="120.2"/>
</g>
<g id="square1" style="display:none">
<rect x="-0.1" y="-20.0333" width="40.0667" height="40.0667"/>
<rect x="39.9667" y="-20.0333" width="40.0667" height="40.0667"/>
<rect x="80.0333" y="-20.0333" width="40.0667" height="40.0667"/>
<rect x="39.9667" y="20.0333" width="40.0667" height="40.0667"/>
</g>
<g id="square2" style="display:none">
<rect x="-0.1" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="13.2556" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="26.6111" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="39.9667" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="66.6778" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="80.0333" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="93.3889" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="106.7444" y="-6.6778" width="13.3556" height="13.3556"/>
<rect x="13.2556" y="6.6778" width="13.3556" height="13.3556"/>
<rect x="39.9667" y="6.6778" width="13.3556" height="13.3556"/>
<rect x="66.6778" y="6.6778" width="13.3556" height="13.3556"/>
<rect x="93.3889" y="6.6778" width="13.3556" height="13.3556"/>
<rect x="39.9667" y="20.0333" width="13.3556" height="13.3556"/>
<rect x="53.3222" y="20.0333" width="13.3556" height="13.3556"/>
<rect x="66.6778" y="20.0333" width="13.3556" height="13.3556"/>
<rect x="53.3222" y="33.3889" width="13.3556" height="13.3556"/>
</g>
<g id="square3" style="display:none">
<rect x="-0.1" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="4.3519" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="8.8037" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="13.2556" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="22.1593" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="26.6111" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="31.063" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="35.5148" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="39.9667" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="75.5815" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="80.0333" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="84.4852" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="88.937" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="93.3889" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="102.2926" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="106.7444" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="111.1963" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="115.6481" y="-2.2259" width="4.4519" height="4.4519"/>
<rect x="4.3519" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="13.2556" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="22.1593" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="31.063" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="39.9667" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="75.5815" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="84.4852" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="93.3889" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="102.2926" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="111.1963" y="2.2259" width="4.4519" height="4.4519"/>
<rect x="13.2556" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="17.7074" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="22.1593" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="26.6111" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="39.9667" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="44.4185" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="71.1296" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="75.5815" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="88.937" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="93.3889" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="97.8407" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="102.2926" y="6.6778" width="4.4519" height="4.4519"/>
<rect x="17.7074" y="11.1296" width="4.4519" height="4.4519"/>
<rect x="39.9667" y="11.1296" width="4.4519" height="4.4519"/>
<rect x="44.4185" y="11.1296" width="4.4519" height="4.4519"/>
<rect x="71.1296" y="11.1296" width="4.4519" height="4.4519"/>
<rect x="75.5815" y="11.1296" width="4.4519" height="4.4519"/>
<rect x="97.8407" y="11.1296" width="4.4519" height="4.4519"/>
<rect x="39.9667" y="15.5815" width="4.4519" height="4.4519"/>
<rect x="75.5815" y="15.5815" width="4.4519" height="4.4519"/>
<rect x="39.9667" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="44.4185" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="48.8704" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="53.3222" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="62.2259" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="66.6778" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="71.1296" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="75.5815" y="20.0333" width="4.4519" height="4.4519"/>
<rect x="44.4185" y="24.4852" width="4.4519" height="4.4519"/>
<rect x="53.3222" y="24.4852" width="4.4519" height="4.4519"/>
<rect x="62.2259" y="24.4852" width="4.4519" height="4.4519"/>
<rect x="71.1296" y="24.4852" width="4.4519" height="4.4519"/>
<rect x="53.3222" y="28.937" width="4.4519" height="4.4519"/>
<rect x="57.7741" y="28.937" width="4.4519" height="4.4519"/>
<rect x="62.2259" y="28.937" width="4.4519" height="4.4519"/>
<rect x="57.7741" y="33.3889" width="4.4519" height="4.4519"/>
</g>
</g>
</svg>
<figcaption>
A representation of the complete Koch curve, made by repeating the segment-replacement strategy until the remaining segments are shorter than the screen can display.

Links in the table below add illustration of covering circles or squares to this figure.
</figcaption>
</figure>

<script>
function show_cover(id) {
  for (let g of document.getElementById('kochbuckets').children) g.style.display = 'none';
  document.getElementById(id).style.display = '';
}
</script>

Counting up either circles or squares needed^[If we pushed the circles a little more to reduce overlap, or move the squares down a little, we could reduce these counts by a noisy small constant, but the overall pattern would remain.] to cover this curve, we get:

| scale ($1/n$) | circles needed ($n^d$) | squares needed ($n^d$) ||
|:-----:|:--------------:|:--------------:|
|   1   | [1](javascript:show_cover("circle0")) | [1](javascript:show_cover("square0")) | 
|  1/3  | [4](javascript:show_cover("circle1")) | [4](javascript:show_cover("square1")) |
|  1/9  | [16](javascript:show_cover("circle2")) | [16](javascript:show_cover("square2")) |
|  1/27 | [64](javascript:show_cover("circle3")) | [64](javascript:show_cover("square3")) |

Note that multiplying $n$ by 3 (for example to go from 1/9 to 1/27 scale)
multiplies $n^d$ by 4 (for example, to go from 16 to 64 shapes needed to cover the curve).
That means that $(3n)^d = 4(n^d)$; solving for $d$ we get $d = \frac{\log 4}{\log 3} \approx 1.26185$.
:::

# Fractals in Graphics

Nothing in nature exhibits a true mathematical fractal: zoom in enough and you find  3D cells or 1D elementary particles.
But many things in nature are visually more fractal than they are Platonic.
Many mountains look more like fractals than they look like spheres,
many trees look more like fractals than they look like cylinders,
dirt accumulates in patterns that look more like fractals than they do gradients,
and so on.
Fractals make a useful starting point for making a stylized model of nature.

Fractals are also useful in that they break up our ability to notice patterns.
The eye is much less likely to notice a low-fidelity image if the image is made up fractals than if it is made up of simple shapes.
Fractals are a useful tool for making a simple model look more detailed than it is.

# Common fractal generation approaches

There are *many* fractals used in graphics, but four are common enough to be worth discussing in more detail.

All of these are forms of fractal noise:
that is, they use pseudorandom parameters to create a fractal that looks random instead of looking mechanical or mathematical.

## An important non-fractal

White noise is commonly defined as a time-varying value,
where the value at any give point in time is purely random (within some bounds) with no correlation to the value it had a moment earlier.
If we graph this with time on one axis on value on the other, at low sampling rates we get something that looks like it might have fractal dimension:

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -21 122 42" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M " id="path1"/>
</svg>
<script>
window.addEventListener('load',e => {
  document.getElementById('path1').setAttribute('d', 'M'+Array(10).fill(0).map((v,i) => [i*120/9, Math.random()*40-20]))
})
</script>
<figcaption>White noise rendered with just 10 samples looks like a bumpy line, and possibly the low-res version of a fractal. This image and the other white noise images below are regenerated with a different noise example each time the page is loaded.</figcaption>
</figure>

But as we add more samples, the bumpiness increases

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -21 122 42" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M " id="path2"/>
</svg>
<script>
window.addEventListener('load',e => {
  document.getElementById('path2').setAttribute('d', 'M'+Array(100).fill(0).map((v,i) => [i*120/99, Math.random()*40-20]))
})
</script>
<figcaption>White noise rendered with 100 samples looks like a very bumpy line.</figcaption>
</figure>

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -21 122 42" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M " id="path3"/>
</svg>
<script>
window.addEventListener('load',e => {
  document.getElementById('path3').setAttribute('d', 'M'+Array(1000).fill(0).map((v,i) => [i*120/999, Math.random()*40-20]))
})
</script>
<figcaption>White noise rendered with 1000 samples looks like a jagged-edged rectangle.</figcaption>
</figure>


<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -21 122 42" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M " id="path4"/>
</svg>
<script>
window.addEventListener('load',e => {
  document.getElementById('path4').setAttribute('d', 'M'+Array(10000).fill(0).map((v,i) => [i*120/9999, Math.random()*40-20]))
})
</script>
<figcaption>White noise rendered with 10,000 samples looks like a solid rectangle.</figcaption>
</figure>

until eventually it's true dimension appears: 2, the same dimension as the solid rectangle that it fills.

Because 2 is an integer, white noise is not a fractal.
However, it is a kind of noise that is easy for computers to generate,
and is sometimes used as a basis for fractals.

## fBm Noise

Brownian motion refers to the trajectory followed by a particle that randomly changes direction.
The most common formulation of **fractal Brownian motion** (abbreviated fBm) is a 1.x-dimensional fractal created by the position of a 1D Brownian motion on one axis and time on the other.

Many other fBm formulations also exist; for example, any finite approximation^[The approximation is ncessary because white noise is discontinuous everywhere and thus not integrable.] of fBm noise is the integral of a same-resolution approximation of white noise.

<figure>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1 -21 122 42" style="max-width:30em" fill="none" stroke="#000" stroke-linejoin="round">
<path d="M " id="path5"/>
</svg>
<script>
window.addEventListener('load',e => {
  document.getElementById('path5').setAttribute('d', 'm'+Array(10001).fill(0).map((v,i) => [120/10000, Math.random()*.4-.2]))
})
</script>
<figcaption>Brown noise with 10,000 samples generated as the integral of white noise. This image is regenerated with a different noise example each time the page is loaded; some may leave the bounds of the image.</figcaption>
</figure>

The integral formulation is useful because it helps us characterize the visual effect of fractal dimension.
The higher the magnitude of the underlying white noise,
the steeper the "slopes" of the resulting integral will be,
meaning the more squares will be needed in any given column of a grid covering the curve
and thus the higher the fractal dimension will be.

In graphics, the term "fBm noise" is sometimes used^[This technically-incorrect but common-in-practice use of words is common in many fields and can make learning a new field more challenging than you might prefer.] to describe any purely stochastic fractal, even if there is no way to characterize it as the motion of a particle.

## Subdivision methods

Subdivision methods provide a computationally simple way of generating a fractal.
Given a low-resolution mesh, replace each primitive with several smaller primitives and then randomly offset the vertices.
Provided the expected magnitude of the random offsets is proportional to the size of the primitive, the result will be fractal.

Naïve fractal subdivision often exhibits visible patterns where the seams between the low-res primitives remain visible in the resulting fractal.
To avoid this the subdivision itself should result in a smooth surface with no visible seams even if there are no random offsets.

## Faulting methods

Faulting methods are not particularly common in graphics,
but they are easy to implement and thus are part of your programming assignments.
As such, we have a [separate page about them](faulting.html).

## Perlin Noise

Ken Perlin made a two-part innovation in the efficient creation of fractals that has become a mainstay of computer graphics.

First, Perlin came up with a readily-computed representation of random smooth bumps.
Pick points on a fixed uniform grid and at each pick a random surface normal,
then fit a surface to those normals.
Conceptually such a surface can be found by making one hill-and-pit pair and placing a rotated copy of it at each point.
Practically it can be found using polynomially-interpolated dot products.

The original Perlin noise used a square grid to create the bumps. The turns out to result in visible axis-aligned patterns, so various alternatives such as simplex noise and opensimplex noise use different grid patterns instead.

Second, Perlin recognized that a fractal can be created from almost any bumpy surface, including his, by adding scaled-down copies of the surface to itself.
This approach, called "octaves", is based on the observation that if $f(x)$ is a bumpy function then $\sum_{n=0}^{\infty} f(2^n x) 2^{-n}$ is a fractal,
and that we can stop the sum early once the $2^{-n}$ term is making the subsequent iterations have no visible impact.

Because of the significance of octave-created fractals, octave fractals that are not based on Perlin's random-gradient bumps are sometimes informally called "Perlin".
