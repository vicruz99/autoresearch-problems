You are an expert in functional analysis, harmonic analysis, numerical optimization, and AI-driven mathematical discovery.
Your task is to evolve and optimize a Python script to find the optimal function that minimizes the upper bound of the constant C1.

PROBLEM CONTEXT:
Target: Find a non-negative function f: R → R that minimizes the upper bound of the constant C1 in the inequality:
max_{-1/2≤t≤1/2} f★f(t) ≥ C₁ (∫_{-1/4}^{1/4} f(x) dx)²
where f★f(t) = ∫ f(t-x)f(x) dx is the autoconvolution.

Current best known bounds:
* literature: C1 ≤ 1.5098 (pre-AlphaEvolve)
* AlphaEvolve: C1 ≤ 1.5052939684401607 (a tighter upper bound than literature)
Goal: Beat the current best upper bound of 1.5052939684401607.

Constraint: The function f must be non-negative everywhere and have non-zero integral over [-1/4, 1/4].

PERFORMANCE METRICS:
- score: 1.5052939684401607 / c1 (PRIMARY OBJECTIVE - maximize this)
- c1: constant achieved (current best upper bound)
- sequence_length: number of points used in the integral interval

Your `solve()` function must return a list of non-negative floats.
