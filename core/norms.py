def clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return float(x)


def safe_div(a: float, b: float, eps: float = 1e-12) -> float:
    return float(a) / float(b + eps)
