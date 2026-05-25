# Chapter 5 — Peak Detection in the HT Accumulator

Once accumulation is done, you must turn the count distribution into shape estimates. The accumulator is not the answer; peak detection is.

## Thresholding

- **Global threshold** — simplest: any cell above threshold is a candidate.
- **Sources of threshold:** prior knowledge; automatic selection from count distribution (e.g., a fixed fraction of the maximum single-bin count).
- **Caveat:** finite-image bias (see [[ch06-performance-analysis]] Cohen–Toussaint) makes a single global threshold unsafe — peak heights depend on where the line falls.

## Converging squares (O'Gorman & Sanderson [68])

- Resolution-pyramid algorithm for peak detection in multidimensional data.
- Sequentially investigate from low to high resolution: compare several **overlapping hypercube-shaped regions**; recurse into the densest.
- **Performance:** robust to noise; **8–10× faster** than common peak detectors.
- **Limitation:** assumes ≈ cubic peaks. Elongated or non-convex peaks are mishandled.
- Brown [49] explored a related pyramid approach for n-D histograms.

## Weighted voting (peak sharpening)

Make confident features vote more.

- **Edge-gradient-magnitude weight** [31, 38] — typical heuristic; usually informally justified.
- **Thrift–Dunn influence functions [58]** — each image feature increments **every** accumulator bin by an amount that decays with distance from the feature's parameter hypersurface. Connects HT to curve-fitting. Reported superior to standard HT on noise-perturbed simple shapes.

## Filtering the accumulator (Leavers & Boyce [92, 121, 122])

For `(ρ, θ)`:
- A true image **line** produces a characteristic **"butterfly"** distribution in the accumulator. Design a convolution mask that enhances butterflies.
- A true image **circle** produces a broad band of counts with a characteristic falloff at the band edges. A filter enhances the edges, turning the band into two roughly linear edges in filtered `(ρ, θ)`. Then **run a second line-detection HT** on the filtered accumulator to recover those edges → circle parameters.

## Backtransform sharpening (Gerig & Klein [91, 114])

- Used for circular cell boundaries that are partially missing / obscured / distorted.
- After accumulation, **assign each image point to a unique parameter cell**: of the cells its hypersurface intersects, pick the one with the largest count.
- **Re-accumulate** using this unique image-point-to-cell assignment.
- Result: **strong sharpening** of peaks.

## Projection of the accumulator (Eckhardt & Madedechner [131])

- Project the full HT accumulator into smaller subspaces and interpret there.
- **Theorem-like result:** if the composite operation (HT accumulation + projection) is **linear and translation-invariant** → result is trivial and useless.
- ⇒ Useful projection methods must involve **non-linear** operators.

## CHough — Complementary HT (Brown [48])

- Image points contribute **positively** to some parameter values **and negatively** to others.
- Net effect: cancels some sidelobe contributions, producing more prominent peaks.
- Most useful when transforms produce **symmetric** parameter point-spread functions.
- Brown's findings: vs. standard HT, CHough reduced **both mean and variance** of background; more robust to spurious features; **more sensitive to quantization**.

## Differential evidence (Davies [111])

A GHT-style sharpening for line localization: if the line length is known, an edge point provides evidence for **possible** locations *and* evidence about positions where the line **cannot** occur. Accumulate positive and negative evidence in separate spaces; the **positive space** gives best detection, the **difference signal** gives best localization.

## Decision guide

| Symptom in accumulator | Recommended treatment |
|------------------------|----------------------|
| Peaks lost in finite-retina bias | Non-linear ρ-axis quantization (Cohen–Toussaint, see [[ch06-performance-analysis]]); local thresholds. |
| Smeared "butterfly" peaks for lines | Leavers–Boyce butterfly filter. |
| Broad-band peaks for circles | Leavers–Boyce edge-enhancement + second line HT. |
| Cluttered overlapping peaks | Gerig–Klein backtransform sharpening, or CHough. |
| Sidelobe interference between objects | CHough. |
| Need fast detection of localized peaks | Converging squares. |
| Need to interpret accumulator structurally | Eckhardt–Madedechner non-linear projection. |

Cross-refs: [[ch04-efficient-accumulation]], [[ch06-performance-analysis]], [[patterns]], [[cheatsheet]].
