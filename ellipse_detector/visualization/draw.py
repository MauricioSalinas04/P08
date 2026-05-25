from __future__ import annotations

import math

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse as MplEllipse

from ellipse_detector import Ellipse

_PALETTE = [
    "#ff3b30",  # red
    "#34c759",  # green
    "#007aff",  # blue
    "#ff9500",  # orange
    "#af52de",  # purple
    "#ffcc00",  # yellow
    "#5ac8fa",  # cyan
    "#ff2d55",  # pink
]


def draw_ellipses(
    image: np.ndarray,
    ellipses: list[Ellipse],
    color: tuple[int, int, int] = (0, 255, 0),
    thickness: int = 2,
) -> np.ndarray:
    output = _ensure_rgb(image)
    H, W = output.shape[:2]

    for ellipse in ellipses:
        t = np.linspace(0.0, 2.0 * math.pi, 1000)
        cos_t = np.cos(ellipse.angle_rad)
        sin_t = np.sin(ellipse.angle_rad)
        a, b = ellipse.semi_major, ellipse.semi_minor
        xs = ellipse.center_x + a * np.cos(t) * cos_t - b * np.sin(t) * sin_t
        ys = ellipse.center_y + a * np.cos(t) * sin_t + b * np.sin(t) * cos_t
        xi = np.clip(np.round(xs).astype(int), 0, W - 1)
        yi = np.clip(np.round(ys).astype(int), 0, H - 1)
        radius = max(thickness // 2, 1)
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                xc = np.clip(xi + dx, 0, W - 1)
                yc = np.clip(yi + dy, 0, H - 1)
                output[yc, xc] = color
    return output


def save_result(
    image: np.ndarray,
    ellipses: list[Ellipse],
    output_path: str,
    edge_mask: np.ndarray | None = None,
) -> None:
    rgb = _ensure_rgb(image)
    n_panels = 3 if edge_mask is not None else 2
    fig, axes = plt.subplots(1, n_panels, figsize=(6 * n_panels, 6), dpi=110)
    if n_panels == 2:
        axes = list(axes)

    axes[0].imshow(rgb)
    axes[0].set_title("Original")
    axes[0].axis("off")

    panel_idx = 1
    if edge_mask is not None:
        axes[panel_idx].imshow(edge_mask, cmap="gray")
        axes[panel_idx].set_title(f"Bordes detectados ({int(edge_mask.sum())} px)")
        axes[panel_idx].axis("off")
        panel_idx += 1

    ax_overlay = axes[panel_idx]
    ax_overlay.imshow(rgb)
    for i, ell in enumerate(ellipses):
        color = _PALETTE[i % len(_PALETTE)]
        patch = MplEllipse(
            xy=(ell.center_x, ell.center_y),
            width=2 * ell.semi_major,
            height=2 * ell.semi_minor,
            angle=math.degrees(ell.angle_rad),
            edgecolor=color,
            facecolor="none",
            linewidth=2.5,
        )
        ax_overlay.add_patch(patch)
        ax_overlay.plot(ell.center_x, ell.center_y, "+", color=color, markersize=12, mew=2)
        ax_overlay.annotate(
            f"#{i + 1}",
            xy=(ell.center_x, ell.center_y),
            xytext=(8, -10),
            textcoords="offset points",
            color=color,
            fontsize=11,
            fontweight="bold",
        )
    ax_overlay.set_title(f"Elipses detectadas: {len(ellipses)}")
    ax_overlay.axis("off")

    fig.suptitle("Detector de elipses — Yuen, Illingworth & Kittler (1988)", fontsize=13)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def save_overlay_only(
    image: np.ndarray,
    ellipses: list[Ellipse],
    output_path: str,
) -> None:
    rgb = _ensure_rgb(image)
    fig, ax = plt.subplots(figsize=(8, 8), dpi=130)
    ax.imshow(rgb)
    for i, ell in enumerate(ellipses):
        color = _PALETTE[i % len(_PALETTE)]
        patch = MplEllipse(
            xy=(ell.center_x, ell.center_y),
            width=2 * ell.semi_major,
            height=2 * ell.semi_minor,
            angle=math.degrees(ell.angle_rad),
            edgecolor=color,
            facecolor="none",
            linewidth=2.5,
        )
        ax.add_patch(patch)
        ax.plot(ell.center_x, ell.center_y, "+", color=color, markersize=12, mew=2)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight", pad_inches=0)
    plt.close(fig)


def _ensure_rgb(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return np.stack([image, image, image], axis=-1)
    if image.ndim == 3 and image.shape[2] == 4:
        return image[:, :, :3].copy()
    return image.copy()
