import os
import csv
import tempfile
from experiments.parameter_sweep import run_parameter_sweep


def test_parameter_sweep_runs():
    """
    Test that parameter sweep executes and produces results.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        results = run_parameter_sweep(
            k_S_range=(0.05, 0.1, 2),
            k_D_range=(0.05, 0.1, 2),
            k_err_range=(0.01, 0.05, 2),
            lambda_Td_range=(0.001, 0.01, 2),
            num_steps=20,
            seed=42,
            save_dir=tmpdir,
            verbose=False
        )
        
        # Should have 2^4 = 16 results
        assert len(results) == 16, f"Expected 16 results, got {len(results)}"
        
        # Each result should have the required keys
        for result in results:
            assert 'run_id' in result
            assert 'k_S' in result
            assert 'k_D' in result
            assert 'k_err' in result
            assert 'lambda_Td' in result
            assert 'final_S' in result
            assert 'final_D' in result
            assert 'final_C' in result
            assert 'final_Omega' in result
            assert 'convergence_status' in result
            assert 'volume_ratio' in result
            assert 'final_alignment_score' in result


def test_parameter_sweep_csv_output():
    """
    Test that CSV file is created with correct structure.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        results = run_parameter_sweep(
            k_S_range=(0.05, 0.1, 2),
            k_D_range=(0.05, 0.1, 2),
            k_err_range=(0.01, 0.05, 2),
            lambda_Td_range=(0.001, 0.01, 2),
            num_steps=20,
            seed=42,
            save_dir=tmpdir,
            verbose=False,
            write_csv=True
        )
        
        csv_path = os.path.join(tmpdir, "sweep_results.csv")
        
        # File should exist
        assert os.path.exists(csv_path), "CSV file was not created"
        
        # Read CSV and verify structure
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Should have 16 data rows
        assert len(rows) == 16, f"Expected 16 data rows, got {len(rows)}"
        
        # Check that all expected columns are present
        expected_columns = ['run_id', 'k_S', 'k_D', 'k_err', 'lambda_Td', 'final_S',
                           'final_D', 'final_C', 'final_K', 'final_B', 'final_T_u',
                           'final_Omega', 'final_Lambda',
                           'convergence_status', 'volume_ratio', 'final_alignment_score']
        for col in expected_columns:
            assert col in rows[0], f"Missing column: {col}"


def test_parameter_grid_coverage():
    """
    Test that all parameter combinations are covered in the sweep.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        results = run_parameter_sweep(
            k_S_range=(0.05, 0.15, 3),
            k_D_range=(0.05, 0.15, 3),
            k_err_range=(0.01, 0.05, 2),
            lambda_Td_range=(0.001, 0.01, 2),
            num_steps=20,
            seed=42,
            save_dir=tmpdir,
            verbose=False
        )
        
        # Should have 3 * 3 * 2 * 2 = 36 results
        assert len(results) == 36, f"Expected 36 results, got {len(results)}"
        
        # Collect unique parameter combinations
        k_S_values = set(round(r['k_S'], 10) for r in results)
        k_D_values = set(round(r['k_D'], 10) for r in results)
        k_err_values = set(round(r['k_err'], 10) for r in results)
        lambda_Td_values = set(round(r['lambda_Td'], 10) for r in results)
        
        # Should have the expected number of unique values
        assert len(k_S_values) == 3, f"Expected 3 k_S values, got {len(k_S_values)}"
        assert len(k_D_values) == 3, f"Expected 3 k_D values, got {len(k_D_values)}"
        assert len(k_err_values) == 2, f"Expected 2 k_err values, got {len(k_err_values)}"
        assert len(lambda_Td_values) == 2, f"Expected 2 lambda_Td values, got {len(lambda_Td_values)}"


def test_convergence_status_recorded():
    """
    Test that convergence status is properly recorded in all runs.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        results = run_parameter_sweep(
            k_S_range=(0.05, 0.1, 2),
            k_D_range=(0.05, 0.1, 2),
            k_err_range=(0.01, 0.05, 2),
            lambda_Td_range=(0.001, 0.01, 2),
            num_steps=20,
            seed=42,
            save_dir=tmpdir,
            verbose=False
        )
        
        for result in results:
            status = result['convergence_status']
            assert status in ['converging', 'diverging', 'stable', 'insufficient_data'], \
                f"Invalid convergence status: {status}"
            
            # Volume ratio should be valid
            ratio = result['volume_ratio']
            assert isinstance(ratio, (int, float)), f"Volume ratio should be numeric: {ratio}"
