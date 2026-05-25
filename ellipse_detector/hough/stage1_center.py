from __future__ import annotations

import warnings
from typing import Final

import numpy as np

from ellipse_detector import EdgePoint
from ellipse_detector.hough.accumulator import Accumulator2D
from ellipse_detector.postprocessing.peak_detector import find_peaks_2d

AHT_ACCUMULATOR_SIZE: Final[int] = 9
AHT_MAX_ITERATIONS: Final[int] = 10
AHT_RANGE_REDUCTION: Final[float] = 1 / 3
DEFAULT_DELTA_X: Final[int] = 30
DEFAULT_DELTA_Y: Final[int] = 30
CENTER_VOTE_THRESHOLD: Final[int] = 5
PARALLEL_SLOPE_EPS: Final[float] = 0.01
MAX_POINTS_FOR_PAIRS: Final[int] = 2000


def generate_pairs(
    points: np.ndarray,
    delta_x: float = DEFAULT_DELTA_X,
    delta_y: float = DEFAULT_DELTA_Y,
) -> tuple[np.ndarray, np.ndarray]:
    N = len(points)
    if N == 0:
        return np.array([], dtype=int), np.array([], dtype=int)
    i, j = np.triu_indices(N, k=1)
    dx = np.abs(points[i, 0] - points[j, 0])
    dy = np.abs(points[i, 1] - points[j, 1])
    mask = (dx < delta_x) & (dy < delta_y)
    return i[mask], j[mask]


def compute_tm_vectors(
    points: np.ndarray,
    idx_p: np.ndarray,
    idx_q: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    if len(idx_p) == 0:
        return np.empty((0, 2)), np.empty((0, 2))

    x1 = points[idx_p, 0]
    y1 = points[idx_p, 1]
    s1 = points[idx_p, 2]
    x2 = points[idx_q, 0]
    y2 = points[idx_q, 1]
    s2 = points[idx_q, 2]

    ds = s2 - s1
    parallel = np.abs(ds) < PARALLEL_SLOPE_EPS
    ds_safe = np.where(parallel, 1.0, ds)

    t1 = (y1 - y2 - s1 * x1 + s2 * x2) / ds_safe
    t2 = s1 * (t1 - x1) + y1
    m1 = (x1 + x2) / 2.0
    m2 = (y1 + y2) / 2.0

    T = np.column_stack([t1, t2])
    M = np.column_stack([m1, m2])
    T[parallel] = np.nan
    return T, M


def vote_centers(
    t_coords: np.ndarray,
    m_coords: np.ndarray,
    accumulator: Accumulator2D,
    segment_length: float,
) -> None:
    if len(t_coords) == 0:
        return
    valid = ~np.isnan(t_coords[:, 0])
    in_bounds = (
        (t_coords[:, 0] >= 0)
        & (t_coords[:, 0] < accumulator.width)
        & (t_coords[:, 1] >= 0)
        & (t_coords[:, 1] < accumulator.height)
    )
    mask = valid & in_bounds
    for idx in np.where(mask)[0]:
        t = (float(t_coords[idx, 0]), float(t_coords[idx, 1]))
        m = (float(m_coords[idx, 0]), float(m_coords[idx, 1]))
        accumulator.vote_segment(m, t, segment_length)


def find_centers(
    points: list[EdgePoint],
    image_shape: tuple[int, int],
    delta_x: float = DEFAULT_DELTA_X,
    delta_y: float = DEFAULT_DELTA_Y,
    segment_length: float | None = None,
    threshold: int = CENTER_VOTE_THRESHOLD,
    min_peak_distance: int = 5,
    max_points: int = MAX_POINTS_FOR_PAIRS,
) -> list[tuple[float, float, int]]:
    if not points:
        return []

    H, W = image_shape
    if segment_length is None:
        segment_length = 0.3 * min(H, W)

    if len(points) > max_points:
        warnings.warn(
            f"Edge points ({len(points)}) exceed {max_points}; "
            "subsampling to avoid memory issues.",
            RuntimeWarning,
            stacklevel=2,
        )
        rng = np.random.default_rng(0)
        indices = rng.choice(len(points), max_points, replace=False)
        points = [points[i] for i in sorted(indices)]

    pts = np.array([[p.x, p.y, p.slope] for p in points], dtype=np.float64)
    idx_p, idx_q = generate_pairs(pts, delta_x, delta_y)
    T, M = compute_tm_vectors(pts, idx_p, idx_q)

    accumulator = Accumulator2D(width=W, height=H)
    vote_centers(T, M, accumulator, segment_length)

    peaks = find_peaks_2d(accumulator.get_data(), min_votes=threshold, min_distance=min_peak_distance)
    return [(float(col), float(row), votes) for row, col, votes in peaks]
