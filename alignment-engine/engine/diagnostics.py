import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def compute_convergence_metric(telemetry):
    """
    Compute convergence metric by comparing phase-space bounding box areas across all 8 state variables.
    
    Returns:
        dict with 'status' ('converging' or 'diverging') and 'ratio' (area_last / area_first)
    """
    if len(telemetry) < 5:
        return {'status': 'insufficient_data', 'ratio': None}
    
    # Extract all 8 state variables
    state_vars = ['S', 'D', 'C', 'K', 'B', 'T_u', 'Omega', 'Lambda']
    state_data = {}
    
    for var in state_vars:
        state_data[var] = np.array([t[var] for t in telemetry])
    
    n = len(telemetry)
    split_idx = max(1, n // 5)  # 20% of steps
    
    # Compute total phase space volume for first and last 20%
    volume_first = 1.0
    volume_last = 1.0
    
    for var in state_vars:
        data = state_data[var]
        
        # First 20% of steps
        data_first = data[:split_idx]
        if len(data_first) > 0:
            range_first = np.max(data_first) - np.min(data_first)
            volume_first *= max(range_first, 1e-10)
        
        # Last 20% of steps
        data_last = data[-split_idx:]
        if len(data_last) > 0:
            range_last = np.max(data_last) - np.min(data_last)
            volume_last *= max(range_last, 1e-10)
    
    # Avoid division by zero
    if volume_first < 1e-10:
        ratio = 0.0 if volume_last < 1e-10 else float('inf')
    else:
        ratio = volume_last / volume_first
    
    # Determine convergence status
    if ratio < 0.8:
        status = 'converging'
    elif ratio > 1.2:
        status = 'diverging'
    else:
        status = 'stable'
    
    return {
        'status': status,
        'ratio': ratio,
        'volume_first_20pct': volume_first,
        'volume_last_20pct': volume_last
    }

def plot_simulation(telemetry, save_dir=None, show=True, run_id=None):
    if not telemetry:
        print("No telemetry data to plot.")
        return

    # Create save directory if needed
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
    
    # Generate timestamp and filename prefix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_prefix = f"{run_id}_{timestamp}" if run_id else timestamp

    # Extract data for all 8 state variables
    steps = list(range(len(telemetry)))
    state_vars = ['S', 'D', 'C', 'K', 'B', 'T_u', 'Omega', 'Lambda']
    state_data = {}
    
    for var in state_vars:
        state_data[var] = [t[var] for t in telemetry]
    
    alignment = [t['alignment_score'] for t in telemetry]
    trust_H = [t['trust_weights']['H'] for t in telemetry]
    trust_E = [t['trust_weights']['E'] for t in telemetry]
    trust_P = [t['trust_weights']['P'] for t in telemetry]
    trust_S = [t['trust_weights']['S'] for t in telemetry]
    phase = [t['phase'] for t in telemetry]

    # Compute convergence metric
    convergence = compute_convergence_metric(telemetry)

    # Create comprehensive subplots: 4x3 grid for 8 state vars + trust + alignment + phase space
    fig, axs = plt.subplots(4, 3, figsize=(18, 16))

    # Plot all 8 state variables (first 8 subplots)
    plot_titles = ['Signal (S)', 'Distortion (D)', 'Constraints (C)', 'Inertia (K)', 
                   'Capacity (B)', 'Time (Tᵤ)', 'Options (Ω)', 'Coupling (Λ)']
    
    for i, (var, title) in enumerate(zip(state_vars, plot_titles)):
        row, col = i // 3, i % 3
        axs[row, col].plot(steps, state_data[var], 'b-', linewidth=2)
        axs[row, col].set_title(f'{title} Evolution')
        axs[row, col].set_xlabel('Time Steps')
        axs[row, col].set_ylabel('Value [0,1]')
        axs[row, col].grid(True, alpha=0.3)

    # 9. Alignment score over time
    axs[2, 2].plot(steps, alignment, 'g-', linewidth=2)
    axs[2, 2].set_title('Alignment Score')
    axs[2, 2].set_xlabel('Time Steps')
    axs[2, 2].set_ylabel('Score [0,1]')
    axs[2, 2].grid(True, alpha=0.3)

    # 10. Trust weights for H,E,P,S
    axs[3, 0].plot(steps, trust_H, label='Historical (H)', linewidth=2)
    axs[3, 0].plot(steps, trust_E, label='Error (E)', linewidth=2)
    axs[3, 0].plot(steps, trust_P, label='Prediction (P)', linewidth=2)
    axs[3, 0].plot(steps, trust_S, label='Stability (S)', linewidth=2)
    axs[3, 0].set_title('Trust Weights Evolution')
    axs[3, 0].set_xlabel('Time Steps')
    axs[3, 0].set_ylabel('Weight [0,1]')
    axs[3, 0].legend()
    axs[3, 0].grid(True, alpha=0.3)

    # 11. Phase evolution
    axs[3, 1].plot(steps, phase, 'm-', linewidth=2)
    axs[3, 1].set_title('Phase Evolution')
    axs[3, 1].set_xlabel('Time Steps')
    axs[3, 1].set_ylabel('Phase')
    axs[3, 1].grid(True, alpha=0.3)

    # 12. Diamond lattice phase space: Signal vs Distortion trajectory
    scatter = axs[3, 2].scatter(state_data['S'], state_data['D'], 
                                c=steps, cmap='plasma', s=40, alpha=0.7)
    axs[3, 2].plot(state_data['S'], state_data['D'], 'k-', alpha=0.3, linewidth=1)
    axs[3, 2].set_xlabel('Signal (S)')
    axs[3, 2].set_ylabel('Distortion (D)')
    axs[3, 2].set_title('Diamond Core: Signal vs Distortion')
    axs[3, 2].grid(True, alpha=0.3)
    cbar = plt.colorbar(scatter, ax=axs[3, 2])
    cbar.set_label('Time Steps')

    plt.tight_layout()
    
    # Save figure if directory specified
    if save_dir:
        filepath = os.path.join(save_dir, f"{filename_prefix}_diamond_diagnostics.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved diamond diagnostic plot to {filepath}")
    
    # Print convergence analysis
    print("\n=== Diamond Lattice Convergence Analysis ===")
    print(f"Status: {convergence['status'].upper()}")
    print(f"Phase space volume ratio (last 20% / first 20%): {convergence['ratio']:.4f}")
    print(f"First 20% phase space volume: {convergence['volume_first_20pct']:.6f}")
    print(f"Last 20% phase space volume: {convergence['volume_last_20pct']:.6f}")
    
    # Show plot if requested
    if show:
        plt.show()
    else:
        plt.close(fig)
        plt.close()
    
    return convergence