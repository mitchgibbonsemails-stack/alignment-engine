import numpy as np
from engine.alignment_engine import AlignmentEngine
from engine.diagnostics import compute_convergence_metric


def test_state_stays_in_bounds():
    """
    Test that all normalized state values stay in [0, 1] range.
    """
    engine = AlignmentEngine(debug=False)
    engine.run_simulation(num_steps=50, seed=42)
    
    # Check that all telemetry values are finite
    for t in engine.telemetry:
        assert np.isfinite(t['S_hat']), f"S_hat is not finite: {t['S_hat']}"
        assert np.isfinite(t['D_hat']), f"D_hat is not finite: {t['D_hat']}"
        assert np.isfinite(t['alignment_score']), f"alignment_score is not finite: {t['alignment_score']}"
        
        # Check bounds [0, 1]
        assert 0 <= t['S_hat'] <= 1, f"S_hat out of bounds: {t['S_hat']}"
        assert 0 <= t['D_hat'] <= 1, f"D_hat out of bounds: {t['D_hat']}"
        assert 0 <= t['alignment_score'] <= 1, f"alignment_score out of bounds: {t['alignment_score']}"


def test_trust_weights_in_valid_range():
    """
    Test that trust weights stay in (0, 1) range.
    """
    engine = AlignmentEngine(debug=False)
    engine.run_simulation(num_steps=50, seed=42)
    
    for t in engine.telemetry:
        for key in ['H', 'E', 'P', 'S']:
            weight = t['trust_weights'][key]
            assert np.isfinite(weight), f"Trust weight {key} is not finite: {weight}"
            assert 0 < weight < 1, f"Trust weight {key} out of range (0,1): {weight}"


def test_no_nans_in_telemetry():
    """
    Test that no NaN values appear in telemetry data.
    """
    engine = AlignmentEngine(debug=False)
    engine.run_simulation(num_steps=50, seed=42)
    
    for i, t in enumerate(engine.telemetry):
        if np.isnan(t['S_hat']):
            raise AssertionError(f"NaN in S_hat at step {i}")
        if np.isnan(t['D_hat']):
            raise AssertionError(f"NaN in D_hat at step {i}")
        if np.isnan(t['alignment_score']):
            raise AssertionError(f"NaN in alignment_score at step {i}")


def test_engine_with_debug_sanity_checks():
    """
    Test that engine with debug=True runs sanity checks.
    """
    engine = AlignmentEngine(debug=True)
    # Should run without raising exceptions
    engine.run_simulation(num_steps=50, seed=42)
    
    # Verify final state is valid
    assert 0 <= engine.x[0] <= 1
    assert 0 <= engine.x[1] <= 1
    assert len(engine.telemetry) == 50


def test_reproducibility_with_seed():
    """
    Test that same seed produces same results.
    """
    engine1 = AlignmentEngine()
    engine1.run_simulation(num_steps=30, seed=123)
    
    engine2 = AlignmentEngine()
    engine2.run_simulation(num_steps=30, seed=123)
    
    # Check that telemetry matches
    for t1, t2 in zip(engine1.telemetry, engine2.telemetry):
        assert t1['S_hat'] == t2['S_hat'], "S_hat differs between runs"
        assert t1['D_hat'] == t2['D_hat'], "D_hat differs between runs"
        assert t1['alignment_score'] == t2['alignment_score'], "alignment_score differs between runs"


def test_convergence_metric_computation():
    """
    Test that convergence metric is computed correctly.
    """
    engine = AlignmentEngine()
    engine.run_simulation(num_steps=100, seed=42)
    
    convergence = compute_convergence_metric(engine.telemetry)
    
    # Check that required keys are present
    assert 'status' in convergence
    assert 'ratio' in convergence
    assert 'area_first_20pct' in convergence
    assert 'area_last_20pct' in convergence
    
    # Status should be one of the valid values
    assert convergence['status'] in ['converging', 'diverging', 'stable', 'insufficient_data']
    
    # Ratio should be non-negative
    if convergence['ratio'] is not None:
        assert convergence['ratio'] >= 0.0, f"Convergence ratio should be non-negative: {convergence['ratio']}"
    
    # Areas should be non-negative
    assert convergence['area_first_20pct'] >= 0.0
    assert convergence['area_last_20pct'] >= 0.0
