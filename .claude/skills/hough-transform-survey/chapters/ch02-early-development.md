# Chapter 2 — Early Development of the HT

## Origin

- **Paul Hough (1962)** — U.S. patent 3,069,654: a method for recognizing complex point patterns. Originally used to detect curves in **bubble chamber photographs** [refs 2, 4].
- **Rosenfeld (1969)** — brought the HT to the mainstream image-processing community via *Picture Processing by Computer*.

## Duda & Hart (1972) — the `(ρ, θ)` parameterization (Eq. 14)

```
ρ = x cos(θ) + y sin(θ)
```

Replaces the singular `(m, c)` parameterization (slope `m → ∞` blows up). Each image point becomes a **sinusoidal curve** in the two-parameter `(ρ, θ)` space. This became the dominant line parameterization.

## Polyhedral scene parsing

- **O'Gorman & Clowes (1973/76)** — used HT to recover straight lines in digitized images of polyhedral block scenes.

## Shapiro's analytical program (1970s)

Numerous papers [7, 10–12, 14, 17–22, 26, 28] analyzed:
- Choice of parameter-space quantization.
- Effect of noisy input data on parameter accuracy.
- Variance of parameter estimates as a function of measurement error.

## Background-count statistics

- **Cohen & Toussaint (1977)** — distribution of background counts for random noise points in finite-size images.
- **Van Veen & Groen (1981)** — effect of discretization in both image and parameter spaces on detection.

## Shapes beyond straight lines

- **Kimme, Ballard, Sklansky (1975)** — circle detection ("finding circles by an array of accumulators"); medical imaging task. Crucially used **edge direction** to restrict parameter range — a recurring theme.
- **Parabolas and ellipses** [refs 16, 24, 59] — Tsuji & Matsumoto, Wechsler & Sklansky, Tsukune & Goto. Standard tactic: keep dimensionality low by **determining groups of parameters in sequential stages**.

## From specific shapes to arbitrary shapes

- **Merlin & Farber (1975)** — generalized HT for arbitrary shape at a *given* orientation and *given* scale.
- **Stockman & Agrawala (1977)** — demonstrated HT is just an efficient implementation of template matching.
- **Sklansky (1978)** — same observation, but added that HT is *potentially more useful* because it can incorporate local constraints to improve matching efficiency.
- **Ballard (1981) — Generalized Hough Transform (GHT)** [refs 29, 31]: extended Merlin–Farber to *arbitrary* orientation and scale. Key to success: **use directional edge information**.

## Take-aways

- The `(ρ, θ)` parameterization is the historical default for lines — use it unless you have a reason not to.
- Edge direction is the most consistently cited efficiency lever across the literature.
- Parameter decomposition (treating sub-groups sequentially) is older than GHT and has always been the way to keep dimensionality manageable.

Cross-refs: [[ch03-shape-parameterizations]], [[ch04-efficient-accumulation]], [[patterns]], [[glossary]].
