# Chapter 6 — Analysis of HT Performance and Parameters

## Variance of parameter estimates under measurement error

Shapiro's program [10–12, 14, 17–22, 26] derived variance of parameter estimates as a function of measurement error for HTs where each image point produces a single vote. Sklansky [23] proposed a **geometric construction** for straight-line detection used to study the precision of curves derived from estimated parameters. Shapiro & Iannino [26] extended the construction to noisy measurements, deriving relations between **quantization error** and **parameter accuracy** — useful guides for choosing accumulator quantization.

## Finite-retina background bias (Cohen & Toussaint [13])

A uniform distribution of image points on a finite (e.g., circular) retina **does not** produce a uniform background in parameter space.

- Lines through the **center** of the retina are long → contribute many counts to **low-ρ** bins.
- Lines near the **edge** are short → contribute few counts to **high-ρ** bins.

⇒ A globally derived, ρ-independent threshold is unsuitable for peak detection. Cohen–Toussaint remedies:
1. **Empirical background subtraction.**
2. **Non-linear ρ-axis quantization** so each bin receives equal counts from random noise.

## Generalization (Alagar & Thiel [30])

For detecting m-D lines in n-D space:
- Cohen–Toussaint's non-linear ρ quantization makes the count distribution uniform only **for each fixed θ**.
- In `(ρ, θ)`, the invariant for uniform image → uniform parameter is **`(dρ, dθ)`**.
- Their analysis yields a parameter-space quantization related to a **beta distribution**.

## Robustness measures (P, R, G)

If an image truly contains `Mₖ` lines and the algorithm reports `mₖ` of which `m_T` match true lines and `m_F` are false (Eq. 15):

```
P (precision) = m_T / m_k
R (recall)    = m_T / M_k
G (goodness)  = (m_T - m_F) / M_k
```

A single composite score can be a linear combination of `P`, `R`, `G`. Alagar & Thiel use these to empirically compare quantization schemes.

## Maître's analysis [95]

Most recent (as of survey) treatment of random-noise count density. Confirms Alagar–Thiel's `(ρ, θ)` quantization for a circular image via a different derivation. Also analyzes:
- `(m, c)` count density.
- **Rectangular image** cases.
- **SNR for line detection** as a function of reliability and precision of the linear feature extractor (signal-processing framing).

## Van Veen & Groen [38]

For real (non-random) image lines in `(ρ, θ)`, analytic results for the **shape and extent of parameter peaks** as functions of image quantization, parameter quantization, and line-segment width. Suggested weighting accumulator votes by edge-gradient magnitude to sharpen peaks.

## Brown's imaging-model view [48]

Recast the HT as a **linear imaging problem**:

- **Feature point-spread function (feature psf):** the pattern of parameter-space counts produced by a single image point.
- **Parameter point-spread function (parameter psf):** the superposition of feature psfs for all image points of an object — a central peak plus a sidelobe background.

For continuous, noiseless conditions, the parameter psf is **the image of the shape through a pinhole-like camera whose pinhole aperture is the shape itself** — i.e., **autoconvolution** of the shape.

- For many shapes (including simple lines) parameter psfs are **extended ridges, not sharp symmetric peaks** → big implication for peak finders.
- For multi-object scenes, mutual interference between objects' parameter and feature psfs degrades detection → motivated **CHough** (see [[ch05-peak-detection]]).

## Davies — matched-filter view [110, 111]

Within a matched-filter framework, **vote weight ∝ edge-gradient magnitude × a priori edge gradient**. Davies sharply distinguishes:

- **Accuracy of object location** vs.
- **Sensitivity of object detection.**

Notes that sensitivity is often sacrificed for computational savings — keep this distinction explicit when comparing algorithms.

## HT vs. statistical signal detection (Hunt et al. [116, 117])

Comparison of HT line detection vs. signal-detection-theory line detection under additive noise (Gaussian, Laplacian, uniform).

- Signal-detection methods explicitly use line length, a-priori line distribution, and noise distribution.
- **Result:** there *exists* a signal-detection method superior to HT in both detection and location performance.
- **Caveat:** if noise characteristics are not well known, HT wins on robustness; signal-detection's edge is paid for in computation; and results are for a *single* line.

## Take-aways for analysis

1. Always model the finite-retina bias before setting thresholds.
2. Real parameter peaks are usually ridges, not points — pick peak finders accordingly.
3. Quote P/R/G or an equivalent composite, not just qualitative results.
4. Edge-gradient weighting has both empirical and matched-filter justification.
5. HT's competitive edge is **robustness when noise is poorly characterized**, not raw detection optimality.

Cross-refs: [[ch04-efficient-accumulation]], [[ch05-peak-detection]], [[ch07-ht-and-other-transforms]], [[cheatsheet]].
