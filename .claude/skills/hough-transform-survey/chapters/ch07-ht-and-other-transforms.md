# Chapter 7 — The HT and Other Transforms

## Radon transform (Deans, 1981 [32])

The HT for linear features is a **special case of the Radon transform** (known since 1917; richly developed in computer-aided tomography). Radon transform on a 2-D function `f(x, y)` (Eq. 16):

```
R(ρ, θ) = ∫∫ f(x, y) · δ(ρ - x cos θ - y sin θ) dx dy
```

The δ forces integration of `f(x, y)` along the line `ρ = x cos θ + y sin θ` (Eq. 17). Radon yields projections of `f` for offset `ρ` and orientation `θ`.

**Equivalence:** Radon ≡ HT for binary images.

## Computation routes inherited from Radon

- **Radon ↔ Fourier transform** [96, 129] — use Fourier-slice/projection-slice machinery. Has been used for line detection and enhancement in noisy SAR images.
- **Parallel incremental algorithms for digital Radon** — Suter [82].
- **Generalization to non-linear shapes:** replace the δ argument with a function that forces integration along contours of the shape.

## Optical / hybrid implementations

Radon equivalence opened the door to real-time analog optics:
- **Coherent optical processor** — Eichmann & Dong [52].
- **Incoherent optics** — Stier & Shori [99].
- **Hybrid optical + digital** — Gindi & Gmitro [62].

## Other projection-flavored work

- **Sloan [42]** — "dot-product space" representation for blob-like objects; uses local shape evidence projected into a transform space for global judgement; same occlusion robustness as HT.
- **Nagoa & Nakajima [124]** — variable-size slit method: investigate the image by projecting onto edges of a movable rectangular window of arbitrary size/orientation; related to HT.
- **Mostafavi & Shah [57]** — implemented HT-as-projection using commercially available image-processing hardware features → rapid line detection.
- **Sanz & Dinstein [80, 126–128]** — extended the projection idea. Algorithm:
  1. For a fixed orientation `θ`, multiply the binary line image by a **template image** where each pixel on a line at normal distance `p` from the origin has intensity `p`.
  2. The **gray-level histogram** of the product has peaks only at the intensity equal to `p` of each line.
  3. Repeat for each `θ` → full HT.
  - Exploits pipelined hardware for template generation, image convolution, and histogram computation. Generalizes to shapes other than lines via different template images.

## Why this chapter matters

If you have access to:
- A **Fourier engine** → you can compute the HT via FFT slices.
- An **optical bench** → real-time HT is on the table.
- **Pipelined image-processing silicon** with fast histogramming → use Sanz–Dinstein.

Pick the equivalence that matches your hardware before writing a brute-force HT.

Cross-refs: [[ch06-performance-analysis]], [[ch09-architectures]], [[patterns]], [[glossary]].
