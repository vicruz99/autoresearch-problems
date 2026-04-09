# Agent Guide — No Isosceles Triangles

## Goal

Return a list of (x, y) integer coordinate pairs from the 64×64 grid, with no three forming an isosceles triangle (no equal adjacent distances); maximize len(points)/64.

## Strategy hints

- Start with a small verified set (e.g., points on a geometric progression) and extend greedily.
- Check the isosceles condition before adding each new point: O(k²) per candidate.
- Points from arithmetic progressions tend to create many isosceles triangles — avoid them.
- Consider points where coordinates follow specific number-theoretic patterns (e.g., all coordinates are powers of 2 modulo n).
- Use squared distances to avoid floating-point issues.

## Output format

Return a Python `list` of 2-element tuples or lists `[[x, y], ...]` with integer coordinates in `[0, 64)`.

```python
def solve(n: int = 64) -> list:
    points = []
    distances = {}
    for x in range(n):
        for y in range(n):
            valid = True
            for i, (px, py) in enumerate(points):
                d = (x-px)**2 + (y-py)**2
                if d == 0:
                    valid = False
                    break
                for j, (qx, qy) in enumerate(points[:i]):
                    if (px-qx)**2 + (py-qy)**2 == d or (x-qx)**2 + (y-qy)**2 == d:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                points.append([x, y])
    return points
```

## Pitfalls

- The greedy check becomes slow for large point sets; cache distance sets per point.
- Coordinates must be integers in [0, n) — not arbitrary floats.
- An isosceles triangle requires two equal distances from the same vertex; check all three vertex choices.

## Baseline

A single row of points is highly isosceles-prone. A greedy algorithm typically finds ~5–10 valid points; the best constructions may achieve 15–30 for n=64.
