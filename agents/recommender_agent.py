# agents/recommender_agent.py
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from groq import Groq
from utils.logging import logger
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))


class RecommenderAgent:
    def __init__(self):
        self.model = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "Provides actionable financial recommendations based on research and analysis."
        self.instructions = """
            1. Take inputs from AnalystAgent and ResearchAgent.
            2. Suggest investment actions (buy/sell/hold) per ticker.
            3. Recommend portfolio adjustments, diversification, and risk mitigation.
            4. Explain reasoning and cite supporting data.
        """
    def recommend(self, analysis_results: str) -> str:
        """
        Generate investment recommendations based on analysis results.

        Args:
            analysis_results (str): Output from AnalystAgent.

        Returns:
            str: Model-generated recommendations.
        """
        logger.info("RecommenderAgent: Generating recommendations")
        prompt = f"""{self.description}

        Instructions:
        {self.instructions}

        Analysis Results:
        {analysis_results}
        """
        try:
            response = self.model.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("RecommenderAgent: Recommendations generated")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"RecommenderAgent: Recommendation failed — {e}")
            return "Error: Unable to generate recommendations at this time."
    