from typing import List, Dict
import matplotlib.pyplot as plt


def plot_pulse(logs: List[Dict], title: str, out_png: str) -> None:
    t = [row["t"] for row in logs]
    dN = [row.get("deltaN", 0.0) for row in logs]
    dD = [row.get("deltaD", 0.0) for row in logs]

    plt.figure()
    plt.plot(t, dN, label="ΔN")
    plt.plot(t, dD, label="ΔD")
    plt.xlabel("t")
    plt.ylabel("value")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=160)
    plt.close()
