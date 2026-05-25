from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter, sobel


def compute_gradients(
    image: np.ndarray,
    sigma: float = 1.0,
) -> tuple[np.ndarray, np.ndarray]:
    smoothed = gaussian_filter(image.astype(np.float32), sigma=sigma)
    grad_x = sobel(smoothed, axis=1)
    grad_y = sobel(smoothed, axis=0)
    return grad_x, grad_y


def gradient_to_slope(
    grad_x: np.ndarray,
    grad_y: np.ndarray,
    eps: float = 1e-6,
) -> np.ndarray:
    safe_x = np.where(np.abs(grad_x) < eps, np.sign(grad_x) * eps, grad_x)
    safe_x = np.where(safe_x == 0, eps, safe_x)
    return (grad_y / safe_x).astype(np.float32)
