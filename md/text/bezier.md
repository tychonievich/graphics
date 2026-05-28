---
title: Bézier curves
summary: A brief introduction to how to evaluate them using de Casteljau's algorithm.
...

This page is intended to be a brief reference on implementing Bézier curves.
It is not intended to be a full discussion of the topic, only a reference.

# Special polynomials

Bézier curves are a specific way of representing a polynomial of one input variable,
typically denoted with the parameter $t$.
The polynomial is represented using a sequence of $n+1$ <dfn>control points</dfn>,
where $n$ is the order of the polynomial.
In graphics, cubic Bézier curves (meaning 4 control points) is by far the most common.
The control points need not be points, <i lang="la">per se</i>:
they are the same datatype as the output of the polynomial function, whatever that might be.
The two most common uses are:

- 2D or 3D points as control points; $t$ has not intrinsic meaning, it's just a tool used to represent a 2D or 3D curve.
- $t$ representing time; control points are anything we want to animate (orientation, position, illumination, etc).

We will refer to the control points as $p_0, p_1, ..., p_n$.

Bézier curves can be defined with any range of permitted $t$ values.
We will refer to that range as going from $t_0$ to $t_n$, with $t_0 < t_n$.

# Properties of Bézier curves

The curve with control points $p_0, p_1, ..., p_n$

- Begins at $p_0$ and ends at $p_n$;
    that is, $C(t_0) = p_0$ and $C(t_n) = p_n$.
- Remains within the convex hull of the control points.
- Applying any affine transformation to the control points applies the same affine transformation to the curve.

They also roughly follow the polyline through the control points,
more completely at the ends than the middle in order to be smooth.
While this is harder to define formally,
it is arguably the one that is of most interest to artists and animators.

# De Casteljau's Algorithm

To find the point on a Bézier curve at some parameter value $t'$, we use de Casteljau's algorithm.
This algorithm actually splits the curve into two parts,
one covering $[t_0, t']$ and the other covering $[t', t_n]$.
Because the curves start and end at a control point,
this finds the point at $t'$ as the last control point of the first curve
and the first control point of the second curve.

The core operation in de Casteljau's algorithm
is the linear interpolation or <dfn>lerp</dfn>.
Given some $t \in [0,1]$,
the lerp from $A$ to $B$ is the point $t$ of the way along the line segment from $A$ to $B$: $(1-t) A + (t) B$.

<figure>
<svg id="lerp" viewBox="-50 -10 500 200">
<line x1="20" x2="380" y1="180" y2="20" fill="none" stroke="black"/>
<text text-anchor="end" x="15" y="185">A</text>
<text text-anchor="start" x="385" y="25">B</text>
<circle id="lerp_marker" cx="200" cy="100" fill="red" r="3"/>
<text id="lerp_label" text-anchor="middle" x="200" y="95">0.5 A + 0.5 B</text>
</svg>
<input type="range" id="lerp_t" min="0" max="1" step="0.01" value="0.5" oninput="redraw_lerp(Number(value))">
<div>t = <output for="lerp_t">0.5</output></div>
```{=html}
<script>
function redraw_lerp(t) {
  t = Math.round(t*100)/100;
  const s = Math.round((1-t)*100)/100;
  const x = 20*s + 380*t;
  const y = 180*s + 20*t;
  document.getElementById('lerp_marker').setAttribute('cx',x);
  document.getElementById('lerp_marker').setAttribute('cy',y);
  document.getElementById('lerp_label').setAttribute('x',x);
  document.getElementById('lerp_label').setAttribute('y',y-5);
  document.getElementById('lerp_label').textContent = `${s} A + ${t} B`;
  document.querySelector('output[for="lerp_t"]').textContent = t;
}
redraw_lerp(Number(document.getElementById('lerp_t').value));
</script>
```
<figcaption>An illustration of a lerp: </figcaption>
</figure>

De Casteljau lerps every conseuctive pair of control points using the same $t$,
giving a new list of points one smaller than the list of control points;
then treats those as the control points of a lower-order Bézier curve and repeats
until only a single point remains.
The first and last point of each order Bézier curve
are the control points of the two split curves.

:::algorithm
de Casteljau's algorithm

- Let $t$ be the relative parameter value defined by $t = \frac{t'-t_0}{t_n-t_0}$.
- Let the list of control points for the first partial curve be $[p_0]$
- Let the list of control points for the second partial curve be $[p_n]$
- Repeat while $n > 0$:
    - Replace the control points with new $p_i$ being old $(1-t) p_i + (t) p_{i+1}$ and reduce $n$ by 1
    - append $p_0$ to the list of control points for the first partial curve
    - prepend $p_n$ to the list of control points for the second partial curve
:::


<details class="example"><summary>JavaScript code for de Casteljau's algorithm</summary>
```js
const lerp = (t,p0,p1) => add(mul(p0,1-t), mul(p1,t))
const decasteljau = (t, ...p) => {
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

Within the interval $t_0 \le t \le t_n$, de Casteljau's algorithm is unconditionally numerically stable:
it gives the value of the polynomial with as much numerical precision as the control points and $t$ values are themselves specified.
Outside that interval de Casteljau's algorithm still works in principle, but it is not stable, accumulating numerical error at a rate polynomial in the distance outside the interval.



# Beyond the basics

Bézier curves have been studied and extended in many ways.
They can be degree-elevated and degree-reduced;
can efficiently determine their derivative using a hodograph;
can represent conic sections if the control points are homogeneous coordinates;
and can be generated in a smooth spline using B-splines and their variants;
can be extended into multiple dimensions to create smooth surfaces;
can be created from splines as a smooth sequence of curve segments;
can be re-posed as subdivision schemes;
and so on.
For an extensive treatment, see [Thomas Sederberg's book *Computer Aided Geometric Design*](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=1000&context=facpub).
