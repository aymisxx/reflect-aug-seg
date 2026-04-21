from pathlib import Path
import random


def list_sequences(dataset_root: Path):
    """
    Returns available sequence IDs like ['00', '01', '02']
    """
    seq_root = dataset_root / "sequences"
    return sorted([p.name for p in seq_root.iterdir() if p.is_dir()])


def list_frames(sequence_path: Path):
    """
    Returns sorted frame IDs like ['000000', '000001', ...]
    """
    velodyne_dir = sequence_path / "velodyne"
    return sorted([p.stem for p in velodyne_dir.glob("*.bin")])


def sample_contiguous_window(
    dataset_root: Path,
    window_size: int,
    allowed_sequences=None
):
    """
    Randomly:
    1. pick a sequence (restricted if provided)
    2. pick a valid continuous window

    Args:
        dataset_root: Path to SemanticKITTI dataset root
        window_size: number of frames required
        allowed_sequences: list like ['00','01','02'] (optional)

    Returns:
        sequence_id (str)
        frame_ids (list[str])
    """

    # --- Step 1: discover sequences ---
    all_sequences = list_sequences(dataset_root)

    # --- Step 2: restrict if needed ---
    if allowed_sequences is not None:
        sequences = [s for s in all_sequences if s in allowed_sequences]
    else:
        sequences = all_sequences

    if len(sequences) == 0:
        raise ValueError("No valid sequences found")

    # --- Step 3: pick random sequence ---
    seq_id = random.choice(sequences)
    sequence_path = dataset_root / "sequences" / seq_id

    # --- Step 4: get frames ---
    frames = list_frames(sequence_path)

    if len(frames) < window_size:
        raise ValueError(f"Sequence {seq_id} too short for window size {window_size}")

    # --- Step 5: sample contiguous window ---
    max_start = len(frames) - window_size
    start_idx = random.randint(0, max_start)

    selected_frames = frames[start_idx : start_idx + window_size]

    return seq_id, selected_frames