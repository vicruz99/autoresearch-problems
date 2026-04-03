"""Initial solution for the 3D Moving Sofa: linear path through corridor."""
import numpy as np


def solve() -> np.ndarray:
    """Return a simple linear path of poses for moving a 3D sofa through the corridor."""
    # EVOLVE-BLOCK-START
    n_poses = 20
    poses = np.zeros((n_poses, 6))
    for i in range(n_poses):
        t = i / max(n_poses - 1, 1)
        # Move from entry arm to exit arm by translating along y-axis
        # and rotating 90 degrees around z-axis
        poses[i, 0] = 0.5 * t        # tx: move into x-corridor
        poses[i, 1] = 5.0 * t        # ty: move along y-axis
        poses[i, 2] = 0.0            # tz
        poses[i, 3] = 90.0 * t       # yaw: rotate 90 deg around Z
        poses[i, 4] = 0.0            # pitch
        poses[i, 5] = 0.0            # roll
    return poses
    # EVOLVE-BLOCK-END
