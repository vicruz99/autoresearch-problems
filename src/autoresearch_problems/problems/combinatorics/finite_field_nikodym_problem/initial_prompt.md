# Finite Field Nikodym Problem

Act as a research mathematician specialising in combinatorics over finite fields.

## Problem Statement

The finite field Nikodym problem asks for the minimum-size Nikodym set in
F_q^2, where q = p^2 for a prime p.

A set N ⊆ F_q^2 is a **Nikodym set** if for every point x ∈ F_q^2 there
exists a direction v ∈ F_q^2 \ {0} such that the *punctured line*

    { x + t·v : t ∈ F_q, t ≠ 0 }

is entirely contained in N.

## Task

Write a Python function `solve(p, d)` that directly returns a proposed Nikodym
set as a NumPy array.

**Input:**
- `p`: prime number (base field is F_p; the full field is F_q with q = p^2)
- `d`: dimension of the vector space (fixed at 2)

**Output:** A NumPy array of shape `(k, 2, 2)` with dtype `int64`, where each
row `[[xa, xb], [ya, yb]]` represents a point in F_{p^2}^2.  Coordinates
`(xa, xb)` represent the F_{p^2} element `xa + xb·α` where α is a root of an
irreducible polynomial over F_p.

## Evaluation

Your construction is scored by:

    score = |F_q^2| - |N| = q^2 - |N|  (higher is better)

A larger complement means N is smaller.  If N is not a valid Nikodym set, the
score is 0 (heavy penalty).

## Hints

- The trivial Nikodym set is the full F_q^2 (score = 0).
- A good construction is based on the *Unital* and a *Blocking Set*:
  1. Build U = {(x,y) : Trace(x) + Norm(y) = 0} (the Hermitian unital, |U| = p^3)
  2. Build B ⊆ U using Y_special = {u^2 + v·α : u,v ∈ F_p}  (size ≈ p^2(p+1)/2)
  3. Excluded = U \ B;  N = F_q^2 \ Excluded
  This gives complement size ≈ |U \ B| ≈ p^3/2.
- With a more refined "proper blocking set" (Step 2.5 in the paper), the
  complement grows to ≈ c · p^2 · log p.
- For p=5 the simple construction yields complement 50.
- For p=29 AlphaEvolve achieved complement ~24 000.

## Key Algebraic Definitions

In F_q with q = p^2, represent elements as (a, b) meaning `a + b·α` where
α^2 = w (w = smallest quadratic non-residue mod p):

- **Addition:** (a,b) + (c,d) = ((a+c)%p, (b+d)%p)
- **Multiplication:** (a,b)·(c,d) = ((ac+bdw)%p, (ad+bc)%p)
- **Trace(x):** x + x^p = (2a, 0)
- **Norm(x):** x · x^p = (a²−b²w, 0)
