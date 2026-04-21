import numpy as np


def compute_range(xyz: np.ndarray) -> np.ndarray:
    """
    Compute Euclidean range for each point.

    Args:
        xyz: (N, 3)

    Returns:
        ranges: (N,)
    """
    return np.linalg.norm(xyz, axis=1)


def compute_pseudo_reflectivity(intensity: np.ndarray, ranges: np.ndarray) -> np.ndarray:
    """
    Compute pseudo-reflectivity: I * R

    Args:
        intensity: (N,)
        ranges: (N,)

    Returns:
        pseudo_reflectivity: (N,)
    """
    eps = 1e-6
    return intensity * np.maximum(ranges, eps)


def compute_signals(frame: dict) -> dict:
    """
    Given raw frame, compute derived signals.

    Input frame must contain:
        xyz
        intensity

    Returns:
        extended frame dict with:
            ranges
            pseudo_reflectivity
    """

    xyz = frame["xyz"]
    intensity = frame["intensity"]

    ranges = compute_range(xyz)
    pseudo_reflectivity = compute_pseudo_reflectivity(intensity, ranges)

    frame_out = frame.copy()
    frame_out["ranges"] = ranges
    frame_out["pseudo_reflectivity"] = pseudo_reflectivity

    return frame_out