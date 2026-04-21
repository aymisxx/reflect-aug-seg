from pathlib import Path
import numpy as np


def load_frame(sequence_path: Path, frame_id: str):
    """
    Load a single SemanticKITTI frame.

    Args:
        sequence_path: Path to sequence folder (e.g., .../sequences/00)
        frame_id: string like "000000"

    Returns:
        dict with:
            xyz: (N, 3)
            intensity: (N,)
            semantic_labels: (N,)
    """

    velodyne_path = sequence_path / "velodyne" / f"{frame_id}.bin"
    label_path = sequence_path / "labels" / f"{frame_id}.label"

    # Load point cloud
    points = np.fromfile(velodyne_path, dtype=np.float32).reshape(-1, 4)

    xyz = points[:, :3]
    intensity = points[:, 3]

    # Load labels
    labels = np.fromfile(label_path, dtype=np.uint32)

    # Alignment check
    if points.shape[0] != labels.shape[0]:
        raise ValueError(f"Point-label mismatch at frame {frame_id}")

    # Extract semantic labels
    semantic_labels = labels & 0xFFFF

    return {
        "xyz": xyz,
        "intensity": intensity,
        "semantic_labels": semantic_labels,
    }