PRIORITY_ORDER = {
    "HIGH": 1,
    "MEDIUM": 2,
    "OPPORTUNITY": 3,
    "LOW": 4,
}


def calculate_priority(recommendations):
    """
    Sorts advisory recommendations from highest
    priority to lowest priority.
    """

    sorted_recommendations = sorted(
        recommendations,
        key=lambda item: PRIORITY_ORDER.get(
            item.get("priority", "LOW"),
            3
        )
    )

    return sorted_recommendations


def get_highest_priority(recommendations):
    """
    Returns the most important recommendation.
    """

    if not recommendations:
        return None

    sorted_recommendations = calculate_priority(recommendations)

    return sorted_recommendations[0]
