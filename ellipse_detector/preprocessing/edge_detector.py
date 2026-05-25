from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter, sobel, binary_dilation

from ellipse_detector import EdgePoint
from ellipse_detector.preprocessing.gradient import compute_gradients, gradient_to_slope


def detect_edges(
    image: np.ndarray,
    low_threshold: float = 50.0,
    high_threshold: float = 150.0,
    sigma: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gray = _to_grayscale(image)
    grad_x, grad_y = compute_gradients(gray, sigma=sigma)
    magnitude = np.hypot(grad_x, grad_y)
    suppressed = _non_maximum_suppression(magnitude, grad_x, grad_y)
    edge_mask = _hysteresis_threshold(suppressed, low_threshold, high_threshold)
    return edge_mask, grad_x, grad_y


def edges_to_points(
    edge_mask: np.ndarray,
    grad_x: np.ndarray,
    grad_y: np.ndarray,
) -> list[EdgePoint]:
    coords = np.argwhere(edge_mask)
    if len(coords) == 0:
        return []
    ys, xs = coords[:, 0], coords[:, 1]
    slopes = gradient_to_slope(grad_x[ys, xs], grad_y[ys, xs])
    return [
        EdgePoint(x=float(x), y=float(y), slope=float(s))
        for x, y, s in zip(xs, ys, slopes)
    ]


def _to_grayscale(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image.astype(np.float32)
    if image.ndim == 3:
        weights = np.array([0.2989, 0.5870, 0.1140], dtype=np.float32)
        return (image[:, :, :3].astype(np.float32) @ weights)
    raise ValueError(f"Unsupported image shape: {image.shape}")


def _non_maximum_suppression(
    magnitude: np.ndarray,
    grad_x: np.ndarray,
    grad_y: np.ndarray,
) -> np.ndarray:
    H, W = magnitude.shape
    suppressed = np.zeros_like(magnitude)
    angle = np.arctan2(grad_y, grad_x) * 180.0 / np.pi
    angle = angle % 180.0

    for y in range(1, H - 1):
        for x in range(1, W - 1):
            a = angle[y, x]
            mag = magnitude[y, x]
            if (0 <= a < 22.5) or (157.5 <= a <= 180):
                n1, n2 = magnitude[y, x - 1], magnitude[y, x + 1]
            elif 22.5 <= a < 67.5:
                n1, n2 = magnitude[y - 1, x + 1], magnitude[y + 1, x - 1]
            elif 67.5 <= a < 112.5:
                n1, n2 = magnitude[y - 1, x], magnitude[y + 1, x]
            else:
                n1, n2 = magnitude[y - 1, x - 1], magnitude[y + 1, x + 1]
            if mag >= n1 and mag >= n2:
                suppressed[y, x] = mag
    return suppressed


def _hysteresis_threshold(
    magnitude: np.ndarray,
    low: float,
    high: float,
) -> np.ndarray:
    strong = magnitude >= high
    weak = (magnitude >= low) & ~strong
    visited = strong.copy()
    structure = np.ones((3, 3), dtype=bool)
    prev = np.zeros_like(visited)
    while not np.array_equal(visited, prev):
        prev = visited.copy()
        dilated = binary_dilation(visited, structure=structure)
        visited = visited | (weak & dilated)
    return visited
