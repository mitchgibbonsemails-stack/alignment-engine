# Alignment Engine

A cybernetic control system implementing measurement-driven alignment mechanics through prediction without belief.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run basic simulation with diagnostics
python3 -m experiments.run_simulation --steps 200 --seed 42

# Run parameter sweep
python3 -m experiments.parameter_sweep --k_S_steps 3 --k_D_steps 3 --steps 100 --verbose

# Run tests
pytest
```

## What This Is

The Alignment Engine is a framework for building systems that:
- Learn through measurement rather than assumption
- Build trust through empirical validation
- Maintain stability through bounded state spaces
- Provide transparency through comprehensive diagnostics

## Three Levels of Engagement

### 🔬 Application Level (End Users)
Black-box usage for simulation and analysis:
- Run simulations with different parameters
- Analyze convergence behavior
- Generate diagnostic plots
- Export results for further analysis

### ⚙️ Engineering Level (Developers)
System architecture and extension:
- Add new operators to the pipeline
- Implement domain-specific mechanics
- Extend diagnostic capabilities
- Build new experimental workflows

### 🔢 Mathematical Level (Researchers)
Theoretical foundations and analysis:
- Study convergence properties
- Analyze parameter sensitivity
- Prove system invariants
- Extend mathematical framework

## Architecture Overview

```
alignment-engine/
├── engine/                 # Core implementation
│   ├── alignment_engine.py # Main simulation engine
│   ├── diagnostics.py      # Analysis and plotting
│   └── operators.py        # Operator pipeline (extensible)
├── experiments/            # Simulation runners
│   ├── run_simulation.py   # Single simulation
│   └── parameter_sweep.py  # Grid search over parameters
├── notebooks/              # Interactive exploration
├── tests/                  # Comprehensive test suite
│   ├── test_engine.py      # Basic functionality
│   ├── test_invariants.py  # State constraints
│   └── test_parameter_sweep.py # Sweep validation
├── docs/                   # Documentation
└── artifacts/              # Generated outputs
```

## Core Concepts

### State Variables (All ∈ [0,1])
- **S_hat**: Signal strength estimate
- **D_hat**: Distortion level estimate
- **Trust Weights**: H,E,P,S (credibility components)

### Control Parameters
- **k_S**: Signal processing gain
- **k_D**: Distortion sensitivity
- **k_err**: Error amplification
- **λ_Td**: Trust decay rate

### Key Invariants
- All normalized variables stay in [0,1]
- No NaN values in telemetry
- Trust weights sum appropriately
- System remains bounded under shocks

## Current Capabilities

### ✅ Implemented
- Complete simulation framework with telemetry
- State clipping and sanity checking
- Comprehensive diagnostics (6 plot types + convergence analysis)
- Parameter sweep infrastructure (4D grid search)
- CSV export and reproducibility
- Full test suite (11 tests, all passing)
- CLI interfaces with argparse

### 🚧 Ready for Extension
- Operator pipeline (`engine/operators.py`)
- Domain-specific mechanics integration
- Advanced convergence metrics
- Multi-agent scenarios

## Usage Examples

### Single Simulation
```bash
# Basic run
python3 -m experiments.run_simulation

# With custom parameters and plots
python3 -m experiments.run_simulation \
  --steps 500 \
  --seed 123 \
  --save_dir results \
  --shock 100:DISRUPTION 300:RECOVERY
```

### Parameter Exploration
```bash
# Small sweep (3x3x3x3 = 81 runs)
python3 -m experiments.parameter_sweep \
  --k_S_steps 3 --k_D_steps 3 \
  --k_err_steps 3 --lambda_Td_steps 3 \
  --steps 200 --verbose

# Analyze results in artifacts/sweep_results.csv
```

### Interactive Exploration
```python
# In notebooks/exploration.ipynb
from engine.alignment_engine import AlignmentEngine
from engine.diagnostics import plot_simulation

engine = AlignmentEngine()
engine.run_simulation(num_steps=100, seed=42)
plot_simulation(engine.telemetry)
```

## Development Status

**Phase 1: Foundation** ✅
- Core simulation engine
- Basic operators (placeholder)
- Diagnostic infrastructure
- Testing framework

**Phase 2: Mechanics** 🔄
- Implement domain-specific operators
- Advanced convergence analysis
- Multi-dimensional parameter sweeps
- Performance optimization

**Phase 3: Applications** 📋
- Real-world problem adaptation
- Multi-agent extensions
- Integration APIs
- Production deployment

## Contributing

### Adding New Operators
1. Define function in `engine/operators.py`
2. Add to pipeline in `AlignmentEngine.update_state()`
3. Update tests in `tests/test_invariants.py`

### Adding Diagnostics
1. Implement metric in `engine/diagnostics.py`
2. Add to `plot_simulation()` output
3. Include in sweep results CSV

### Testing Changes
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=engine --cov-report=html

# Specific test file
pytest tests/test_invariants.py -v
```

## Dependencies

- numpy: Numerical computations
- matplotlib: Plotting and visualization
- pandas: Data manipulation (future use)

## License

See LICENSE file (to be created).

## Contact

For questions about different usage levels:
- **Application**: Use the CLI examples above
- **Engineering**: Check `docs/mechanics.md`
- **Mathematical**: Examine `engine/alignment_engine.py` implementation