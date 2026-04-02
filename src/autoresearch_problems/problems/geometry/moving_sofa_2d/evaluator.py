"""Evaluator for the 2D Moving Sofa problem."""
import numpy as np

CORRIDOR_WIDTH = 1.0


def _in_L_corridor(pts):
    """Check which points lie in the L-shaped corridor.

    The L-corridor consists of:
    - Horizontal arm: y in [0, 1], x can be any value <= 1
    - Vertical arm: x in [0, 1], y >= 0
    The corner region (x in [0,1], y in [0,1]) is shared.
    """
    x, y = pts[:, 0], pts[:, 1]
    w = CORRIDOR_WIDTH
    mask_h = (y >= 0) & (y <= w) & (x <= w)
    mask_v = (x >= 0) & (x <= w) & (y >= 0)
    return mask_h | mask_v


def _rotate_pts(pts, theta_deg):
    theta = np.deg2rad(theta_deg)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, -s], [s, c]])
    return pts @ R.T


def evaluate(output: object, n_poses: int = 20, n_grid: int = 50, **kwargs) -> dict:
    try:
        poses = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if poses.ndim != 2 or poses.shape[1] != 3:
        return {"score": 0.0, "valid": False,
                "error": f"Expected shape (m, 3) for poses [tx, ty, theta_deg], got {poses.shape}",
                "metrics": {}}

    # Candidate sofa points: sample the horizontal corridor region
    xs = np.linspace(-3 * CORRIDOR_WIDTH, CORRIDOR_WIDTH, n_grid)
    ys = np.linspace(0, CORRIDOR_WIDTH, n_grid)
    gx, gy = np.meshgrid(xs, ys)
    candidate_pts = np.column_stack([gx.ravel(), gy.ravel()])

    # A point p is in the sofa iff at every pose (tx, ty, theta), the
    # transformed point R(theta)*p + (tx, ty) lies in the L-corridor.
    alive = np.ones(len(candidate_pts), dtype=bool)

    for pose in poses:
        tx, ty, theta_deg = float(pose[0]), float(pose[1]), float(pose[2])
        rotated = _rotate_pts(candidate_pts, theta_deg)
        translated = rotated + np.array([tx, ty])
        in_corr = _in_L_corridor(translated)
        alive &= in_corr

    n_alive = int(np.sum(alive))
    cell_area = abs((xs[1] - xs[0]) * (ys[1] - ys[0]))
    area = n_alive * cell_area

    return {"score": area, "valid": True, "error": "",
            "metrics": {"area": area, "n_alive": n_alive}}
