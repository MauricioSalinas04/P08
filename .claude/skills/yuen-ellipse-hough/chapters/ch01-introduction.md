# Section 1: Introduction

## Core Idea
Ellipse detection is critical in computer vision because circular 3D objects project to ellipses in 2D images. The Hough Transform is well-suited for this but naively requires an impractical 5D parameter space.

## Frameworks Introduced
- **Hough Transform (HT)**: Each image edge point votes for all parameter combinations consistent with it; the accumulator cell with the most votes identifies the shape.
  - When to use: Detecting parameterized shapes in noisy, partially-occluded images
  - How: Build accumulator array → accumulate votes → find peaks → read off parameters

## Key Concepts
- **Accumulator array**: Discrete partitioning of parameter space that counts votes; peak = detected shape
- **5-parameter ellipse**: General ellipse X² + B'Y² + 2D'XY + 2E'X + 2G'Y + C' = 0 requires 5 independent parameters → 5D accumulator is memory-prohibitive
- **Self-occlusion**: An ellipse arc can be asymmetric about the center when the object partially blocks itself; earlier methods fail here
- **Parameter space decomposition**: The key idea — break 5D problem into sequential lower-dimensional subproblems

## Why the HT Is Appropriate for Ellipses
- Insensitive to image noise
- Works with fragmentary evidence (partial arcs)
- Tolerates poor segmentation and object occlusion
- **Principal disadvantage**: Memory and computation scale as a^5 for 5 parameters → must decompose

## Historical Context
- ACRONYM system (Brooks & Binford): used generalized cylinders, needed ellipse extraction, suffered from poor segmentation
- Tsukune & Goto (1983); Tsuji & Matsumoto (1978): earlier decomposition methods using parallel tangents — fail when arcs are asymmetric
- This paper: proposes a new center-finding method that works in the general (asymmetric) case

## Key Takeaways
1. Any HT implementation for ellipses must reduce memory from a^5 by decomposing the problem
2. Edge direction information is essential for the decomposition — it enables the constraint that makes Stage 1 possible
3. The limitation of previous methods (requiring symmetric arcs) motivates the novel TM-line approach

## Connects To
- **Ch02**: Detailed derivation of both stages of the decomposed method
- **Hough Transform survey**: Illingworth & Kittler (1988) provides full HT background
