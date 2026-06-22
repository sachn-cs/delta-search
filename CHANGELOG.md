# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Context engineering module for RAG context selection under token budgets
- Test-time compute module for reasoning tree expansion under compute budgets
- Multi-objective optimization with Pareto frontier tracking
- Learned heuristic guidance with online model training
- Adaptive beam search with diversity-aware selection
- Hybrid pipeline for two-stage retrieval + reasoning
- Budget metrics for quality-per-token and quality-latency analysis
- Ablation study and scaling analysis utilities
- Theoretical approximation bounds and convergence analysis
- Progress bar (tqdm) and streaming observer output
- Streaming graph mutations with resume support
- Multi-start solver with random initial state generation

### Changed

- Refactored `SubgraphState` protocol to include `metrics` dict
- Made `DefaultState` generic over `NodeT` for type safety
- Replaced all `print()` calls with `logging` throughout codebase
- Improved encapsulation: private fields with controlled accessors
- Updated CI workflows to latest GitHub Actions versions

### Fixed

- Type hierarchy LSP violations in context_engineering and test_time_compute
- Removed all `# type: ignore` comments through proper type fixes
- Fixed file handle leak in StreamingObserver with proper cleanup

## [0.1.0] - 2026-06-15

### Added

- Initial release of the ΔSearch framework
- Core graph data structures with O(1) lookups and incremental mutation
- `ThreadSafeGraph` wrapper with `RLock` for concurrent access
- `SubgraphExtractionProblem` abstract base class with 5 required methods
- 6 concrete problem implementations:
  - Maximum Planar Subgraph (MPS)
  - Minimum Connected Dominating Set (MCDS)
  - Maximum Weighted Independent Set (MWIS)
  - Prize Collecting Vertex Cover (PCVC)
  - Uncapacitated Facility Location (UFLP)
  - Minimum Weighted Steiner Tree (MWST)
- `GreedySolver` with early termination conditions
- Undo-stack pattern with full rollback support
- `SolverObserver` protocol for lifecycle observability
- NetworkX graph interop via `to_networkx()` / `from_networkx()`
- JSON file I/O for graph serialization
- Command-line interface with solve and validate commands
- Full test suite (320 tests) with 80%+ coverage
- CI/CD pipeline with lint, typecheck, security scan, tests, and build
- PyPI release automation via GitHub Actions
- Documentation: getting-started, architecture, FAQ
- Community files: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- PEP 561 typed package with `py.typed` marker
- Zero runtime dependencies
