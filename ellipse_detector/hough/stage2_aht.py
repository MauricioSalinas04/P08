from __future__ import annotations

from typing import Final

import numpy as np

from ellipse_detector import EdgePoint
from ellipse_detector.hough.accumulator import Accumulator3D
from ellipse_detector.hough.stage1_center import AHT_MAX_ITERATIONS
from ellipse_detector.postprocessing.ellipse_params import is_valid_ellipse

_INIT_B_RANGE: Final[tuple[float, float]] = (0.1, 10.0)
_INIT_D_RANGE: Final[tuple[float, float]] = (-5.0, 5.0)


def accumulate_bdc(
    translated_points: np.ndarray,
    accumulator: Accumulator3D,
) -> None:
    if len(translated_points) == 0:
        return

    X = translated_points[:, 0]
    Y = translated_points[:, 1]

    B_centers = accumulator.bin_centers(0)
    D_centers = accumulator.bin_centers(1)
    B_grid, D_grid = np.meshgrid(B_centers, D_centers, indexing="ij")

    # C = -(X² + B·Y² + 2·D·X·Y) for each point and each (B, D) cell
    C_vals = -(
        X[:, None, None] ** 2
        + B_grid[None, :, :] * Y[:, None, None] ** 2
        + 2.0 * D_grid[None, :, :] * X[:, None, None] * Y[:, None, None]
    )  # shape (K, 9, 9)

    c_lo, c_hi = accumulator.c_range
    c_width = (c_hi - c_lo) / accumulator.size
    if abs(c_width) < 1e-30:
        return

    c_bin = np.floor((C_vals - c_lo) / c_width).astype(np.int32)
    b_idx = np.broadcast_to(
        np.arange(accumulator.size)[None, :, None],
        C_vals.shape,
    )
    d_idx = np.broadcast_to(
        np.arange(accumulator.size)[None, None, :],
        C_vals.shape,
    )

    valid = (c_bin >= 0) & (c_bin < accumulator.size)
    np.add.at(
        accumulator._data,
        (b_idx[valid], d_idx[valid], c_bin[valid]),
        1,
    )


def run_aht(
    center: tuple[float, float],
    points: list[EdgePoint],
    max_iterations: int = AHT_MAX_ITERATIONS,
    init_b_range: tuple[float, float] = _INIT_B_RANGE,
    init_d_range: tuple[float, float] = _INIT_D_RANGE,
    init_c_range: tuple[float, float] | None = None,
) -> tuple[float, float, float] | None:
    if not points:
        return None

    cx, cy = center
    translated = np.array(
        [[p.x - cx, p.y - cy] for p in points], dtype=np.float64
    )

    if init_c_range is None:
        # Estimate C range from point extents: C ≈ -a² where a is the semi-major axis.
        # The furthest point from the center gives an upper bound on a.
        max_sq = float(np.max(translated[:, 0] ** 2 + translated[:, 1] ** 2))
        max_sq = max(max_sq, 1.0)
        effective_c_range: tuple[float, float] = (-max_sq * 2.5, -max_sq * 0.01)
    else:
        effective_c_range = init_c_range

    acc = Accumulator3D(
        b_range=init_b_range,
        d_range=init_d_range,
        c_range=effective_c_range,
    )

    for _ in range(max_iterations):
        acc.reset()
        accumulate_bdc(translated, acc)
        peak_b, peak_d, peak_c, _votes = acc.peak()
        acc.recenter(peak_b, peak_d, peak_c)

    if not is_valid_ellipse(peak_b, peak_d, peak_c):
        return None

    return peak_b, peak_d, peak_c
