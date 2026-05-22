from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class GameResult:
    name: str
    score: int


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
