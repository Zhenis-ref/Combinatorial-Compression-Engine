# CCE / ΔN–ΔD Engine

A delta-controlled search mechanism that reduces combinatorial explosion.

## Main Result (Search Stress-Test, 30 seeds: 1–30)

Metric:
CR_nodes = baseline_nodes / dn_nodes

Results:

- Mean CR = 8.394×
- Median CR = 8.467×
- Min CR = 5.431×
- Max CR = 11.308×

This means DN reduces the number of explored nodes by approximately 8× on average compared to the baseline.

---

## Architecture

Law (ΔN–ΔD) → DeltaEngine → Backends

- `core/` — ΔN–ΔD engine implementation
- `backends/` — stress-test and decoding demo
- `visualizer/` — pulse plots (ΔN, ΔD over time)
- `experiments/` — generated CSV and PNG results
- `docs/` — model formalization

---

## Quick Start

Install dependencies:

pip install -r requirements.txt

Run the batch test (30 runs):

python run_search_stress.py

Results are saved in the `experiments/` folder:
- search_stress_results.csv
- CR over seeds plot
- baseline vs DN scatter plot
- pulse plots

  ---

## Intellectual Property

The ΔN–ΔD model and the Delta Engine architecture presented in this repository are original works by Zhengis Tileubay.

© 2026 Zhengis Tileubay. All rights reserved.

For licensing or collaboration inquiries, please contact the author.
