# First Autocorrelation Inequality

## Task

Find a **non-negative step function** f on [-1/4, 1/4] (discretized as a list
of 600 equally-spaced values) that **minimizes** the first autocorrelation
constant:

$$C_1 = \frac{\max_{|t| \le 1/2} (f * f)(t)}{\left(\int_{-1/4}^{1/4} f(x)\,dx\right)^2}$$

where $(f * f)(t) = \int f(t-x)\,f(x)\,dx$ is the autoconvolution of f.

A lower C₁ gives a tighter upper bound on the true constant — **lower score is
better**.

## Background

For any non-negative integrable f the inequality

$$\max_{-1/2 \le t \le 1/2} (f*f)(t) \ge C_1 \left(\int_{-1/4}^{1/4} f(x)\,dx\right)^2$$

holds for some universal constant C₁.  Finding the smallest C₁ for which this
is tight is an open problem in additive combinatorics.

Currently known bounds: **1.28 ≤ C₁ ≤ 1.5098**.
AlphaEvolve achieved C₁ ≈ **1.5053** with 600 intervals.

## What to implement

Implement a function `solve() -> list[float]` that returns a list of **600
non-negative floats** representing the step-function values on
[-1/4, 1/4].

```python
def solve() -> list[float]:
    # Return a list of 600 non-negative floats.
    # Lower C₁ is better.
    ...
```

## Scoring

The evaluator computes:

1. `dx = 0.5 / 600`  (interval width)
2. `integral_f = sum(f) * dx`
3. `autoconv = convolve(f, f) * dx`  (discrete autoconvolution)
4. `C₁ = max(autoconv) / integral_f²`

**Score = C₁** — lower is better.  Invalid sequences (empty, non-numeric,
all-zero, containing NaN/inf) receive score `inf`.

## Notes and hints

- The simplest baseline is a uniform function (all 1.0s), giving C₁ ≈ 2.0.
- Shape matters: peaked or asymmetric functions can significantly reduce C₁.
- LP relaxation approaches: iteratively solve a linear program that asks "which
  perturbation direction lowers C₁?" and blend it with the current function.
- Gradient-based optimization of the discrete step-function values also works.
- Ensure all returned values are non-negative (the evaluator takes `abs` so
  negative values are treated as their absolute value).
- The benchmark to beat is **1.5052939684401607**.
