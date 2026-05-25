# Chapter 9 — Architectures for the HT

The HT is a series of simple, independent per-feature calculations → naturally parallel. This chapter catalogs hardware approaches.

## Pipelined custom / TTL

- **Hanahara, Maruyama, Ichiyama [132]** — `(ρ, θ)` HT pipelining ρ-intersection computation and accumulator incrementation. TTL MSI/SSI + MC68000 controller. Edge detection + HT + accumulation + peak detection = **0.79 s for 1024 features**.

## Restructurable VLSI (RVLSI)

- **Rhodes et al. [134]** — RVLSI HT processor: standard logic cells on a wafer, post-fab testing identifies working cells, uncommitted metal interconnect is fused/broken to wire them up. Runs at **frame rates**.

## Pipelined VLSI projection engine

- **PPPE (Baringer et al. [101])** — Parallel Pipeline Projection Engine. Exploits Radon-as-projection (see [[ch07-ht-and-other-transforms]]) for real-time Radon/HT on **one or two custom ICs**.

## Multitasking / asynchronous parallel

- **Leavers & Sandler [133]** — restrict the cells to be incremented using edge information; use table lookup wherever possible.

## SIMD architectures

Square arrays of simple PEs, each with a single-bit ALU, a few registers, a few kbits of RAM, communicating with 4 or 8 neighbors.

- **Silberberg [81]** — distributed image + accumulator across all PEs; each PE held both an image feature and a parameter cell. **>98 % of time** went to inter-PE data movement; **8000 PEs yielded only 7× speedup** vs. a VAX 11/785. Lesson: parallel mapping must avoid all-to-all data movement.
- **Li [76]** — two FHT-on-SIMD schemes:
  1. Each PE holds an image feature; central controller broadcasts parameter-cell coordinates; PE answers "does my feature's hypersurface hit this cell?"; controller sums returned votes.
  2. Each PE holds a volume of parameter space; image features broadcast.
  Choice depends on PE count, feature count, cell count. Since standard-HT cells grow exponentially with q, the first scheme is usually more feasible.
- **Communication overhead** — naïve n-PE assignment on a 2-D mesh with local shifts costs `O(√n)` per vote (Silberberg's bottleneck). Augmenting with a **tree voting network** reduces this to `O(log n)`, restoring expected `O(n)` speedups.
- **Connection Machine (Little, Blelloch, Cass [123])** — SIMD with a hardware router on a **12-D hypercube**: any pair of PEs ≤ 12 hops apart. Paper light on efficiency numbers.
- **MPP mesh** — Cypher, Sanz, Snyder [107] proposed 5 Radon/HT algorithms on `n × n` mesh; 3 of them achieve `O(P + n)` time vs. Silberberg's `O(P n)` (`P` = number of projections). Four are based on rotating the image so lines at angle θ align with rows → horizontal shifts + adds suffice.
- **MPP block algorithms** — Guerra & Hambrusch [115]: block algorithm (submeshes + combine) plus pipelined tracing algorithm; block expected to outperform tracing in practice despite worse asymptotics.
- **SLAP (Scan-Line Array Processor)** — Fisher & Highman [113]: linear array of SIMD vector processors, one per image column; array scans across rows, processing all pixels of a row concurrently. **Accumulator cells migrate between PEs** to stay co-located with the pixel on the line they represent. Cells enter at one edge, exit at the opposite edge having seen every pixel of their line. Targeted 3 µm CMOS → full HT on 512 × 512 in 2–3 frame times.

## MIMD

- **Olsen, Bukys, Brown [125]** — BBN Butterfly (256 nodes, M68000-class, 1 MB per node, switching network for shared-memory addressing). Two HTs: image partitioned with parameters in shared memory vs. vice versa. Reported processor-utilization **≈ 80 %** (100 PEs → 80× speedup).

## Connectionist / parameter nets

- **Parameter Nets (Ballard [61])** — feature network for pixel-level evidence + parameter network for higher-level entities. Direct connections vote with confidence values. Different connection patterns = different image-to-parameter mappings. Cost: enormous numbers of feature/parameter units and connections.

## Pyramid machines

- **Cantoni et al. [104, 105]** — HT as part of a hierarchical recognition system on SIMD arrays or pyramids; low-resolution feature detection + high-resolution integration. Near real-time on sequential simulation.
- **Blanford DQP [102]** — naturally maps onto parallel pyramid machines. Caveat: needs multiplications/divisions, not ideal for bit-serial PEs of current pyramids.

## Blackboard / database

- **Fischler & Firschein [112]** — HT on a blackboard/database architecture using "**parallel guessing**": compute the HT **incrementally** and stop once a sufficiently significant peak is identified.

## Lessons for parallel implementation

1. Mapping matters more than processor count — Silberberg's 7× from 8000 PEs is the warning.
2. Vote-routing topology (mesh vs. tree vs. hypercube vs. shared-memory switch) is the dominant performance variable.
3. Migrating accumulators (SLAP) or rotating images (Cypher et al.) can sidestep routing entirely.
4. Incremental + early-termination (Fischler–Firschein) is the database-architecture analog of focusing.

Cross-refs: [[ch04-efficient-accumulation]], [[ch07-ht-and-other-transforms]], [[patterns]], [[cheatsheet]].
