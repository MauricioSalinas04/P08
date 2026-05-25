# Section 5: Discussion and Conclusions

## Core Idea
The TM-line center-finding method applies to a wider class of practical problems than previous methods because it requires no arc symmetry. The AHT-based Stage 2 is efficient. The main open problems are the O(k²) multi-ellipse cost and the cluttered center-finding space.

## Key Conclusions

### Advantages over prior methods
- **Asymmetric arc support**: Self-occlusion and partial views produce asymmetric arcs; the TM-line method works; parallel-tangent methods do not
- **Broader applicability**: Any two non-parallel-tangent edge points on the same ellipse contribute a valid vote — no special geometry required
- **Efficient Stage 2**: AHT focuses dynamically; cost is ~10 × 3 × 81 × n_i regardless of parameter range sizes

### Known limitations and future work
- **O(k²) iterative accumulation**: The current point-deletion + reaccumulation strategy is inefficient for many ellipses; alternative peak-analysis methods in the center space are needed
- **Propagated error sensitivity**: More decomposition stages = more reliance on accurate edge gradient directions; grey-level edge measurement is the noise source
- **Hardware potential**: The basic Stage 1 operation (voting along a line in accumulator space) is a natural primitive for dedicated hardware, which could make the O(n²) cost tractable in real-time

## Anti-patterns
- **Applying this method without good edge direction measurements**: The entire method depends on accurate tangent slopes s₁, s₂ from edge detection. Poor gradient estimates directly degrade both stages.
- **Expecting exact axis recovery from very short arcs**: As Ellipse 8 showed (14 points), Stage 2 becomes unreliable when the supporting arc is too short to constrain B, D, C uniquely.

## Mental Models
- Think of the TM-line as "any two points on an ellipse tell you a line that the center is on" — enough constraints from many pairs vote the center into sharp focus
- Think of the iterative deletion loop as a "peel the onion" strategy: find the most prominent ellipse, remove it, repeat

## Key Takeaways
1. The method is applicable wherever previous HT schemes would fail due to arc asymmetry from occlusion
2. The computational cost increase from Stage 1's O(n²) pairing is partially offset by the potential for hardware acceleration
3. Future improvement should target the center-space peak detection to avoid reaccumulation, reducing O(k²) to something closer to O(k)

## Connects To
- **Ch02**: The AHT method described as Stage 2 (Illingworth & Kittler 1987, cited as [5])
- **Ch03**: The O(k²) complexity discussed here is derived in Section 3
