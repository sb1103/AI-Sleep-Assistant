# recommendation_agent.py

class RecommendationAgent:
    def recommend(self, sleep_result, health_result):
        advice = []

        # Sleep-based recommendations
        if "insufficient" in sleep_result:
            advice.append("Try to increase sleep by 1–2 hours.")
        elif "Below recommended" in sleep_result:
            advice.append("Maintain a regular sleep schedule.")
        elif "Excessive" in sleep_result:
            advice.append("Reduce oversleeping and maintain a routine.")
        else:
            advice.append("Your sleep duration looks healthy!")

        # Health-based recommendations
        if "High heart rate" in health_result:
            advice.append("Avoid heavy meals or caffeine before bed.")
        if "Low heart rate" in health_result:
            advice.append("Try light stretching before sleeping.")
        if "High stress" in health_result:
            advice.append("Practice breathing exercises before bed.")
        if "Moderate stress" in health_result:
            advice.append("Try reducing screen time before sleep.")

        return " ".join(advice)
