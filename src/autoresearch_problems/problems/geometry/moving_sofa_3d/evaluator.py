"""Evaluator for the 3D Moving Sofa problem."""
import numpy as np

try:
    from scipy.spatial.transform import Rotation
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

CORRIDOR_WIDTH = 1.0
MIDDLE_LENGTH = 4.0


def _in_corridor(pts):
    """Check which points lie in the 3D L-shaped corridor.

    The corridor has:
    - Entry arm: x <= 0, y in [0, W], z in [0, W]  (extends in negative x)
    - Middle arm: x in [0, W], y in [0, W+L], z in [0, W]
    - Exit arm: x in [0, W], y >= W+L, z in [0, W+?]  (extends in positive y)
    """
    x, y, z = pts[:, 0], pts[:, 1], pts[:, 2]
    w = CORRIDOR_WIDTH
    yt = w + MIDDLE_LENGTH

    mask1 = (x <= 0) & (y >= 0) & (y <= w) & (z >= 0) & (z <= w)
    mask2 = (x >= 0) & (x <= w) & (y >= 0) & (y <= yt) & (z >= 0) & (z <= w)
    mask3 = (x >= 0) & (x <= w) & (y >= yt) & (y <= yt + w) & (z >= 0)
    return mask1 | mask2 | mask3


def evaluate(output: object, n_poses: int = 20, n_grid: int = 20, **kwargs) -> dict:
    if not HAS_SCIPY:
        return {"score": 0.0, "valid": False, "error": "scipy required", "metrics": {}}
    try:
        poses = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if poses.ndim != 2 or poses.shape[1] != 6:
        return {"score": 0.0, "valid": False,
                "error": f"Expected (m, 6) pose array [tx,ty,tz,yaw,pitch,roll], got {poses.shape}",
                "metrics": {}}

    # Candidate sofa points: sample the entry arm region
    xs = np.linspace(-4, 0, n_grid)
    ys = np.linspace(0, CORRIDOR_WIDTH, n_grid)
    zs = np.linspace(0, CORRIDOR_WIDTH, n_grid)
    gx, gy, gz = np.meshgrid(xs, ys, zs, indexing="ij")
    candidate_pts = np.column_stack([gx.ravel(), gy.ravel(), gz.ravel()])

    alive = np.ones(len(candidate_pts), dtype=bool)

    for pose in poses:
        tx, ty, tz = float(pose[0]), float(pose[1]), float(pose[2])
        yaw, pitch, roll = float(pose[3]), float(pose[4]), float(pose[5])
        try:
            rot = Rotation.from_euler("ZYX", [yaw, pitch, roll], degrees=True)
            rotated = rot.apply(candidate_pts)
        except Exception as exc:
            return {"score": 0.0, "valid": False,
                    "error": f"Invalid rotation: {exc}", "metrics": {}}
        translated = rotated + np.array([tx, ty, tz])
        in_corr = _in_corridor(translated)
        alive &= in_corr

    n_alive = int(np.sum(alive))
    cell_vol = abs((xs[1] - xs[0]) * (ys[1] - ys[0]) * (zs[1] - zs[0]))
    volume = n_alive * cell_vol

    return {"score": volume, "valid": True, "error": "",
            "metrics": {"volume": volume, "n_alive": n_alive}}
