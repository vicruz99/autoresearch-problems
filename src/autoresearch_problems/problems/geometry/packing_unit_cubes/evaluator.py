"""Evaluator for the Packing Unit Cubes problem.

Matches packing_unit_cubes.ipynb Cell 4: calculate_packing_score_cubes_3d.
The first 8 cubes (NUM_CUBES_IN_CORNERS=8) are placed at the 8 corners of the
bounding box (axis-aligned). Remaining cubes are scored as provided.
"""
import numpy as np

NUM_CUBES_IN_CORNERS = 8


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


def _get_axes(rot_mat):
    return [rot_mat[:, j] for j in range(3)]


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
        if mx1 < mn2 - 1e-9 or mx2 < mn1 - 1e-9:
            return True
    return False


def _intersects(verts1, axes1, verts2, axes2):
    sat_axes = list(axes1) + list(axes2)
    for a1 in axes1:
        for a2 in axes2:
            cross = np.cross(a1, a2)
            if np.linalg.norm(cross) > 1e-6:
                sat_axes.append(cross)
    return not _separated_by_axis(verts1, verts2, sat_axes)


def _bounding_box(all_verts_list):
    all_verts = np.vstack(all_verts_list)
    min_coords = np.min(all_verts, axis=0)
    max_coords = np.max(all_verts, axis=0)
    side = float(np.max(max_coords - min_coords))
    return side, min_coords, max_coords


def evaluate(output: object, n: int = 11,
             intersection_penalty_factor: float = 100.0, **kwargs) -> dict:
    """Score a candidate cube packing configuration.

    Parameters
    ----------
    output : array-like of shape (n, 6)
        Each row is [cx, cy, cz, rx_deg, ry_deg, rz_deg].
    n : int
        Expected number of cubes (default 11).
    intersection_penalty_factor : float
        Penalty per intersecting pair (default 100.0).

    Returns
    -------
    dict with keys: score, valid, error, metrics.
        score = -final_side_length - intersection_count * penalty.
    """
    try:
        arr = np.asarray(output, dtype=float)
    except Exception as exc:
        return {"score": -1_000_002.0, "valid": False, "error": str(exc), "metrics": {}}
    if arr.ndim != 2 or arr.shape != (n, 6):
        return {"score": -1_000_000.0, "valid": False,
                "error": f"Expected ({n}, 6), got {arr.shape}", "metrics": {}}

    if not np.all(np.isfinite(arr)):
        return {"score": -1_000_002.0, "valid": False,
                "error": "Non-finite values in input", "metrics": {}}

    # Build working copy of placements
    placements = arr.tolist()

    # Compute initial bounding box from all cubes as provided
    init_verts = [
        _get_vertices(np.array(placements[i][:3]),
                      _rotation_matrix(*placements[i][3:]))
        for i in range(n)
    ]
    _, min_b, max_b = _bounding_box(init_verts)

    # Place the first NUM_CUBES_IN_CORNERS cubes at the corners (axis-aligned)
    num_corner_cubes = min(n, NUM_CUBES_IN_CORNERS)
    if num_corner_cubes > 0:
        corner_centers = [
            [min_b[0] + 0.5, min_b[1] + 0.5, min_b[2] + 0.5],
            [min_b[0] + 0.5, min_b[1] + 0.5, max_b[2] - 0.5],
            [min_b[0] + 0.5, max_b[1] - 0.5, min_b[2] + 0.5],
            [min_b[0] + 0.5, max_b[1] - 0.5, max_b[2] - 0.5],
            [max_b[0] - 0.5, min_b[1] + 0.5, min_b[2] + 0.5],
            [max_b[0] - 0.5, min_b[1] + 0.5, max_b[2] - 0.5],
            [max_b[0] - 0.5, max_b[1] - 0.5, min_b[2] + 0.5],
            [max_b[0] - 0.5, max_b[1] - 0.5, max_b[2] - 0.5],
        ]
        for i in range(num_corner_cubes):
            placements[i][:3] = corner_centers[i]
            placements[i][3:] = [0.0, 0.0, 0.0]

    # Build final geometry
    rot_mats = [_rotation_matrix(*placements[i][3:]) for i in range(n)]
    all_verts = [
        _get_vertices(np.array(placements[i][:3]), rot_mats[i])
        for i in range(n)
    ]
    all_axes = [_get_axes(rot_mats[i]) for i in range(n)]

    final_side, _, _ = _bounding_box(all_verts)

    # Count intersections
    intersection_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if _intersects(all_verts[i], all_axes[i], all_verts[j], all_axes[j]):
                intersection_count += 1

    score = -final_side - intersection_count * intersection_penalty_factor
    valid = intersection_count == 0
    error = "" if valid else f"{intersection_count} pair(s) of cubes intersect"

    return {"score": float(score), "valid": valid, "error": error,
            "metrics": {"bounding_box_side": float(final_side),
                        "intersection_count": intersection_count}}
