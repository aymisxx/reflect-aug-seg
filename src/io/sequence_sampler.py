# src/io/sequence_sampler.py

import random
from pathlib import Path


def get_available_sequences(base_path):
    """
    Returns list of available sequence folders (e.g., ['00', '01', '02'])
    """
    base = Path(base_path)
    sequences = [p.name for p in base.iterdir() if p.is_dir()]
    return sorted(sequences)


def get_frame_ids(sequence_path):
    """
    Returns sorted frame IDs (strings) from velodyne folder
    """
    velodyne_dir = Path(sequence_path) / "velodyne"
    frame_ids = sorted([f.stem for f in velodyne_dir.glob("*.bin")])
    return frame_ids


def sample_continuous_sequence(base_path, duration_sec=60, fps=10):
    """
    Randomly selects:
    - a sequence (00, 01, 02)
    - a continuous chunk of frames

    Returns:
    - sequence_path
    - selected_frame_ids (list)
    """

    # Step 1: pick random sequence
    sequences = get_available_sequences(base_path)
    chosen_seq = random.choice(sequences)

    sequence_path = Path(base_path) / chosen_seq

    # Step 2: get all frames
    frame_ids = get_frame_ids(sequence_path)
    N = len(frame_ids)

    # Step 3: compute required frames
    T = duration_sec * fps

    if T >= N:
        raise ValueError(f"Requested {T} frames, but only {N} available.")

    # Step 4: random start index
    start_idx = random.randint(0, N - T)

    selected_frames = frame_ids[start_idx:start_idx + T]

    return sequence_path, selected_frames