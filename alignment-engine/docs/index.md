# Documentation Index

## Overview Documents
- **[README.md](../README.md)**: Main entry point, quick start, architecture overview
- **[docs/mechanics.md](mechanics.md)**: Detailed technical specifications
- **[docs/roadmap.md](roadmap.md)**: Development planning and thread coordination
- **[docs/quickref.md](quickref.md)**: Cheat sheet for different user types

## Technical Reference
- **API Documentation**: Inline code comments
- **Test Coverage**: `pytest --cov` reports
- **CLI Help**: `python3 -m experiments.run_simulation --help`

## Development Resources
- **Git History**: `git log --oneline` for implementation timeline
- **Test Suite**: `pytest -v` for validation status
- **Artifacts**: Generated outputs in `artifacts/` directory

## Key Principles
1. **Reproducibility**: All runs have seeds, timestamps, run_ids
2. **Testability**: Comprehensive invariants prevent regressions
3. **Extensibility**: Modular design allows easy feature addition
4. **Transparency**: Full telemetry and diagnostics available

## Getting Started (3 minutes)
```bash
git clone <repo>
cd alignment-engine
pip install -r requirements.txt
python3 -m experiments.run_simulation
pytest  # Verify everything works
```

This documentation structure supports your multi-threaded development approach by providing:
- **Application users**: Clear usage examples and CLI tools
- **Engineers**: Extension points and integration guides
- **Mathematicians**: Formal specifications and analysis tools
- **All users**: Unified foundation with flexible pivot points