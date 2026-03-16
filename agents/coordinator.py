# coordinator.py
from agents.collector_agent import DataCollectorAgent
from agents.sleep_analysis_agent import SleepAnalysisAgent
from agents.health_agent import HealthAgent
from agents.recommendation_agent import RecommendationAgent
from agents.ml_sleep_agent import MLSleepAgent

# Cloud LLM agent
from agents.llm_agent_cloud import LLMAgentCloud

class Coordinator:
    def __init__(self, llm_model_name: str = "gpt-4o-mini"):
        self.collector = DataCollectorAgent()
        self.rule_sleep_agent = SleepAnalysisAgent()
        self.health_agent = HealthAgent()
        self.recommender = RecommendationAgent()
        self.ml_sleep_agent = MLSleepAgent()
        self.llm = LLMAgentCloud(model=llm_model_name)

    def process(self, sleep_hours, heart_rate, stress_level):
        """
        Main pipeline:
         - collect raw data
         - run rule-based analysis and health evaluation
         - compute score and recommendations
         - ask cloud LLM for summary and trend prediction
        Returns:
         sleep_result, health_result, advice, score, llm_summary, llm_trend
        """
        data = self.collector.collect(sleep_hours, heart_rate, stress_level)

        # Rule-based analysis
        sleep_result = self.rule_sleep_agent.analyze(data)

        # Health agent evaluate (vitals, risk)
        health_result = self.health_agent.evaluate(data)

        # ML sleep stages (if your MLSleepAgent returns something, else placeholder)
        try:
            ml_stages = self.ml_sleep_agent.predict_stages(data)
        except Exception:
            ml_stages = []

        # Compute Sleep Score (example)
        score_value = max(40, 100 - stress_level * 5)
        score = {
            "score": score_value,
            "category": "Good" if stress_level < 5 else "Fair"
        }

        # Rule-based recommendations
        advice = self.recommender.recommend(sleep_result, health_result)

        # Prepare a lightweight report JSON to pass to LLM (keep sensitive data limited)
        report_json = {
            "sleep_hours": sleep_hours,
            "heart_rate": heart_rate,
            "stress_level": stress_level,
            "sleep_analysis": sleep_result,
            "health_analysis": health_result,
            "score": score,
            "ml_stages_preview": ml_stages[:10] if isinstance(ml_stages, list) else ml_stages
        }

        # LLM calls: wrap them in try/except to avoid crashing main pipeline
        try:
            explanation = self.llm.explain_sleep_report(report_json)
        except Exception as e:
            explanation = f"LLM explanation error: {e}"

        try:
            trend = self.llm.predict_trend(report_json)
        except Exception as e:
            trend = f"LLM trend error: {e}"

        return sleep_result, health_result, advice, score, explanation, trend
