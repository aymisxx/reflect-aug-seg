import numpy as np


def compute_class_counts(semantic_labels: np.ndarray):
    """
    Count number of points per class.

    Returns:
        classes: (K,)
        counts: (K,)
    """
    classes, counts = np.unique(semantic_labels, return_counts=True)
    return classes, counts


def compute_class_percentages(semantic_labels: np.ndarray):
    """
    Compute percentage per semantic class.

    Returns:
        dict: {class_id: percentage}
    """
    classes, counts = compute_class_counts(semantic_labels)

    total = counts.sum()
    percentages = counts / total

    return {int(c): float(p) for c, p in zip(classes, percentages)}


def get_top_k_classes(class_percentage_dict, k=5, ignore_classes=None):
    """
    Get top-k classes by percentage.

    Args:
        class_percentage_dict: {class_id: percentage}
        k: number of top classes
        ignore_classes: set/list of class IDs to ignore

    Returns:
        list of tuples: [(class_id, percentage), ...]
    """

    if ignore_classes is None:
        ignore_classes = set()

    filtered = [
        (cls, pct)
        for cls, pct in class_percentage_dict.items()
        if cls not in ignore_classes
    ]

    # sort descending by percentage
    filtered.sort(key=lambda x: x[1], reverse=True)

    return filtered[:k]