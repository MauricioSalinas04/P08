from pathlib import Path

import numpy as np
from PIL import Image

from ellipse_detector.pipeline import DetectorConfig, detect_ellipses
from ellipse_detector.preprocessing.edge_detector import detect_edges
from ellipse_detector.visualization.draw import save_result

IMAGE = Path("data/image.png")
OUTPUT = Path("results")


def main() -> None:
    image = np.array(Image.open(IMAGE))
    config = DetectorConfig(
        canny_low=20.0,
        canny_high=60.0,
        max_edge_points=4000,
        max_ellipses=10,
    )

    print(f"Imagen: {image.shape[1]}x{image.shape[0]} px")
    ellipses = detect_ellipses(image, config)

    if not ellipses:
        print("No se detectaron elipses.")
    else:
        print(f"\nDetectadas {len(ellipses)} elipse(s):")
        for i, e in enumerate(ellipses, 1):
            print(
                f"  [{i}] centro=({e.center_x:.1f}, {e.center_y:.1f})  "
                f"a={e.semi_major:.1f}px  b={e.semi_minor:.1f}px  "
                f"theta={np.degrees(e.angle_rad):.1f}deg  votos={e.votes}"
            )

    OUTPUT.mkdir(exist_ok=True)
    edge_mask, _, _ = detect_edges(image, config.canny_low, config.canny_high)
    out_path = str(OUTPUT / "image_panel.png")
    save_result(image, ellipses, out_path, edge_mask=edge_mask)
    print(f"\nPanel guardado: {out_path}")


if __name__ == "__main__":
    main()
