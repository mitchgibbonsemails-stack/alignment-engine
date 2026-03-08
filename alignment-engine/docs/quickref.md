# Quick Reference Guide

## For Different Perspectives

### 🎯 Application Users (End Users)
```bash
# Quick simulation
python3 -m experiments.run_simulation --steps 100 --seed 42

# Parameter study
python3 -m experiments.parameter_sweep --k_S_steps 5 --steps 50 --verbose

# Results in artifacts/
```

**Key Files:**
- `artifacts/sweep_results.csv`: Parameter sweep data
- `artifacts/*.png`: Diagnostic plots

### 🔧 Engineers (System Builders)
```python
# Core extension points
from engine.alignment_engine import AlignmentEngine

# Add custom operators
def my_operator(state, params):
    # Your logic here
    return updated_state

# Integrate into pipeline
engine = AlignmentEngine()
# Modify engine.update_state() to include my_operator
```

**Key Files:**
- `engine/operators.py`: Add new operators
- `engine/diagnostics.py`: Add new metrics
- `tests/test_invariants.py`: Update tests

### 🔬 Mathematicians (Theoretical Analysis)
```python
# Access internal state
engine = AlignmentEngine()
engine.run_simulation(num_steps=1000)

# Analyze convergence
from engine.diagnostics import compute_convergence_metric
conv = compute_convergence_metric(engine.telemetry)

# Study phase space
S_vals = [t['S_hat'] for t in engine.telemetry]
D_vals = [t['D_hat'] for t in engine.telemetry]
```

**Key Files:**
- `engine/alignment_engine.py`: State evolution equations
- `tests/test_invariants.py`: Invariant proofs
- `docs/mechanics.md`: Mathematical framework

## State Variables Reference

| Variable | Range | Meaning | Updated By |
|----------|-------|---------|------------|
| `S_hat` | [0,1] | Signal strength estimate | O4_lenses |
| `D_hat` | [0,1] | Distortion level estimate | O4_lenses |
| `alignment_score` | [0,1] | Overall alignment quality | O6_objective |
| `trust_weights['H']` | (0,1) | Historical performance | O5_gate |
| `trust_weights['E']` | (0,1) | Error consistency | O5_gate |
| `trust_weights['P']` | (0,1) | Prediction accuracy | O5_gate |
| `trust_weights['S']` | (0,1) | Signal stability | O5_gate |

## Parameter Reference

| Parameter | Default | Range | Effect |
|-----------|---------|-------|--------|
| `k_S` | 0.1 | [0.01, 0.5] | Signal processing gain |
| `k_D` | 0.1 | [0.01, 0.5] | Distortion sensitivity |
| `k_err` | 0.05 | [0.001, 0.2] | Error amplification |
| `lambda_Td` | 0.01 | [0.0001, 0.1] | Trust decay rate |

## Common Workflows

### Debugging a Simulation
```bash
# Run with debug mode
python3 -c "
from engine.alignment_engine import AlignmentEngine
engine = AlignmentEngine(debug=True)
engine.run_simulation(num_steps=10, verbose=True)
print('Final state:', engine.x)
"
```

### Adding a New Metric
```python
# In engine/diagnostics.py
def my_metric(telemetry):
    # Calculate something
    return result

# In plot_simulation()
my_result = my_metric(telemetry)
print(f"My metric: {my_result}")
```

### Testing Parameter Ranges
```bash
# Quick parameter sweep
python3 -m experiments.parameter_sweep \
  --k_S_min 0.01 --k_S_max 0.5 --k_S_steps 5 \
  --k_D_min 0.01 --k_D_max 0.5 --k_D_steps 5 \
  --steps 50 --seed 42 --verbose
```

## Troubleshooting

### Common Issues
- **Import errors**: `PYTHONPATH=. python3 -m experiments.run_simulation`
- **No plots**: Use `--show` flag or check matplotlib backend
- **Slow sweeps**: Reduce `--steps` or parameter grid size
- **Memory issues**: Process results in batches

### Getting Help
- **Application questions**: Check `README.md` examples
- **Engineering questions**: See `docs/mechanics.md`
- **Math questions**: Examine `engine/alignment_engine.py` comments
- **Bugs**: Run `pytest` to check for regressions

## File Organization

```
Quick lookup:
├── Run simulations → experiments/
├── Add features → engine/
├── Add tests → tests/
├── View results → artifacts/
├── Read docs → docs/
├── Interactive work → notebooks/
```