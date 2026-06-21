"""Greedy solver engine for delta search.

Provides the core optimization loop that drives concrete problem
implementations.  The solver evaluates candidate actions, selects
the one that maximizes the combined objective, and applies it.

Usage::

    from delta_search import Graph
    from delta_search.solver import GreedySolver
    from delta_search.problems import MaximumPlanarSubgraphProblem

    graph = Graph[int].from_edges([(1, 2), (2, 3), (3, 1)])
    problem = MaximumPlanarSubgraphProblem(graph)
    solver = GreedySolver(problem)
    result = solver.solve(max_iterations=100)
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from .graph import NodeT

if TYPE_CHECKING:
    from .problem import (
        Action,
        SolverObserver,
        SubgraphExtractionProblem,
        SubgraphState,
    )

__all__ = [
    "SolverState",
    "EarlyTerminationCondition",
    "GreedySolver",
]


@dataclass
class SolverState(Generic[NodeT]):
    """Snapshot of solver progress at any point.

    Attributes:
        iteration: Current iteration number (0-indexed).
        best_objective: Best objective value found so far.
        best_state: State corresponding to best_objective.
        total_evaluations: Total number of candidate actions evaluated.
        elapsed_ms: Total elapsed time in milliseconds.
        converged: Whether the solver has converged.
        convergence_reason: Human-readable reason for termination.
    """
    iteration: int = 0
    best_objective: float = float("-inf")
    best_state: SubgraphState[NodeT] | None = None
    total_evaluations: int = 0
    elapsed_ms: float = 0.0
    converged: bool = False
    convergence_reason: str = ""


@dataclass
class EarlyTerminationCondition(Generic[NodeT]):
    """Configurable early termination for the solver.

    All fields are optional.  A condition triggers when ANY of its
    non-None fields is satisfied.

    Attributes:
        max_iterations: Stop after this many iterations.
        max_evaluations: Stop after this many total action evaluations.
        max_time_ms: Stop after this many milliseconds.
        objective_target: Stop when objective reaches this value.
        stall_iterations: Stop after this many iterations with no improvement.
    """
    max_iterations: int | None = None
    max_evaluations: int | None = None
    max_time_ms: float | None = None
    objective_target: float | None = None
    stall_iterations: int | None = None


class GreedySolver(Generic[NodeT]):
    """Greedy optimization loop for delta search problems.

    At each iteration, the solver:

    1. Enumerates candidate actions via ``problem.enumerate_actions``.
    2. Evaluates each candidate via ``problem.calculate_delta``.
    3. Selects the feasible candidate with highest objective.
    4. Applies the selected action and advances the state.

    Args:
        problem: A concrete SubgraphExtractionProblem instance.
        early_stop: Optional termination conditions.

    Raises:
        ValueError: If ``max_iterations <= 0``.
    """
    def __init__(
        self,
        problem: SubgraphExtractionProblem[NodeT],
        early_stop: EarlyTerminationCondition[NodeT] | None = None,
    ) -> None:
        self.problem = problem
        self.early_stop = early_stop or EarlyTerminationCondition()

    def solve(
        self,
        max_iterations: int = 1000,
        observer: SolverObserver | None = None,
    ) -> SolverState[NodeT]:
        """Run the greedy optimization loop.

        Args:
            max_iterations: Fallback iteration cap (overridden by
                early_stop.max_iterations if set).
            observer: Optional observer for lifecycle events.

        Returns:
            SolverState with the best solution found.

        Raises:
            ValueError: If ``max_iterations <= 0``.
        """
        if max_iterations <= 0:
            raise ValueError(
                f"max_iterations must be positive, got {max_iterations}"
            )

        if observer:
            self.problem.set_observer(observer)

        state = self.problem.evaluate_initial_state(self.problem.graph)
        best_state = state
        best_objective = self.problem.objective(state)

        solver_state = SolverState[NodeT](
            best_objective=best_objective,
            best_state=best_state,
        )

        limit = (
            self.early_stop.max_iterations
            if self.early_stop.max_iterations is not None
            else max_iterations
        )
        stall_count = 0
        start_time = time.monotonic()

        for iteration in range(limit):
            self.problem.on_iteration_start(state, iteration)

            best_action, best_action_obj, evaluated = (
                self.evaluate_actions(state, best_objective, start_time)
            )
            solver_state.total_evaluations += evaluated

            if best_action is None:
                solver_state.converged = True
                solver_state.convergence_reason = "no actions available"
                break

            state = self.apply_best(state, best_action)

            elapsed_total = (time.monotonic() - start_time) * 1000
            solver_state.iteration = iteration + 1
            solver_state.elapsed_ms = elapsed_total

            if best_action_obj > best_objective:
                best_objective = best_action_obj
                best_state = state
                solver_state.best_objective = best_objective
                solver_state.best_state = best_state
                stall_count = 0
            else:
                stall_count += 1

            self.problem.observer.on_iteration_complete(
                iteration, best_action, best_action_obj,
            )
            self.problem.on_iteration_end(state, iteration)

            if self.check_termination(solver_state, stall_count):
                break

        solver_state.elapsed_ms = (time.monotonic() - start_time) * 1000
        self.problem.observer.on_convergence(
            solver_state.iteration, solver_state.best_objective,
        )

        return solver_state

    def evaluate_actions(
        self,
        state: SubgraphState[NodeT],
        current_objective: float,
        start_time: float,
    ) -> tuple[Action | None, float, int]:
        """Evaluate all candidate actions and select the best feasible one.

        Args:
            state: The current candidate state.
            current_objective: The objective value of the current state.
            start_time: The start time of the solve loop (for elapsed_ms).

        Returns:
            Tuple of (best_action, best_action_objective, num_evaluations).
            best_action is None if no feasible actions exist.
        """
        actions = self.problem.enumerate_actions(state)
        if not actions:
            return None, float("-inf"), 0

        best_action: Action | None = None
        best_action_obj = float("-inf")
        evaluated = 0

        for action in actions:
            candidate = self.problem.apply_action(state, action)
            if not self.problem.is_feasible(candidate):
                continue

            delta = self.problem.calculate_delta(state, action)
            obj = self.problem.objective(candidate)
            evaluated += 1

            elapsed = (time.monotonic() - start_time) * 1000
            self.problem.observer.on_action_evaluated(
                action,
                delta,
                elapsed,
            )

            if obj > best_action_obj:
                best_action_obj = obj
                best_action = action

        return best_action, best_action_obj, evaluated

    def apply_best(
        self,
        state: SubgraphState[NodeT],
        action: Action,
    ) -> SubgraphState[NodeT]:
        """Apply the selected best action to the state.

        Args:
            state: The current candidate state.
            action: The action to apply.

        Returns:
            The new state with the action applied.
        """
        return self.problem.apply_action(state, action)

    def check_termination(
        self,
        solver_state: SolverState[NodeT],
        stall_count: int,
    ) -> bool:
        """Check if any early termination condition is met.

        Args:
            solver_state: The current solver progress snapshot.
            stall_count: Number of iterations without improvement.

        Returns:
            True if the solver should stop.
        """
        cond = self.early_stop

        if (cond.max_evaluations is not None
                and solver_state.total_evaluations >= cond.max_evaluations):
            solver_state.converged = True
            solver_state.convergence_reason = (
                f"reached {cond.max_evaluations} evaluations"
            )
            return True

        if (cond.max_time_ms is not None
                and solver_state.elapsed_ms >= cond.max_time_ms):
            solver_state.converged = True
            solver_state.convergence_reason = (
                f"reached {cond.max_time_ms}ms time limit"
            )
            return True

        if (cond.objective_target is not None
                and solver_state.best_objective >= cond.objective_target):
            solver_state.converged = True
            solver_state.convergence_reason = (
                f"reached objective target {cond.objective_target}"
            )
            return True

        if (cond.stall_iterations is not None
                and stall_count >= cond.stall_iterations):
            solver_state.converged = True
            solver_state.convergence_reason = (
                f"stalled for {cond.stall_iterations} iterations"
            )
            return True

        return False
