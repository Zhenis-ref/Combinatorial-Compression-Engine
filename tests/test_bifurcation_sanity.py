from core.delta_engine import DeltaEngine

def test_bifurcation_flag_is_boolean():
    engine = DeltaEngine()
    out = engine.step(0.99, 0.01)  # high ΔN, low ΔD
    assert isinstance(out.bifurcation, bool)
