"""Collect observed moves from simulated Briscola games"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from game import BriscolaGame, Card, PlayerId, PlayerView, PublicState, TrickResult
from opponents import RandomOpponent


class MoveChooser(Protocol):
    """Small interface used by the simulator loop"""

    def choose_card(self, view: PlayerView) -> Card:
        """Choose one card from the current hand"""


@dataclass(frozen=True, slots=True)
class OpponentMoveObservation:
    """Snapshot taken just before the observed opponent plays"""

    game_id: int
    move_index: int
    trick_index: int
    player: PlayerId
    observer_player: PlayerId
    public_state: PublicState
    observer_hand: tuple[Card, ...]
    opponent_hand: tuple[Card, ...]
    legal_cards: tuple[Card, ...]
    chosen_card: Card
    theta_name: str | None = None


@dataclass(frozen=True, slots=True)
class SyntheticGameResult:
    """Finished game and the observations collected from it"""

    game_id: int
    observations: tuple[OpponentMoveObservation, ...]
    trick_history: tuple[TrickResult, ...]
    final_scores: tuple[int, int]
    winner: PlayerId | None


def play_synthetic_game(
    observed_model: MoveChooser,
    observer_model: MoveChooser | None = None,
    *,
    game_id: int = 0,
    seed: int | None = None,
    observer_player: PlayerId = 0,
    observed_player: PlayerId = 1,
    theta_name: str | None = None,
) -> SyntheticGameResult:
    """Run one game and record the selected opponent's moves"""

    _validate_players(observer_player, observed_player)
    if observer_model is None:
        observer_model = RandomOpponent(seed=_derived_seed(seed, game_id, offset=10_000))

    game = BriscolaGame.new(seed=seed, first_player=0)
    models = {
        observer_player: observer_model,
        observed_player: observed_model,
    }
    observations: list[OpponentMoveObservation] = []

    while not game.finished:
        current_player = game.public_state().current_player
        if current_player is None:
            raise RuntimeError("unfinished game has no current player")

        view = game.player_view(current_player)
        chosen_card = models[current_player].choose_card(view)

        if current_player == observed_player:
            observations.append(
                _build_observation(
                    game=game,
                    game_id=game_id,
                    move_index=len(observations),
                    observer_player=observer_player,
                    observed_player=observed_player,
                    chosen_card=chosen_card,
                    theta_name=theta_name,
                )
            )

        game.play_card(current_player, chosen_card)

    return SyntheticGameResult(
        game_id=game_id,
        observations=tuple(observations),
        trick_history=tuple(game.trick_history),
        final_scores=(game.scores[0], game.scores[1]),
        winner=game.winner(),
    )


def collect_observations(
    observed_model: MoveChooser,
    observer_model: MoveChooser | None = None,
    *,
    num_games: int,
    seed: int | None = None,
    observer_player: PlayerId = 0,
    observed_player: PlayerId = 1,
    theta_name: str | None = None,
) -> tuple[OpponentMoveObservation, ...]:
    """Run several games and concatenate their observations"""

    if num_games < 0:
        raise ValueError("num_games must be non-negative")

    observations: list[OpponentMoveObservation] = []
    for game_id in range(num_games):
        result = play_synthetic_game(
            observed_model=observed_model,
            observer_model=observer_model,
            game_id=game_id,
            seed=_derived_seed(seed, game_id),
            observer_player=observer_player,
            observed_player=observed_player,
            theta_name=theta_name,
        )
        observations.extend(result.observations)
    return tuple(observations)


def _build_observation(
    *,
    game: BriscolaGame,
    game_id: int,
    move_index: int,
    observer_player: PlayerId,
    observed_player: PlayerId,
    chosen_card: Card,
    theta_name: str | None,
) -> OpponentMoveObservation:
    public_state = game.public_state()
    opponent_hand = tuple(game.hands[observed_player])

    return OpponentMoveObservation(
        game_id=game_id,
        move_index=move_index,
        trick_index=public_state.tricks_played,
        player=observed_player,
        observer_player=observer_player,
        public_state=public_state,
        observer_hand=tuple(game.hands[observer_player]),
        opponent_hand=opponent_hand,
        legal_cards=opponent_hand,
        chosen_card=chosen_card,
        theta_name=theta_name,
    )


def _validate_players(observer_player: PlayerId, observed_player: PlayerId) -> None:
    if observer_player not in (0, 1):
        raise ValueError("observer_player must be 0 or 1")
    if observed_player not in (0, 1):
        raise ValueError("observed_player must be 0 or 1")
    if observer_player == observed_player:
        raise ValueError("observer_player and observed_player must differ")


def _derived_seed(seed: int | None, game_id: int, offset: int = 0) -> int | None:
    if seed is None:
        return None
    return seed + offset + game_id
