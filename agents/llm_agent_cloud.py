import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=API_KEY)


class LLMAgentCloud:

    def __init__(self, model="gemini-2.5-flash"):
        self.model = model

    def _ask(self, system_prompt: str, user_prompt: str):

        prompt = f"""
{system_prompt}

{user_prompt}
"""

        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
            )

            return response.text

        except Exception as e:
            return f"Gemini Error: {e}"

    def explain_sleep_report(self, report_json):

        system = """
You are a professional sleep expert.

Analyze the sleep report.

Return:
1. Overall Sleep Quality
2. Summary
3. Health Insights
4. Top 5 Recommendations
"""

        return self._ask(system, json.dumps(report_json, indent=2))

    def predict_trend(self, report_json):

        system = """
Predict the user's sleep trend for the next 3 nights.

Include:
- Prediction
- Confidence
- Explanation
- Suggestions
"""

        return self._ask(system, json.dumps(report_json, indent=2))

    def chat_with_user(self, message):

        system = """
You are an AI Sleep Coach.

Keep answers short, practical and friendly.
"""

        return self._ask(system, message)