# Cheat Sheet — Yuen et al. Ellipse Detection

## Key Formulas

| Symbol | Formula | Notes |
|--------|---------|-------|
| Ellipse (general) | X² + BY² + 2DXY + C = 0 | Centered at origin; B−D²>0 |
| Tangent intersection t₁ | (y₁−y₂−s₁x₁+s₂x₂)/(s₂−s₁) | s₁,s₂ = tangent slopes |
| Tangent intersection t₂ | s₁(t₁−x₁)+y₁ | |
| Midpoint m₁, m₂ | (x₁+x₂)/2, (y₁+y₂)/2 | |
| Semi-major axis a | √(−2C / [(B+1) − √((B−1)²+4D²)]) | |
| Semi-minor axis b | √(−2C / [(B+1) + √((B−1)²+4D²)]) | |
| Rotation angle θ | 0.5 × arctan(2D / (1−B)) | radians |

## Algorithm Decision Guide

```
Do you need to detect ellipses?
├─ Single ellipse, symmetric arc? → Parallel-tangent midpoint (simpler)
└─ Partial/occluded arc OR multiple ellipses?
   └─ Use two-stage HT (this paper)
      ├─ Stage 1: TM-line voting → get center (x₀, y₀)
      └─ Stage 2: AHT 9×9×9 → get B, D, C → compute a, b, θ
```

## Parameter Selection Guide

| Parameter | Meaning | Typical value | Effect if too large | Effect if too small |
|-----------|---------|--------------|---------------------|---------------------|
| δ₁ | Max x-pair distance | 5 px | Cross-ellipse pairs, clutter | Miss valid pairs |
| δ₂ | Max y-pair distance | 30 px | Cross-ellipse pairs, clutter | Miss valid pairs |
| L | MN segment length | 30 px | Extra votes, slower | Miss center |
| Threshold | Min votes to accept center | empirical | False detections | Missed ellipses |

## Complexity Summary

| Stage | Cost | Dominant factor |
|-------|------|----------------|
| Stage 1 (single ellipse) | O(n²·L) | n = edge points per ellipse |
| Stage 2 (AHT) | ≈ 10 × 3 × 81 × n | Always ≤10 iterations |
| k ellipses total | O(k²) × single | Point deletion + reaccumulation |

## Validity Check

Before using B, D, C:
```
B - D² > 0   ← must be positive for a real ellipse
C < 0        ← required for √(-2C) to be real
```

## Quick Implementation Checklist

- [ ] Edge detector provides gradient directions (not just positions)
- [ ] Set δ₁, δ₂ to exclude cross-ellipse pairs
- [ ] Set L based on expected ellipse size range
- [ ] Initialize AHT ranges large enough to encompass all valid ellipses
- [ ] Set accumulator threshold to reject spurious peaks
- [ ] After each detected ellipse: delete supporting points before reaccumulating
- [ ] Validate B−D²>0 before computing axes
