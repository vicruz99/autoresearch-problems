# Two-dimensional Kakeya Needle Problem

Act as a research mathematician, software developer and optimization specialist
specializing in constructing lists of floats with certain extremal properties.

## Goal

Your task is to find an algorithm which, for a given natural number n > 1,
produces a Python list x = (x_i)_{i=1}^n consisting of n positive floats
("positions") which optimize the following task.

Let a_i = i / n for i = 1, ..., n. For each i = 1, ..., n consider the
two-dimensional triangle R_i in the plane given by vertices:

    (x_i, 0),  (x_i + 1/n, 0),  (x_i + a_i, 1)

Find x so that the **union** of the triangles R_i has the **smallest possible
area**.

## Interface

The Python function you must provide is called `solve`:

```python
def solve(n: int = 32) -> np.ndarray:
    """Return positions [x_1, ..., x_n] minimising the union area."""
    ...
```

You have access to a `get_score(x)` function that computes the negative union
area (higher = better). Call it as many times as you like.

## Evaluation

Your function will be called with `n = 32`. It will be terminated after
120 seconds. Return the best array found before the timeout.

Use a time-limited loop:

```python
start_time = time.time()
while time.time() - start_time < 100:
    ...
```

## Hints

- The Keich construction achieves area ≈ 0.155 for n = 32. Beat it!
- Overlapping triangles cancel area — pack them cleverly.
- Small perturbations around a good starting point often help.
- Local search, gradient-free optimisation, or clever analytic patterns all work.
- Good luck!
