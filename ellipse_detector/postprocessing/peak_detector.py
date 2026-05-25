from __future__ import annotations

import numpy as np
from scipy.ndimage import maximum_filter


def find_peaks_2d(
    accumulator: np.ndarray,
    min_votes: int,
    min_distance: int = 5,
) -> list[tuple[int, int, int]]:
    neighborhood = maximum_filter(accumulator, size=2 * min_distance + 1)
    is_peak = (accumulator == neighborhood) & (accumulator >= min_votes)
    coords = np.argwhere(is_peak)
    if len(coords) == 0:
        return []
    votes = accumulator[coords[:, 0], coords[:, 1]]
    order = np.argsort(-votes)
    return [
        (int(coords[i, 0]), int(coords[i, 1]), int(votes[i]))
        for i in order
    ]
