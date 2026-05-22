from dataclasses import dataclass
from enum import StrEnum
from random import choice
from typing import Protocol


COIN_TOSS_COUNT = 10
PERCENT_MULTIPLIER = 100


class CoinSide(StrEnum):
    HEADS = "Kopf"
    TAILS = "Zahl"


@dataclass(frozen=True)
class GameResult:
    name: str
    score: float
    hits: int
    total_rounds: int
    selected_side: CoinSide
    tosses: list[CoinSide]


class MiniGame(Protocol):
    name: str

    def start(self) -> None:
        ...

    def get_result(self) -> GameResult | None:
        ...


class LuckGameRegistry:
    def __init__(self) -> None:
        self._games: list[MiniGame] = []

    def register(self, game: MiniGame) -> None:
        self._games.append(game)

    def get_games(self) -> list[MiniGame]:
        return list(self._games)


class CoinTossGame:
    name = "Münzwurf-Serie"

    def __init__(self, toss_count: int = COIN_TOSS_COUNT) -> None:
        self._toss_count = toss_count

    def play(self, selected_side: CoinSide) -> GameResult:
        tosses = [self._toss_coin() for _ in range(self._toss_count)]
        hits = sum(toss == selected_side for toss in tosses)
        score = self._calculate_points(hits)

        return GameResult(
            name=self.name,
            score=score,
            hits=hits,
            total_rounds=self._toss_count,
            selected_side=selected_side,
            tosses=tosses,
        )

    def _toss_coin(self) -> CoinSide:
        return choice(list(CoinSide))

    def _calculate_points(self, hits: int) -> float:
        return round(hits / self._toss_count * PERCENT_MULTIPLIER, 1)
