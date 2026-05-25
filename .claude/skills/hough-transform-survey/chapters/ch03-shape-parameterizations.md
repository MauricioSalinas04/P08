# Chapter 3 — Shape Parameterizations

The choice of parameterization controls accuracy, storage, and how easily extra information can be exploited.

## Line parameterizations

| Scheme | Form | Notes |
|--------|------|-------|
| `(m, c)` | `y = mx + c` | Singular when `m → ∞` (vertical lines). |
| `(ρ, θ)` | `ρ = x cos θ + y sin θ` | Duda–Hart, default. Image point → sinusoid in `(ρ, θ)`. |
| **Foot of normal** (Davies [86]) | Line ↔ intersection of normal-from-origin with the line | Edge-gradient gives `m` directly → restricts one-to-many to **one-to-one** mapping. Parameter space congruent with image space. Error grows with distance from origin → use small subimages; may need multiple origins. Achieves pixel-accurate location, 1–2° orientation. |
| **Muff** (Wallace [84]) | Line = two intersection points `(s₁, s₂)` on image perimeter, measured CCW from lower-left corner, with `s₁ < s₂` | Bounded; no transcendentals to compute `(s₁,s₂)` from `(x,y)`; resolution matches digital-graphics rasterizable lines. |
| **Forman hybrid** [90] | `(s₁, θ)` — first exit point + measured orientation | Local operator searches for two close line elements; used for linear-road extraction in FLIR. |

## Curves via the line HT (Casasent–Krishnapuram [106, 120])

A curve = a succession of short straight-line segments. Each maps to a `(ρ, θ)` cell with value proportional to length. The accumulator shows a characteristic *pattern* of small peaks. Semi-threshold to drop random background; apply a **shape-specific accumulator transform** (shifting of bins) that lines characteristic peaks up on a common sinusoid. Inverse straight-line transform of the modified accumulator yields a peak at the curve's location. Demonstrated for circles, ellipses, parabolas.

## High-dimensional → sequential low-D decomposition (the key idea)

| Shape | Naïve dim | Decomposed |
|-------|-----------|------------|
| Circle `(a, b, r)` | 3 | 2-D HT for `(a, b)` using edge direction [118], then 1-D histogram for `r`. |
| Ellipse | 5 | Series of problems with max dimensionality 2 [24, 59]. |
| 2-D-to-3-D viewing transform (scale, orientation, translation) | 7 | Ballard & Sabbah [46] — natural dominance ordering: solve scale → orientation → translation sequentially. |

**Take-away pattern:** if you can detect *any* invariant relation between local features (parallel tangents, edge-direction constraints, symmetry axes), use it to peel off parameters one subgroup at a time. See [[patterns]] for the recipe.

## R-table representation (Ballard [31])

Store each boundary point as a vector `(r, α)` relative to the reference point — distance and angle of the line connecting boundary point to reference point. **Index the list by the local edge direction** at the boundary point. Result: an R-table.

- Indexing benefit: an image point is only compared with R-table entries whose stored edge direction matches the image-point's measured edge direction. Massive computational savings.
- Composite shapes: Ballard discusses building R-tables of composites from R-tables of primitives. Davis [41] argues for a structured hierarchical approach — better control because the system can demand that specific primitives are detected before confirming a composite.

## Hyperplane formulation (Li, Lavin, LeMaster [75])

Parameterize shapes so that their backprojected surfaces in parameter space are **hyperplanes**. Plane-vs-hyperrectangle intersection is fast and well-understood. Examples:
- Straight lines in 2-D ✓
- Plane detection in 3-D ✓
- 3-parameter circle finding ✓ (experiments in [119])
- Circle-center finding via intersecting straight lines in 2-D parameter space [118]

## HT as subgraph isomorphism (Kasif, Kitchen, Rosenfeld [54])

GHT is equivalent to subgraph-isomorphism: nodes in a labelled graph are described by sequences of arc/node labels along paths to a reference node `r`. The list of such relational sequences votes for reference nodes during graph matching.

## HT as distributed pattern recognition (Wahl & Biland [100])

For polyhedra in a 2-D image, transform to `(m, c)` and read the **pattern** of peaks:
- Vertically aligned clusters → parallel lines in image.
- Colinear arrangement of `n` clusters → an `n`-line vertex in image.

A higher-level reasoning step over the accumulator, not just peak picking.

## Decision guide

- Vertical lines possible → never `(m, c)`; use `(ρ, θ)` or foot-of-normal.
- Have reliable edge-gradient estimates → foot-of-normal or R-table indexing.
- Need bounded parameter space matching digital pixels → Muff.
- Want hardware-friendly intersection tests → hyperplane formulation.
- Detecting a curve but only have line-HT hardware → Casasent–Krishnapuram transform-the-accumulator trick.
- High-dim shape → look for decomposition into ≤2-D subproblems before anything else.

Cross-refs: [[ch04-efficient-accumulation]], [[ch08-applications]], [[patterns]], [[cheatsheet]], [[glossary]].
