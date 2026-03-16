# sleep_analysis_agent.py

class SleepAnalysisAgent:
    def analyze(self, data):
        sleep_hours = data["sleep_hours"]

        if sleep_hours < 5:
            return "Severely insufficient sleep"
        elif sleep_hours < 7:
            return "Below recommended sleep duration"
        elif sleep_hours <= 9:
            return "Healthy sleep duration"
        else:
            return "Excessive sleep duration"
