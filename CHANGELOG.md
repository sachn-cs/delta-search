# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `Graph` class with O(1) neighbor/edge lookups and incremental mutation
- `ThreadSafeGraph` wrapper with `RLock` for concurrent access
- `SubgraphExtractionProblem` abstract base class with 5 required methods
- `SubgraphState` protocol for type-safe state objects
- `SolverObserver` protocol for solver lifecycle observability
- `Action` and `DeltaResult` named tuples for the Reward-Penalty loop
- Undo-stack pattern in `apply_action` with full rollback support
- `generate_composite_actions` hook for compound moves
- Defensive copy in `SubgraphExtractionProblem.__init__`
- Canonical edge ordering to prevent duplicate action enumeration
- Self-loop rejection at API boundary
- 89 tests covering graph operations, problem framework, and edge cases
- CI/CD pipeline with lint, typecheck, test, and build stages
- Documentation: README, getting-started, architecture, FAQ
- Community files: CONTRIBUTING, CODE_OF_CONDUCT, SECURITY
- GitHub templates: issue templates, PR template, dependabot config

### Changed

- N/A (initial release)

### Fixed

- N/A (initial release)

### Removed

- N/A (initial release)

## [0.1.0] - 2026-06-15

### Added

- Initial release of the ΔSearch framework
- Core graph data structures and problem interface
- Full test suite and CI/CD pipeline
