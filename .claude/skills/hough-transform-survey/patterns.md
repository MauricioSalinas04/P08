# Patterns

Reusable techniques abstracted from the survey, each with a "use when" trigger and a pointer to the chapter that explains it.

## Pattern: Parameter decomposition

**Use when:** the naïve parameterization has `q ≥ 3` and you have *any* invariant (edge direction, geometric symmetry, image-feature pair) that constrains a subset of parameters.

**Recipe:**
1. Find a relation among image features that determines a subgroup of parameters independently of the rest.
2. Run a low-D HT for that subgroup.
3. Fix the recovered subgroup; run another low-D HT for the next group.

**Examples in the survey:**
- Circle `(a, b, r)`: 2-D HT for `(a, b)` using edge direction; then 1-D histogram for `r`.
- Ellipse: 5 parameters → series of ≤2-D problems.
- Viewing transform: 7 parameters → scale → orientation → translation (Ballard–Sabbah).

See [[ch03-shape-parameterizations]].

## Pattern: Edge-direction pruning

**Use when:** you have reliable per-pixel edge orientation (Sobel/Prewitt gradients) and you are iterating over `image_points × template_points` (or `image_points × parameter_cells`).

**Recipe:** index the template (R-table) or the parameter-cell list by edge direction; for each image point only iterate over entries whose stored edge direction is compatible with the measured one.

See [[ch02-early-development]], [[ch03-shape-parameterizations]].

## Pattern: Coarse-to-fine focusing

**Use when:** you can afford a coarse pass and the shape will produce a coherent vote cluster at coarse resolution.

**Recipe:**
1. Accumulate at small per-axis resolution β (e.g., β = 9 in AHT).
2. Threshold + connected-components on the small accumulator.
3. For each component, set new per-axis parameter limits (translated, rotated, expanded, or shrunk to fit the component).
4. Repeat.

Storage gain `O((α/β)^q)`. Watch out: in cluttered images, multiple objects' coarse votes can overlap into a spurious peak that wanders away from any real feature.

See [[ch04-efficient-accumulation]] (AHT, FHT).

## Pattern: Hyperplane mapping

**Use when:** you can re-derive your shape so each image point backprojects to a *hyperplane* (not a curved hypersurface).

**Benefit:** plane–hyperrectangle intersections compute incrementally with adds and shifts; complexity scales linearly in q. VLSI-friendly.

**Caveats:** not every shape maps naturally; needs per-quadrant storage of feature distances.

See [[ch04-efficient-accumulation]] (FHT), [[ch03-shape-parameterizations]].

## Pattern: R-table indexing

**Use when:** generalized HT for arbitrary shape; you have edge orientation.

**Recipe:** store `(r, α)` vectors from each boundary point to the reference point, bucketed by local edge direction. Match image points only against buckets with matching gradient.

See [[ch03-shape-parameterizations]] (Ballard's R-table).

## Pattern: Projection HT (Radon view)

**Use when:** you have hardware for fast image rotation/translation, FFT, template multiplication, and histogramming — but not for general accumulator updates.

**Recipe (Sanz–Dinstein flavor):** for each θ, multiply binary image by a template image whose pixel intensity equals its `ρ`-value; the gray-level histogram has peaks at the `ρ` values of present lines. Sweep θ → full HT.

See [[ch07-ht-and-other-transforms]].

## Pattern: CHough cancellation

**Use when:** parameter psfs are roughly symmetric and multi-object sidelobe interference degrades peak detection.

**Recipe:** image points cast positive votes for parameters consistent with them and negative votes for parameters where the shape *cannot* be — net effect cancels sidelobes. Reduces background mean and variance. Be aware: more sensitive to quantization.

See [[ch05-peak-detection]] (Brown), [[ch06-performance-analysis]].

## Pattern: Butterfly filter on `(ρ, θ)`

**Use when:** detecting lines in `(ρ, θ)` and the raw accumulator has smeared butterfly-shaped peaks.

**Recipe:** convolve accumulator with a Leavers–Boyce butterfly mask (designed from the analytic shape of the line peak). For circles, enhance band edges, then run a *second* line HT on the filtered accumulator.

See [[ch05-peak-detection]].

## Pattern: Backtransform sharpening

**Use when:** peaks are broad/fuzzy and you can re-process the image with the first-pass accumulator in hand.

**Recipe:** for each image point, of the cells its hypersurface intersects pick the one with the largest count and reassign the point uniquely to that cell. Re-accumulate using the unique assignment → sharper peaks.

See [[ch05-peak-detection]] (Gerig–Klein).

## Pattern: Non-linear ρ quantization for finite retinas

**Use when:** image is bounded (especially circular) and you plan to use a global threshold.

**Recipe:** use a non-linear `ρ`-axis quantization (Cohen–Toussaint / beta-distribution-related per Alagar–Thiel) so each accumulator bin receives equal counts under uniform random image points. Alternatively, subtract an empirical background.

See [[ch06-performance-analysis]].

## Pattern: Vote weighting by edge gradient

**Use when:** edge-gradient magnitudes are meaningful (not all-or-nothing thresholded).

**Recipe:** weight each vote by edge-gradient magnitude (heuristic) or by `magnitude × a priori edge gradient` (Davies's matched-filter form).

See [[ch05-peak-detection]], [[ch06-performance-analysis]].

## Pattern: Decomposed accumulator with connection bit

**Use when:** you want to bias detection toward *connected* edge segments (e.g., SEM resist lines, Shu et al.).

**Recipe:** augment the accumulator with a parallel **bit array**; incrementation of an accumulator cell is conditional on the corresponding bit (which encodes the most recent contributing edge's status, enforcing connectivity).

See [[ch08-applications]] (Shu et al. [135]).

## Pattern: Incremental + early termination ("parallel guessing")

**Use when:** any cell exceeding a significance bound is enough; latency matters.

**Recipe:** compute the HT incrementally (one image point at a time); poll for significance after each update; stop when a peak passes a confidence bound. Database/blackboard friendly.

See [[ch09-architectures]] (Fischler & Firschein).

## Pattern: Migrating accumulator cells (SLAP topology)

**Use when:** targeting a linear SIMD array and you want to avoid all-to-all routing of votes.

**Recipe:** assign one PE per image column; let accumulator cells move between PEs at a rate set by their `θ` parameter so they always sit at the PE handling the pixel on their line. Cells emerge at the array's opposite edge having seen all relevant pixels.

See [[ch09-architectures]] (Fisher & Highman [113]).

## Anti-patterns

- **Global threshold on a finite retina without correction.** Will bias toward low-ρ peaks (Cohen–Toussaint). [[ch06-performance-analysis]]
- **`(m, c)` for arbitrary-orientation lines.** Singular at verticals. Use `(ρ, θ)`. [[ch02-early-development]]
- **Distributing both image and accumulator across all SIMD PEs naively.** Silberberg's 8000 PEs → 7× speedup. Voting topology dominates compute. [[ch09-architectures]]
- **Linear, translation-invariant projection of the accumulator.** Eckhardt–Madedechner: result is trivial. Use non-linear projection operators. [[ch05-peak-detection]]
- **Storing entries indefinitely in a hash-accumulator without a flush policy.** Cache will saturate and lose new high-vote candidates. [[ch04-efficient-accumulation]]
