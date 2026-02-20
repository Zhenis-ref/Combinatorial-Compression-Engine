from core.delta_engine import DeltaEngine
from backends.llm_decoding.toy_decoding_backend import ToyDecodingBackend
from visualizer.pulse import plot_pulse


def run(seed: int, dn_control: bool):
    engine = DeltaEngine()
    backend = ToyDecodingBackend(dn_control=dn_control)
    backend.reset(seed)

    for _ in range(200):
        obs = backend.observe()
        out = engine.step(obs["deltaN"], obs["deltaD"])
        backend.apply_controls(out.controls)
        m = backend.step()
        if m["done"]:
            break

    logs = backend.get_logs()
    last = logs[-1]
    return last, logs


if __name__ == "__main__":
    last_b, logs_b = run(seed=2, dn_control=False)
    last_dn, logs_dn = run(seed=2, dn_control=True)

    cr_calls = (last_b["calls"] / max(last_dn["calls"], 1))

    print("=== LLM-Decoding (Toy) ===")
    print("Baseline calls:", last_b["calls"])
    print("DN calls:", last_dn["calls"])
    print("CR_calls:", round(cr_calls, 3))

    plot_pulse(logs_b, "Pulse (Baseline) - LLM Decoding Toy", "experiments/pulse_llm_baseline.png")
    plot_pulse(logs_dn, "Pulse (DN) - LLM Decoding Toy", "experiments/pulse_llm_dn.png")
    print("Saved plots to experiments/")
