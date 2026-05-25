# Cheatsheet

Quick-reference tables and equations from the survey.

## Core equations

| Eq # | Form | Meaning |
|------|------|---------|
| 1 | `y − m x − c = 0` | `(m, c)` line definition |
| 2 | `ŷ − x̂ m − c = 0` | Backprojection of image point into `(m, c)` |
| 3 | `f((a₁,…,aₙ),(x,y)) = 0` | General shape definition |
| 4 | `g((x̂,ŷ),(a₁,…,aₙ)) = 0` | Backprojection (variables ↔ parameters swap) |
| 5–10 | (see [[ch01-introduction]]) | GHT scale-rotate-translate transformation |
| 11 | `g = f` (analytic) or `(distance from transformed template)² = 0` (template) | Unified backprojection |
| 12 | `H(a₁,…,aₙ) = Σⱼ h(x̂ⱼ, ŷⱼ, a₁,…,aₙ)` | HT as a sum over image points |
| 13 | `h = 1` if `g=0` else `0` | Per-point vote |
| 14 | `ρ = x cos θ + y sin θ` | Duda–Hart line parameterization |
| 15 | `P = m_T/m_k`, `R = m_T/M_k`, `G = (m_T − m_F)/M_k` | Alagar–Thiel robustness measures |
| 16 | `R(ρ,θ) = ∬ f(x,y) δ(ρ − x cos θ − y sin θ) dx dy` | Radon transform |
| 17 | `ρ = x cos θ + y sin θ` | Line traced by the Radon δ |
| 18 | `g = (V/I) · (...)` | Peek–Mayhew–Frisby gaze/distance from vertical disparity |

## Complexity quick reference

| Quantity | Standard HT | Focused (AHT/FHT) | DQS/DQP |
|----------|-------------|-------------------|---------|
| Accumulator storage | `O(αᵍ)` | `O(βᵍ)` per iteration | Fixed cell budget |
| Iterations | 1 | `O(log α / log β)` | n/a |
| Total compute (focusing) | — | `O((α/β)^q · log β / log α)` saving | — |
| FHT plane–cell test | — | adds + shifts; **linear in q** | — |
| FHT reported gains | — | `O(10³)` 2-D lines, `O(10⁶)` 3-D planes | — |

## Line parameterization decision

| Constraint | Use |
|------------|-----|
| Lines can be vertical (`m → ∞`) | `(ρ, θ)` |
| Reliable edge gradient, small subimages | Foot-of-normal (Davies) |
| Need bounded params matching digital pixels | Muff (Wallace) |
| Pipeline-friendly hardware via projections | Sanz–Dinstein projection HT |
| You want hyperplane-only intersection tests | Hyperplane formulation |

## Shape detection decision

| Shape | Best practice |
|-------|---------------|
| Line | `(ρ, θ)` HT + Leavers–Boyce butterfly filter |
| Circle `(a, b, r)` | 2-D HT for `(a, b)` using edge direction → 1-D histogram for `r` |
| Ellipse | Decompose 5 params into ≤2-D subproblems (see [[ch03-shape-parameterizations]]) |
| Polygon (known size) | GHT with symmetry to shrink accumulator (Davies) |
| Arbitrary shape | GHT with R-table, indexed by edge direction |
| Curve via line hardware | Casasent–Krishnapuram transform-the-accumulator trick |

## Storage-reduction decision

| Need | Method | Section |
|------|--------|---------|
| Single shape, few params | AHT | [[ch04-efficient-accumulation]] |
| Shape maps to hyperplane | FHT | [[ch04-efficient-accumulation]] |
| Best peak localization for fixed cell budget | DQS | [[ch04-efficient-accumulation]] |
| Pyramid hardware | Blanford DQP | [[ch04-efficient-accumulation]] |
| Tight memory, OK to drop low-vote entries | Brown hash/cache | [[ch04-efficient-accumulation]] |
| Adaptive per-axis precision | AHT (or bintree FHT variant) | [[ch04-efficient-accumulation]] |

## Peak detection decision

| Symptom | Treatment |
|---------|-----------|
| Spread "butterfly" peaks for lines | Leavers–Boyce butterfly filter |
| Broad band for circles in `(ρ, θ)` | Filter band edges + second line HT |
| Broad/fuzzy peaks, can re-process | Gerig–Klein backtransform |
| Sidelobe / multi-object interference, symmetric psf | CHough |
| Need fast pyramid-style detection | O'Gorman–Sanderson converging squares |
| Finite-retina ρ bias | Non-linear ρ quantization (Cohen–Toussaint) |
| Want sharper peaks generically | Weight votes by edge-gradient magnitude |
| Structurally interpret accumulator | Non-linear projection (Eckhardt–Madedechner) or Wahl–Biland cluster rules |

## Parallel-architecture quick guide

| Hardware | Strategy | Reference |
|----------|----------|-----------|
| TTL pipeline + 68k controller | Pipeline ρ-intersection + accumulator | Hanahara [132] |
| RVLSI wafer | Fuse working cells into HT pipeline | Rhodes [134] |
| Custom IC | PPPE (Radon as projection) | Baringer [101] |
| SIMD mesh | Image-feature per PE + tree voting net → `O(log n)` routing | Li [76], lessons from Silberberg [81] |
| SIMD with router (Connection Machine) | Hypercube routing | Little et al. [123] |
| MPP `n × n` mesh | Cypher et al. `O(P + n)` rotation-based; or Guerra–Hambrusch block | [107, 115] |
| Scan-line array (SLAP) | Migrate accumulator cells between PEs | Fisher & Highman [113] |
| MIMD shared-memory (BBN Butterfly) | Partition either image or parameter space | Olsen et al. [125] |
| Pyramid | Blanford-corrected DQP | [102] |
| Blackboard/database | Parallel guessing + early termination | Fischler & Firschein [112] |

## Properties to track when reporting an HT experiment

- Parameterization choice and singularities.
- Accumulator size per axis and per dimension.
- Vote weighting (uniform, edge-grad, influence function, signed).
- Peak-detection method.
- P, R, G figures (Alagar–Thiel).
- Background-bias correction applied (yes/no, which).
- Compute / storage compared to standard HT.

## Equation-free rules of thumb

- Random noise → low, uniform background; **structured** background (other shapes) → can mimic peaks.
- Real parameter peaks are ridges more often than they are points.
- Edge direction is the single biggest cost reducer.
- A finite retina biases ρ-peaks; correct before thresholding globally.
- The HT becomes Radon for binary images; reach for FFT/optical implementations when available.
- Mapping an HT onto parallel hardware is dominated by vote-routing topology, not PE count.
