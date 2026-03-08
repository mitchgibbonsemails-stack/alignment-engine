import numpy as np
import uuid
from datetime import datetime

class AlignmentEngine:
    def __init__(self, config=None, debug=False):
        # Initialize 8-node lattice state variables (normalized [0,1])
        self.state = {
            'S_hat': 0.5,      # Signal estimate (Node S)
            'D_hat': 0.5,      # Distortion estimate (Node D) 
            'option_space': 0.5,  # Available options (Node Ω)
            'action': 0.5,     # Current action (Node A)
            'K_constraint': 0.5,   # Structural constraints (Node K)
            'B_capacity': 0.5,     # System capacity (Node B)
            'Lambda_coupling': 0.5, # Coupling strength (Node Λ)
            'T_time': 0.0      # Time evolution (Node T)
        }
        
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
        for key in self.state:
            self.state[key] = np.clip(self.state[key], 0.0, 1.0)
        self.alignment_score = np.clip(self.alignment_score, 0.0, 1.0)
    
    def _sanity_check(self):
        """Assert no NaNs and state within bounds."""
        for key, value in self.state.items():
            if np.isnan(value):
                raise ValueError(f"NaN detected in state[{key}]: {value}")
            if value < 0 or value > 1:
                raise ValueError(f"State variable {key}={value} out of bounds [0,1]")
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
            
            # Diamond Layer Architecture update cycle
            # Signal → Distortion → Options → Action → Structure → Capacity → Coupling → Time
            
            # 1. Signal processing (Node S): Update signal estimate with noise
            signal_noise = np.random.normal(0, 0.05)
            self.state['S_hat'] += self.k_S * (self.S_true/20.0 - self.state['S_hat']) + signal_noise
            
            # 2. Distortion detection (Node D): Measure error between signal and reality
            distortion_error = abs(self.state['S_hat'] - self.S_true/20.0)
            self.state['D_hat'] += self.k_D * (distortion_error - self.state['D_hat'])
            
            # 3. Options expansion/contraction (Node Ω): Based on distortion level
            if self.state['D_hat'] < 0.3:  # Low distortion = expand options
                self.state['option_space'] += 0.02
            else:  # High distortion = contract options
                self.state['option_space'] -= 0.02
            
            # 4. Action selection (Node A): Choose based on options and distortion
            if self.state['option_space'] > 0.5 and self.state['D_hat'] < 0.4:
                self.state['action'] = 0.7  # Positive action (+1)
            elif self.state['D_hat'] > 0.6:
                self.state['action'] = 0.3  # Negative action (-1)
            else:
                self.state['action'] = 0.5  # Neutral action (0)
            
            # 5. Structure update (Node K): Accumulate constraints based on actions
            if self.state['action'] > 0.6:  # Positive actions reduce constraints
                self.state['K_constraint'] -= 0.01
            else:  # Negative actions increase constraints
                self.state['K_constraint'] += 0.01
            
            # 6. Capacity management (Node B): Resource allocation based on structure
            capacity_efficiency = 1.0 - self.state['K_constraint']
            self.state['B_capacity'] += 0.01 * capacity_efficiency
            
            # 7. Coupling dynamics (Node Λ): Interaction strength based on capacity
            if self.state['B_capacity'] > 0.6:
                self.state['Lambda_coupling'] += 0.005  # Strong coupling when capacity high
            else:
                self.state['Lambda_coupling'] -= 0.005  # Weak coupling when capacity low
            
            # 8. Time evolution (Node T): Increment time
            self.state['T_time'] += 0.1
            
            # Update alignment score based on distortion reduction
            alignment_improvement = max(0, 0.5 - self.state['D_hat'])
            self.alignment_score += 0.01 * alignment_improvement
            
            # Update trust weights based on prediction accuracy
            prediction_error = abs(self.state['S_hat'] - self.S_true/20.0)
            for k in self.trust_weights:
                if prediction_error < 0.1:  # Good prediction
                    self.trust_weights[k] += 0.005
                else:  # Poor prediction
                    self.trust_weights[k] -= 0.005
            
            self.phase += 1
            
            # Clip state to maintain invariants
            self._clip_state()
            
            # Sanity check if debug enabled
            if self.debug:
                self._sanity_check()
            
            # Collect telemetry
            telemetry_entry = self.state.copy()
            telemetry_entry.update({
                'S_true': self.S_true,
                'D_true': self.D_true,
                'alignment_score': self.alignment_score,
                'trust_weights': self.trust_weights.copy(),
                'phase': self.phase
            })
            self.telemetry.append(telemetry_entry)
            
        if verbose:
            print("Simulation done")
        self.telemetry_meta['end_time'] = datetime.now().isoformat()
    
    def get_telemetry_with_meta(self):
        """Return telemetry data with metadata."""
        return {
            'meta': self.telemetry_meta,
            'data': self.telemetry
        }