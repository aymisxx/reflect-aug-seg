import numpy as np


def fisher_separability(signal, labels, ignore={0, 255}, min_points=500):
    classes, counts = np.unique(labels, return_counts=True)

    valid = [
        c for c, cnt in zip(classes, counts)
        if c not in ignore and cnt >= min_points
    ]

    if len(valid) < 2:
        return 0.0

    means = []
    vars_ = []
    ns = []

    for c in valid:
        vals = signal[labels == c]
        means.append(vals.mean())
        vars_.append(vals.var())
        ns.append(len(vals))

    means = np.array(means)
    vars_ = np.array(vars_)
    ns = np.array(ns)

    global_mean = np.average(means, weights=ns)

    between = np.sum(ns * (means - global_mean) ** 2)
    within = np.sum(ns * vars_)

    return float(between / (within + 1e-12))