---
name: hough-transform-survey
description: Knowledge base from "A Survey of the Hough Transform" by J. Illingworth and J. Kittler (CVGIP, 1988). Use when implementing or reasoning about Hough Transform variants (standard HT, generalized HT, Adaptive HT, Fast HT), parameter-space decomposition, accumulator design, peak detection strategies, computational/storage complexity, the HT–Radon equivalence, or HT architectures for line/circle/ellipse/arbitrary-shape detection.
---

# A Survey of the Hough Transform — Illingworth & Kittler (1988)

This skill organizes the comprehensive 1988 survey of Hough Transform (HT) research by J. Illingworth and J. Kittler (CVGIP 44, 87–116). The survey covers theory, parameterizations, efficient accumulation, peak detection, performance analysis, the link to the Radon transform, applications, and parallel architectures up to early 1988.

## When to use this skill

- Designing or implementing any HT variant (line, circle, ellipse, arbitrary shape).
- Choosing a parameterization (`(m,c)`, `(ρ,θ)`, foot-of-normal, Muff, R-table, hyperplane).
- Reducing storage/computation: parameter decomposition, focusing (AHT, FHT), DQS/DQP, hash/cache accumulators.
- Designing peak detection in cluttered accumulators (thresholding, converging squares, butterfly filter, CHough, backtransform).
- Comparing HT to Radon, matched filter, template matching, or statistical signal detection.
- Planning HT execution on parallel/SIMD/MIMD/pyramid/SLAP architectures.
- Estimating complexity (O(α^q) storage; focusing gains O((α/β)^q · log(β)/log(α))).

## Core mental models (front-loaded)

1. **HT = evidence gathering in parameter space.** Each image point votes for *every* parameter combination compatible with it; peaks in the accumulator are shapes. See [[ch01-introduction]].
2. **Backprojection inverts the role of variables and parameters.** A defining relation `f((a₁..aₙ),(x,y))=0` becomes `g((x̂,ŷ),(a₁..aₙ))=0` — one image point → a hypersurface in parameter space. See [[ch01-introduction]].
3. **Standard storage scales as O(αᵍ)** (α bins per axis, q parameters). This is the central pain that *every* efficient method attacks. See [[ch01-introduction]], [[cheatsheet]].
4. **Parameter decomposition is the #1 efficiency tool.** Use edge direction or geometric invariants to break an n-D problem into a sequence of ≤2-D problems. Circles (3→2+1), ellipses (5→sequence of ≤2-D), viewing transform (7→scale/orientation/translation). See [[ch03-shape-parameterizations]], [[patterns]].
5. **Edge-gradient information is leverage.** Knowing local edge orientation collapses one-to-many backprojection toward one-to-one and indexes R-tables. See [[ch02-early-development]], [[ch03-shape-parameterizations]].
6. **Focusing beats brute force.** Coarse-to-fine search (AHT, FHT, DQS, DQP) gives `O((α/β)^q · log(β)/log(α))` savings vs. uniform grid. See [[ch04-efficient-accumulation]].
7. **Peaks are rarely sharp symmetric spikes.** Lines produce a "butterfly" in `(ρ,θ)`; circles a broad band; finite retinas bias counts. Threshold globally → fails. See [[ch05-peak-detection]], [[ch06-performance-analysis]].
8. **HT ≡ Radon transform on binary images.** Anything proven for Radon (Fourier-slice, optical implementation, projection algebra) applies to HT. See [[ch07-ht-and-other-transforms]].
9. **Robustness comes from independence.** Each pixel votes independently → parallelizable, occlusion-tolerant, multiple-shape-capable, robust to random noise (but *structured* background — e.g., other shapes — can fool it). See [[ch01-introduction]].

## Chapter index (load on demand)

- [[ch01-introduction]] — HT definition, backprojection, accumulator, generalized HT, formal statement (Eqs. 11–13), advantages and disadvantages.
- [[ch02-early-development]] — Hough's patent (1962), Duda–Hart `(ρ,θ)`, Shapiro's analyses, Ballard's GHT.
- [[ch03-shape-parameterizations]] — `(m,c)`, `(ρ,θ)`, foot-of-normal (Davies), Muff (Wallace), Forman hybrid, Casasent–Krishnapuram curve-via-line trick, decomposition (circle 3→2+1, ellipse 5→≤2-D, viewing 7-param), R-table, hyperplane formulation.
- [[ch04-efficient-accumulation]] — DQS, DQP, hierarchical warping, iterative focusing (AHT, FHT), bintree, Brown's hash/cache, projection HT.
- [[ch05-peak-detection]] — global/adaptive thresholds, converging squares, weighting by edge gradient, Thrift–Dunn influence functions, butterfly filter (Leavers–Boyce), backtransform sharpening (Gerig–Klein), CHough.
- [[ch06-performance-analysis]] — variance of parameter estimates, finite-retina bias (Cohen–Toussaint, Alagar–Thiel), `(dρ,dθ)` invariant, P/R/G robustness measures, Brown's feature-psf / parameter-psf imaging model, matched-filter weighting, HT vs. statistical signal detection.
- [[ch07-ht-and-other-transforms]] — Radon equivalence (Deans 1981), Fourier-slice computation, optical/hybrid implementations, dot-product space, variable-slit projection.
- [[ch08-applications]] — lines (roads, gauges, seismograms, characters, fingerprints, targets, SAR, SEM), GHT (industrial inspection, polygons, corners), motion (Fennema–Thompson, Adiv), viewing parameters (Ballard–Sabbah, Silberberg), 3D range (Henderson, Muller–Mohr, Dhome), stereo, registration, contour compression.
- [[ch09-architectures]] — pipelined TTL, RVLSI, PPPE, SIMD (mesh, MPP, connection machine), MIMD (BBN Butterfly), SLAP, pyramid, blackboard, connectionist parameter nets.
- [[ch10-summary]] — bottom line: HT's storage/computation pain is being solved; analog/optical and focusing implementations make it competitive; expect growing adoption.

## Reference layers

- [[glossary]] — every named term (HT, GHT, R-table, DQS, DQP, AHT, FHT, CHough, Muff, feature-psf, parameter-psf, P/R/G, etc.) with chapter pointers.
- [[patterns]] — reusable design techniques: decomposition, edge-gradient pruning, focusing, R-table indexing, projection HT, CHough cancellation, butterfly filter, backtransform.
- [[cheatsheet]] — decision tables (which parameterization, which efficiency method, which peak detector), complexity formulas, quick equations.

## Bibliographic anchor

Source: J. Illingworth and J. Kittler, "A Survey of the Hough Transform," *Computer Vision, Graphics, and Image Processing* 44, 87–116 (1988). Department of Electronics and Electrical Engineering, University of Surrey. © 1988 Academic Press. Survey covers literature up to early 1988 (≈136 references).
