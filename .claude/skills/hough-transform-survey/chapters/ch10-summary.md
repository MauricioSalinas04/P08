# Chapter 10 — Summary

## The authors' bottom line

The HT is an important method for many computer-vision tasks. It is **very robust** in the presence of extra data and copes well with missing data. Adoption has historically been slow because the simplest implementation needs **lots of computation and lots of storage** for high-dimensional accumulators.

## Where progress had been made (as of 1988)

- **Focusing approaches** (AHT, FHT, DQS, DQP, hash/cache) → fast and/or space-efficient digital implementations.
- **Radon equivalence** → real-time **analog** and **optical** implementations.
- **Peak detection / enhancement** — non-trivial work on butterfly filters, backtransform, CHough.
- **Detailed analysis** of accumulator distributions for both noise and real features.
- **Low-dimensional parameterizations** of curves (decomposition trick).
- **Specialized computer architectures** for the HT.

## The forecast

> "Taking all this together suggests that the HT is provoking more interest and offering more promise than ever before."

## How to read this survey when planning new work

1. Start at [[ch01-introduction]] for the formal definition.
2. Read [[ch03-shape-parameterizations]] **before** writing any HT — choice of parameterization dominates everything.
3. Then [[ch04-efficient-accumulation]] for storage/compute strategy.
4. [[ch05-peak-detection]] and [[ch06-performance-analysis]] for output quality.
5. [[ch07-ht-and-other-transforms]] if you have FFT or optical hardware.
6. [[ch08-applications]] to find a precedent.
7. [[ch09-architectures]] if you are targeting custom or massively parallel hardware.
8. Use [[patterns]] and [[cheatsheet]] as the running reference while coding.

Cross-refs: [[SKILL]].
