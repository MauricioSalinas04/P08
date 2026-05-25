# Glossary — Ellipse Detection Using the Hough Transform

**Accumulator array** — Discrete N-dimensional grid of counters indexed by parameter values; each edge point votes into cells consistent with its evidence. The cell with the most votes identifies the most likely shape. (Ch1, Ch2)

**Adaptive Hough Transform (AHT)** — Iterative coarse-to-fine peak-finding algorithm: uses a fixed small accumulator (9×9×9) that progressively centers on the maximum cell and reduces parameter range by 3× per iteration, converging in ≤10 steps. (Ch2, Ch3)

**B, D, C parameters** — The three parameters of a centered ellipse equation `X² + BY² + 2DXY + C = 0`. B and D describe the shape and orientation; C is a scale factor. Must satisfy `B - D² > 0`. (Ch2)

**Center finding** — Stage 1 of the two-stage method: locating the center (x₀, y₀) of an ellipse using a 2D accumulator. (Ch2)

**Coarse-to-fine** — A search strategy that starts with low resolution over a large range, identifies a promising region, and increases resolution iteratively. Used in AHT for Stage 2. (Ch2, Ch3)

**δ₁, δ₂ (delta constraints)** — Proximity thresholds for pairing edge points: only pair (x₁,y₁) and (x₂,y₂) if `|x₁-x₂| < δ₁` AND `|y₁-y₂| < δ₂`. Experimental values: δ₁=5, δ₂=30 pixels. (Ch2, Ch4)

**Edge gradient direction** — The direction perpendicular to an edge contour at a given pixel, used to compute the tangent slope. Essential for the TM-line constraint and the differentiation-based Stage 2 formulation. (Ch1, Ch2)

**Ellipse** — A conic section defined by 5 parameters (in general position). The general equation is `X² + B'Y² + 2D'XY + 2E'X + 2G'Y + C' = 0`. When centered at origin: `X² + BY² + 2DXY + C = 0`. (Ch1, Ch2)

**Hough Transform (HT)** — Parameter estimation method that maps image evidence (edge points) into a multi-dimensional parameter space via voting; robust to noise and fragmentation. (Ch1)

**L (segment length)** — The prespecified length of segment MN along which votes are cast in the center-finding accumulator. Set based on prior knowledge of ellipse sizes. Experimental value: 30 pixels. (Ch2, Ch3)

**M (midpoint)** — The midpoint M(m₁, m₂) of the line segment connecting two edge points P and Q. Together with T, it defines the TM line. (Ch2)

**MN segment** — The portion of the TM line over which votes are cast. Length L is set in advance. Restricting votes to MN (rather than the full line) improves efficiency. (Ch2)

**n_i** — Number of edge points on ellipse i. Complexity of Stage 1 scales as n_i². (Ch3)

**Occlusion** — When part of an object is hidden by another object or itself (self-occlusion), producing asymmetric arc fragments that defeat parallel-tangent methods. (Ch1, Ch5)

**P, Q** — Two edge points on the same ellipse used to construct a TM-line vote. Must satisfy pairing constraints δ₁, δ₂. (Ch2)

**Parallel-tangent method** — Classical center-finding: mid-point of two points with identical tangent direction is the center. Requires symmetric arc presence. Fails under occlusion. Used by Tsukune & Goto and Tsuji & Matsumoto. (Ch1, Ch2)

**Parameter space decomposition** — Breaking a high-dimensional HT into multiple lower-dimensional stages, each requiring less memory and computation. (Ch1, Ch2)

**Point deletion** — After finding and recording an ellipse, its associated edge points are removed from the dataset before reaccumulating for the next ellipse. Prevents cross-contamination in multi-ellipse images. (Ch2, Ch3)

**s₁, s₂** — Tangent slopes at edge points P and Q, derived from edge gradient measurements. Used to compute tangent intersection T. (Ch2)

**Spacek's edge detection algorithm** — Edge detector used in experiments to extract edge points and their gradient directions. (Ch4)

**T (tangent intersection)** — The intersection point T(t₁, t₂) of the tangent lines at P and Q. Together with midpoint M, defines the TM line. (Ch2)

**θ (rotation angle)** — The angle of the major axis of the ellipse with respect to the x-axis. Computed from B and D as `θ = 0.5 × arctan(2D / (1-B))`. (Ch2)

**TM line** — The line through T (tangent intersection) and M (midpoint of PQ). The ellipse center always lies on this line, regardless of arc symmetry. The key novel constraint of this paper. (Ch2)

**Two-stage decomposition** — Stage 1: center finding (2D accumulator); Stage 2: remaining 3 parameters via AHT. Reduces impractical 5D problem into two tractable subproblems. (Ch1, Ch2)

**a, b (semi-axes)** — Semi-major and semi-minor axes of the ellipse. Computed from B, D, C after Stage 2. (Ch2)
