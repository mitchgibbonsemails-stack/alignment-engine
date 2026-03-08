import numpy as np
import uuid
from datetime import datetime

class AlignmentEngine:
    def __init__(self, config=None, debug=False):
        # Initialize 8-node lattice state variables (normalized [0,1])
        # Canonical state representation: X = [S, D, C, K, B, T_u, Ω, Λ]
        self.state = {
            'S': 0.5,        # Signal clarity and reliability
            'D': 0.5,        # Distortion level
            'C': 0.5,        # Constraint load
            'K': 0.5,        # Structural inertia
            'B': 0.5,        # System capacity
            'T_u': 0.5,      # Usable time available
            'Omega': 0.5,    # Option space available
            'Lambda': 0.5    # Coupling strength
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
            
            # 1. Signal processing (S): Update signal clarity with noise
            signal_noise = np.random.normal(0, 0.05)
            self.state['S'] += self.k_S * (self.S_true/20.0 - self.state['S']) + signal_noise
            
            # 2. Distortion detection (D): Measure error between signal and reality
            distortion_error = abs(self.state['S'] - self.S_true/20.0)
            self.state['D'] += self.k_D * (distortion_error - self.state['D'])
            
            # 3. Constraint load (C): External limits resisting change
            # Constraints increase with distortion and decrease with capacity
            constraint_pressure = 0.01 * (self.state['D'] - self.state['B'])
            self.state['C'] += constraint_pressure
            
            # 4. Options expansion/contraction (Ω): Based on distortion and constraints
            if self.state['D'] < 0.3 and self.state['C'] < 0.4:  # Low distortion & constraints = expand options
                self.state['Omega'] += 0.02
            else:  # High distortion or constraints = contract options
                self.state['Omega'] -= 0.02
            
            # 5. Structural inertia (K): Accumulate constraints based on system rigidity
            if self.state['C'] > 0.6:  # High constraints increase structural inertia
                self.state['K'] += 0.01
            else:  # Low constraints allow structural flexibility
                self.state['K'] -= 0.005
            
            # 6. Capacity management (B): Resource allocation based on structure and constraints
            capacity_efficiency = 1.0 - self.state['K'] - self.state['C']
            self.state['B'] += 0.01 * capacity_efficiency
            
            # 7. Coupling dynamics (Λ): Interaction strength based on capacity and constraints
            if self.state['B'] > 0.6 and self.state['C'] < 0.4:
                self.state['Lambda'] += 0.005  # Strong coupling when capacity high and constraints low
            else:
                self.state['Lambda'] -= 0.005  # Weak coupling when capacity low or constraints high
            
            # 8. Usable time (T_u): Time available before degradation
            time_pressure = self.state['D'] + self.state['C'] - self.state['B']
            self.state['T_u'] -= 0.01 * time_pressure
            
            # Update alignment score based on distortion reduction and option preservation
            alignment_improvement = max(0, 0.5 - self.state['D']) + max(0, self.state['Omega'] - 0.4)
            self.alignment_score += 0.01 * alignment_improvement
            
            # Update trust weights based on prediction accuracy and constraint respect
            prediction_error = abs(self.state['S'] - self.S_true/20.0)
            constraint_violation = max(0, self.state['C'] - 0.8)
            for k in self.trust_weights:
                if prediction_error < 0.1 and constraint_violation < 0.1:  # Good prediction & constraint respect
                    self.trust_weights[k] += 0.005
                else:  # Poor prediction or constraint violation
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