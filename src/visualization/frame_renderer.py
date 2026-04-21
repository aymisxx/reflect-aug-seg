import numpy as np
import matplotlib.pyplot as plt

from src.semantics.label_map import get_class_name
from src.semantics.class_stats import compute_class_percentages, get_top_k_classes


# =========================================================
# 🎨 COLORS
# =========================================================

CLASS_COLORS = {
    40: (1.0, 0.0, 1.0),   # road
    48: (0.6, 0.0, 0.6),   # sidewalk
    70: (0.0, 0.7, 0.0),   # vegetation
    50: (0.0, 0.0, 1.0),   # building
    10: (1.0, 0.5, 0.2),   # car
    44: (0.8, 0.6, 0.8),   # parking
    72: (0.5, 0.4, 0.2),   # terrain
}


# =========================================================
# 🔆 REFLECTIVITY
# =========================================================

def normalize(values, vmin=0.0, vmax=20.0):
    values = np.clip(values, vmin, vmax)
    return (values - vmin) / (vmax - vmin + 1e-6)


def build_rgb(sem, refl):
    norm = normalize(refl)
    rgb = np.zeros((len(sem), 3))

    for cls, color in CLASS_COLORS.items():
        mask = sem == cls
        rgb[mask] = np.array(color) * norm[mask][:, None]

    return rgb


# =========================================================
# 📍 BEV (unchanged)
# =========================================================

def render_bev(frame):
    xyz = frame["xyz"]
    rgb = build_rgb(frame["semantic_labels"], frame["pseudo_reflectivity"])

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(xyz[:, 0], xyz[:, 1], c=rgb, s=0.4)

    ax.set_title("BEV")
    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_aspect("equal")

    return fig


# =========================================================
# 🎮 FPS VIEW (ego-centric, front-facing, perspective-like)
# =========================================================

def render_forward(frame):
    xyz = frame["xyz"]
    sem = frame["semantic_labels"]
    refl = frame["pseudo_reflectivity"]

    x = xyz[:, 0]   # forward
    y = xyz[:, 1]   # left/right
    z = xyz[:, 2]   # height

    # Only keep points in front of the moving agent
    mask = (
        (x > 1.0) &
        (x < 50.0) &
        (np.abs(y) < 25.0) &
        (z > -3.0) &
        (z < 3.0)
    )

    x = x[mask]
    y = y[mask]
    z = z[mask]
    sem = sem[mask]
    refl = refl[mask]

    rgb = build_rgb(sem, refl)

    # Perspective-like FPS projection
    u = y / x
    v = z / x

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(u, v, c=rgb, s=0.4)

    ax.set_title("FPS View")
    ax.set_xlabel("Horizontal")
    ax.set_ylabel("Vertical")

    ax.set_xlim(-0.8, 0.8)
    ax.set_ylim(-0.25, 0.25)

    return fig


# =========================================================
# 📊 TEXT PANEL
# =========================================================

def render_text(frame):
    class_pct = compute_class_percentages(frame["semantic_labels"])
    top = get_top_k_classes(class_pct, k=6, ignore_classes={0, 255})

    fig, ax = plt.subplots(figsize=(4.3, 5))
    ax.axis("off")
    ax.set_title("Top Classes", fontsize=14)

    y = 0.9
    for cls, pct in top:
        name = get_class_name(cls)
        color = CLASS_COLORS.get(cls, (0.5, 0.5, 0.5))

        ax.add_patch(
            plt.Rectangle(
                (0.05, y - 0.03),
                0.05,
                0.05,
                color=color,
                transform=ax.transAxes,
                clip_on=False,
            )
        )

        ax.text(
            0.13,
            y,
            f"{name}: {pct * 100:.1f}%",
            fontsize=12,
            va="center",
            transform=ax.transAxes,
        )

        y -= 0.11

    return fig


# =========================================================
# 🧱 FIG → IMAGE (FIXED SAFE)
# =========================================================

def fig_to_img(fig):
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    img = np.asarray(buf)[:, :, :3]
    plt.close(fig)
    return img


# =========================================================
# 🚫 NO BLACK PADDING — WHITE BACKGROUND
# =========================================================

def pad(img, H):
    if img.shape[0] == H:
        return img

    pad_h = H - img.shape[0]
    white = np.ones((pad_h, img.shape[1], 3), dtype=np.uint8) * 255

    return np.vstack([img, white])


# =========================================================
# 🎬 FINAL FRAME
# =========================================================

def render_frame(frame):
    bev = fig_to_img(render_bev(frame))
    fwd = fig_to_img(render_forward(frame))
    txt = fig_to_img(render_text(frame))

    H = max(bev.shape[0], fwd.shape[0], txt.shape[0])

    bev = pad(bev, H)
    fwd = pad(fwd, H)
    txt = pad(txt, H)

    combined = np.concatenate([bev, fwd, txt], axis=1)

    return combined