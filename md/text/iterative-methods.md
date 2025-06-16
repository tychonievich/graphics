---
title: Three solvers
summary: Numerical approaches to solving constraints, including linear equations.
...


In visual simulations, we often have a structure roughly like the following:

- We have a current state vector $\vec s$
- and a guess at how it will update $\Delta \vec s$
- and a set of constraints that the new state should satisfy $C(\vec s + \Delta \vec s) = 0$
- but the constraints aren't satisfied, so we want to find a different $\Delta \vec s'$, as similar to $\Delta \vec s$ as we can, that does satisfy them.

For some constraints we can define an explicit solution to this problem,
but usually we either can't or don't want to because solving the explicit form is too slow.
Instead, we usually use an iterative approach.

Iterative approaches work as follows:

1. Given an initial guess that violates constraints
2. Tweak the guess to come closer to satisfying the constraints
3. Repeat until the constraints are close enough to being satisfied

The variation in iterative approaches comes in how the compute the tweak to apply in step 2.
There are three common ways to do this:

Gauss-Sidel
:   Find a single change
    that reduces the error of one constraint or caused by one variable,
    and apply it; then do the same for each other constraint or variable.

    For some problems, Gauss-Sidel iterations fails to converge, converges slowly, or converges to a non-optimal solution because the order of solution introduces some kind of bias in the results.
    In such cases, Jacobi iterations are preferred.

Jacobi
:   Find a set of individual changes,
    each reducing the error of one constraint or caused by one variable,
    and apply that set.
    
    For some problems, Jacobi is slower than Gauss-Sidel because it fails to incorporate advances in one variable when computing the next.
    It can also result in over-correction if several constraints make overlapping updates simultaneously.
    In such cases, Gauss-Sidel iterations are preferred.

Gradient
:   Find a change involving all variables
    that improves the cumulative error in the full set of constraints.
    
    For some problems, gradient methods are difficult to implement because the complexity or heterogeneity of constraints makes finding a gradient direction challenging or computationally prohibitive.
    In such cases, Jacobi or Gauss-Sidel methods are preferred.

    Newton's method is a particular type of gradient method sometimes called out explicitly because of its well-understood convergence properties.
    
    Conjugate-gradient is a particular type of gradient method that only works if the constraints have a specific set of properties, but when it works is generally one of the most rapidly-converging iterative methods.

These are not the only approaches used in simulations in computer graphics, but they are the most common.
