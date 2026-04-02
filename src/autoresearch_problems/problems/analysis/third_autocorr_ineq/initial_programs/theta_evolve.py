import numpy as np


def solve():
    """Construct a function minimizing C₃ = 2·n·max(|conv(f,f)|) / (∑f)²."""
    n = 400
    x = np.linspace(-0.25, 0.25, n)
    center = 0.0
    width = 0.1
    heights = np.exp(-((x - center) ** 2) / (2 * width ** 2))
    freq1 = 8.0
    freq2 = 16.0
    heights += 0.3 * np.cos(2 * np.pi * freq1 * x)
    heights += 0.15 * np.sin(2 * np.pi * freq2 * x)
    target_sum = 25.0
    heights = heights * (target_sum / np.sum(heights))
    return heights
