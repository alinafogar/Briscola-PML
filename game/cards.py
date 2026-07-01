"""Cards and card values for a 40-card Briscola deck"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Suit(str, Enum):
    """The four suits used in this project"""

    CUPS = "cups"
    COINS = "coins"
    SWORDS = "swords"
    CLUBS = "clubs"


class Rank(str, Enum):
    """Ranks ordered as they appear in the deck builder"""

    ACE = "ace"
    THREE = "three"
    KING = "king"
    HORSE = "horse"
    JACK = "jack"
    SEVEN = "seven"
    SIX = "six"
    FIVE = "five"
    FOUR = "four"
    TWO = "two"


POINTS_BY_RANK: dict[Rank, int] = {
    Rank.ACE: 11,
    Rank.THREE: 10,
    Rank.KING: 4,
    Rank.HORSE: 3,
    Rank.JACK: 2,
    Rank.SEVEN: 0,
    Rank.SIX: 0,
    Rank.FIVE: 0,
    Rank.FOUR: 0,
    Rank.TWO: 0,
}

STRENGTH_BY_RANK: dict[Rank, int] = {
    Rank.TWO: 0,
    Rank.FOUR: 1,
    Rank.FIVE: 2,
    Rank.SIX: 3,
    Rank.SEVEN: 4,
    Rank.JACK: 5,
    Rank.HORSE: 6,
    Rank.KING: 7,
    Rank.THREE: 8,
    Rank.ACE: 9,
}


@dataclass(frozen=True, slots=True)
class Card:
    """One rank-suit card"""

    rank: Rank
    suit: Suit

    @property
    def points(self) -> int:
        return POINTS_BY_RANK[self.rank]

    @property
    def strength(self) -> int:
        return STRENGTH_BY_RANK[self.rank]

    def __str__(self) -> str:
        return f"{self.rank.value} of {self.suit.value}"


def full_deck() -> tuple[Card, ...]:
    """Build the full deck once in a predictable order"""

    return tuple(Card(rank, suit) for suit in Suit for rank in Rank)
