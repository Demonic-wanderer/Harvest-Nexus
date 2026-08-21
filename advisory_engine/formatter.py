def format_recommendation(recommendation):
    """
    Converts one technical recommendation into
    a farmer-friendly advisory.
    """
    priority = recommendation.get("priority", "LOW")
    message = recommendation.get("message", "")
    message_hi = recommendation.get("message_hi", message)
    advisory_type = recommendation.get("type", "general")

    return {
        "priority": priority,
        "category": advisory_type,
        "action": message,
        "action_hi": message_hi,
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
        "title_hi": "आज की कार्य योजना",
        "recommendations": action_plan,
        "farm_health_score": None,
    }
