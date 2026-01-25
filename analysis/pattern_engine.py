def generate_insights(data):
    if not data:
        return ["No habits logged yet"]

    insights = []
    avg_phone = sum(d[1] for d in data) / len(data)
    avg_sleep = sum(d[2] for d in data) / len(data)

    if avg_phone > 4:
        insights.append("High phone usage detected 📱")

    if avg_sleep < 6:
        insights.append("Low sleep duration 😴")

    insights.append("Keep tracking habits daily 👍")
    return insights


def burnout_score(data):
    score = 100
    for d in data:
        if d[1] > 5:
            score -= 10
        if d[2] < 6:
            score -= 10
    return max(score, 0)
