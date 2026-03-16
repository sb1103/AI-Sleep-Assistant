#llm_agent_cloud.py
import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY
else:
    openai.api_key = None


class LLMAgentCloud:
    def __init__(self, model="gpt-4o-mini"):
        """
        model: change to whichever model you have access to
        """
        self.model = model

    def _ask(self, system_prompt: str, user_prompt: str, max_tokens: int = 512, temperature: float = 0.2):
        """
        Send a chat-style request to OpenAI.
        """
        if openai.api_key is None:
            raise RuntimeError("OpenAI API key not set. Set OPENAI_API_KEY environment variable.")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        text = response.choices[0].message["content"]
        return text

    # Sleep report explanation
    def explain_sleep_report(self, report_json: dict):
        system = "You are a concise sleep expert. Explain results clearly and give prioritized practical suggestions."

        user = (
            "Please analyze the following sleep report and produce:\n"
            "1) A short summary (3-5 sentences)\n"
            "2) Top 5 prioritized actionable recommendations\n"
            "3) One brief important risk note (if applicable)\n\n"
            f"Data:\n{json.dumps(report_json, indent=2)}"
        )

        return self._ask(system, user, max_tokens=400)

    # Chat-based coach
    def chat_with_user(self, message: str):
        system = "You are a friendly, evidence-based sleep coach. Provide clear, short answers and practical tips."

        return self._ask(system, message, max_tokens=300)

    # Predictive trend
    def predict_trend(self, report_json: dict):
        system = "You are a sleep trends analyst. Use recent metrics to predict short-term trend."

        user = (
            "Predict whether sleep efficiency will improve, worsen, or stay similar over the next 3 nights.\n\n"
            f"Data:\n{json.dumps(report_json, indent=2)}"
        )

        return self._ask(system, user, max_tokens=400)
