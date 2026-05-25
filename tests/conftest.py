from __future__ import annotations

import math

import numpy as np
import pytest


def make_ellipse_image(
    width: int,
    height: int,
    center: tuple[float, float],
    semi_major: float,
    semi_minor: float,
    angle_deg: float,
    noise_sigma: float = 0.0,
) -> np.ndarray:
    t = np.linspace(0.0, 2.0 * math.pi, 2000)
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    xs = center[0] + semi_major * np.cos(t) * cos_a - semi_minor * np.sin(t) * sin_a
    ys = center[1] + semi_major * np.cos(t) * sin_a + semi_minor * np.sin(t) * cos_a
    img = np.zeros((height, width), dtype=np.uint8)
    xi = np.clip(np.round(xs).astype(int), 0, width - 1)
    yi = np.clip(np.round(ys).astype(int), 0, height - 1)
    img[yi, xi] = 255
    if noise_sigma > 0.0:
        rng = np.random.default_rng(42)
        noise = rng.normal(0, noise_sigma, img.shape).astype(np.float32)
        img = np.clip(img.astype(np.float32) + noise, 0, 255).astype(np.uint8)
    return img
