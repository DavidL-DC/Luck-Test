MIN_SCORE = 0
MAX_SCORE = 10


def calculate_final_score(scores: list[int]) -> float:
    if not scores:
        return 0.0

    clamped_scores = [max(MIN_SCORE, min(MAX_SCORE, score)) for score in scores]
    return round(sum(clamped_scores) / len(clamped_scores), 1)
