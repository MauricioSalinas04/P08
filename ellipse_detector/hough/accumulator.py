from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Accumulator2D:
    width: int
    height: int
    _data: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._data = np.zeros((self.height, self.width), dtype=np.int32)

    def vote_segment(
        self,
        m: tuple[float, float],
        t: tuple[float, float],
        segment_length: float,
    ) -> None:
        mx, my = m
        tx, ty = t
        direction = np.array([tx - mx, ty - my], dtype=np.float64)
        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            return
        direction /= norm
        n_steps = max(int(segment_length), 1)
        ts = np.linspace(0.0, segment_length, n_steps)
        xs = np.round(mx + ts * direction[0]).astype(int)
        ys = np.round(my + ts * direction[1]).astype(int)
        valid = (xs >= 0) & (xs < self.width) & (ys >= 0) & (ys < self.height)
        np.add.at(self._data, (ys[valid], xs[valid]), 1)

    def get_data(self) -> np.ndarray:
        return self._data

    def reset(self) -> None:
        self._data[:] = 0


@dataclass
class Accumulator3D:
    size: int = 9
    b_range: tuple[float, float] = (0.1, 10.0)
    d_range: tuple[float, float] = (-5.0, 5.0)
    c_range: tuple[float, float] = (-1e6, -1.0)
    _data: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._data = np.zeros((self.size, self.size, self.size), dtype=np.int32)

    def bin_centers(self, axis: int) -> np.ndarray:
        ranges = [self.b_range, self.d_range, self.c_range]
        lo, hi = ranges[axis]
        edges = np.linspace(lo, hi, self.size + 1)
        return (edges[:-1] + edges[1:]) / 2.0

    def _bin_width(self, axis: int) -> float:
        ranges = [self.b_range, self.d_range, self.c_range]
        lo, hi = ranges[axis]
        return (hi - lo) / self.size

    def recenter(self, peak_b: float, peak_d: float, peak_c: float) -> None:
        def new_range(center: float, old_range: tuple[float, float]) -> tuple[float, float]:
            width = (old_range[1] - old_range[0]) / 3.0
            return (center - width / 2.0, center + width / 2.0)

        self.b_range = new_range(peak_b, self.b_range)
        self.d_range = new_range(peak_d, self.d_range)
        self.c_range = new_range(peak_c, self.c_range)
        self._data[:] = 0

    def peak(self) -> tuple[float, float, float, int]:
        idx = np.unravel_index(np.argmax(self._data), self._data.shape)
        ib, id_, ic = int(idx[0]), int(idx[1]), int(idx[2])
        votes = int(self._data[ib, id_, ic])
        b_centers = self.bin_centers(0)
        d_centers = self.bin_centers(1)
        c_centers = self.bin_centers(2)
        return float(b_centers[ib]), float(d_centers[id_]), float(c_centers[ic]), votes

    def reset(self) -> None:
        self._data[:] = 0
