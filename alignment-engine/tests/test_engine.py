from engine.alignment_engine import AlignmentEngine


def test_engine_runs():

    engine = AlignmentEngine()

    engine.run_simulation(num_steps=10)

    assert engine.state is not None
    assert len(engine.state) == 8  # 8-node lattice
    assert 'S' in engine.state
    assert 'D' in engine.state
    assert 'C' in engine.state
    assert 'Omega' in engine.state