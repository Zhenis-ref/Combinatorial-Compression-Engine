# CCE (Combinatorial Compression Engine)

An open search-regulation mechanism based on the ΔN–ΔD model that reduces combinatorial explosion.

## Main Result (Search Stress-Test, 30 seeds: 1–30)

Metric:
CR_nodes = baseline_nodes / dn_nodes

Results:

- Mean CR = 8.394×
- Median CR = 8.467×
- Min CR = 5.431×
- Max CR = 11.308×

This means CCE, driven by the ΔN–ΔD control model, reduces the number of explored nodes by approximately 8× on average compared to the baseline.

---

## Architecture

ΔN–ΔD model → CCE regulator → Backends
ΔN–ΔD is a formal dynamic framework describing structural evolution 
through two orthogonal parameters: nonequilibrium (ΔN) and duality (ΔD).

- `core/` — CCE core implementation
- `backends/` — stress-test and decoding demo
- `visualizer/` — pulse plots (ΔN, ΔD over time)
- `experiments/` — generated CSV and PNG results
- `docs/` — model formalization

---

## Mathematical Core

The structural dynamics implemented in this repository are based on the following equation:

dS/dt = α(ΔN, ΔD) · ΔN + β · ΔD

where:
- ΔN — nonequilibrium (external gradient),
- ΔD — structural duality (internal divergence),
- α(ΔN, ΔD) — nonlinear system response,
- β — structural contribution coefficient.

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

## Intellectual Property & Patent Notice

The ΔN–ΔD theoretical framework and the CCE architecture presented in this repository are original works by Zhengis Tileubay and are covered by an international patent application:
* **Patent Application:** International Patent Publication **[WO/2026/155638](https://patentscope.wipo.int/search/en/detail.jsf?docId=WO2026155638)** (*Method for Controlling the Dynamics of a Complex System*, PCT/KZ2026/000001).
© 2026 Zhengis Tileubay. Source code and documentation are licensed for **research and non-commercial use only**. 
Commercial licensing or technology transfer agreements are available upon request. For licensing, partnership, or collaboration inquiries, please contact the author.
