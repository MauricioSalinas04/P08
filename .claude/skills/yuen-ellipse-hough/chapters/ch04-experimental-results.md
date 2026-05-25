# Section 4: Experimental Results

## Core Idea
The method is validated on two experiments: a single-ellipse arc (67 edge points, asymmetric — previous methods inapplicable) and a complex 8-ellipse image (657 edge points, overlapping), demonstrating accurate parameter recovery in both cases.

## Experimental Parameters Used
| Parameter | Value | Meaning |
|---|---|---|
| δ₁ | 5 pixels | Max x-distance for valid pair |
| δ₂ | 30 pixels | Max y-distance for valid pair |
| L | 30 pixels | Length of voting segment MN |
| Accumulator (Stage 1) | 256×256 | Center-finding resolution |
| Accumulator (Stage 2) | 9×9×9 | AHT for B, D, C |
| Edge detector | Spacek's algorithm | Provides gradient directions |

## Experiment 1: Single Ellipse Arc (Figure 2)
- **Input**: 67 edge points from a partial ellipse arc; no symmetric counterpart — parallel-tangent methods inapplicable
- **True center**: (116.8, 85.72)
- **Detected center**: (116.5 ± 0.5, 86.5 ± 0.5) ✓
- **Estimated params**: B=0.93827±0.25, D=-0.17284±0.25, C=-382.2588±0.5
- **Recovered geometry**:
  - Estimated: a=21.948, b=18.274, θ=50.062°
  - True:      a=22.231, b=18.437, θ=50.675°
- **Verdict**: Sub-pixel center accuracy; axis lengths within ~1.3%; angle within 0.6°

## Experiment 2: Eight Overlapping Ellipses (Figure 4)
- **Input**: 657 edge points from 8 ellipses with various sizes, orientations, and overlaps
- **7 of 8 ellipses**: Parameters estimated well
- **Ellipse 8** (center ~(140,36), 14 points): Center found correctly, but Stage 2 failed — the arc was too short (only 14 points) and could equally be interpreted as part of another ellipse
- **Key finding**: Failure occurs only on a near-degenerate case; 14 points is at the practical limit of the method

## Reference Table: True vs. Estimated Parameters (8-Ellipse Experiment)
| Ellipse | True Center | Est. Center | True a,b | Est. a,b | True θ | Est. θ |
|---------|------------|-------------|----------|----------|--------|--------|
| 1 | (84.56, 110.98) | (81.5, 109.5) | 25.5, 7.25 | 23.45, 7.26 | 20° | 19.76° |
| 2 | (120.56, 110.98) | (118.5, 110.5) | 25.5, 7.25 | 22.01, 6.64 | 20° | 20.41° |
| 3 | (100.12, 60.24) | (100.5, 60.5) | 12.35, 8.35 | 14.05, 8.46 | 80° | 74.43° |
| 4 | (130.49, 30.68) | (129.5, 31.5) | 30.67, 15.43 | 29.04, 16.38 | 145° | 145.36° |
| 5 | (99.25, 140.56) | (98.5, 145.5) | 32.67, 21.98 | 27.55, 20.70 | 85° | 66.26° |
| 6 | (130.90, 150.56) | (130.5, 150.5) | 22.35, 15.67 | 24.14, 15.90 | 33.75° | 31.17° |
| 7 | (250.05, 56.90) | (249.5, 57.5) | 30.5, 12.67 | 32.94, 13.04 | 128.34° | 127.52° |
| 8 | (140.24, 35.78) | (141.5, 34.5) | 17.95, 11.45 | 27.86, 14.13 | 32.49° | 19.20° |

## Key Takeaways
1. The method successfully finds asymmetric arc centers where classical methods fail entirely
2. Practical parameter values: δ₁=5, δ₂=30, L=30 pixels work well for 256×256 images
3. A minimum of ~20+ edge points per ellipse arc is needed for reliable Stage 2 estimation
4. Stage 2 failures occur when the arc is very short and ambiguous, not because of the Stage 1 center finding

## Connects To
- **Ch02**: Experimental values match the theoretical setup of δ₁, δ₂, L described there
- **Ch03**: With n=67 for Experiment 1, Stage 1 uses ~67×66/2 × 30 ≈ 66,330 votes
