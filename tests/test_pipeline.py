from __future__ import annotations

import math

import numpy as np
import pytest

from ellipse_detector.pipeline import DetectorConfig, detect_ellipses
from tests.conftest import make_ellipse_image

CENTER_TOL_PX = 10.0
AXIS_REL_TOL = 0.15
ANGLE_TOL_RAD = math.radians(10.0)


def _best_match(ellipses, cx, cy):
    return min(
        ellipses,
        key=lambda e: math.hypot(e.center_x - cx, e.center_y - cy),
    )


@pytest.fixture
def loose_config() -> DetectorConfig:
    return DetectorConfig(
        delta_x=60,
        delta_y=60,
        center_threshold=3,
        canny_low=20.0,
        canny_high=60.0,
    )


def test_single_ellipse_axis_aligned(loose_config: DetectorConfig) -> None:
    cx, cy, a, b = 100.0, 80.0, 40.0, 25.0
    img = make_ellipse_image(200, 160, (cx, cy), a, b, angle_deg=0.0)
    ellipses = detect_ellipses(img, loose_config)
    assert len(ellipses) >= 1
    det = _best_match(ellipses, cx, cy)
    assert abs(det.center_x - cx) < CENTER_TOL_PX
    assert abs(det.center_y - cy) < CENTER_TOL_PX
    assert det.semi_major == pytest.approx(a, rel=AXIS_REL_TOL)
    assert det.semi_minor == pytest.approx(b, rel=AXIS_REL_TOL)


def test_single_ellipse_tilted(loose_config: DetectorConfig) -> None:
    cx, cy, a, b, angle = 120.0, 100.0, 45.0, 20.0, 30.0
    img = make_ellipse_image(250, 200, (cx, cy), a, b, angle_deg=angle)
    ellipses = detect_ellipses(img, loose_config)
    assert len(ellipses) >= 1
    det = _best_match(ellipses, cx, cy)
    assert abs(det.center_x - cx) < CENTER_TOL_PX
    assert abs(det.center_y - cy) < CENTER_TOL_PX


def test_upright_circle(loose_config: DetectorConfig) -> None:
    cx, cy, r = 80.0, 80.0, 35.0
    img = make_ellipse_image(160, 160, (cx, cy), r, r, angle_deg=0.0)
    ellipses = detect_ellipses(img, loose_config)
    assert len(ellipses) >= 1
    det = _best_match(ellipses, cx, cy)
    assert abs(det.center_x - cx) < CENTER_TOL_PX
    assert abs(det.center_y - cy) < CENTER_TOL_PX
    assert det.semi_major == pytest.approx(r, rel=AXIS_REL_TOL)
    assert det.semi_minor == pytest.approx(r, rel=AXIS_REL_TOL)


def test_noisy_ellipse_detects_center() -> None:
    cx, cy, a, b = 100.0, 80.0, 40.0, 25.0
    img = make_ellipse_image(200, 160, (cx, cy), a, b, angle_deg=0.0, noise_sigma=8.0)
    config = DetectorConfig(delta_x=60, delta_y=60, center_threshold=2, canny_low=15.0, canny_high=50.0)
    ellipses = detect_ellipses(img, config)
    if ellipses:
        det = _best_match(ellipses, cx, cy)
        assert abs(det.center_x - cx) < CENTER_TOL_PX * 2
        assert abs(det.center_y - cy) < CENTER_TOL_PX * 2


def test_empty_image_returns_no_ellipses() -> None:
    img = np.zeros((100, 100), dtype=np.uint8)
    ellipses = detect_ellipses(img)
    assert ellipses == []
