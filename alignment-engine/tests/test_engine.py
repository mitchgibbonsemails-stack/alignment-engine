from engine.alignment_engine import AlignmentEngine


def test_engine_runs():

    engine = AlignmentEngine()

    engine.run_simulation(num_steps=10)

    assert engine.x is not None