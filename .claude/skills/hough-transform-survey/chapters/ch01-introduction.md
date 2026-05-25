# Chapter 1 — Introduction

## What the HT does

The Hough Transform (HT) detects spatially extended patterns of points in binary image data by converting a **global detection problem in image space** into a **local peak detection problem in parameter space**. Each value of the parameter tuple characterizes one instance of the sought shape.

## Backprojection (the central idea)

The defining relation of a parametric shape can be read two ways:

- **Forward (parameters → image points):** `f((a₁,…,aₙ), (x,y)) = 0` maps each parameter combination to the set of image points lying on that shape.
- **Backward (image point → parameter set):** `g((x̂,ŷ), (a₁,…,aₙ)) = 0` is the same equation with the roles swapped. A single image point produces a hypersurface in parameter space — the set of all shapes compatible with that point.

**Straight line example.** Parameterization `f((m̂,ĉ),(x,y)) = y - m̂x - ĉ = 0` (Eq. 1). Backprojection: `g((x̂,ŷ),(m,c)) = ŷ - x̂m - c = 0` (Eq. 2). Each image point is a line in `(m,c)` space; colinear image points produce lines that intersect at a single `(m,c)` peak (Fig. 1).

## Generalized HT (arbitrary shapes)

A shape is given as a template list of boundary points `{(vᵢ, wᵢ)}, i = 1,…,N` plus a reference point `(xᵣ, yᵣ)`. Scaling by `a₄`, rotating by `a₃`, translating by `(a₁, a₂)` gives transformed boundary points (Eqs. 5–8). For each image point `(xⱼ, yⱼ)` and each template point `i`, solve for the four transform parameters (Eqs. 9–10):

- `a₁ = xⱼ + xᵣ - vᵢ - (yᵣ - wᵢ) a₄ sin(a₃) + (xᵣ - vᵢ) a₄ cos(a₃)`
- `a₂ = yⱼ + yᵣ - wᵢ + (xᵣ - vᵢ) a₄ sin(a₃) + (yᵣ - wᵢ) a₄ cos(a₃)`

Each image point → a hypersurface; intersection density indicates how many image points fit a shape with those parameters.

## Formal definition

Let `g(x̂ⱼ, ŷⱼ, a₁,…,aₙ)` be the backprojection defining relation. Then (Eq. 12):

```
H(a₁,…,aₙ) = Σⱼ h(x̂ⱼ, ŷⱼ, a₁,…,aₙ)
```

where `h = 1` if `g = 0`, else `h = 0` (Eq. 13). On a computer, continuous parameter space is partitioned into multidimensional rectangles (cells). Each cell is an **accumulator** counter, incremented whenever a backprojected hypersurface passes through it.

## Why HT beats template matching

Template matching generates *every* candidate template and checks for image-point matches — many template points have no corresponding image point, wasting work. The HT *always* assumes the image point matches *some* template point and computes the transform that links them. Same quantity, less wasted computation.

## Advantages (memorize this list)

1. **Parallelizable** — each image point processed independently.
2. **Occlusion-tolerant** — peak size ≈ proportional to number of matching points; graceful degradation.
3. **Noise-robust** — random points don't coherently vote for one cell, so only a low background appears.
4. **Multi-instance** — multiple shapes of the same class each produce their own peak.

## Disadvantages

1. **Storage:** `O(αᵍ)` for q parameters with α intervals each — prohibitive for large `α` or `q`.
2. **Computation:** dominated by computing cell–hypersurface intersections; scales exponentially with parameter dimension.
3. **Structured background:** boundaries of *other* shapes can produce structured backgrounds that mimic peaks (random noise does not).

## Efficiency levers introduced by the survey

- Use smaller accumulators (focusing methods → [[ch04-efficient-accumulation]]).
- Use extra data (edge direction) to restrict parameter range (→ [[ch03-shape-parameterizations]]).

## Survey roadmap (Section 1 closing)

§2 history → §3 parameterizations → §4 efficient accumulation → §5 peak detection → §6 analytic results → §7 Radon/projection relationship → §8 applications → §9 parallel architectures → §10 summary.

Cross-refs: [[ch02-early-development]], [[ch03-shape-parameterizations]], [[ch04-efficient-accumulation]], [[patterns]], [[glossary]].
