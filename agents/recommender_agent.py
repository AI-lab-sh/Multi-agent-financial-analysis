# agents/recommender_agent.py
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from groq import Groq
from utils.logging import logger
from dotenv import load_dotenv
from textwrap import dedent


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))


class RecommenderAgent:
    """
    RecommenderAgent:
    Translates analysis into actionable investment advice.
    - Provides buy/hold/sell guidance.
    - Suggests portfolio allocations and risk management strategies.
    """

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "RecommenderAgent: Generates actionable investment recommendations."
        self.instructions = dedent("""
            Responsibilities:
            1. Take AnalystAgent outputs (quantitative + qualitative synthesis).
            2. Suggest clear investment actions for each symbol:
                - Buy / Hold / Sell recommendations
                - Suggested entry or exit price ranges
                - Allocation size recommendations for portfolios
            3. Offer portfolio-level strategies:
                - Diversification ideas
                - Risk mitigation options (hedging, stop-loss levels)
            4. Explain reasoning in plain language, citing supporting data from analysis.
        """)

    def recommend(self, analysis_results: str) -> str:
        logger.info("RecommenderAgent: Generating recommendations")
        prompt = f"""{self.description}

Instructions:
{self.instructions}

Analysis Results:
{analysis_results}
"""

        try:
            response = self.client.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("RecommenderAgent: Recommendations generated")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"RecommenderAgent: Recommendation failed — {e}")
            return "Error: Unable to generate recommendations at this time."
