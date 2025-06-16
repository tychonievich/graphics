---
title: Two Paths to Pretty
summary: Heuristics put computability first, simulations put emulating science first.
...


In many areas of computer graphics we find approaches that arose from two different philosophies or paths: heuristics and simulations.

# Heuristics

In computer science^[But not in other fields. The word "heuristic" derives from the Greek adjective *heuretikos* "inventive" and Greek noun *heurema* "an invention or discovery*, neither of which suggest its meaning in computing], a **heuristic** is a a method that seems to work but is not backed by theory or proof.

Many computer graphics algorithms are essentially heuristic in nature:
we notice some visual phenomenon, observe it is somewhat related to something we know how to compute, and then use that computable thing to make pictures.

:::example
Mountains are bumpy viewed from a distance and bumpy viewed up close,
and are created by very complex processes spanning multiple entire disciplines of study.

Fractals are also bumpy at all scales and can be easily learned in a single sitting and programmed by beginning programmers.

Heuristic solution: use fractals to represent mountains.
:::

Heuristics often give the feel of a visual phenomenon at a very reasonable computational cost.
As computers get more powerful, more advanced heuristics often get proposed that given better approximations of the phenomenon.
But the more complicated the heuristic is the less efficient it becomes and the more likely it is that one or another part of its ad-hoc approach gives a visible pattern that isn't what we really wanted.

# Simulation

Simulation involves starting from first principles, the model created by scientists from various disciplines to describe how some part of the world works, and embodying them in a computer program.

Most models we try to simulate in graphics include
either differential equations with no closed-form solution that we'll have to approximate with some kind of numerical solver
or incompletely-modeled but statistically-characterized components that we'll have to approximate with some kind of pseudo-random number generator
or both.
There are often multiple such numerical approximations we could use, each capturing a different aspect of the phenomenon we hope to visualize.
There are always more parts than we have computational resources to fully simulate
and multiple ways to reduce them to a manageable number, each with different visual character.

But all that complexity aside, if we spend the time and energy to get it right a simulation can give us very nice realistic-looking images.

:::example
Physicists have developed detailed models of the photons emitted by a black body like a fire, incandescent light bulb, star, or sun. The input to that model is simple: a single temperature. This is about as clean and simple as a physical model gets.

Except we can't use the model as-is because just storing basic information about each of the visible-spectrum photons emitted by one light-bulb during one frame of an animation would require several petabytes of storage. So to use this model we'll have to simplify it a lot, and can do so in several ways with different resulting computational costs and visual results.
:::

# Hybrid Approaches

Often, graphics applications use a mix of heuristics and simulations to render a single visual phenomenon.
Generally, the simulation is used for the most obvious parts of the result, with heuristics for less important parts or to cover up unfortunate patterns caused by low-fidelity simulations.

:::example
A common process for creating landscapes is

1. Heuristic: create large-scale bumps with a fractal.
2. Simulation: simulate the erosive effects of rainfall, converting mathematical bumps into plausible hills and valleys.
3. Heuristic: because the erosion simulation worked on a low-resolution version of the terrain, fill in high-resolution details using fractals or a library of example landforms so that up-close views seem reasonable too.
:::

Advances in graphics can come from better simulations, better heuristics, or better ways of combining them.
Advances in simulations usually require deep understanding of multiple fields and generally come from research teams at universities and major motion picture companies.
Advances in heuristics generally depends on far fewer prerequisites and may come from anywhere^[Some years ago I was compiling a list of heuristics for distributing plants on a landscape and found almost as many methods first published on blogs as I did first published in the academic literature.].
Advances in hybrid approaches are often made by developers for a specific application and are often treated as design decisions rather than innovations, though they can have as large a visual impact as a better simulation or heuristic can.
