from __future__ import annotations

import math

import numpy as np
import pytest

from ellipse_detector import EdgePoint
from ellipse_detector.hough.stage1_center import (
    DEFAULT_DELTA_X,
    DEFAULT_DELTA_Y,
    PARALLEL_SLOPE_EPS,
    compute_tm_vectors,
    find_centers,
    generate_pairs,
)
from tests.conftest import make_ellipse_image
from ellipse_detector.preprocessing.edge_detector import detect_edges, edges_to_points


def test_parallel_pair_excluded_from_tm() -> None:
    pts = np.array([
        [0.0, 0.0, 1.0],
        [10.0, 10.0, 1.0 + PARALLEL_SLOPE_EPS * 0.5],
    ])
    idx_p, idx_q = generate_pairs(pts, delta_x=50, delta_y=50)
    T, M = compute_tm_vectors(pts, idx_p, idx_q)
    assert np.all(np.isnan(T))


def test_non_parallel_pair_produces_valid_T() -> None:
    pts = np.array([
        [0.0, 0.0, 0.0],
        [10.0, 0.0, 1.0],
    ])
    idx_p, idx_q = generate_pairs(pts, delta_x=50, delta_y=50)
    assert len(idx_p) == 1
    T, M = compute_tm_vectors(pts, idx_p, idx_q)
    assert not np.any(np.isnan(T))


def test_pair_constraint_excludes_distant_points() -> None:
    pts = np.array([
        [0.0, 0.0, 0.5],
        [DEFAULT_DELTA_X + 1, 0.0, 1.5],
    ])
    idx_p, idx_q = generate_pairs(pts, delta_x=DEFAULT_DELTA_X, delta_y=DEFAULT_DELTA_Y)
    assert len(idx_p) == 0


def test_tm_formula_known_values() -> None:
    # Tangents at (a, 0) and (0, b) of circle radius r: s1=0, s2=undefined
    # Use axis-aligned pair with known geometry
    # P=(10, 0) slope=0, Q=(0, 10) slope=inf — skip (inf slope problematic)
    # Use P=(5, 0) slope=0, Q=(0, 5) slope=-1
    # Tangent at P: y = 0 (horizontal). Tangent at Q: y = -x + 5.
    # Intersection T: 0 = -x + 5 → x=5, y=0 → T=(5, 0) — same as P
    # Use a less degenerate pair: circle r=10, P=(10,0) slope=0, Q=(0,10) slope=-1
    pts = np.array([
        [10.0, 0.0, 0.0],
        [0.0, 10.0, -1.0],
    ])
    idx_p = np.array([0])
    idx_q = np.array([1])
    T, M = compute_tm_vectors(pts, idx_p, idx_q)
    # t1 = (y1-y2 - s1*x1 + s2*x2) / (s2-s1) = (0-10 - 0 + (-1)*0) / (-1-0) = -10/-1 = 10
    # t2 = s1*(t1-x1)+y1 = 0*(10-10)+0 = 0
    assert T[0, 0] == pytest.approx(10.0, abs=1e-6)
    assert T[0, 1] == pytest.approx(0.0, abs=1e-6)
    # m1 = (10+0)/2 = 5, m2 = (0+10)/2 = 5
    assert M[0, 0] == pytest.approx(5.0, abs=1e-6)
    assert M[0, 1] == pytest.approx(5.0, abs=1e-6)


def test_center_found_on_synthetic_circle() -> None:
    cx_true, cy_true = 100, 80
    img = make_ellipse_image(
        width=200, height=160,
        center=(cx_true, cy_true),
        semi_major=40, semi_minor=40,
        angle_deg=0.0,
    )
    edge_mask, gx, gy = detect_edges(img, low_threshold=30, high_threshold=80)
    points = edges_to_points(edge_mask, gx, gy)
    assert len(points) > 0, "No edge points found in synthetic circle image"

    centers = find_centers(
        points,
        image_shape=img.shape,
        delta_x=50,
        delta_y=50,
        threshold=3,
    )
    assert len(centers) > 0, "No centers detected"
    cx_det, cy_det, _ = centers[0]
    assert abs(cx_det - cx_true) < 10.0, f"Center X off: {cx_det} vs {cx_true}"
    assert abs(cy_det - cy_true) < 10.0, f"Center Y off: {cy_det} vs {cy_true}"
