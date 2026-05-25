from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from ellipse_detector import EdgePoint, Ellipse
from ellipse_detector.hough.stage1_center import (
    AHT_MAX_ITERATIONS,
    CENTER_VOTE_THRESHOLD,
    MAX_POINTS_FOR_PAIRS,
    find_centers,
)
from ellipse_detector.hough.stage2_aht import (
    _INIT_B_RANGE,
    _INIT_D_RANGE,
    run_aht,
)
from ellipse_detector.postprocessing.ellipse_params import bdc_to_axes
from ellipse_detector.preprocessing.edge_detector import detect_edges, edges_to_points


@dataclass
class DetectorConfig:
    # Pairing constraint — None = auto-scaled adaptively based on edge density
    delta_x: float | None = None
    delta_y: float | None = None
    center_threshold: int = CENTER_VOTE_THRESHOLD
    aht_max_iterations: int = AHT_MAX_ITERATIONS
    canny_low: float = 20.0
    canny_high: float = 60.0
    aht_init_b_range: tuple[float, float] = field(default_factory=lambda: _INIT_B_RANGE)
    aht_init_d_range: tuple[float, float] = field(default_factory=lambda: _INIT_D_RANGE)
    aht_init_c_range: tuple[float, float] | None = None  # None → auto-detected from points
    # Point deletion: geometric tolerance in pixels (None = 4% of min(H,W))
    point_deletion_tolerance: float | None = None
    # Minimum pixel distance between distinct ellipse centres
    min_center_distance: float | None = None
    # Quality filters
    min_axis_ratio: float = 0.20       # b/a must exceed this (rejects near-degenerate ellipses)
    min_votes_fraction: float = 0.05   # votes / best_votes — rejects weak detections
    max_ellipses: int = 10
    # Max edge points before subsampling in Stage 1 pairing
    max_edge_points: int = 4000
    # Radius around each center candidate for AHT point selection (None = auto)
    aht_radius: float | None = None
    # Adaptive Canny: max fraction of image pixels that can be edges before
    # thresholds are automatically raised
    max_edge_fraction: float = 0.10


def detect_ellipses(
    image: np.ndarray,
    config: DetectorConfig | None = None,
) -> list[Ellipse]:
    if config is None:
        config = DetectorConfig()

    H, W = image.shape[:2]
    n_pixels = H * W
    deletion_tol = (
        config.point_deletion_tolerance
        if config.point_deletion_tolerance is not None
        else 0.04 * min(H, W)
    )
    min_center_dist = (
        config.min_center_distance
        if config.min_center_distance is not None
        else 0.15 * min(H, W)
    )

    # --- Adaptive Canny: raise thresholds if edge map is too dense ----------
    canny_low = config.canny_low
    canny_high = config.canny_high
    max_edge_px = int(n_pixels * config.max_edge_fraction)

    edge_mask, grad_x, grad_y = detect_edges(
        image, low_threshold=canny_low, high_threshold=canny_high,
    )
    n_edge = int(np.count_nonzero(edge_mask))

    while n_edge > max_edge_px and canny_high < 500:
        canny_low *= 1.15
        canny_high *= 1.15
        edge_mask, grad_x, grad_y = detect_edges(
            image, low_threshold=canny_low, high_threshold=canny_high,
        )
        n_edge = int(np.count_nonzero(edge_mask))

    points = edges_to_points(edge_mask, grad_x, grad_y)

    # --- Adaptive delta: scale based on edge density -----------------------
    if config.delta_x is not None:
        delta_x = config.delta_x
    else:
        base_delta = 0.20 * max(H, W)
        edge_density = n_edge / n_pixels
        if edge_density > 0.02:
            # sqrt scaling: less aggressive than linear for dense images
            scale = min(1.0, math.sqrt(0.02 / edge_density))
            delta_x = max(15.0, base_delta * scale)
        else:
            delta_x = base_delta
    if config.delta_y is not None:
        delta_y = config.delta_y
    else:
        delta_y = delta_x  # symmetric by default

    ellipses: list[Ellipse] = []

    aht_radius = (
        config.aht_radius if config.aht_radius is not None else 0.3 * min(H, W)
    )

    best_votes: int = 0

    for _ in range(config.max_ellipses):
        if not points:
            break

        centers = find_centers(
            points,
            image_shape=(H, W),
            delta_x=delta_x,
            delta_y=delta_y,
            threshold=config.center_threshold,
            min_peak_distance=5,
            max_points=config.max_edge_points,
        )
        if not centers:
            break

        ellipse = _fit_best_ellipse(
            centers, points, ellipses, min_center_dist, config, max(H, W), aht_radius
        )
        if ellipse is None:
            break

        if best_votes == 0:
            best_votes = ellipse.votes

        # Reject weak detections relative to the first (strongest) ellipse
        if ellipse.votes < config.min_votes_fraction * best_votes:
            break

        ellipses.append(ellipse)
        points = _delete_ellipse_points(points, ellipse, deletion_tol)

    return ellipses


def _fit_best_ellipse(
    centers: list[tuple[float, float, int]],
    points: list[EdgePoint],
    existing: list[Ellipse],
    min_dist: float,
    config: DetectorConfig,
    max_image_dim: float,
    aht_radius: float,
) -> Ellipse | None:
    """Try centres in vote-order; return first that produces a valid ellipse.

    Points near each candidate centre are grouped into radial rings so that
    concentric ellipses are fitted individually rather than blended together.
    """
    pts_arr = np.array([[p.x, p.y] for p in points], dtype=np.float64) if points else None

    for cx, cy, votes in centers:
        if pts_arr is None:
            continue

        dists = np.hypot(pts_arr[:, 0] - cx, pts_arr[:, 1] - cy)
        nearby_mask = dists <= aht_radius
        nearby_dists = dists[nearby_mask]
        nearby_pts = [p for p, m in zip(points, nearby_mask) if m]

        if len(nearby_pts) < 5:
            continue

        # --- Ring-based segmentation: group points by distance to center ---
        ring_width = max(8.0, 0.04 * min(max_image_dim, aht_radius * 2))
        max_dist_val = float(np.max(nearby_dists)) if len(nearby_dists) > 0 else 0
        n_rings = max(1, int(np.ceil(max_dist_val / ring_width)))

        rings: list[tuple[list[EdgePoint], float, int]] = []
        for r_idx in range(n_rings):
            r_lo = r_idx * ring_width
            r_hi = r_lo + ring_width
            ring_mask = (nearby_dists >= r_lo) & (nearby_dists < r_hi)
            ring_pts = [p for p, m in zip(nearby_pts, ring_mask) if m]
            if len(ring_pts) >= 5:
                mean_d = float(np.mean(nearby_dists[ring_mask]))
                rings.append((ring_pts, mean_d, len(ring_pts)))

        if not rings:
            rings = [(nearby_pts, float(np.mean(nearby_dists)), len(nearby_pts))]

        # Try rings from most populated to least
        rings.sort(key=lambda t: t[2], reverse=True)

        for ring_pts, _mean_d, _count in rings:
            result = run_aht(
                center=(cx, cy),
                points=ring_pts,
                max_iterations=config.aht_max_iterations,
                init_b_range=config.aht_init_b_range,
                init_d_range=config.aht_init_d_range,
                init_c_range=config.aht_init_c_range,
            )
            if result is None:
                continue
            B, D, C = result
            try:
                semi_major, semi_minor, angle_rad = bdc_to_axes(B, D, C)
            except ValueError:
                continue
            axis_ratio = semi_minor / semi_major if semi_major > 0 else 0
            if semi_major > max_image_dim or semi_minor < 2.0:
                continue
            if axis_ratio < config.min_axis_ratio:
                continue

            # Check for duplicate: skip only if both center AND size are similar
            is_duplicate = False
            for e in existing:
                dist_centers = math.hypot(cx - e.center_x, cy - e.center_y)
                if dist_centers < min_dist:
                    size_ratio = semi_major / e.semi_major if e.semi_major > 0 else 0
                    if 0.8 < size_ratio < 1.2:
                        is_duplicate = True
                        break
            if is_duplicate:
                continue

            return Ellipse(
                center_x=cx, center_y=cy,
                semi_major=semi_major, semi_minor=semi_minor,
                angle_rad=angle_rad, votes=votes,
            )
    return None


def _delete_ellipse_points(
    points: list[EdgePoint],
    ellipse: Ellipse,
    tolerance_px: float,
) -> list[EdgePoint]:
    if not points:
        return []
    pts = np.array([[p.x, p.y] for p in points], dtype=np.float64)
    distances = _ellipse_geometric_distance(pts, ellipse)
    keep = distances > tolerance_px
    return [p for p, k in zip(points, keep) if k]


def _ellipse_geometric_distance(pts: np.ndarray, ellipse: Ellipse) -> np.ndarray:
    """Approximate geometric distance from each point to the nearest ellipse boundary."""
    X = pts[:, 0] - ellipse.center_x
    Y = pts[:, 1] - ellipse.center_y
    cos_t = math.cos(ellipse.angle_rad)
    sin_t = math.sin(ellipse.angle_rad)
    u = X * cos_t + Y * sin_t
    v = -X * sin_t + Y * cos_t
    a, b = ellipse.semi_major, ellipse.semi_minor
    phi = np.arctan2(v / b, u / a)
    u_near = a * np.cos(phi)
    v_near = b * np.sin(phi)
    return np.sqrt((u - u_near) ** 2 + (v - v_near) ** 2)

