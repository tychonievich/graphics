---
title: Bézier curves
...

This page is intended to be a brief reference on implementing Bézier curves.
It is not intended to be a full discussion of the topic, only a reference.

# Definition

A Bézier curve is a sequence of control points on a parameter interval.

The control points may be scalars or vectors, and there may be an number of them;
we will denote the control points as $p_0, p_1, \dots, p_n$.
The $n$ here is the "order" of the Bézier curve and is one less than the number of control points.

We will refer to the parameter interval as going from $t_0$ to $t_n$
and will use $\Delta t$ to mean $t_n-t_0$.
We assume $t_0 < t_n$.

# de Casteljau's Algorithm

To find the point on a Bézier curve at some parameter value $t$, we proceed as follows.

Let $t_a$ by the relative parameter value defined by $t_a = \frac{t-t_0}{t_n-t_0}$;
let $t_b = 1-t_a$.

If $n=0$, return $p_0$.
Otherwise, define a set of control points
where the new $n$ is the old $n-1$
and the new $p_i$ is the old $t_b p_i + t_a p_{i+1}$;
repeat until the new $n$ is zero.

In addition to providing the point on the curve at $t$,
De Casteljau's algorithm also splits the original Bézier curve into two:
the set of all $p_0$ (in the order created) define the portion of the Bézier curve in the interval $[t_0, t]$
and the set of all $p_n$ (in the reverse order created) define the portion of the Bézier curve in the interval $[t, t_n]$

