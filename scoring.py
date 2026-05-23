MIN_SCORE = 0
MAX_SCORE = 10
MAX_PERCENT_SCORE = 100
LOW_LUCK_LIMIT = 2
AVERAGE_LUCK_LIMIT = 5
GOOD_LUCK_LIMIT = 8

LOW_LUCK_MESSAGE = "Heute verfolgt dich das Pech."
AVERAGE_LUCK_MESSAGE = "Durchschnittliches Glück."
GOOD_LUCK_MESSAGE = "Das Glück ist auf deiner Seite."
GREAT_LUCK_MESSAGE = "Heute könntest du den Jackpot knacken."
SCORE_COLOR_RED = "#ef4444"
SCORE_COLOR_ORANGE = "#f97316"
SCORE_COLOR_YELLOW = "#eab308"
SCORE_COLOR_GREEN = "#22c55e"
SCORE_COLOR_GOLD = "#f5c542"


def calculate_average_score(scores: list[float]) -> float:
    if not scores:
        return 0.0

    clamped_scores = [clamp_percent_score(score) for score in scores]
    return round(sum(clamped_scores) / len(clamped_scores), 1)


def calculate_luck_score(game_score: float) -> float:
    clamped_score = clamp_percent_score(game_score)
    return round(clamped_score / MAX_SCORE, 1)


def calculate_final_score(scores: list[int]) -> float:
    if not scores:
        return 0.0

    clamped_scores = [max(MIN_SCORE, min(MAX_SCORE, score)) for score in scores]
    return round(sum(clamped_scores) / len(clamped_scores), 1)


def clamp_percent_score(score: float) -> float:
    return max(0.0, min(float(MAX_PERCENT_SCORE), score))


def get_result_message(luck_score: float) -> str:
    if luck_score <= LOW_LUCK_LIMIT:
        return LOW_LUCK_MESSAGE

    if luck_score <= AVERAGE_LUCK_LIMIT:
        return AVERAGE_LUCK_MESSAGE

    if luck_score <= GOOD_LUCK_LIMIT:
        return GOOD_LUCK_MESSAGE

    return GREAT_LUCK_MESSAGE


def get_score_color(luck_score: float) -> str:
    if luck_score <= 2:
        return SCORE_COLOR_RED

    if luck_score <= 4:
        return SCORE_COLOR_ORANGE

    if luck_score <= 6:
        return SCORE_COLOR_YELLOW

    if luck_score <= 8:
        return SCORE_COLOR_GREEN

    return SCORE_COLOR_GOLD
