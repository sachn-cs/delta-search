<!-- Badges -->
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/delta-search/delta-search/actions/workflows/ci.yml/badge.svg)](https://github.com/delta-search/delta-search/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://img.shields.io/pypi/v/delta-search.svg)](https://pypi.org/project/delta-search/)
[![Downloads](https://img.shields.io/pypi/dm/delta-search.svg)](https://pypi.org/project/delta-search/)

# ΔSearch

A general, fast heuristic framework for solving NP-hard subgraph extraction problems via Reward-Penalty optimization.

## Disclaimer

This is an **independent implementation** of the ΔSearch framework described in the paper below. It is **not affiliated with, endorsed by, or produced by the original authors** of the paper.

**Algorithm Credit:** The ΔSearch algorithm was developed by [Rebin Silva Valan Arasu](https://github.com/raabarah) and [Rajiv Gupta](https://cse.ucr.edu/~gupta/) at the University of California, Riverside. If you use this software in academic work, please cite their paper.

**Implementation Credit:** This Python package was written and maintained by [Sachin (sachn-cs)](https://github.com/sachn-cs).

**Paper:** [Solving Subgraph Extraction Problems Using ΔSearch](https://arxiv.org/abs/2606.13834) (arXiv:2606.13834)

## Features

- **General-purpose** — solves Maximum Planar Subgraph, UFLP, PCVC, Minimum Connected Dominating Set, MWIS, and MWST with a single framework
- **O(1) incremental deltas** — evaluates candidate moves without re-evaluating the entire graph
- **Undo-stack actions** — efficient state mutations with rollback support
- **Thread-safe graph** — concurrent access via `ThreadSafeGraph` with `RLock`
- **Observer protocol** — hook into solver lifecycle for logging, metrics, and tracing
- **Zero dependencies** — pure Python standard library; optional NetworkX interop
- **Fully typed** — `mypy --strict` compliant with `py.typed` marker

## Installation

```bash
# From source (recommended for development)
git clone https://github.com/delta-search/delta-search.git
cd delta-search
pip install -e ".[dev]"

# From PyPI
pip install delta-search
```

## Quick Start

```python
from delta_search import (
    Graph,
    GreedySolver,
    MaximumPlanarSubgraphProblem,
)

# Create input graph
graph = Graph[int].from_edges([(1, 2), (2, 3), (3, 1), (3, 4), (1, 4)])

# Initialize problem and solver
problem = MaximumPlanarSubgraphProblem(graph)
solver = GreedySolver(problem)

# Run the solver
result = solver.solve(max_iterations=100)

print(f"Objective: {result.best_objective}")
print(f"Converged: {result.converged} ({result.convergence_reason})")
print(f"Iterations: {result.iteration}")
```

See [docs/getting-started.md](docs/getting-started.md) for a detailed walkthrough.

## API Reference

### Core Types

| Type | Description |
|------|-------------|
| `Graph[Node]` | Adjacency-set graph with O(1) lookups |
| `ThreadSafeGraph[Node]` | Thread-safe wrapper with `RLock` |
| `Action` | A single candidate mutation (add/remove node/edge) |
| `ActionType` | Enum: `ADD_NODE`, `REMOVE_NODE`, `ADD_EDGE`, `REMOVE_EDGE` |
| `DeltaResult` | `(reward_change, penalty_change, feasible)` |
| `SubgraphState` | Protocol for state objects (must have `.graph`) |
| `SolverObserver` | Observer protocol for solver lifecycle events |
| `GreedySolver` | Greedy optimization loop |
| `SolverState` | Solver progress snapshot |
| `EarlyTerminationCondition` | Configurable stopping criteria |

### SubgraphExtractionProblem Methods

| Method | Required | Description |
|--------|----------|-------------|
| `evaluate_initial_state(graph)` | Yes | Generate starting candidate subgraph |
| `calculate_delta(state, action)` | Yes | Compute incremental objective change |
| `compute_reward(state)` | Yes | Scalar reward (higher = better) |
| `compute_penalty(state)` | Yes | Scalar penalty (lower = better) |
| `is_feasible(state)` | Yes | Check hard constraints |
| `enumerate_actions(state)` | No | Generate candidate actions |
| `generate_composite_actions(state)` | No | Add compound actions |
| `apply_action(state, action)` | No | Apply mutation with undo support |
| `undo_action(state)` | No | Reverse last action |

### Built-in Problems

| Problem | Class | Type |
|---------|-------|------|
| Maximum Planar Subgraph | `MaximumPlanarSubgraphProblem` | Monotone |
| Minimum Connected Dominating Set | `MinimumConnectedDominatingSetProblem` | Monotone |
| Maximum Weight Independent Set | `MaximumWeightedIndependentSetProblem` | Monotone |
| Prize Collecting Vertex Cover | `PrizeCollectingVertexCoverProblem` | Non-monotone |
| Uncapacitated Facility Location | `UncapacitatedFacilityLocationProblem` | Non-monotone |
| Minimum Weighted Steiner Tree | `MinimumWeightedSteinerTreeProblem` | Non-monotone |

## Project Structure

```
delta-search/
├── delta_search/          # Main package
│   ├── __init__.py        # Public API exports
│   ├── graph.py           # Graph data structures
│   ├── problem.py         # Abstract problem interface
│   ├── problems.py        # Concrete problem implementations
│   ├── solver.py          # Greedy solver engine
│   ├── utils.py           # Graph utility functions
│   ├── interop.py         # NetworkX conversion
│   ├── io.py              # JSON file I/O
│   ├── cli.py             # Command-line interface
│   └── py.typed           # PEP 561 marker
├── tests/                 # Test suite (227 tests)
│   ├── test_graph.py      # Graph unit tests
│   ├── test_problem.py    # Problem framework tests
│   ├── test_problems.py   # Concrete problem tests
│   ├── test_solver.py     # Solver tests
│   ├── test_utils.py      # Utility function tests
│   ├── test_interop.py    # NetworkX interop tests
│   ├── test_io.py         # File I/O tests
│   ├── test_cli.py        # CLI integration tests
│   └── conftest.py        # Shared fixtures
├── docs/                  # Documentation
│   ├── getting-started.md
│   ├── architecture.md
│   └── faq.md
├── .github/               # GitHub configuration
│   ├── workflows/
│   │   ├── ci.yml         # CI pipeline
│   │   └── release.yml    # PyPI release automation
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
├── .pre-commit-config.yaml
├── pyproject.toml         # Package configuration
├── CHANGELOG.md           # Version history
├── CONTRIBUTING.md        # Contribution guide
├── CODE_OF_CONDUCT.md     # Community standards
└── SECURITY.md            # Security policy
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Type check
mypy delta_search/

# Lint
ruff check .

# Format
ruff format .

# Security audit
pip-audit
```

## CLI Usage

```bash
# Solve a problem
delta-search solve --problem mps --graph input.json --output result.json

# Validate a graph
delta-search validate --graph input.json

# Available problems: mps, mcds, mwis, pcvc, uflp, mwst
```

## Tech Stack

- **Language:** Python 3.10+
- **Type Checker:** mypy (strict mode)
- **Linter:** ruff
- **Test Framework:** pytest
- **CI/CD:** GitHub Actions
- **Dependencies:** None (pure Python)

## Roadmap

- [x] Implement all 6 problem types from the paper
- [x] GreedySolver with early termination conditions
- [x] NetworkX graph interop
- [x] Thread-safe graph variant
- [x] Observer protocol for solver lifecycle
- [x] JSON file I/O
- [x] Command-line interface
- [x] PEP 561 typed package
- [x] CI with lint, typecheck, security scan, tests
- [x] PyPI release automation
- [ ] Benchmark suite against paper results
- [ ] Multi-start / randomized solver
- [ ] Visualization utilities
- [ ] Progress bar / streaming output

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards.

## Security

For security vulnerabilities, please see [SECURITY.md](SECURITY.md).

## Citation

If you use this **algorithm** in your research, please cite the original paper by Arasu and Gupta:

```bibtex
@article{arasu2026deltasearch,
  title={Solving Subgraph Extraction Problems Using $\Delta$Search},
  author={Arasu, Rebin Silva Valan and Gupta, Rajiv},
  journal={arXiv preprint arXiv:2606.13834},
  year={2026}
}
```

If you use this **software** (the Python implementation), please also credit [Sachin (sachn-cs)](https://github.com/sachn-cs).

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.
