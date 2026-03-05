import numpy as np

class AlignmentEngine:
    def __init__(self):
        self.x = np.array([0.0, 0.0])

    def run_simulation(self, num_steps=10, shocks=None, seed=None, verbose=False):
        if seed is not None:
            np.random.seed(seed)
        for step in range(num_steps):
            if verbose:
                print(f"Step {step}")
            if shocks and step in shocks:
                print(f"Shock: {shocks[step]}")
            # Dummy update for demonstration
            self.x += np.random.random(2) * 0.1
        if verbose:
            print("Simulation done")