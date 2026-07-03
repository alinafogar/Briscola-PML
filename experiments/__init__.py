"""Helpers for collecting synthetic games"""

from experiments.episode_collection import (
    MoveChooser,
    OpponentMoveObservation,
    SyntheticGameResult,
    collect_observations,
    play_synthetic_game,
)

__all__ = [
    "MoveChooser",
    "OpponentMoveObservation",
    "SyntheticGameResult",
    "collect_observations",
    "play_synthetic_game",
]