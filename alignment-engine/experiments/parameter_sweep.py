import argparse
import csv
import os
from datetime import datetime
import numpy as np
from engine.alignment_engine import AlignmentEngine
from engine.diagnostics import plot_simulation, compute_convergence_metric


def run_parameter_sweep(k_S_range, k_D_range, k_err_range, lambda_Td_range, 
                        num_steps=200, seed=None, save_dir="artifacts", verbose=False, write_csv=False):
    """
    Run a grid sweep over parameter combinations.
    
    Args:
        k_S_range: tuple of (min, max, num_steps)
        k_D_range: tuple of (min, max, num_steps)
        k_err_range: tuple of (min, max, num_steps)
        lambda_Td_range: tuple of (min, max, num_steps)
        num_steps: steps per simulation
        seed: random seed (base seed, increment for each run)
        save_dir: where to save results
        verbose: print progress
        write_csv: write results to CSV file
    
    Returns:
        list of result dicts
    """
    os.makedirs(save_dir, exist_ok=True)
    
    # Create parameter grids
    k_S_values = np.linspace(k_S_range[0], k_S_range[1], k_S_range[2])
    k_D_values = np.linspace(k_D_range[0], k_D_range[1], k_D_range[2])
    k_err_values = np.linspace(k_err_range[0], k_err_range[1], k_err_range[2])
    lambda_Td_values = np.linspace(lambda_Td_range[0], lambda_Td_range[1], lambda_Td_range[2])
    
    results = []
    run_count = 0
    total_runs = len(k_S_values) * len(k_D_values) * len(k_err_values) * len(lambda_Td_values)
    
    shocks = {
        int(num_steps * 0.3): "DISINFO_BURST",
        int(num_steps * 0.6): "RESOURCE_CRUNCH"
    }
    
    for k_S in k_S_values:
        for k_D in k_D_values:
            for k_err in k_err_values:
                for lambda_Td in lambda_Td_values:
                    run_count += 1
                    if verbose:
                        print(f"[{run_count}/{total_runs}] Running: k_S={k_S:.3f}, k_D={k_D:.3f}, k_err={k_err:.3f}, lambda_Td={lambda_Td:.3f}")
                    
                    # Create config
                    config = {
                        'k_S': k_S,
                        'k_D': k_D,
                        'k_err': k_err,
                        'lambda_Td': lambda_Td,
                        'num_steps': num_steps,
                        'seed': seed
                    }
                    
                    # Create and run engine
                    engine = AlignmentEngine(config=config, debug=False)
                    run_seed = seed + run_count if seed is not None else None
                    engine.run_simulation(num_steps=num_steps, shocks=shocks, seed=run_seed, verbose=False)
                    
                    # Compute convergence metric
                    convergence = compute_convergence_metric(engine.telemetry)
                    
                    # Record result
                    result = {
                        'run_id': engine.run_id,
                        'k_S': k_S,
                        'k_D': k_D,
                        'k_err': k_err,
                        'lambda_Td': lambda_Td,
                        'final_S': engine.state['S'],
                        'final_D': engine.state['D'],
                        'final_C': engine.state['C'],
                        'final_K': engine.state['K'],
                        'final_B': engine.state['B'],
                        'final_T_u': engine.state['T_u'],
                        'final_Omega': engine.state['Omega'],
                        'final_Lambda': engine.state['Lambda'],
                        'convergence_status': convergence['status'],
                        'volume_ratio': convergence['ratio'] if convergence['ratio'] is not None else -1.0,
                        'final_alignment_score': engine.alignment_score
                    }
                    results.append(result)
    
    # Write CSV if requested
    if write_csv:
        csv_path = os.path.join(save_dir, "sweep_results.csv")
        fieldnames = ['run_id', 'k_S', 'k_D', 'k_err', 'lambda_Td', 'final_S', 
                      'final_D', 'final_C', 'final_K', 'final_B', 'final_T_u',
                      'final_Omega', 'final_Lambda',
                      'convergence_status', 'volume_ratio', 'final_alignment_score']
        
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Run parameter sweep for alignment engine")
    parser.add_argument("--k_S_min", type=float, default=0.05, help="Min k_S")
    parser.add_argument("--k_S_max", type=float, default=0.2, help="Max k_S")
    parser.add_argument("--k_S_steps", type=int, default=3, help="Number of k_S steps")
    
    parser.add_argument("--k_D_min", type=float, default=0.05, help="Min k_D")
    parser.add_argument("--k_D_max", type=float, default=0.2, help="Max k_D")
    parser.add_argument("--k_D_steps", type=int, default=3, help="Number of k_D steps")
    
    parser.add_argument("--k_err_min", type=float, default=0.01, help="Min k_err")
    parser.add_argument("--k_err_max", type=float, default=0.1, help="Max k_err")
    parser.add_argument("--k_err_steps", type=int, default=3, help="Number of k_err steps")
    
    parser.add_argument("--lambda_Td_min", type=float, default=0.001, help="Min lambda_Td")
    parser.add_argument("--lambda_Td_max", type=float, default=0.05, help="Max lambda_Td")
    parser.add_argument("--lambda_Td_steps", type=int, default=3, help="Number of lambda_Td steps")
    
    parser.add_argument("--steps", type=int, default=100, help="Steps per simulation")
    parser.add_argument("--seed", type=int, default=42, help="Base random seed")
    parser.add_argument("--save_dir", type=str, default="artifacts", help="Directory to save results")
    parser.add_argument("--verbose", action="store_true", help="Print progress")
    
    args = parser.parse_args()
    
    # Run sweep
    results = run_parameter_sweep(
        k_S_range=(args.k_S_min, args.k_S_max, args.k_S_steps),
        k_D_range=(args.k_D_min, args.k_D_max, args.k_D_steps),
        k_err_range=(args.k_err_min, args.k_err_max, args.k_err_steps),
        lambda_Td_range=(args.lambda_Td_min, args.lambda_Td_max, args.lambda_Td_steps),
        num_steps=args.steps,
        seed=args.seed,
        save_dir=args.save_dir,
        verbose=args.verbose,
        write_csv=True
    )
    
    csv_path = os.path.join(args.save_dir, "sweep_results.csv")
    
    print(f"\n✓ Sweep complete: {len(results)} runs")
    print(f"✓ Results saved to: {csv_path}")
    
    # Summary statistics
    converging = sum(1 for r in results if r['convergence_status'] == 'converging')
    diverging = sum(1 for r in results if r['convergence_status'] == 'diverging')
    stable = sum(1 for r in results if r['convergence_status'] == 'stable')
    
    print(f"\nConvergence Summary:")
    print(f"  Converging: {converging}")
    print(f"  Diverging:  {diverging}")
    print(f"  Stable:     {stable}")


if __name__ == "__main__":
    main()
