from __future__ import annotations

import math

import pytest

from ellipse_detector.postprocessing.ellipse_params import bdc_to_axes, is_valid_ellipse


def test_circle() -> None:
    r = 30.0
    B, D, C = 1.0, 0.0, -(r * r)
    a, b, theta = bdc_to_axes(B, D, C)
    assert a == pytest.approx(r, rel=1e-6)
    assert b == pytest.approx(r, rel=1e-6)
    assert theta == pytest.approx(0.0, abs=1e-6)


def test_axis_aligned_horizontal() -> None:
    # X²/a² + Y²/b² = 1  →  X² + (a/b)²·Y² + (-a²) = 0
    a_true, b_true = 50.0, 20.0
    B = (a_true / b_true) ** 2
    D = 0.0
    C = -(a_true ** 2)
    a, b, theta = bdc_to_axes(B, D, C)
    assert a == pytest.approx(a_true, rel=1e-4)
    assert b == pytest.approx(b_true, rel=1e-4)
    assert abs(theta) == pytest.approx(0.0, abs=1e-4)


def test_invalid_hyperbola_raises() -> None:
    # B - D² ≤ 0 → invalid
    with pytest.raises(ValueError, match="Invalid ellipse"):
        bdc_to_axes(B=1.0, D=2.0, C=-100.0)


def test_positive_C_raises() -> None:
    with pytest.raises(ValueError, match="Invalid ellipse"):
        bdc_to_axes(B=2.0, D=0.5, C=50.0)


def test_canonical_angle_in_range() -> None:
    B, D, C = 2.0, 0.8, -500.0
    _, _, theta = bdc_to_axes(B, D, C)
    assert -math.pi / 2.0 < theta <= math.pi / 2.0


def test_semi_major_ge_minor() -> None:
    for B, D, C in [
        (3.0, 0.5, -200.0),
        (1.5, -0.3, -1000.0),
        (4.0, 1.0, -5000.0),
    ]:
        if is_valid_ellipse(B, D, C):
            a, b, _ = bdc_to_axes(B, D, C)
            assert a >= b, f"a={a} < b={b} for B={B}, D={D}, C={C}"


def test_is_valid_ellipse() -> None:
    assert is_valid_ellipse(2.0, 0.5, -100.0) is True
    assert is_valid_ellipse(1.0, 2.0, -100.0) is False  # B - D² = -3 < 0
    assert is_valid_ellipse(2.0, 0.5, 10.0) is False    # C > 0
