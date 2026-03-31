# Circle Packing Problem

## Task

Place **26 points** inside the unit square [0, 1]² so that the **minimum pairwise Euclidean distance** between any two points is **maximised**.

This is equivalent to packing 26 equal circles into a unit square with the largest possible radius.

## What to implement

Implement a function `solve() -> np.ndarray` that returns the centre coordinates as a 2-D NumPy array of shape `(26, 2)`.  All coordinates must be in [0, 1].

```python
import numpy as np

def solve() -> np.ndarray:
    # Return a (26, 2) float array with all values in [0, 1].
    # Maximise the minimum pairwise Euclidean distance.
    ...
```

## Scoring

- **Score = minimum pairwise distance** between any two centres.
- A higher score is better.
- Score = 0 if any centre is outside [0, 1]² or the shape is wrong.

## Notes

- The theoretical optimum for 26 circles in a unit square is approximately 0.1778.
- A simple grid arrangement is a reasonable starting point.
- Consider gradient-based optimisation, simulated annealing, or force-directed methods.
