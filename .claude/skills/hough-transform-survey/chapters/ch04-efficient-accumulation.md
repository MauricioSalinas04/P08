# Chapter 4 — Efficient HT Accumulation

The standard accumulator's `O(αᵍ)` storage is the dragon every method in this chapter slays. The unifying principle: **high resolution only where votes concentrate.**

## Dynamically Quantized Spaces — DQS (O'Rourke & Sloan [35, 69])

- **Data structure:** binary tree; each node = a rectangular region of parameter space.
- **Rules:** as data arrives, **split** dense cells and **merge** sparse ones so that every cell contains ≈ the same number of counts, evenly distributed.
- **Input:** total number of cells (fixed).
- **Outcome:** small cells cluster around peaks → better peak localization than uniform quantization with the same cell budget.

## Dynamically Quantized Pyramids — DQP (O'Rourke & Sloan [37, 69])

- **Data structure:** multidimensional quadtree — fixed number and connectivity of cells.
- **Drawback of vanilla quadtrees:** static boundaries → fixed spatial resolution.
- **Fix — hierarchical warping:** dynamically modify cell boundaries by tracking the mean position of data points within each region. Cells end up with ≈ equal vote counts.
- **Caveats:** warping introduces errors in final totals; final partitioning **depends on insertion order** (recently accumulated points have outsized influence).
- **Empirical comparison [O'Rourke & Sloan]:** DQS marginally outperforms DQP; DQS harder to implement.
- **Blanford [102]:** reworked DQP so votes are correctly distributed through the quadtree; costs ≈ 3× original DQP compute but kills order-dependence.

## Iterative focusing (the workhorse pattern)

Accumulate the HT at a **coarse but uniform** resolution; pick regions of high counts; re-accumulate inside those regions at higher resolution. A few iterations → very high parameter resolution.

**Complexity argument.** A q-D space of resolution `α` searched in iterations of size `β`:
- Iterations needed: `O(log(α) / log(β))`.
- Computational saving vs. brute force: `O((α/β)^q · log(β) / log(α))`.

Used by Adiv [43] for motion parameters, Silberberg [72] for viewing parameters.

## Fast Hough Transform — FHT (Li et al. [75, 76, 94])

- Multidimensional **quadtree** combined with HTs that map image points to **hyperplanes** (see hyperplane formulation in [[ch03-shape-parameterizations]]).
- **Plane–cell intersection** computed by an incremental test from the known geometric relation of a quadrant to its 4 sons → **only adds and shifts**, cost scales **linearly in dimensionality**.
- **Reported gains:** `O(10³)` for 2-D line detection, `O(10⁶)` for 3-D plane detection.
- VLSI-friendly, easily extends to higher-D spaces.
- **Weaknesses:**
  - Focusing controlled by a **fixed vote-count threshold** → hard to set in complex images; too low → explores too many quadrants.
  - Incremental test requires each quadrant to store distance of every feature from its center — large overhead.
  - Not every shape maps naturally to hyperplanes.
  - Static quadtree can't adapt to different per-axis resolutions → Li et al. propose **bintrees** [93] (rectangular partitioning).

## Adaptive Hough Transform — AHT (Illingworth & Kittler [118, 119])

- Iterative coarse-to-fine search for 2-D and 3-D parameter spaces (lines, circles).
- Small accumulator (typical `β = 9` per axis).
- After each pass: **threshold**, then **connected-components**. The shape and extent of components dictate parameter limits for the next iteration — limits can be decreased, expanded, rotated, or merely translated.
- Parameter limits set **independently per axis** → method picks the right precision for each parameter.
- Storage gain `O((α/β)^q)`; for one circle example **several hundred times faster** than standard.
- **Failure mode:** in complex images, extended vote patterns from two or more objects can **overlap at coarse resolution** producing a spurious peak whose location matches no real feature. Mitigations under investigation in [118, 119].

## Hash / cache accumulators (Brown [40, 47, 49])

- Replace the array with a **small fixed-size content-addressable store** (software hash table or hardware cache).
- When full → **flushing** (garbage collect) to free space.
- Flushing strategies: drop fewest-vote entries; or favor recent entries; or favor geometric locality.
- Tested cache sizes 32, 64, 128 → comparable in practice to full accumulators; degradation as noise rises / cache shrinks is predictable.

## Projection of the GHT (David & Yam [27])

Compute only a **projection** of the full GHT to dodge storage. Still robust as a shape matcher; recover lost parameter values with separate methods.

## Decision guide

| Problem | Recommended method |
|---------|-------------------|
| Single shape, moderate q | AHT (coarse-to-fine, connected-component-guided) |
| Hyperplane-mapped shape, want linear-in-q cost | FHT |
| Limited memory, willing to lose order-independence | Brown hash/cache |
| Need adaptive per-axis precision | AHT or bintree variant of FHT |
| Want best peak localization within fixed cell budget | DQS |
| Pyramid-machine target architecture | Blanford-corrected DQP |

Cross-refs: [[ch03-shape-parameterizations]], [[ch05-peak-detection]], [[ch09-architectures]], [[patterns]], [[cheatsheet]].
