import numpy as np


def solve():
    """Construct a non-negative function maximizing C₂ = ‖f*f‖₂² / (‖f*f‖₁ · ‖f*f‖∞)."""
    N = 256
    rng = np.random.default_rng(42)
    heights = rng.uniform(0.0, 1.0, size=N).astype(np.float32)
    return heights
