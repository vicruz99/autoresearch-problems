# Problems Summary

Complete catalogue of all benchmark problems in `autoresearch-problems`.

A score of `↑` means higher is better (maximize); `↓` means lower is better (minimize).

## Analysis (9 problems)

| Problem ID | Description | Opt | Known Best Score | Source |
|---|---|---|---|---|
| `analysis/erdos_min_overlap` | Minimize Erdős minimum overlap constant C₅ via step function h:[0,2]→[0,1] | ↓ | ≤ 0.3809 | AlphaEvolve |
| `analysis/first_autocorrelation_inequality` | Minimize first autocorrelation constant C₁ via non-negative step function | ↓ | ≤ 1.5053 | AlphaEvolve |
| `analysis/flat_polynomials` | Minimize L∞ norm of ±1-coefficient polynomial on unit circle, scaled by √(n+1), n=64 | ↓ | ≈ 1.384 | AlphaEvolve |
| `analysis/gagliardo_nirenberg_inequality` | Maximize Gagliardo-Nirenberg quotient Q(f), p=4; optimal f=sech(x) gives Q=1/9 | ↑ | ≈ 0.1111 | AlphaEvolve |
| `analysis/hausdorff_young_inequality` | Maximize Hausdorff-Young quotient Q(f), p=1.5; optimal f=Gaussian gives Babenko-Beckner constant | ↑ | ≈ 0.9532 | AlphaEvolve |
| `analysis/second_autocorr_ineq` | Maximize second autocorrelation lower bound C₂ = ‖f*f‖₂² / (‖f*f‖₁ · ‖f*f‖∞) | ↑ | ≥ 0.8963 | AlphaEvolve |
| `analysis/sphere_packing_uncertainty` | Maximize largest sign change of Laguerre combination; m=10 roots, n_dim=25 | ↑ | open | AlphaEvolve |
| `analysis/third_autocorr_ineq` | Minimize third autocorrelation constant C₃ via step function on [-¼, ¼] | ↓ | ≤ 1.4556 | AlphaEvolve |
| `analysis/young_convolution_inequality` | Maximize Young convolution quotient Q(f,g), p=4/3, q=7/5; optimal are Gaussians | ↑ | open | AlphaEvolve |

## Combinatorics (9 problems)

| Problem ID | Description | Opt | Known Best Score | Source |
|---|---|---|---|---|
| `combinatorics/cap_set` | Largest cap set (no 3-AP) in F_3^8 | ↑ | open | FunSearch |
| `combinatorics/edges_vs_triangles` | Trace edge/triangle density boundary for graphs; n=20 probability vectors | ↑ | 1.0 | AlphaEvolve |
| `combinatorics/erdos_szekeres_happy_ending` | Minimize convex n-gons (n=6) among 2^(n-2)+1 points in general position | ↑ | open | AlphaEvolve |
| `combinatorics/finite_field_nikodym_problem` | Minimize Nikodym sets in F_q^2 across primes p; maximize complement fraction | ↑ | open | AlphaEvolve |
| `combinatorics/imo_2025_p6` | Minimize rectangular tiles in n=10 grid tiling (each row & column has one uncovered cell) | ↑ | open | AlphaEvolve |
| `combinatorics/no_isosceles_triangles` | Largest subset of 64×64 integer grid with no isosceles triangle; score = points/n | ↑ | open | AlphaEvolve |
| `combinatorics/online_bin_packing` | Minimize bins used for 100 online items via a packing heuristic | ↑ | open | FunSearch |
| `combinatorics/ring_loading_problem` | Maximize alpha (min imbalance) over all sign choices; m=15 pairs | ↑ | open | AlphaEvolve |
| `combinatorics/sums_differences` | Maximize log\|A−A\| / log\|A+A\| (Ruzsa ratio) for integer set A | ↑ | open | AlphaEvolve |

## Geometry (24 problems)

| Problem ID | Description | Opt | Known Best Score | Source |
|---|---|---|---|---|
| `geometry/circle_packing` | Pack n=26 points in unit square; maximize minimum pairwise distance | ↑ | open | ShinkaEvolve |
| `geometry/equidistant_points_in_convex_polygons` | Find convex polygon (10 vertices) where every vertex has ≥4 equidistant neighbours | ↑ | 1.0 | AlphaEvolve |
| `geometry/kakeya_needle_2d` | Minimize area of union of n=32 triangles (2D Kakeya needle problem) | ↑ | open | AlphaEvolve |
| `geometry/kakeya_needle_3d` | Minimize volume of union of cap_n²=16 tubes (3D Kakeya needle problem) | ↑ | open | AlphaEvolve |
| `geometry/kissing_cylinders` | Place n=7 unit cylinders all tangent to a central cylinder; maximize -Σ(dist−2)² | ↑ | 0.0 | AlphaEvolve |
| `geometry/kissing_number_3d` | Kissing number in R³; K(3)=12 is proved | ↑ | 12 | AlphaEvolve |
| `geometry/kissing_number_5d` | Kissing number in R⁵; best lower bound 40, upper bound 44 | ↑ | 40 | AlphaEvolve |
| `geometry/kissing_number_6d` | Kissing number in R⁶; best lower bound 72, upper bound 78 | ↑ | 72 | AlphaEvolve |
| `geometry/kissing_number_7d` | Kissing number in R⁷; best lower bound 126, upper bound 134 | ↑ | 126 | AlphaEvolve |
| `geometry/kissing_number_9d` | Kissing number in R⁹; best lower bound 306, upper bound 364 | ↑ | 306 | AlphaEvolve |
| `geometry/kissing_number_10d` | Kissing number in R¹⁰; best lower bound 500, upper bound 554 | ↑ | 500 | AlphaEvolve |
| `geometry/kissing_number_11d` | Kissing number in R¹¹; AlphaEvolve improved lower bound from 592 to 593 | ↑ | 593 | AlphaEvolve |
| `geometry/minimizing_max_min_dist_2d` | Place n=16 points in 2D; maximize (dmin/dmax)²/BENCHMARK | ↑ | 1.0 | ShinkaEvolve |
| `geometry/minimizing_max_min_dist_3d` | Place n=14 points in 3D; maximize (dmin/dmax)²/BENCHMARK | ↑ | 1.0 | ShinkaEvolve |
| `geometry/moving_sofa_2d` | Maximize sofa area through L-shaped corridor; n_poses=20 | ↑ | open | AlphaEvolve |
| `geometry/moving_sofa_3d` | Maximize solid volume through 3D L-shaped corridor; n_poses=20 | ↑ | open | AlphaEvolve |
| `geometry/no_5_on_sphere` | Place as many points as possible on unit sphere with no 5 coplanar with origin; n≤50 | ↑ | open | AlphaEvolve |
| `geometry/ovals_problem` | Minimize Rayleigh quotient R over convex curves; n=100 points | ↑ | open | AlphaEvolve |
| `geometry/packing_circles_max_sum_radii` | Pack n=26 circles of varying radii in unit square; maximize sum of radii | ↑ | open | AlphaEvolve |
| `geometry/packing_unit_cubes` | Pack n=11 unit cubes (arbitrary rotation) in smallest bounding cube | ↑ | open | AlphaEvolve |
| `geometry/spherical_t_design_n24_t7` | Construct spherical 7-design with n=24 points; minimize max Gegenbauer error | ↑ | open | AlphaEvolve |
| `geometry/tammes_n14` | Place n=14 points on unit sphere; maximize minimum pairwise distance | ↑ | open | AlphaEvolve |
| `geometry/tammes_n24` | Place n=24 points on unit sphere; maximize minimum pairwise distance | ↑ | open | AlphaEvolve |
| `geometry/thomson_n32` | Place n=32 points on unit sphere; minimize Thomson (Coulomb) energy | ↑ | open | AlphaEvolve |

## Number Theory (8 problems)

| Problem ID | Description | Opt | Known Best Score | Source |
|---|---|---|---|---|
| `number_theory/difference_bases` | Find efficient difference basis B; maximize k/n² where every int ≤ k is a difference | ↑ | ≤ 0.5 | AlphaEvolve |
| `number_theory/finite_field_kakeya` | Minimize Kakeya sets in F_p^d (d=3); average −\|K(p)\|/reference across primes | ↑ | open | AlphaEvolve |
| `number_theory/finite_field_kakeya/d2` | Finite field Kakeya in d=2; primes [3,5,7,11,13] | ↑ | open | AlphaEvolve |
| `number_theory/finite_field_kakeya/d3` | Finite field Kakeya in d=3 (Lean-verified proof found by AlphaEvolve); primes [3,5,7,11] | ↑ | open | AlphaEvolve |
| `number_theory/finite_field_kakeya/d4` | Finite field Kakeya in d=4 (links to elliptic curves found); primes [3,5,7] | ↑ | open | AlphaEvolve |
| `number_theory/finite_field_kakeya/d5` | Finite field Kakeya in d=5 (computationally demanding); primes [3,5] | ↑ | open | AlphaEvolve |
| `number_theory/finite_field_sum_product_problem` | Minimize log(max(\|X+X\|,\|X·X\|))/log(\|X\|) for sets X ⊆ F_p of size ⌊√p⌋ | ↓ | open | AlphaEvolve |
| `number_theory/prime_number_theorem` | Find partial function f: Z⁺→ℝ maximizing −Σf(k)log(k)/k subject to Dirichlet series constraint | ↑ | open | AlphaEvolve |

## Notes

- **open** = exact optimum unknown; best known score recorded in `spec.known_best_score`.
- Scores for `↑` problems: higher = better. Scores for `↓` problems: lower = better.
- All problem IDs use the pattern `category/problem_name` and can be passed directly to `registry.load()`.
- Sub-problems (e.g., `finite_field_kakeya/d2`) share an evaluator with the parent problem.
