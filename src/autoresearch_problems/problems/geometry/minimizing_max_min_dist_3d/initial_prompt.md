SETTING:
You are an expert computational geometer and optimization specialist focusing on 3D point dispersion problems.
Your task is to evolve a constructor function that generates an optimal arrangement of exactly 14 points in 3D space, maximizing the ratio of minimum distance to maximum distance between all point pairs.

PROBLEM CONTEXT:
- Target: Beat the current state-of-the-art benchmark of min/max ratio = 1/√4.165849767 ≈ 0.4899
- Constraint: Points must be placed in 3D Euclidean space
- Mathematical formulation: For points Pᵢ = (xᵢ, yᵢ, zᵢ), i = 1,...,14:
  * Minimum distance: dmin = min{dᵢⱼ : i≠j}
  * Maximum distance: dmax = max{dᵢⱼ : i≠j}
  * Objective: maximize (dmin/dmax)²

PERFORMANCE METRICS:
1. **ratio_squared**: (dmin/dmax)² (PRIMARY OBJECTIVE - maximize)
2. **score**: ratio_squared / (1/4.165849767) (progress toward beating benchmark; > 1 means new record)

Your `solve()` function must return a numpy array of shape (14, 3).
