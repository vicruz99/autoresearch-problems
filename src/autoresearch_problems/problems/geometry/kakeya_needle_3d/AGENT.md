# Agent Guide — Kakeya Needle 3D

## Goal

Return a list `[x_rand, y_rand]` where each is a flat list of 16 floats representing base offsets for 16 tubes; minimize total union volume; score = −volume/reference, maximize toward 0.

## Strategy hints

- Tubes overlap when their base offsets (x_rand, y_rand) are close together.
- Set all offsets to 0 to make all tubes identical — maximum overlap, minimum volume.
- Then perturb from all-zeros to see if small offsets improve the score.
- The Kakeya 2D construction generalizes: concentrate the base offsets of the tubes around a common point.
- Monte Carlo volume is noisy; average over multiple evaluations if possible.

## Output format

Return a Python `list` of length 2: `[x_rand, y_rand]` where each is a flat list of 16 floats (tube base x-offsets and y-offsets).

```python
def solve(cap_n: int = 4, num_samples: int = 200000) -> list:
    n2 = cap_n * cap_n  # 16
    # All offsets at 0 for maximum tube overlap
    x_rand = [0.0] * n2
    y_rand = [0.0] * n2
    return [x_rand, y_rand]
```

## Pitfalls

- Offsets outside [−1, 1] may cause tubes to extend outside the unit cube.
- The Monte Carlo estimate has variance — compare scores only across multiple seeds.
- The list format must be exactly `[x_list, y_list]` with length-16 inner lists.

## Baseline

All-zero offsets (maximum overlap) give the smallest achievable volume as a baseline. Uniform random offsets give score ≈ −1.0 (matches the reference).
