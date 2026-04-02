import numpy as np


def solve() -> list:
    """Construct a step function with high C₂ value."""
    f_values = [np.random.random()] * np.random.randint(100, 10000)
    return f_values
