You are an expert in functional analysis, harmonic analysis, numerical optimization, and AI-driven mathematical discovery.
Your task is to evolve and optimize a Python script to find a better **upper bound** for the third autocorrelation inequality constant C₃.

PROBLEM CONTEXT:
Target: Find a function f: R → R (which can take positive and negative values) that **minimizes** C₃ in:
max_{-1/2≤t≤1/2} |f ★ f(t)| ≥ C₃ (∫_{-1/4}^{1/4} f(x) dx)²

Current best known bounds:
* Vinuesa 2009 literature: C₃ ≤ 1.45810
* AlphaEvolve: C₃ ≤ 1.4556427953745406 (an improvement over the literature bound)
Goal: Beat the AlphaEvolve upper bound of 1.4556427953745406.

Constraint: The function's integral must be non-zero to avoid division by zero.

PERFORMANCE METRICS:
- c3: The C₃ constant achieved by the discovered function.
- score: 1.4556427953745406 / c3 (PRIMARY OBJECTIVE - maximize; > 1 means a new record).

Your `solve()` function must return a list or numpy array of floats.
