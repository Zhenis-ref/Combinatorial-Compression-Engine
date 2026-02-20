from core.delta_engine import DeltaEngine

def test_engine_outputs_in_range():
    engine = DeltaEngine()
    out = engine.step(0.8, 0.2)
    assert 0.0 <= out.deltaN <= 1.0
    assert 0.0 <= out.deltaD <= 1.0
    assert isinstance(out.alpha, float)
    assert isinstance(out.dsdt, float)
    assert isinstance(out.controls, dict)
