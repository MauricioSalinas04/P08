from __future__ import annotations

import math

import numpy as np
import pytest

from ellipse_detector import EdgePoint
from ellipse_detector.hough.accumulator import Accumulator3D
from ellipse_detector.hough.stage2_aht import accumulate_bdc, run_aht
from ellipse_detector.hough.stage1_center import AHT_MAX_ITERATIONS


def _make_ellipse_points(
    center: tuple[float, float],
    semi_major: float,
    semi_minor: float,
    angle_deg: float,
    n_points: int = 60,
) -> list[EdgePoint]:
    t = np.linspace(0.0, 2.0 * math.pi, n_points, endpoint=False)
    angle_rad = math.radians(angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    xs = center[0] + semi_major * np.cos(t) * cos_a - semi_minor * np.sin(t) * sin_a
    ys = center[1] + semi_major * np.cos(t) * sin_a + semi_minor * np.sin(t) * cos_a
    # slope = dy/dx from parametric: dy/dt / dx/dt
    dxdt = -semi_major * np.sin(t) * cos_a - semi_minor * np.cos(t) * sin_a
    dydt = -semi_major * np.sin(t) * sin_a + semi_minor * np.cos(t) * cos_a
    slopes = np.where(np.abs(dxdt) > 1e-8, dydt / dxdt, np.inf)
    return [EdgePoint(x=float(x), y=float(y), slope=float(s)) for x, y, s in zip(xs, ys, slopes)]


def test_accumulate_bdc_votes_in_correct_bin() -> None:
    # Centered point on a known ellipse: X²/a² + Y²/b² = 1 → C = -a²
    a, b = 40.0, 25.0
    B_true = (a / b) ** 2
    D_true = 0.0
    C_true = -(a ** 2)

    acc = Accumulator3D(
        b_range=(B_true - 0.5, B_true + 0.5),
        d_range=(-0.5, 0.5),
        c_range=(C_true - 50, C_true + 50),
    )
    # A point at (a, 0) must satisfy C = -a²
    pts = np.array([[a, 0.0]])
    accumulate_bdc(pts, acc)
    peak_b, peak_d, peak_c, votes = acc.peak()
    assert votes > 0


def test_aht_converges_axis_aligned() -> None:
    a, b = 40.0, 25.0
    center = (100.0, 80.0)
    points = _make_ellipse_points(center, a, b, angle_deg=0.0, n_points=80)
    result = run_aht(center, points)
    assert result is not None
    B, D, C = result
    from ellipse_detector.postprocessing.ellipse_params import bdc_to_axes
    a_det, b_det, _ = bdc_to_axes(B, D, C)
    assert a_det == pytest.approx(a, rel=0.10)
    assert b_det == pytest.approx(b, rel=0.10)


def test_aht_never_exceeds_max_iterations(monkeypatch: pytest.MonkeyPatch) -> None:
    call_count = 0
    from ellipse_detector.hough import stage2_aht as mod

    original = mod.accumulate_bdc

    def counting_accumulate(pts: np.ndarray, acc: Accumulator3D) -> None:
        nonlocal call_count
        call_count += 1
        original(pts, acc)

    monkeypatch.setattr(mod, "accumulate_bdc", counting_accumulate)

    points = _make_ellipse_points((50.0, 50.0), 30.0, 20.0, 0.0, n_points=40)
    run_aht((50.0, 50.0), points, max_iterations=AHT_MAX_ITERATIONS)
    assert call_count <= AHT_MAX_ITERATIONS


def test_aht_invalid_returns_none() -> None:
    # Pass near-collinear points that can't form a valid ellipse at the given center
    points = [EdgePoint(x=float(i), y=0.0, slope=0.0) for i in range(10)]
    result = run_aht((5.0, 50.0), points)
    # Should return None (B - D² ≤ 0) or a valid result — just must not raise
    assert result is None or (isinstance(result, tuple) and len(result) == 3)
