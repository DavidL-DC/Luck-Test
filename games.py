from dataclasses import dataclass
from enum import StrEnum
from random import choice, randint, shuffle
from typing import Protocol


COIN_TOSS_COUNT = 10
PERCENT_MULTIPLIER = 100
LUCKY_NUMBER_MIN = 1
LUCKY_NUMBER_MAX = 20
LUCKY_NUMBER_MAX_POINTS = 100
LUCKY_NUMBER_POINT_STEP = 20
LUCKY_NUMBER_ZERO_LIMIT = 5
TREASURE_GRID_SIZE = 3
TREASURE_OPEN_COUNT = 3
TREASURE_MAX_POINTS = 100
TREASURE_DISTRIBUTION = (
    ("Jackpot", 100, 1),
    ("Großes Glück", 60, 2),
    ("Kleines Glück", 30, 3),
    ("Niete", 0, 3),
)


class CoinSide(StrEnum):
    HEADS = "Kopf"
    TAILS = "Zahl"


@dataclass(frozen=True)
class CoinTossResult:
    name: str
    score: float
    hits: int
    total_rounds: int
    selected_side: CoinSide
    tosses: list[CoinSide]


@dataclass(frozen=True)
class LuckyNumberResult:
    name: str
    score: float
    selected_number: int
    drawn_number: int
    difference: int


@dataclass(frozen=True)
class TreasureChest:
    label: str
    points: int


@dataclass(frozen=True)
class TreasureChestResult:
    name: str
    score: float
    opened_chests: list[TreasureChest]
    opened_count: int


class MiniGame(Protocol):
    name: str


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

    def play(self, selected_side: CoinSide) -> CoinTossResult:
        tosses = [self._toss_coin() for _ in range(self._toss_count)]
        hits = sum(toss == selected_side for toss in tosses)
        score = self._calculate_points(hits)

        return CoinTossResult(
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


class LuckyNumberGame:
    name = "Glückszahl"

    def __init__(
        self,
        min_number: int = LUCKY_NUMBER_MIN,
        max_number: int = LUCKY_NUMBER_MAX,
    ) -> None:
        self._min_number = min_number
        self._max_number = max_number

    def play(self, selected_number: int) -> LuckyNumberResult:
        drawn_number = randint(self._min_number, self._max_number)
        difference = abs(selected_number - drawn_number)
        score = self._calculate_points(difference)

        return LuckyNumberResult(
            name=self.name,
            score=score,
            selected_number=selected_number,
            drawn_number=drawn_number,
            difference=difference,
        )

    def get_options(self) -> list[int]:
        return list(range(self._min_number, self._max_number + 1))

    def _calculate_points(self, difference: int) -> float:
        if difference >= LUCKY_NUMBER_ZERO_LIMIT:
            return 0.0

        points = LUCKY_NUMBER_MAX_POINTS - difference * LUCKY_NUMBER_POINT_STEP
        return float(points)


class TreasureChestGame:
    name = "Schatzkisten"

    def create_chests(self) -> list[TreasureChest]:
        chests = [
            TreasureChest(label=label, points=points)
            for label, points, amount in TREASURE_DISTRIBUTION
            for _ in range(amount)
        ]
        shuffle(chests)
        return chests

    def score_opened_chests(
        self,
        opened_chests: list[TreasureChest],
    ) -> TreasureChestResult:
        total_points = sum(chest.points for chest in opened_chests)
        score = min(float(TREASURE_MAX_POINTS), float(total_points))

        return TreasureChestResult(
            name=self.name,
            score=score,
            opened_chests=opened_chests,
            opened_count=len(opened_chests),
        )
