import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

def compute_convergence_metric(telemetry):
    """
    Compute convergence metric by comparing phase-space bounding box areas.
    
    Returns:
        dict with 'status' ('converging' or 'diverging') and 'ratio' (area_last / area_first)
    """
    if len(telemetry) < 5:
        return {'status': 'insufficient_data', 'ratio': None}
    
    # Extract S_hat and D_hat
    S_hat = np.array([t['S_hat'] for t in telemetry])
    D_hat = np.array([t['D_hat'] for t in telemetry])
    
    n = len(telemetry)
    split_idx = max(1, n // 5)  # 20% of steps
    
    # First 20% of steps
    S_first = S_hat[:split_idx]
    D_first = D_hat[:split_idx]
    
    # Last 20% of steps
    S_last = S_hat[-split_idx:]
    D_last = D_hat[-split_idx:]
    
    # Compute bounding box areas
    if len(S_first) > 0:
        area_first = (np.max(S_first) - np.min(S_first)) * (np.max(D_first) - np.min(D_first))
    else:
        area_first = 0.0
    
    if len(S_last) > 0:
        area_last = (np.max(S_last) - np.min(S_last)) * (np.max(D_last) - np.min(D_last))
    else:
        area_last = 0.0
    
    # Avoid division by zero
    if area_first < 1e-10:
        ratio = 0.0 if area_last < 1e-10 else float('inf')
    else:
        ratio = area_last / area_first
    
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
        'area_first_20pct': area_first,
        'area_last_20pct': area_last
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

    # Extract data
    steps = list(range(len(telemetry)))
    S_hat = [t['S_hat'] for t in telemetry]
    S_true = [t['S_true'] for t in telemetry]
    D_hat = [t['D_hat'] for t in telemetry]
    D_true = [t['D_true'] for t in telemetry]
    alignment = [t['alignment_score'] for t in telemetry]
    trust_H = [t['trust_weights']['H'] for t in telemetry]
    trust_E = [t['trust_weights']['E'] for t in telemetry]
    trust_P = [t['trust_weights']['P'] for t in telemetry]
    trust_S = [t['trust_weights']['S'] for t in telemetry]
    phase = [t['phase'] for t in telemetry]

    # Compute convergence metric
    convergence = compute_convergence_metric(telemetry)

    # Create subplots
    fig, axs = plt.subplots(3, 2, figsize=(15, 13))

    # 1. S_hat vs S_true
    axs[0, 0].plot(steps, S_hat, label='S_hat')
    axs[0, 0].plot(steps, S_true, label='S_true')
    axs[0, 0].set_title('S_hat vs S_true')
    axs[0, 0].legend()

    # 2. D_hat vs D_true
    axs[0, 1].plot(steps, D_hat, label='D_hat')
    axs[0, 1].plot(steps, D_true, label='D_true')
    axs[0, 1].set_title('D_hat vs D_true')
    axs[0, 1].legend()

    # 3. Alignment score over time
    axs[1, 0].plot(steps, alignment)
    axs[1, 0].set_title('Alignment Score over Time')

    # 4. Trust weights for H,E,P,S
    axs[1, 1].plot(steps, trust_H, label='H')
    axs[1, 1].plot(steps, trust_E, label='E')
    axs[1, 1].plot(steps, trust_P, label='P')
    axs[1, 1].plot(steps, trust_S, label='S')
    axs[1, 1].set_title('Trust Weights')
    axs[1, 1].legend()

    # 5. Phase evolution
    axs[2, 0].plot(steps, phase)
    axs[2, 0].set_title('Phase Evolution')

    # 6. Phase space plot: S_hat vs D_hat trajectory
    scatter = axs[2, 1].scatter(S_hat, D_hat, c=steps, cmap='viridis', s=30)
    axs[2, 1].plot(S_hat, D_hat, 'k-', alpha=0.3, linewidth=1)
    axs[2, 1].set_xlabel('S_hat')
    axs[2, 1].set_ylabel('D_hat')
    axs[2, 1].set_title('Phase Space: S_hat vs D_hat Trajectory')
    cbar = plt.colorbar(scatter, ax=axs[2, 1])
    cbar.set_label('Time (steps)')

    plt.tight_layout()
    
    # Save figure if directory specified
    if save_dir:
        filepath = os.path.join(save_dir, f"{filename_prefix}_all_diagnostics.png")
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"Saved diagnostic plot to {filepath}")
    
    # Print convergence analysis
    print("\n=== Convergence Analysis ===")
    print(f"Status: {convergence['status'].upper()}")
    print(f"Area ratio (last 20% / first 20%): {convergence['ratio']:.4f}")
    print(f"First 20% bounding box area: {convergence['area_first_20pct']:.6f}")
    print(f"Last 20% bounding box area: {convergence['area_last_20pct']:.6f}")
    
    # Show plot if requested
    if show:
        plt.show()
    else:
        plt.close()
    
    return convergence