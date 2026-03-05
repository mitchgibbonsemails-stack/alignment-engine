import argparse
from engine.alignment_engine import AlignmentEngine
from engine.diagnostics import plot_simulation


def main():
    parser = argparse.ArgumentParser(description="Run the alignment engine simulation")
    parser.add_argument("--steps", type=int, default=200, help="Number of simulation steps")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--save_dir", type=str, default=None, help="Directory to save diagnostic plots")
    parser.add_argument("--show", action="store_true", default=True, help="Show plots (default: True)")
    parser.add_argument("--no-show", dest="show", action="store_false", help="Don't show plots")
    parser.add_argument("--shock", type=str, nargs="*", default=[], help="Shock events as 'step:type' pairs")
    
    args = parser.parse_args()
    
    # Parse shocks
    shocks = {}
    for shock_spec in args.shock:
        if ":" in shock_spec:
            step, shock_type = shock_spec.split(":", 1)
            shocks[int(step)] = shock_type
    
    if not shocks:
        shocks = {
            60: "DISINFO_BURST",
            120: "RESOURCE_CRUNCH"
        }

    # Create engine with config
    config = {
        'num_steps': args.steps,
        'seed': args.seed,
        'shocks': shocks
    }
    engine = AlignmentEngine(config=config, debug=False)

    # Set seed if provided
    if args.seed is not None:
        import numpy as np
        np.random.seed(args.seed)

    # Run simulation
    engine.run_simulation(
        num_steps=args.steps,
        shocks=shocks,
        seed=args.seed,
        verbose=True
    )

    print("\nSimulation complete")
    print(f"Run ID: {engine.run_id}")
    print(f"Final S_hat: {engine.x[0]:.4f}")
    print(f"Final D_hat: {engine.x[1]:.4f}")

    # Plot diagnostics and collect convergence metric
    convergence = plot_simulation(engine.telemetry, save_dir=args.save_dir, show=args.show, run_id=engine.run_id)
    
    # Store convergence metric in telemetry metadata
    engine.telemetry_meta['convergence'] = convergence


if __name__ == "__main__":
    main()