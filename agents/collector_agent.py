# collector_agent.py
class DataCollectorAgent:
    def collect(self, sleep_hours, heart_rate, stress_level):
        return {
            "sleep_hours": sleep_hours,
            "heart_rate": heart_rate,
            "stress_level": stress_level
        }
