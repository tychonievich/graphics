---
title: Conjugate Gradient for Differential Equations
summary: An overview of the approach and pseudocode for the solver.
...

# Differential Equations

Many graphics problems include differential equations.
They have the general form "the rate of change of $x$ is some function of $x$".
For most graphics simulations, the following all hold:

- We describe the differential equation locally.
    For example, the motion of each bit of cloth depends on its state and the states of the nearby bits of cloth.

- But the local bits chain together to form non-local results.

- And the resulting equation has no closed-form solution:
    the solution families you learn about in differential equations class don't work.

- So we solve them by
    1. Making a linear approximation of the equations at the current time.
    
        Because of Newton's Third Law, the resulting matrix is usually symmetric.
        
        Because motion is smooth and the linearization of smooth systems is convex, the resulting matrix is positive-definite; that is, all its eigenvalues are positive.
        
        Because the equations were local, the resulting matrix is sparse;
        that is, most of its entries are zero.
        
    2. Solve the linear system.
    
        The Conjugate Gradient method is particularly good at solving sparse symmetric positive-definite problems.
    
    3. Use the solution to bump up to a slightly greater time

There are two approximations being used here:
first, we treat complicated math as if it were linear,
and, second, we use a bunch of small steps in time instead of a continuous model of time.
These two are related:
as each time step length approaches zero, the linear solution approaches the correct solution.

# Implementing a sparse matrix solver

This section presents the conjugate gradient method.
It is generally the fastest class of solvers for the kinds of differential equations we encounter in graphics.
It's general process runs as follows:

a. Given an initial "solution" of the equation "$A \vec x = \vec b$".
a. Find the gradient (i.e. direction of maximal change) of the error (i.e. absolute magnitude of "$A \vec x - \vec b$").
a. Tweak that gradient so that it is conjugate (with respect to $A$) with every previous gradient we've considered. For symmetric positive-definite matrices, this tweak will make the method converge on the correct answer much more quickly than a simple gradient descent method.
a. Move the guessed solution along that tweaked gradient to minimize error.
a. Repeat.

Given a linear system $A \vec x = \vec b$,
where $A$ is sparse, symmetric, and positive-definite:

1. Store $A$ well. The operation we'll do with $A$ is $A \vec v$ for various $\vec v$,
    so we need a storage that makes multiplication by a vector fast.
    [LIL](https://en.wikipedia.org/wiki/Sparse_matrix#List_of_lists_(LIL)) is the easiest such storage technique to code:
    A matrix is a list of rows
    and each row is a list of (column index, value) pairs for the non-zero entries in that row.

2. Optionally, precondition the system.
    Instead of solving $A \vec x = \vec b$,
    solve $E^{-1}A(E^{-1})^T \vec y = E^{-1}\vec b$ and $\vec y = E^T x$.
    
    Preconditioning is a topic we'll not really discuss in this class.
    A good $E$ can make the algorithm converge in fewer steps, but also adds extra up-front work that becomes more involved for better $E$s; that means picking $E$ is something of a balancing act, one more involved than we can adequately cover in this class.

3. Use the following algorithm which, given an initial estimate $\vec x$, iteratively improves it:

    1. $\vec r = \vec b - A \vec x$ <small style="padding-left: 1em">// the residual vector; stores the error of the current estimate</small>
    
    1. $\vec p = \vec r$ <small style="padding-left: 1em">// the direction we'll move $\vec x$ in to improve it</small>
    
    1. $\rho = \vec r \cdot \vec r$ <small style="padding-left: 1em">// the squared magnitude of $\vec r$</small>
    
    1. repeat until $\rho$ is "sufficiently small":
        
        1. $\vec a_p = A \vec p$
        
        1. $\alpha = \dfrac{\rho}{\vec p \cdot \vec a_p}$ <small style="padding-left: 1em">// how far to move in the $\vec p$ direction</small>
    
        1. $\vec x \mathrel{+}= \alpha \vec p$ <small style="padding-left: 1em">// move</small>
        
        1. $\vec r \mathrel{-}= \alpha \vec a_p$ <small style="padding-left: 1em">// update the error</small>
        
        1. $\rho' = \vec r \cdot \vec r$
        
        1. $\beta = \dfrac{\rho'}{\rho}$ <small style="padding-left: 1em">// used to ensure each direction is conjugate with all previous directions</small>
        
        1. $\rho := \rho'$ <small style="padding-left: 1em">// update the error squared magnitude</small>
        
        1. $\vec p \mathrel{\times}= \beta$ <small style="padding-left: 1em">// update the direction for the next step</small>
        
        1. $\vec p \mathrel{+}= \vec r$ <small style="padding-left: 1em">// update the direction for the next step</small>


