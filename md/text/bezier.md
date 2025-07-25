---
title: Bézier curves
summary: A brief introduction to how to evaluate them using de Casteljau's algorithm.
...

This page is intended to be a brief reference on implementing Bézier curves.
It is not intended to be a full discussion of the topic, only a reference.

# Definition

A Bézier curve is a sequence of control points on a parameter interval.

The control points may be scalars or vectors, and there may be an number of them;
we will denote the control points as $p_0, p_1, \dots, p_n$.
The $n$ here is the "order" of the Bézier curve and is one less than the number of control points.

We will refer to the parameter interval as going from $t_0$ to $t_n$.
We assume $t_0 < t_n$.

# de Casteljau's Algorithm

To find the point on a Bézier curve at some parameter value $t'$, we proceed as follows.

Let $t$ be the relative parameter value defined by $t = \frac{t'-t_0}{t_n-t_0}$.

If $n=0$, return $p_0$.
Otherwise, define a set of control points
where the new $n$ is the old $n-1$
and the new $p_i$ is the old $(1-t) p_i + (t) p_{i+1}$;
repeat until the new $n$ is zero.
The operation $(1-t) p_i + (t) p_{i+1}$ is called a "lerp" (short for **l**inear int**erp**olation).

<details class="example"><summary>JavaScript code for basic de Casteljau</summary>
```js
const lerp = (t,p0,p1) => add(mul(p0,1-t), mul(p1,t))
const lbez = (t, ...p) => {
  while(p.length > 1) p = p.slice(1).map((e,i) => lerp(t,p[i],e))
  return p[0]
}
```
</details>

In addition to providing the point on the curve at $t$,
De Casteljau's algorithm also splits the original Bézier curve into two:
the set of all $p_0$ (in the order created) define the portion of the Bézier curve in the interval $[t_0, t]$
and the set of all $p_n$ (in the reverse order created) define the portion of the Bézier curve in the interval $[t, t_n]$

<details class="example"><summary>JavaScript code for de Casteljau curve spliting</summary>
```js
const bezcut = (t, ...p) => {
  let front = [], back = []
  while(p.length > 0) {
    front.push(p[0])
    back.unshift(p[p.length-1])
    p = p.slice(1).map((e,i) => lerp(t,p[i],e))
  }
  return [front, back]
}
```
</details>


# Comments

At $t = t_0$, the value of a Bézier curve is $p_0$.
At $t = t_n$, the value of a Bézier curve is $p_n$.
In general, the Bézier curve does not pass through any of its other control points.

Bézier curves always remain inside the convex hull of their control points.

Within the interval $t_0 \le t \le t_n$, de Casteljau's algorithm is unconditionally numerically stable:
it gives the value of the polynomial with as much numerical precision as the control points and $t$ values are themselves specified.
Outside that interval de Casteljau's algorithm still works in principle, but it is not stable, accumulating numerical error at a rate polynomial in the distance outside the interval.

Bézier curves also can be degree-elevated and degree-reduced;
can efficiently determine their derivative using a hodograph;
can represent conic sections if the control points are homogeneous coordinates;
and can be generated in a smooth spline using B-splines and their variants.
For an extensive treatment, see [Thomas Sederberg's book *Computer Aided Geometric Design*](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1000&context=facpub).
