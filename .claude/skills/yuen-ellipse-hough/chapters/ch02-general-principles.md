# Section 2: General Principles

## Core Idea
The two-stage method decomposes 5-parameter ellipse detection: Stage 1 finds the center (x₀, y₀) using the novel TM-line constraint; Stage 2 finds B, D, C using the Adaptive Hough Transform on a coarse-to-fine 9×9×9 accumulator.

## Frameworks Introduced

### TM-Line Center-Finding Constraint
- **Exact formulation**: Given edge points P(x₁,y₁) and Q(x₂,y₂) on the same ellipse with non-parallel tangent slopes s₁, s₂ — the ellipse center lies on segment MN, where T is the tangent intersection and M is the midpoint of PQ.
- When to use: Always prefer over parallel-tangent midpoint method; works even when the arc is asymmetric
- How:
  1. Compute T: `t₁ = (y₁ - y₂ - s₁x₁ + s₂x₂)/(s₂-s₁)`, `t₂ = s₁(t₁-x₁)+y₁`
  2. Compute M: `m₁=(x₁+x₂)/2`, `m₂=(y₁+y₂)/2`
  3. Accumulate votes along TM segment of length L

### Adaptive Hough Transform (AHT)
- **Exact formulation**: Fixed 9×9×9 accumulator iteratively centers on the maximum cell and reduces range to 1/3, converging in ≤10 iterations.
- When to use: Stage 2 — estimating B, D, C from centered ellipse equation
- How: Accumulate → find max cell → re-center + reduce range by 3× → repeat

## Key Concepts
- **Centered ellipse equation**: `X² + BY² + 2DXY + C = 0, B - D² > 0` (after translating to estimated center)
- **Pairing constraint**: Only pair (x₁,y₁), (x₂,y₂) if `|x₁-x₂| < δ₁` AND `|y₁-y₂| < δ₂` — avoids cross-ellipse pairs
- **Simplified voting direction**: If |slope of TM| ≤ 1, vote in x-direction; if > 1, vote in y-direction. Only vote MN (not full line).
- **Vote segment length L**: Set by prior knowledge of expected ellipse size
- **Parameter range**: C has much larger range than B and D — AHT handles this by independent per-parameter resolution

## Formulas

### TM Line
```
y(t₁ - m₁) = x(t₂ - m₂) + (t₂m₁ - t₁m₂)
```

### Recovering Ellipse Geometry from B, D, C
```
a = sqrt(-2C / [(B+1) - sqrt((B-1)² + 4D²)])
b = sqrt(-2C / [(B+1) + sqrt((B-1)² + 4D²)])
θ = 0.5 × arctan(2D / (1 - B))
```

### Differentiation of centered equation (basis for 2D sub-HT in prior work)
```
dX/dY = -(2DX + 2BY) / (2X + 2DY)
```

## Anti-patterns
- **Using parallel-tangent midpoint method**: Fails whenever the visible arc is asymmetric about the center (common in occlusion). Use TM-line instead.
- **Skipping the pairing constraint**: Cross-ellipse pairs add background clutter to the accumulator, making peak detection unreliable.
- **Using a large fixed accumulator for Stage 2**: Memory cost of C range makes this impractical. Use AHT's coarse-to-fine approach.
- **Voting the full TM line**: Wastes computation. Only vote segment MN of prespecified length L.

## Key Takeaways
1. The TM-line constraint is valid for any two non-parallel-tangent edge points on the same ellipse — no symmetry assumption required
2. AHT independently adapts resolution per parameter — critical because C range >> B, D range
3. The iterative point-deletion loop (find center → Stage 2 → delete → repeat) is necessary for multi-ellipse images but costly: O(k²) for k ellipses

## Connects To
- **Ch03**: Complexity analysis of the pairing and accumulation steps
- **Ch04**: Experimental values for δ₁=5, δ₂=30, L=30 pixels used in practice
