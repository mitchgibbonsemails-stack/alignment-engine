import numpy as np
import uuid
from datetime import datetime

class AlignmentEngine:
    def __init__(self, config=None, debug=False):
        self.x = np.array([0.0, 0.0])
        self.telemetry = []
        self.S_true = 10.0
        self.D_true = 10.0
        self.alignment_score = 0.0
        self.trust_weights = {'H': 0.25, 'E': 0.25, 'P': 0.25, 'S': 0.25}
        self.phase = 0
        self.debug = debug
        self.run_id = str(uuid.uuid4())
        
        # Default parameter values
        self.k_S = 0.1
        self.k_D = 0.1
        self.k_err = 0.05
        self.lambda_Td = 0.01
        
        # Update from config if provided
        self.config = config or {}
        if config:
            self.k_S = config.get('k_S', self.k_S)
            self.k_D = config.get('k_D', self.k_D)
            self.k_err = config.get('k_err', self.k_err)
            self.lambda_Td = config.get('lambda_Td', self.lambda_Td)
        
        self.telemetry_meta = {
            'run_id': self.run_id,
            'config': self.config,
            'start_time': datetime.now().isoformat(),
            'parameters': {
                'k_S': self.k_S,
                'k_D': self.k_D,
                'k_err': self.k_err,
                'lambda_Td': self.lambda_Td
            }
        }

    def _clip_state(self):
        """Clip state variables to [0, 1] to maintain invariants."""
        self.x = np.clip(self.x, 0.0, 1.0)
        self.alignment_score = np.clip(self.alignment_score, 0.0, 1.0)
    
    def _sanity_check(self):
        """Assert no NaNs and state within bounds."""
        if np.any(np.isnan(self.x)):
            raise ValueError(f"NaN detected in state: {self.x}")
        if np.any(self.x < 0) or np.any(self.x > 1):
            raise ValueError(f"State out of bounds [0,1]: {self.x}")
        if np.isnan(self.alignment_score):
            raise ValueError("NaN detected in alignment_score")
        for k, v in self.trust_weights.items():
            if np.isnan(v) or v <= 0 or v >= 1:
                raise ValueError(f"Trust weight {k}={v} out of bounds (0,1)")
    
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
            self.alignment_score += 0.01
            self.phase += 1
            # Update trust weights randomly
            for k in self.trust_weights:
                self.trust_weights[k] += np.random.random() * 0.01
            # Clip state to maintain invariants
            self._clip_state()
            # Sanity check if debug enabled
            if self.debug:
                self._sanity_check()
            # Collect telemetry
            self.telemetry.append({
                'S_hat': self.x[0],
                'S_true': self.S_true,
                'D_hat': self.x[1],
                'D_true': self.D_true,
                'alignment_score': self.alignment_score,
                'trust_weights': self.trust_weights.copy(),
                'phase': self.phase
            })
        if verbose:
            print("Simulation done")
        self.telemetry_meta['end_time'] = datetime.now().isoformat()
    
    def get_telemetry_with_meta(self):
        """Return telemetry data with metadata."""
        return {
            'meta': self.telemetry_meta,
            'data': self.telemetry
        }