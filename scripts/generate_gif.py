import sys
import time
import argparse
from pathlib import Path

# =========================================================
# 🧭 MAKE PROJECT ROOT IMPORTABLE
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# =========================================================
# 📦 IMPORTS
# =========================================================

from src.io.sequence_sampler import sample_contiguous_window
from src.io.loader import load_frame
from src.signals.reflectivity import compute_signals
from src.visualization.frame_renderer import render_frame
from src.animation.gif_writer import save_gif

from src.metrics.separability import fisher_separability
from src.metrics.csv_logger import init_csv, append_row


# =========================================================
# 🚀 MAIN PIPELINE
# =========================================================

def run_pipeline(dataset_root, fps, duration, allowed_sequences, output_gif):
    window = fps * duration

    output_gif = Path(output_gif)
    output_gif.parent.mkdir(parents=True, exist_ok=True)

    print("\nSampling sequence...")
    seq_id, frame_ids = sample_contiguous_window(
        dataset_root,
        window_size=window,
        allowed_sequences=allowed_sequences
    )

    seq_path = dataset_root / "sequences" / seq_id

    print(f"Sequence: {seq_id}")
    print(f"Frames: {window}")

    csv_path = output_gif.with_suffix(".csv")
    init_csv(csv_path)

    frames = []
    start_time = time.time()

    for i, fid in enumerate(frame_ids):
        if i % 20 == 0:
            elapsed = time.time() - start_time
            print(f"[{i}/{window}] elapsed={elapsed:.1f}s")

        frame = load_frame(seq_path, fid)
        frame = compute_signals(frame)

        raw_sep = fisher_separability(
            frame["intensity"],
            frame["semantic_labels"]
        )
        aug_sep = fisher_separability(
            frame["pseudo_reflectivity"],
            frame["semantic_labels"]
        )
        delta = aug_sep - raw_sep

        append_row(csv_path, [
            fid,
            seq_id,
            raw_sep,
            aug_sep,
            delta
        ])

        img = render_frame(frame)
        frames.append(img)

    save_gif(frames, output_gif, fps=fps)

    total_time = time.time() - start_time

    print("\nDONE")
    print("GIF:", output_gif)
    print("CSV:", csv_path)
    print(f"Time: {total_time/60:.2f} min")


# =========================================================
# 🧠 CLI ENTRYPOINT
# =========================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate reflectivity-augmented LiDAR GIF and CSV metrics"
    )

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Path to SemanticKITTI dataset root"
    )
    parser.add_argument("--fps", type=int, default=10)
    parser.add_argument("--duration", type=int, default=60)
    parser.add_argument("--output", type=str, default="artifacts/final_seq.gif")
    parser.add_argument(
        "--sequences",
        nargs="+",
        default=["00", "01", "02"],
        help="Allowed sequence IDs"
    )

    args = parser.parse_args()

    dataset_root = Path(args.dataset)

    run_pipeline(
        dataset_root=dataset_root,
        fps=args.fps,
        duration=args.duration,
        allowed_sequences=args.sequences,
        output_gif=args.output
    )


if __name__ == "__main__":
    main()