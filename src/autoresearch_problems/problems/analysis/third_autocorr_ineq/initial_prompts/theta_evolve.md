You are an expert mathematician and computational scientist specializing in harmonic analysis and extremal problems, specifically the third autocorrelation inequality.

Your task is to design a Python program that constructs a discrete function `f` on [-1/4, 1/4] to minimize C₃, aiming to beat the SOTA of 1.4556427953745406.

**Key Insight from Mathematical Literature (Host, Vinuesa):**
The best-known constructions are often based on the product of a smooth, oscillating function and a window function with compact support. A highly successful continuous analog is `f(x) = (1 + cos(2*pi*x))` for `x` in `[-1/4, 1/4]` and `0` otherwise.

**Construction Guidelines:**
1. **Window Function:** Define a centered window occupying a fraction of the total domain.
2. **Oscillatory Component:** Inside the window, define f using a smooth, symmetric, oscillating pattern.
3. **Parameterization:** Explore different parameters (support_width, amplitude, frequency).

Your `solve()` function must return a numpy array of floats representing the step-function heights.

PERFORMANCE METRICS:
- score: 1.4556427953745406 / c3 (PRIMARY OBJECTIVE - maximize)
- c3: the C₃ value achieved
