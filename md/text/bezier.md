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
- Is perfeclty numerically stable: any point on the curve can be found with the same numerical precision as the control points.

Bézier curves also roughly follow the polyline through the control points,
more completely at the ends than the middle in order to be smooth.
While this shaping is harder to define formally,
it is arguably the property that is of most interest to artists and animators.

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
<line x1="20" x2="380" y1="180" y2="20" fill="none" stroke="#07f"/>
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
<figcaption>An illustration of a lerp: given points $\mathbf A$ and $\mathbf B$ and user-input $t \in [0,1]$, shows the point $(1-t) A + (t) B$ which is close to $\mathbf A$ when $t$ is close to $0$ and close to $B$ when $t$ is close to $1$.</figcaption>
</figure>

De Casteljau lerps every conseuctive pair of control points using the same $t$,
giving a new list of points one smaller than the list of control points;
then treats those as the control points of a lower-order Bézier curve and repeats
until only a single point remains.
The first and last point of each order Bézier curve
are the control points of the two split curves.

<figure>
<svg id="cbez" viewBox="-50 -10 500 200">
<g fill="none" stroke="#07f">
<path d"M 100,100 380,180 20,170 380,20"/>
</g>
<text text-anchor="end" x="95" y="95">A</text>
<text text-anchor="start" x="385" y="175">B</text>
<text text-anchor="end" x="15" y="165">C</text>
<text text-anchor="start" x="385" y="15">D</text>
<circle id="cbez_marker" cx="200" cy="100" fill="red" r="3"/>
</svg>
<input type="range" id="cbez_t" min="0" max="1" step="0.01" value="0.5" oninput="redraw_cbez(Number(value))">
<div>t = <output for="cbez_t">0.5</output></div>
```{=html}
<script>
function redraw_cbez(t) {
  t = Math.round(t*100)/100;
  const s = Math.round((1-t)*100)/100;
  const x0 = [100,380,20,380];
  const x1 = x0.slice(1).map((e,i)=>x0[i]*s+e*t);
  const x2 = x1.slice(1).map((e,i)=>x1[i]*s+e*t);
  const x3 = x2.slice(1).map((e,i)=>x2[i]*s+e*t);
  const y0 = [100, 180, 170, 20];
  const y1 = y0.slice(1).map((e,i)=>y0[i]*s+e*t);
  const y2 = y1.slice(1).map((e,i)=>y1[i]*s+e*t);
  const y3 = y2.slice(1).map((e,i)=>y2[i]*s+e*t);
  document.getElementById('cbez_marker').setAttribute('cx',x3[0]);
  document.getElementById('cbez_marker').setAttribute('cy',y3[0]);
  document.querySelector('output[for="cbez_t"]').textContent = t;
}
redraw_cbez(Number(document.getElementById('cbez_t').value));
</script>
```
<figcaption>An illustration of a cubic Bézier curve: given control points $\mathbf A, \mathbf B, \mathbf C, $\mathbf D$ and user-input $t \in [0,1]$, shows the point $t$ of the way along the curve which is close to $\mathbf A$ when $t$ is close to $0$ and close to $D$ when $t$ is close to $1$, diverting towards $B$ and $C$ in between.</figcaption>
</figure>


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
