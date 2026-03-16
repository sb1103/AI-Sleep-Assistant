# agents/score_agent.py

class ScoreAgent:
    """
    Simple rule-based sleep scoring:
    - Base on sleep hours (0..10 -> 0..100)
    - penalty for stress and abnormal HR
    """
    def compute_score(self, data):
        sleep_hours = float(data.get("sleep_hours", 0))
        hr = float(data.get("heart_rate", 70))
        stress = float(data.get("stress_level", 1))

        # Base score from hours: 0h -> 0, 8h -> 100, >10 clamp
        base = max(0, min(100, (sleep_hours / 8.0) * 100))

        # HR penalty (if >100 or <50)
        hr_pen = 0
        if hr > 100:
            hr_pen = 15
        elif hr < 50:
            hr_pen = 10

        # Stress penalty (scale 1-10)
        stress_pen = (stress - 1) * 3  # upto 27

        score = base - hr_pen - stress_pen
        score = int(max(0, min(100, score)))

        # categorize
        if score < 50:
            category = "Poor"
        elif score < 70:
            category = "Fair"
        elif score < 85:
            category = "Good"
        else:
            category = "Excellent"

        return {"score": score, "category": category}
