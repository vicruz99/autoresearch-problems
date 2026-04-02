## Edges vs Triangles

Act as a specialist in extremal graph theory and combinatorial optimisation.

### Problem

For a graph G on n vertices with edge density ρ (= fraction of possible edges
present) and triangle density τ (= fraction of possible triangles present),
the **Kruskal-Katona theorem** gives a lower bound on τ in terms of ρ.

Your task is to find a set of **probability vectors** of length N = 20 whose
corresponding (edge_density, triangle_density) pairs **densely trace the
theoretical boundary** of the achievable region.

### Representation

A probability vector **v** = (v₀, …, v₁₉) with vᵢ ≥ 0, Σvᵢ = 1 represents
a weighted graph where vᵢ is the fraction of vertices of "type i".  Its
densities are:

```
edge_density     = Σ_{i<j} vᵢ vⱼ       = (1 - Σvᵢ²) / 2
triangle_density = Σ_{i<j<k} vᵢ vⱼ vₖ  = (S₁³ - 3·S₁·S₂ + 2·S₃) / 6
```

### Scoring

The evaluator constructs a *capped slope-3* density curve from the provided
solutions and computes:

- **area**: area under the boundary function (lower is better; minimum = 5/6)
- **max_gap**: maximum gap between consecutive edge densities (want 0)

```
score = (5/6) / (area + 10 × max_gap)
```

A score of **1.0** corresponds to area = 5/6 with zero gap (theoretical limit).
**Higher scores are better.**

### Strategy

Good solutions densely cover edge densities in [0, ~0.5].  Key densities to
target:
- ρ = 0 → v = (1, 0, 0, …) (all weight on one type)
- ρ = 1/4 → v = (1/2, 1/2, 0, …) (equal two types)
- ρ = (k-1)/(2k) for k types with equal weight 1/k
- Optimised intermediate vectors close to the Kruskal-Katona curve

### Constraints

- Output shape: (M, 20) with M ≥ 1.
- All values ≥ 0; rows need not sum to 1 (they are normalised automatically).
- All values finite.

```python
import numpy as np

N = 20

def solve() -> np.ndarray:
    # EVOLVE-BLOCK-START
    solutions = []
    for k in range(1, N + 1):
        v = np.zeros(N, dtype=float)
        v[:k] = 1.0 / k
        solutions.append(v)
    # EVOLVE-BLOCK-END
    return np.array(solutions)
```
