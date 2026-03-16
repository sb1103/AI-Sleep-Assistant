# health_agent.py

class HealthAgent:
    def evaluate(self, data):
        heart_rate = data["heart_rate"]
        stress_level = data["stress_level"]

        hr_status = ""
        stress_status = ""

        if heart_rate > 100:
            hr_status = "High heart rate"
        elif heart_rate < 55:
            hr_status = "Low heart rate"
        else:
            hr_status = "Normal heart rate"

        if stress_level > 7:
            stress_status = "High stress"
        elif stress_level > 4:
            stress_status = "Moderate stress"
        else:
            stress_status = "Low stress"

        return f"{hr_status}, {stress_status}"
