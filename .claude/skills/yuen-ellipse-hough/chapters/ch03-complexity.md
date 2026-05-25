# Section 3: Complexity Analysis

## Core Idea
Stage 1 pairing is O(n²) per ellipse; finding k ellipses iteratively costs O(k²) times that. Stage 2 AHT converges in ≤10 iterations with a fixed 9×9×9 accumulator, making it cheap relative to Stage 1.

## Key Concepts
- **Pairing complexity**: For n_i points on ellipse i, the number of pairs is n_i(n_i-1)/2 — quadratic in edge points per ellipse
- **Votes per pair**: Each pair contributes L votes (one per pixel along segment MN)
- **Total votes for ellipse i**: `V_i = [n_i(n_i-1)/2] × L`
- **Multi-ellipse cost**: Finding k ellipses costs O(k²) that of a single ellipse (because points are not removed between accumulations in the worst case)
- **Equal-size special case**: If all k ellipses have the same n points, total cost is O(k(k+1)/2) × single-ellipse cost

## Reference Tables

### Stage 1 Complexity
| Quantity | Formula |
|---|---|
| Pairs for ellipse i | n_i(n_i-1)/2 |
| Votes per pair | L (length of MN) |
| Votes for ellipse i | n_i(n_i-1)L/2 |
| Total votes for k ellipses (upper bound) | O(k²) × single-ellipse |

### Stage 2 Complexity (AHT)
| Quantity | Value |
|---|---|
| Accumulator size | 9×9×9 = 729 cells |
| Function evaluations per iteration | 3 × 9² × n_i |
| Max iterations | 10 |
| Total cost Stage 2 | ≈ 10 × 3 × 81 × Σ n_i |

## Mental Models
- Think of Stage 1 as "all pairs × line votes" — the L factor is tunable and directly controls speed vs. center resolution trade-off
- Think of Stage 2 as "729-cell binary search in 3D" — each iteration triples precision; 10 iterations give 3^10 ≈ 59,000× resolution improvement
- The O(k²) multi-ellipse cost is the price of reliable detection in a complex space; future work could optimize this

## Anti-patterns
- **Setting L too large**: Increases Stage 1 cost linearly and adds spurious votes from points on different ellipses
- **Using a full-resolution 3D accumulator for Stage 2**: Memory and computation scale as a³; AHT's 9×9×9 fixed size avoids this
- **Not removing points after each ellipse**: The background vote problem makes peak detection unreliable in multi-ellipse images

## Key Takeaways
1. The bottleneck is Stage 1 pairing: O(n²) per ellipse — minimize n_i by using tight pairing constraints δ₁, δ₂
2. Stage 2 is cheap: fixed-size accumulator + 10 iterations, total cost proportional to n_i
3. The iterative O(k²) strategy is acknowledged as inefficient; future work needed for better multi-ellipse peak analysis

## Connects To
- **Ch02**: Definition of L, δ₁, δ₂ that appear in complexity formulas
- **Ch04**: Experimental values n_i=67 (single), Σn_i=657 (8 ellipses) — plug into formulas above
