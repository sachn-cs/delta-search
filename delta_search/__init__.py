"""Delta search -- a general heuristic framework for subgraph extraction.

This package provides the foundational data structures and abstract
interfaces described in "Solving Subgraph Extraction Problems Using
Delta Search" (arXiv:2606.13834).

Public API:
    Graph: Optimized adjacency-set graph representation.
    ThreadSafeGraph: Thread-safe wrapper around Graph.
    Action: A single candidate mutation (add/remove node/edge).
    ActionType: Enum of primitive mutation kinds.
    DeltaResult: Return type of calculate_delta.
    SubgraphExtractionProblem: Abstract base class for concrete problems.
    SubgraphState: Protocol for state objects.
    SolverObserver: Observer protocol for solver lifecycle events.
    GreedySolver: Greedy optimization loop.
    SolverState: Solver progress snapshot.
    EarlyTerminationCondition: Configurable stopping criteria.
    DefaultState: Generic mutable state for problems.
    ProblemType: Monotone vs non-monotone classification.
"""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .graph import Graph, ThreadSafeGraph
from .problem import (
    Action,
    ActionType,
    DefaultState,
    DeltaResult,
    NullObserver,
    SolverObserver,
    SubgraphExtractionProblem,
    SubgraphState,
    UndoEntry,
)
from .problems import (
    MaximumPlanarSubgraphProblem,
    MaximumWeightedIndependentSetProblem,
    MinimumConnectedDominatingSetProblem,
    MinimumWeightedSteinerTreeProblem,
    PrizeCollectingVertexCoverProblem,
    ProblemType,
    UncapacitatedFacilityLocationProblem,
)
from .solver import EarlyTerminationCondition, GreedySolver, SolverState

__all__ = [
    "Graph",
    "ThreadSafeGraph",
    "Action",
    "ActionType",
    "DeltaResult",
    "NullObserver",
    "SolverObserver",
    "SubgraphExtractionProblem",
    "SubgraphState",
    "UndoEntry",
    "GreedySolver",
    "SolverState",
    "EarlyTerminationCondition",
    "DefaultState",
    "ProblemType",
    "MaximumPlanarSubgraphProblem",
    "MinimumConnectedDominatingSetProblem",
    "MaximumWeightedIndependentSetProblem",
    "PrizeCollectingVertexCoverProblem",
    "UncapacitatedFacilityLocationProblem",
    "MinimumWeightedSteinerTreeProblem",
]

try:
    __version__ = version("delta-search")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
