"""Evaluator for the Packing Unit Cubes problem."""
import numpy as np


def _rotation_matrix(rx, ry, rz):
    rx, ry, rz = np.deg2rad([rx, ry, rz])
    cos_x, sin_x = np.cos(rx), np.sin(rx)
    cos_y, sin_y = np.cos(ry), np.sin(ry)
    cos_z, sin_z = np.cos(rz), np.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cos_x, -sin_x], [0, sin_x, cos_x]])
    Ry = np.array([[cos_y, 0, sin_y], [0, 1, 0], [-sin_y, 0, cos_y]])
    Rz = np.array([[cos_z, -sin_z, 0], [sin_z, cos_z, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def _get_vertices(center, rot_mat):
    h = 0.5
    local = np.array([
        [-h, -h, -h], [-h, -h, h], [-h, h, -h], [-h, h, h],
        [h, -h, -h], [h, -h, h], [h, h, -h], [h, h, h],
    ])
    return (local @ rot_mat.T) + center


def _project(verts, axis):
    norm = np.linalg.norm(axis)
    if norm < 1e-9:
        return 0.0, 0.0
    axis = axis / norm
    p = verts @ axis
    return float(p.min()), float(p.max())


def _separated_by_axis(v1, v2, axes):
    for ax in axes:
        mn1, mx1 = _project(v1, ax)
        mn2, mx2 = _project(v2, ax)
        # Allow face-touching (separation >= 0); only flag strict overlap
        if mx1 < mn2 + 1e-6 or mx2 < mn1 + 1e-6:
            return True
    return False


def _intersects(verts1, axes1, verts2, axes2):
    sat_axes = list(axes1) + list(axes2)
    for a1 in axes1:
        for a2 in axes2:
            cross = np.cross(a1, a2)
            if np.linalg.norm(cross) > 1e-9:
                sat_axes.append(cross)
    return not _separated_by_axis(verts1, verts2, sat_axes)


def evaluate(output: object, n: int = 11, **kwargs) -> dict:
    try:
        arr = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": 0.0, "valid": False, "error": str(exc), "metrics": {}}
    if arr.ndim != 2 or arr.shape != (n, 6):
        return {"score": 0.0, "valid": False,
                "error": f"Expected ({n}, 6), got {arr.shape}", "metrics": {}}

    cubes = []
    for i in range(n):
        center = arr[i, :3]
        rot = _rotation_matrix(*arr[i, 3:])
        verts = _get_vertices(center, rot)
        axes = [rot[:, j] for j in range(3)]
        cubes.append((verts, axes))

    for i in range(n):
        for j in range(i + 1, n):
            if _intersects(cubes[i][0], cubes[i][1], cubes[j][0], cubes[j][1]):
                return {"score": 0.0, "valid": False,
                        "error": f"Cubes {i} and {j} intersect", "metrics": {}}

    all_verts = np.vstack([c[0] for c in cubes])
    span = np.max(all_verts, axis=0) - np.min(all_verts, axis=0)
    side = float(np.max(span))
    return {"score": -side, "valid": True, "error": "",
            "metrics": {"bounding_box_side": side}}
