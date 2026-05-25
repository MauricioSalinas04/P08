# Patterns & Algorithms — Ellipse Detection Using the Hough Transform

## Pattern 1: Two-Stage Hough Transform for Ellipses

**When to use**: Detecting ellipses in images with noise, partial occlusion, or multiple overlapping ellipses.

**How**:
1. Extract edge points and their gradient directions
2. Stage 1: accumulate TM-line votes in a 2D center accumulator
3. Threshold the accumulator; accept peaks as candidate centers
4. Stage 2: for each candidate center, translate origin, run AHT on `X² + BY² + 2DXY + C = 0`
5. Compute a, b, θ from B, D, C
6. Delete associated points; repeat for remaining ellipses

**Trade-offs**: Higher computational cost than direct 5D HT? No — 5D is intractable. Trade-off is O(n²) pairing in Stage 1 vs. accuracy of center finding.

---

## Pattern 2: TM-Line Center Voting

**When to use**: Stage 1 of the two-stage method; works even when visible arc is asymmetric.

**How**:
```
For each valid pair (P=(x1,y1,s1), Q=(x2,y2,s2)):
  if |x1-x2| > δ1 or |y1-y2| > δ2: skip
  if s1 ≈ s2: skip (parallel tangents → use midpoint method instead, or just skip)
  
  # Compute tangent intersection T
  t1 = (y1 - y2 - s1*x1 + s2*x2) / (s2 - s1)
  t2 = s1*(t1 - x1) + y1
  
  # Compute midpoint M
  m1 = (x1 + x2) / 2
  m2 = (y1 + y2) / 2
  
  # Compute slope of TM
  slope_TM = (t2 - m2) / (t1 - m1)  # if t1 != m1
  
  # Vote along segment MN of length L centered at M toward T
  # If |slope_TM| <= 1: step in x, compute y
  # If |slope_TM| > 1:  step in y, compute x
  for point in MN:
    accumulator[point] += 1
```

**Trade-offs**: O(n²) pairs; but adding δ₁, δ₂ constraints and restricting MN length keeps practical cost manageable.

---

## Pattern 3: Adaptive Hough Transform (AHT) — 3-Parameter Estimation

**When to use**: Stage 2 — finding B, D, C from a set of edge points with known center.

**How**:
```
Initialize range: B_range=[B_min, B_max], D_range=[D_min, D_max], C_range=[C_min, C_max]
Accumulator: 9×9×9

repeat up to 10 times:
  Clear accumulator
  For each edge point (X, Y):
    Evaluate which accumulator cells (B_cell, D_cell, C_cell) satisfy:
      X² + B*Y² + 2*D*X*Y + C = 0
    (each point defines a surface in B,D,C space; find intersecting cells)
    accumulator[B_cell][D_cell][C_cell] += 1
  
  (B*, D*, C*) = argmax(accumulator)
  
  Center each range on the selected cell
  Reduce each range to 1/3 of previous size
  
  if all ranges < required_resolution: break

return (B*, D*, C*) = center of final ranges
```

**Trade-offs**: Fixed memory (729 cells); always converges in ≤10 iterations; independent resolution per axis. Trade-off: requires subset of points already associated with one center.

---

## Pattern 4: Iterative Multi-Ellipse Extraction

**When to use**: Image contains k > 1 ellipses.

**How**:
```
remaining_points = all_edge_points
ellipses = []

while True:
  Run Stage 1 (TM-line voting) on remaining_points
  (cx, cy), peak_count = find_accumulator_peak()
  
  if peak_count < threshold: break
  
  supporting_points = points consistent with (cx, cy)
  Run Stage 2 (AHT) on supporting_points with center (cx, cy)
  B, D, C = AHT result
  a, b, θ = compute_axes(B, D, C)
  
  ellipses.append(Ellipse(cx, cy, a, b, θ))
  remaining_points = remaining_points - supporting_points

return ellipses
```

**Trade-offs**: O(k²) total cost (each removal triggers full reaccumulation). Reliable for moderate k; future work needed for large k.

---

## Pattern 5: Axis Recovery from B, D, C

**When to use**: After Stage 2, to get human-interpretable ellipse parameters.

**How**:
```python
import math

def axes_from_params(B, D, C):
    discriminant = math.sqrt((B - 1)**2 + 4 * D**2)
    a = math.sqrt(-2 * C / ((B + 1) - discriminant))  # semi-major
    b = math.sqrt(-2 * C / ((B + 1) + discriminant))  # semi-minor
    theta = 0.5 * math.atan2(2 * D, 1 - B)             # rotation angle (radians)
    return a, b, theta
```

**Trade-offs**: Direct closed-form; no iteration needed. Valid only when B - D² > 0 (true ellipse condition).
