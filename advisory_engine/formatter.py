def format_recommendation(recommendation):
    """
    Converts one technical recommendation into
    a farmer-friendly advisory.
    """

    priority = recommendation.get("priority", "LOW")
    message = recommendation.get("message", "")
    advisory_type = recommendation.get("type", "general")

    return {
        "priority": priority,
        "category": advisory_type,
        "action": message
    }


def format_action_plan(recommendations):
    """
    Converts all recommendations into a final
    farmer-friendly action plan.
    """

    action_plan = []

    for recommendation in recommendations:
        formatted = format_recommendation(recommendation)
        action_plan.append(formatted)

    return {
        "title": "Today's Action Plan",
        "recommendations": action_plan
    }
