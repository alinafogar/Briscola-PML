"""Opponent models used to generate synthetic games"""

from opponents.features import (
    CORE_FEATURE_NAMES,
    FEATURE_NAMES,
    INTERACTION_FEATURE_NAMES,
    card_features,
    feature_dict,
)
from opponents.models import (
    AGGRESSIVE_THETA,
    CONSERVATIVE_THETA,
    GREEDY_POINTS_THETA,
    INTERACTION_AGGRESSIVE_THETA,
    INTERACTION_CONSERVATIVE_THETA,
    INTERACTION_GREEDY_POINTS_THETA,
    INTERACTION_RANDOM_THETA,
    RANDOM_THETA,
    RandomOpponent,
    ThetaSoftmaxOpponent,
    theta_from_weights,
    zero_theta,
)

__all__ = [
    "AGGRESSIVE_THETA",
    "CONSERVATIVE_THETA",
    "CORE_FEATURE_NAMES",
    "FEATURE_NAMES",
    "GREEDY_POINTS_THETA",
    "INTERACTION_AGGRESSIVE_THETA",
    "INTERACTION_CONSERVATIVE_THETA",
    "INTERACTION_FEATURE_NAMES",
    "INTERACTION_GREEDY_POINTS_THETA",
    "INTERACTION_RANDOM_THETA",
    "RANDOM_THETA",
    "RandomOpponent",
    "ThetaSoftmaxOpponent",
    "card_features",
    "feature_dict",
    "theta_from_weights",
    "zero_theta",
]
