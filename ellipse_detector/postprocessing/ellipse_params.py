from __future__ import annotations

import math


def is_valid_ellipse(B: float, D: float, C: float) -> bool:
    return (B - D * D) > 0 and C < 0


def bdc_to_axes(B: float, D: float, C: float) -> tuple[float, float, float]:
    if not is_valid_ellipse(B, D, C):
        raise ValueError(
            f"Invalid ellipse parameters: B={B}, D={D}, C={C} "
            f"(require B-D²>0 and C<0)"
        )
    discriminant = math.sqrt((B - 1.0) ** 2 + 4.0 * D * D)
    denom_major = (B + 1.0) - discriminant
    denom_minor = (B + 1.0) + discriminant

    if denom_major <= 0 or denom_minor <= 0:
        raise ValueError(
            f"Degenerate ellipse: denominators non-positive "
            f"(denom_major={denom_major}, denom_minor={denom_minor})"
        )

    a_raw = math.sqrt(-2.0 * C / denom_major)
    b_raw = math.sqrt(-2.0 * C / denom_minor)

    # Paper formula: theta = 0.5 * arctan(2D / (1-B))
    # arctan (not arctan2) so theta_raw ∈ (-π/4, π/4); swap logic covers the rest
    one_minus_B = 1.0 - B
    if abs(one_minus_B) < 1e-10:
        # B ≈ 1: handle limit (only reached when D ≠ 0)
        theta = math.pi / 4.0 * (math.copysign(1.0, D) if abs(D) > 1e-10 else 0.0)
    else:
        theta = 0.5 * math.atan(2.0 * D / one_minus_B)

    if b_raw > a_raw:
        a_raw, b_raw = b_raw, a_raw
        theta += math.pi / 2.0

    # Normalize theta to (-pi/2, pi/2]
    while theta > math.pi / 2.0:
        theta -= math.pi
    while theta <= -math.pi / 2.0:
        theta += math.pi

    return a_raw, b_raw, theta
