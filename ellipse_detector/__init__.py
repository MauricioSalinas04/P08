from __future__ import annotations

from dataclasses import dataclass, field

__all__ = ["EdgePoint", "EllipseCandidate", "Ellipse"]


@dataclass(frozen=True, slots=True)
class EdgePoint:
    x: float
    y: float
    slope: float


@dataclass
class EllipseCandidate:
    center_x: float
    center_y: float
    B: float
    D: float
    C: float


@dataclass
class Ellipse:
    center_x: float
    center_y: float
    semi_major: float
    semi_minor: float
    angle_rad: float
    votes: int
