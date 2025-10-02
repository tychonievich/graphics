---
title: Hydraulic Erosion
summary: Two methods for making weathered terrain.
...

Hydraulic erosion is a dominant force in shaping most landscapes on Earth.
The basic process runs as follows:

1. Rain falls from the sky, putting water on the ground
1. Water flows down hill
1. Water can store and transport sediment
    - Faster water can store more than slower water
    - Faster water erodes more, removing material from the ground
1. Water both evaporates and is absorbed by the ground

Within these general guidelines there are many additional factors to consider.
Water has momentum and interacts with other water;
water dynamics change with temperature and amount of carried sediment;
the ground is made of many types of material, some more easily eroded than others;
drying out can change the material properties of the ground;
and so on.

Simple hydraulic erosion works as follows:

1. An initial non-eroded terrain is created, either by a fractal method like [faulting planes](faulting.html) or by an artist-supplied base mesh.

1. A few thousand iterations of water moving across the terrain are simulated.
    There are two broad ways to do this:
    
    a. Water is modeled as a grid of water heights and other properties.
        Basic laws of water flow are used to update this grid.
        A few thousand iterations are needed to get reasonable erosion effects,
        each of which processes the entire grid.
    
    a. Water is modeled as a sequence of individual particles.
        Particles are distributed based on rainfall models and roll down hill.
        Hundreds of thousand of iterations are needed to get reasonable erosion effects,
        each of which processes the path of just one particle.

This page explores a simple version of each of these methods.

# Grid-based approach

A simple grid-based erosion technique was published by [Musgrave, Kolb, and Mace in 1989](https://dl.acm.org/doi/10.1145/74334.74337).
It runs as follows:

- Let each vertex have an altitude $a$, water volume $w$, and suspended sediment $s$.
    
    The top of the water at a vertex is thus at height $w+a$; that's important because the difference in top-of-water heights is what decides which way water flows (and how quickly).

- Move water and sediment between adjacent vertices $i$ and $j$ using
    $$\Delta w = \min\big(w_i, (w_i+a_i)-(w_j+a_j)\big)$$
    
- If $\Delta w \le 0$, increase $a_i$ and decrease $s_i$ by $K_d s_i$, where $K_d$ is a deposition rate constant you pick

- Otherwise,
    - move $\Delta w$ from $w_i$ to $w_j$
    - let $c = K_c \Delta w$, where $K_c$ is a sediment carrying capacity constant you pick
    - If $s_i > c$
        - add $c$ to $s_j$
        - add $K_d(s_i-c)$ to $a_i$
        - set $s_i$ to $(1-K_d)(s_i-c)$
    - otherwise
        - add $s_i+K_s(c-s_i)$ to $s_j$, where $K_s$ is a soil softness constant you pick
        - subtract $K_s(c-s_i)$ from $a_i$
        - set $s_i$ to $0$

In the original paper this algorithm was said to apply to "each neighboring vertex" with this caveat:

> <q>In a full two-dimensional implementation, one must take care to distribute water and sediment to all neighboring lower vertices in amounts proportional to their respective differences in overall elevation.</q>

This not only requires some care to pick the distributions, but also requires care so that the order in which you compute the motion from cell $i$ to $j$ vs the motion from cell $j$ to $k$ does not change the results.

Various realizations of this distribution criteria has been used; one of the simplest is a two-pass system

1. In the first pass, find how water and sediment should move:
    - Pick $\Delta w$ for each pair of cells such that the total $\Delta w$ out of cell $i$ is at most $w_i$ and is distributed between all neighbors with $a_j+w_j < a_i+w_i$ proportionally to how different those are
    - Accumulate the corresponding changes to $w$, $a$, and $s$ but do not apply them yet
2. In the second pass, apply the changes to $w$, $a$, and $s$

Parameters in this method:

- how much $w$ to add initially (rainfall amounts)
- how often to have more $w$ added (rainfall frequency)
- whether to have $w$ reduce a bit each step (evaporation) or not, and if so by how much
- $K_d$, $K_c$, and $K_s$ controlling erosion rates

# Particle-based approach

The first particle-based erosion technique was published by [Chiba, Muraoka, and Jujita in 1999](https://doi.org/10.1002/(SICI)1099-1778(1998100)9:4%3C185::AID-VIS178%3E3.0.CO;2-2).
That paper described a fairly involved algorithm, including a model of the under-cutting effects of turning rivers, though their simulations did not show that complexity's impact.

A simpler version works as follows:

1. Pick a random point and drop a particle there with
    - Zero velocity $\vec v$
    - Some initial water volume $w$ (i.e. a positive starting value you pick)
    - No sediment $s$

1. While the particle retains volume,
    - Accelerate the particle by adding $K_a$ times the non-vertical component of the surface normal to its velocity
        - $K_a$ is an acceleration constant you pick
        - you'll need to dynamically compute the normal based on the ever-changing heights (and normalized it after computation)
    - Slow the particle by multiplying its velocity by $(1-K_f)$
        - $K_f$ is a friction constant you pick
    - Move the particle by adding its velocity to its position
        - if it goes off the map, stop working with this particle
    - Compare the sediment it is carrying ($s$) to the sediment it could carry ($K_c \|\vec v\| w$)
        - $K_c$ is a sediment carrying constant you pick
        - if it has more sediment than it should, move $K_d$ of the difference from $s$ to the altitude of the terrain particle
            - $0 \le K_d \le 1$ is a deposition constant you pick
        - if it has less sediment than it should, move $K_s$ of the difference from the altitude of the terrain to $s$
            - $0 \le K_s \le 1$ is a soil softness constant you pick
    - reduce $w$ by some small fixed evaporation rate you pick
        - if $w \le 0$, stop working with this particle

1. Repeat the above several hundred thousand times

The above has a particle moving in analog steps across a discrete grid. While it is somewhat more accurate to interpolate particle positions onto the nearby terrain vertices, it is generally adequate to simply round to the nearest vertex instead when finding normals and lifting and depositing sediment.

Parameters in this method:

- initial $w$ per particle and evaporation rate (together giving a lifetime of the particle)
- $K_a$ and $K_f$ controlling particle motion
- $K_d$, $K_c$, and $K_s$ controlling erosion rates
