---
title: The CFL Conditions
summary: Why large time-steps can make simulations blow up.
...

# Introductory example

Consider simulating a ball on a rippled surface, resting on a rightward-facing slope.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -15 150 30">
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="35" cy="-5" r="7" fill="red"/>
</svg>

The force of gravity is balanced by the force of the ground to give a rightward down-hill acceleration

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -20 150 35">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="35" cy="-5" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 35,-5 l 0,14"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 35,-5 l 10,-10"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="1" d="M 35,-5 l 5,5"/>
</svg>

From here we consider two possible time steps

## Good time step

Applying that acceleration and the resulting velocity with a Euler time step
large enough to move the ball to the bottom of the ripple it is sitting in
also puts the ball inside the ground because the straight velocity does not follow the curved shape of the valley.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 150 25">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="45" cy="5" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 35,-5 l 10,10" stroke-dasharray="1"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 45,5 l 5,5" opacity="0.25"/>
</svg>

Correcting that penetration we now have a ball moving to the right in the bottom of the valley.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 150 20">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="45" cy="0.5" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 35,-5 l 10,10 0,-4.5" stroke-dasharray="1"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 45,0.5 l 5,2.75" opacity="0.25"/>
</svg>

At the bottom of the valley the ground is level, so gravity and the pressure from the ground fully cancel each other out.
Because of this, in the next time step only momentum moves the ball:
horizontally to the middle of the slope rising out of the valley,
and again into the ground because momentum is not yet pointing up the side of the valley.
We correct that incorrect vertical offset.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -15 150 25">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="55" cy="-5" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 45,0.5 l 10,5.5 0,-10.5" stroke-dasharray="1"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 55,-5 l 5,-2.75" opacity="0.25"/>
</svg>

The ball is now on the other side of the valley, with momentum rolling it up the hill.
Gravity pulling it down will be countered by the ground pushing it up and to the left, cancelling out the momentum.
Later, gravity will pull it back down the valley, oscillating back and forth across the valley until friction stops it.

## Bad time step

Applying that acceleration and the resulting velocity with a Euler time step
large enough to move the ball all the way to the left slope of the next valley over
also puts the ball inside the ground because the straight velocity does not follow the curved shape of the valley.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -10 150 75">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="95" cy="55" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 35,-5 l 60,60" stroke-dasharray="1"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 95,55 l 5,5" opacity="0.25"/>
</svg>

Correcting that penetration we now have a ball moving to the right and, because of the large time step, having jumped over to the next hill and sitting on another slope of the same direction as the first.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -15 150 75">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="95" cy="-5" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 35,-5 l 60,60 0,-60" stroke-dasharray="1"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 95,-5 l 5,0" opacity="0.25"/>
</svg>

Because the ball is on another rightward-facing slope, gravity will pull it further to the right, causing it to jump even more hills next time step.

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 -15 270 75">
<defs>
 <marker id="arrow" viewBox="-5 -5 10 10" refX="0" refY="0" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M 0,0 -5,-5 5,0 -5,5 Z"/></marker>
</defs>
<path fill="none" stroke="#000" stroke-width="0.5" d="m 0,0 c 10,-10 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0 s 20,10 30,0 s 20,-10 30,0"/>
<circle cx="215" cy="-5" r="7" fill="red"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 95,-5 l 120,60 0,-60" stroke-dasharray="1"/>
<path marker-end="url(#arrow)" fill="none" stroke="#000" stroke-width="0.5" d="M 215,-5 l 10,0" opacity="0.25"/>
</svg>

This will continue with the ball jumping ever further each new time step.

# CFL conditions

In most time-step simulations, there is a time step that is too large can cause instability.
Courant, Friedrichs and Lewy introduced some criteria describing time steps that do not have that instability;
it is not common to call whatever time step ensures stability "the CFL condition"
even if the particular simulation does not fit their original discussion.

Common CFL conditions look something like
"the time step has to be small enough that no particle can move further than *X* in a single time step."
The specific *X*s vary, but may include simulation-specific features like "half of a particle diameter" and physically-defined features like "the speed of sound".
Because CFL conditions are often defined based on the distance particles would move in a single time step, the time steps they allow are generally different each frame;
they generally allow large time steps when things are mostly still
but require small time steps when things are moving quickly.

Details of how to compute CFL conditions for a specific simulation are beyond the scope of this page.
A reasonable first step is

1. Each frame, find the speed of the fastest-moving thing
2. Divide the time from that frame to the next into a set of time steps
    such that the fastest-moving thing only moves at most $x$ per step,
    where $x$ is a parameter you tuned via guess-and-check in advance.
    
    One particle radius is a good initial guess for $x$ because it will prevent particles from passing completely through one another in a single step.
    Depending on the simulation, a larger or smaller $x$ might be needed.

This simple constant-based approach will not always work.
If you are implementing a method others have published,
look for what CFL condition they used.
CFL conditions are often mentioned only in passing as part of presenting timing results.
