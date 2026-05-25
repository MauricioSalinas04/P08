# Chapter 8 — Applications of the HT

The survey enumerates concrete applications. Use this chapter as a catalog of precedents.

## Industrial inspection / mechanical parts

- **Wallace [60, 130]** — industrial inspection system using linear + circular feature detection in a hypothesis-and-test vision pipeline.
- **Arbuschi, Cantoni, Musso [44]** — GHT for detection and location of mechanical parts.

## Linear feature detection

- **Roads / vehicle guidance** — Inigo et al. [66]: detect straight edges of roads/tracks → guide a robot vehicle.
- **Gauge inspection** — Dyer [51]: angular position of a straight pointer recovered from images for sequential analog inputs; no detailed gauge knowledge required; high-speed hardware implementable.
- **Seismograms** — Huang et al. [74]: direct/refracted waves → straight lines; reflected waves → hyperbolas. HT attractive because seismic data is cluttered and fragmented.
- **Hebrew character recognition** — Kushnir, Abe, Matsumoto [55, 77]: peaks in `(ρ, θ)` used as features. 99.6 % on machine-printed (18 alphabets); 86.9 % on hand-printed.
- **Fingerprint ridge counting** — Lin & Dubes [56]: ridges → distinct `(ρ, θ)` peaks. Found *less* successful than conventional approach: HT expensive, threshold hard to set.

## Target detection & tracking

- **Cowart, Snyder, Rueder [50]** — frame-difference images: nonmaneuvering targets appear as line segments → HT especially good for **multiple simultaneous targets**.
- **Shibata & Frei [36]** — single rectangular target via the pattern of **4 peaks** in `(ρ, θ)` (one per side). Real-time design envisaged.
- **Skingley & Rye [129]** — faint lines in SAR images: peak detection, line endpoint detection, false-alarm removal, detection-probability analysis.
- **Shu et al. [135]** — edge contours of resist lines in SEM images. Augment accumulator with a **bit array** so incrementation is conditional on its status → preferentially detect *connected* edge segments. Adaptive threshold by orientation/location. Systolic architecture proposed.
- **Thomson & Sokolowska [136]** — cleavage cracks in mineral micrographs.
- **Nixon [79]** — detect linear variations of illumination across images; efficient algorithm to remove the artifact.

## Generalized HT applications

- **Hakalahti et al. [63, 78]** — general shape recognition with contour curvature + local image contrast; two-stage coarse-then-fine.
- **Davies [88]** — detecting known-size polygons via GHT; symmetry assumptions reduce accumulator size.
- **Davies [87]** — detecting sharp and blunted **corners**; tradeoff between accuracy of corner location and sensitivity for corner detection determined by reference-point choice.
- **Costabile & Pieroni [85]** — HT to detect corresponding edges in polygon-approximated shapes.
- **Turney, Mudge, Volz [83]** — Hough-like shape detection by matching **overlapping boundary subtemplates**; each subtemplate weighted by its discriminative power.
- **Yam & Davis [39]** — image registration with HT.

## Motion analysis

- **Fennema & Thompson [25]** — rigid-object translational velocity related to image-intensity rate of change + local spatial gradient → Hough accumulation. Strong for multiple independently translating objects and occluded scenes.
- **Jayaramamurthy & Jain [53]** — HT used in segmenting textured objects moving against textured background.
- **Samy & Bozzo [71]** — match objects across image sequences; accumulator increments depend on observed local velocities.
- **Ballard & Kimball [45]** — 9 rigid-body motion params (position, translational velocity, rotational velocity) from depth + 2-D optic flow; coupling iteration between flow/depth estimates and motion estimates.
- **Adiv [43]** — GHT for motion patterns from a displacement-field image. Small objects → small peaks; mitigated by coarse-resolution detection for large objects and subimage detection for small ones; iterative focusing for parameter refinement. Recovered rotation, expansion, translation.
- **Radford [98]** — translation + rotation motion in a 3-D parameter space `(ρ, θ, l)` (l = inter-frame motion length). Finds focus of expansion / center of rotation; groups similar-motion points for segmentation.

## Viewing parameters (model fitting)

- **Ballard & Sabbah [46]** — sequential determination of scale → orientation → translation subgroups.
- **Silberberg, Davis, Harwood [72]** — viewing parameters matching line-segment image features with a 3-D model. Backprojection efficient via heuristics (e.g., match only if projected edge length ≥ measured image length); used iterative focusing.

## Stereo / vision

- **Peek, Mayhew, Frisby [70]** — gaze angle `g` and focus distance `d` recovered from vertical disparity (Eq. 18). Accumulator picks the best global viewing parameters.

## 3-D range data

- **Henderson & Fai [64]** — GHT for object detection in laser range data; choose distinctive feature points to avoid combinatorial blow-up; detect planar segments first.
- **Muller & Mohr [67]** — fit quadric surfaces (and planes) to local neighborhoods; accumulate in the parameter space of the best-fitting surface type; divide-and-conquer focusing.
- **Dhome & Kasvand [89]** — GHT for 3-D polyhedra; store polyhedra as records of attribute + adjacent-face relations; hierarchical clustering identifies dominant hypotheses.

## Data compression / other

- **Shapiro [28]** — HT for **contour / waveform compression**: a curve as a concatenation of segments from known shapes; each segment → cluster in an appropriate parameter space; reconstruct curve from segment parameters + transition points.
- **Poelzleitner [97]** — HT-inspired method for segmenting wooden boards prior to quality classification.
- **Kasif et al. [54]** — GHT for **subgraph matching** in geographical maps; competes with backtracking and relaxation labeling; implementable on connected simple processors.

## Decision guide for "should I use HT here?"

| Scene characteristic | HT verdict |
|----------------------|-----------|
| Cluttered, missing data, parametric shapes | ✓ Strong candidate. |
| Multiple instances of the same shape | ✓ Each gives its own peak. |
| Heavy occlusion | ✓ Graceful degradation. |
| Tight noise model already known | ✗ Use statistical signal detection (better optimal performance). |
| Need cheap real-time on existing hardware | Check Sanz–Dinstein or optical equivalents (see [[ch07-ht-and-other-transforms]]). |
| High-dimensional naive parameterization | ✓ But only with decomposition + focusing (see [[ch03-shape-parameterizations]], [[ch04-efficient-accumulation]]). |

Cross-refs: [[ch01-introduction]], [[ch03-shape-parameterizations]], [[ch04-efficient-accumulation]], [[ch06-performance-analysis]], [[patterns]].
