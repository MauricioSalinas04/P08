from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from ellipse_detector.pipeline import DetectorConfig, detect_ellipses
from ellipse_detector.preprocessing.edge_detector import detect_edges
from ellipse_detector.visualization.draw import save_result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ellipse detector — Yuen, Illingworth & Kittler (1988)"
    )
    parser.add_argument("--image", required=True, type=Path, help="Input image path")
    parser.add_argument("--output", type=Path, default=Path("results"), help="Output directory")
    parser.add_argument("--visualize", action="store_true", help="Save annotated panel image")
    parser.add_argument("--delta-x", type=float, default=None,
                        help="Horizontal pairing constraint in px (default: auto)")
    parser.add_argument("--delta-y", type=float, default=None,
                        help="Vertical pairing constraint in px (default: auto)")
    parser.add_argument("--threshold", type=int, default=5, help="Minimum center votes")
    parser.add_argument("--canny-low", type=float, default=20.0, help="Canny low threshold")
    parser.add_argument("--canny-high", type=float, default=60.0, help="Canny high threshold")
    parser.add_argument("--max-ellipses", type=int, default=10, help="Max ellipses to detect")
    parser.add_argument("--max-edge-points", type=int, default=4000,
                        help="Max edge points before subsampling (default: 4000)")
    parser.add_argument("--aht-radius", type=float, default=None,
                        help="AHT point selection radius in px (default: auto)")
    parser.add_argument("--max-edge-fraction", type=float, default=0.10,
                        help="Max fraction of pixels as edges before raising Canny (default: 0.10)")
    args = parser.parse_args()

    if not args.image.exists():
        print(f"Error: image not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    image = np.array(Image.open(args.image))
    config = DetectorConfig(
        delta_x=args.delta_x,
        delta_y=args.delta_y,
        center_threshold=args.threshold,
        canny_low=args.canny_low,
        canny_high=args.canny_high,
        max_ellipses=args.max_ellipses,
        max_edge_points=args.max_edge_points,
        aht_radius=args.aht_radius,
        max_edge_fraction=args.max_edge_fraction,
    )

    print(f"Image: {image.shape[1]}x{image.shape[0]} px")
    H, W = image.shape[:2]
    effective_delta = config.delta_x or "adaptive"
    print(f"Using delta={effective_delta}, threshold={config.center_threshold}")

    ellipses = detect_ellipses(image, config)

    if not ellipses:
        print("No ellipses detected.")
    else:
        print(f"\nDetected {len(ellipses)} ellipse(s):")
        for i, e in enumerate(ellipses):
            print(
                f"  [{i+1}] center=({e.center_x:.1f}, {e.center_y:.1f})  "
                f"a={e.semi_major:.1f}px  b={e.semi_minor:.1f}px  "
                f"theta={np.degrees(e.angle_rad):.1f}deg  votes={e.votes}"
            )

    if args.visualize:
        args.output.mkdir(parents=True, exist_ok=True)
        stem = args.image.stem
        edge_mask, _, _ = detect_edges(image, config.canny_low, config.canny_high)
        panel_path = str(args.output / f"{stem}_panel.png")
        save_result(image, ellipses, panel_path, edge_mask=edge_mask)
        print(f"\nPanel saved: {panel_path}")


if __name__ == "__main__":
    main()
