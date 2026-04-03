# Ring Loading Problem

## Problem Description

Find **m=15 pairs** `(uᵢ, vᵢ)` with `uᵢ + vᵢ ≤ 1` and `uᵢ, vᵢ ≥ 0` to **maximize α**, where:

```
α = min over all sign assignments z  of  max_{k=1..m-1} |∑_{i=1}^{k} zᵢ - ∑_{i=k+1}^{m} zᵢ|
```

Each `zᵢ` independently takes value either `vᵢ` or `-uᵢ`.

This problem models load balancing on a ring network: each demand `i` can be routed clockwise (load `vᵢ`) or counterclockwise (load `uᵢ`), and we want to guarantee that no matter how demands are routed, the maximum imbalance across any arc is `α`.

## Function Signature

```python
def solve() -> list:
    """
    Returns:
        list: m=15 pairs (u_i, v_i).
              Each element must be indexable: item[0]=u_i, item[1]=v_i.
              Pairs with u_i+v_i > 1 will be normalized.
    """
```

## Evaluation

1. For each pair, `uᵢ, vᵢ` are made non-negative and normalized if `uᵢ + vᵢ > 1`
2. All `2^m = 32768` sign assignments are enumerated
3. For each assignment, the maximum imbalance `max_k |∑_{i≤k} zᵢ - ∑_{i>k} zᵢ|` is computed
4. `score = α = min` over assignments of the maximum imbalance

## Tips

- Uniform pairs `(u, v) = (1/3, 2/3)` give a baseline score.
- Pairs with `u = v = 1/2` may be harder to balance.
- The theoretical maximum α is related to combinatorial discrepancy theory.
- Think about what "worst case" sign assignments look like and design pairs to resist them.
