import csv


def init_csv(path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "frame_id",
            "sequence",
            "sep_raw",
            "sep_aug",
            "delta"
        ])


def append_row(path, row):
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)