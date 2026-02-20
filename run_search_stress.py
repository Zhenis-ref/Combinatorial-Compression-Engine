from core.delta_engine import DeltaEngine
from backends.search_stress.toy_search_backend import ToySearchStressBackend
from visualizer.pulse import plot_pulse


def run(seed: int, dn_control: bool, max_iter: int = 400):
    """
    Single run of the toy search stress backend.

    Returns:
        last: last log dict
        logs: list of log dicts
    """
    engine = DeltaEngine()
    backend = ToySearchStressBackend(dn_control=dn_control)
    backend.reset(seed)

    for _ in range(max_iter):
        obs = backend.observe()
        out = engine.step(obs["deltaN"], obs["deltaD"])
        backend.apply_controls(out.controls)
        m = backend.step()
        if m["done"]:
            break

    logs = backend.get_logs()
    last = logs[-1]
    return last, logs


def run_batch(
    seeds,
    max_iter: int = 400,
    save_csv_path: str = "experiments/search_stress_results.csv",
    save_cr_plot_path: str = "experiments/cr_over_seeds.png",
    save_scatter_plot_path: str = "experiments/baseline_vs_dn_scatter.png",
    save_pulse_examples: bool = True,
):
    """
    Batch runs for multiple seeds. Saves:
      - CSV table with baseline/dn nodes and CR
      - CR over seeds plot
      - baseline vs dn scatter
      - optional example pulse plots (one pair) for the last seed
    """
    import os
    import csv
    import statistics as st

    os.makedirs("experiments", exist_ok=True)

    rows = []
    last_logs_b = None
    last_logs_dn = None
    last_seed = None

    print("=== Search Stress-Test (BATCH) ===")
    for seed in seeds:
        last_b, logs_b = run(seed=seed, dn_control=False, max_iter=max_iter)
        last_dn, logs_dn = run(seed=seed, dn_control=True, max_iter=max_iter)

        b_nodes = int(last_b["nodes_expanded"])
        dn_nodes = int(last_dn["nodes_expanded"])
        cr = b_nodes / max(dn_nodes, 1)

        rows.append((seed, b_nodes, dn_nodes, cr))
        print(f"seed={seed:02d}  baseline={b_nodes:5d}  dn={dn_nodes:5d}  CR={cr:7.3f}")

        last_logs_b = logs_b
        last_logs_dn = logs_dn
        last_seed = seed

    # Save CSV
    with open(save_csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["seed", "baseline_nodes", "dn_nodes", "cr_nodes"])
        w.writerows(rows)

    # Summary
    crs = [r[3] for r in rows]
    mean_cr = st.mean(crs)
    med_cr = st.median(crs)
    min_cr = min(crs)
    max_cr = max(crs)

    print("\n--- Summary ---")
    print(f"Runs: {len(rows)}")
    print(f"Mean CR:   {mean_cr:.3f}")
    print(f"Median CR: {med_cr:.3f}")
    print(f"Min CR:    {min_cr:.3f}")
    print(f"Max CR:    {max_cr:.3f}")
    print(f"Saved CSV: {save_csv_path}")

    # Plots
    try:
        import matplotlib.pyplot as plt

        seeds_ = [r[0] for r in rows]
        bns = [r[1] for r in rows]
        dns = [r[2] for r in rows]

        # CR over seeds
        plt.figure()
        plt.plot(seeds_, crs)
        plt.title("CR_nodes over seeds (Search Stress)")
        plt.xlabel("seed")
        plt.ylabel("CR_nodes")
        plt.savefig(save_cr_plot_path, dpi=150)
        plt.close()
        print(f"Saved plot: {save_cr_plot_path}")

        # Scatter baseline vs dn
        plt.figure()
        plt.scatter(bns, dns)
        plt.title("Baseline nodes vs DN nodes")
        plt.xlabel("baseline_nodes")
        plt.ylabel("dn_nodes")
        plt.savefig(save_scatter_plot_path, dpi=150)
        plt.close()
        print(f"Saved plot: {save_scatter_plot_path}")

    except Exception as e:
        print(f"[warn] matplotlib plots not saved due to error: {e}")

    # Optional: save one example pulse pair (for the last seed in the batch)
    if save_pulse_examples and (last_logs_b is not None) and (last_logs_dn is not None):
        try:
            plot_pulse(
                last_logs_b,
                f"Pulse (Baseline) - Search Stress (seed={last_seed})",
                "experiments/pulse_search_baseline.png",
            )
            plot_pulse(
                last_logs_dn,
                f"Pulse (DN) - Search Stress (seed={last_seed})",
                "experiments/pulse_search_dn.png",
            )
            print("Saved pulse examples to experiments/: pulse_search_baseline.png, pulse_search_dn.png")
        except Exception as e:
            print(f"[warn] pulse plots not saved due to error: {e}")

    print("=== Done ===")


if __name__ == "__main__":
    # Настройка: сколько seed прогнать
    seeds = list(range(1, 31))  # 30 прогонов: 1..30

    # Настройка: лимит шагов симуляции (как у тебя было 400)
    run_batch(
        seeds=seeds,
        max_iter=400,
        save_pulse_examples=True,
    )
