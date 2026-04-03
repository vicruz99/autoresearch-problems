"""Initial solution for the 2D Moving Sofa: semicircular path."""
import numpy as np


def solve() -> np.ndarray:
    """Return a simple path of poses for moving a sofa around the L-corner."""
    # EVOLVE-BLOCK-START
    n_poses = 20
    # Path: rotate from 0 to 90 degrees while translating through the corner
    thetas = np.linspace(0, 90, n_poses)
    poses = np.zeros((n_poses, 3))
    for i, theta in enumerate(thetas):
        t = theta / 90.0  # 0 to 1
        # Translate from (0, 0) to (0.5, 0.5) while rotating
        poses[i, 0] = 0.5 * t          # tx
        poses[i, 1] = 0.5 * t          # ty
        poses[i, 2] = theta             # rotation angle in degrees
    return poses
    # EVOLVE-BLOCK-END
