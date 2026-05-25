---
name: yuen-ellipse-hough
description: "Knowledge base from \"Ellipse Detection Using the Hough Transform\" by H.K. Yuen, J. Illingworth, J. Kittler (1988). Use when implementing ellipse detection with Hough Transform, applying two-stage parameter decomposition, Adaptive Hough Transform, center-finding via TM-line constraint, or analyzing computational complexity of ellipse fitting."
allowed-tools:
  - Read
  - Grep
argument-hint: [topic, section name, or algorithm step]
---

# Ellipse Detection Using the Hough Transform
**Authors**: H.K. Yuen, J. Illingworth, J. Kittler (University of Surrey) | **Pages**: ~8 | **Sections**: 5 | **Year**: 1988 | **Generated**: 2026-05-24

## How to Use This Skill

- **Without arguments** — load core frameworks for reference
- **With a topic** — ask about `center-finding`, `AHT`, `complexity`, or another indexed topic
- **With section** — ask for `ch02` (General Principles) or another section file
- **Browse** — ask "what sections do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read the relevant section file before answering.

---

## Core Frameworks & Mental Models

### Framework 1: Two-Stage Hough Transform Decomposition

**The problem**: Detecting an ellipse requires 5 parameters. A naive 5D accumulator with `a` intervals per axis needs `a^5` storage — impractical even for modest `a`.

**The solution**: Decompose into two sequential stages, each operating in lower-dimensional space:
- **Stage 1** → find center (x₀, y₀) via 2D accumulator
- **Stage 2** → find remaining 3 params (B, D, C) via AHT on a 9×9×9 accumulator

**Use this when**: You need to detect multiple ellipses in noisy or occluded images without exhausting memory.

**Key insight**: Once the center is known, translate origin there. The ellipse equation simplifies to:
```
X² + BY² + 2DXY + C = 0,  B - D² > 0
```
reducing the remaining search from 5D to 3D.

---

### Framework 2: TM-Line Center-Finding Constraint (the novel contribution)

**Classical approach (Tsukune & Goto, Tsuji & Matsumoto)**: Find pairs of edge points with **parallel tangents** → midpoint is the center. **Fails when the ellipse arc is asymmetric** (occlusion, self-occlusion).

**This paper's approach**: Use pairs of edge points with **non-parallel tangents**:
1. Take two edge points P(x₁,y₁) and Q(x₂,y₂) with slopes s₁, s₂ (from gradient)
2. Compute intersection point T(t₁, t₂) of the two tangent lines
3. Compute midpoint M(m₁, m₂) of segment PQ
4. **The ellipse center lies on line TM** — this is always true, no symmetry needed

**TM line equation**:
```
y(t₁ - m₁) = x(t₂ - m₂) + (t₂m₁ - t₁m₂)
```
where:
```
t₁ = (y₁ - y₂ - s₁x₁ + s₂x₂) / (s₂ - s₁)
t₂ = s₁(t₁ - x₁) + y₁
```

**Optimization**: Only vote for the segment MN (not the full line), where L = length(MN) is set by prior knowledge of expected ellipse size.

**Pairing constraint** (avoid cross-ellipse pairs):
```
|x₁ - x₂| < δ₁  AND  |y₁ - y₂| < δ₂
```

---

### Framework 3: Adaptive Hough Transform (AHT) for 3-Parameter Estimation

**Use for**: Stage 2 — finding B, D, C from subset of image points already associated with a candidate center.

**Algorithm** (coarse-to-fine):
1. Start with a **fixed 9×9×9 accumulator** spanning large initial ranges
2. Accumulate votes: each image point evaluates which accumulator cells its surface in (B, D, C) space intersects
3. Find the cell with maximum count
4. **Center the accumulator** on that cell and **reduce each range to 1/3**
5. Repeat until required resolution is reached (max ~10 iterations in practice)

**Why it works**: The AHT independently varies resolution per parameter — critical because C has a much larger range than B and D.

**Cost per iteration**:
```
C_iter = 3 × 9² × n_points
```
**Total Stage 2 cost**: ≈ `10 × 3 × 9² × n_i` per ellipse.

---

### Framework 4: Iterative Ellipse Extraction with Point Deletion

**Use for**: Images containing multiple overlapping/occluding ellipses.

**Algorithm**:
1. Run Stage 1 (center finding) on all edge points
2. Accept center if accumulator count > threshold
3. Run Stage 2 to get B, D, C for that center
4. **Delete all image points** associated with the found ellipse
5. Repeat Stage 1 on remaining points
6. Stop when maximum accumulator count < threshold

**Why necessary**: Without point deletion, background votes from cross-ellipse pairs clutter the center-finding space and make peak detection unreliable.

**Trade-off**: O(k²) cost for k ellipses — finding the i-th ellipse reaccumulates the HT i times.

---

### Computing Ellipse Axes and Rotation from B, D, C

Once B, D, C are known (for equation X² + BY² + 2DXY + C = 0 centered at origin):

```
a = sqrt(-2C / [(B+1) - sqrt((B-1)² + 4D²)])   # semi-major axis
b = sqrt(-2C / [(B+1) + sqrt((B-1)² + 4D²)])   # semi-minor axis
θ = 0.5 × arctan(2D / (1 - B))                  # rotation angle
```

---

## Section Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction.md) | Introduction | Hough Transform motivation, 5-param problem |
| [ch02](chapters/ch02-general-principles.md) | General Principles | TM-line, AHT, two-stage decomposition, formulas |
| [ch03](chapters/ch03-complexity.md) | Complexity Analysis | O(n²) pairing, O(k²) multi-ellipse cost |
| [ch04](chapters/ch04-experimental-results.md) | Experimental Results | Single ellipse, 8-ellipse image, parameter accuracy |
| [ch05](chapters/ch05-discussion.md) | Discussion & Conclusions | Applicability, limitations, future work |

## Topic Index

- **Accumulator array** → ch01, ch02, ch03
- **Adaptive Hough Transform (AHT)** → ch02, ch03
- **Axes computation (a, b, θ)** → ch02
- **Center finding** → ch02, ch04
- **Complexity (O-notation)** → ch03
- **Edge gradient / tangent direction** → ch02, ch03
- **Ellipse equation** → ch01, ch02
- **Multiple ellipses / occlusion** → ch01, ch02, ch04
- **Pairing constraints (δ₁, δ₂)** → ch02, ch03
- **Point deletion** → ch02, ch03
- **Spacek edge detector** → ch04
- **TM-line constraint** → ch02
- **Two-stage decomposition** → ch01, ch02

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — algorithm steps and design patterns
- [cheatsheet.md](cheatsheet.md) — quick-reference formulas and decision guide

---

## Scope & Limits

This skill covers the Yuen et al. 1988 paper only. For implementation details not in the paper (e.g. GPU acceleration, real-time variants), combine with project-specific tools or other references.
