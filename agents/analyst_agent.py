# agents/analyst_agent.py
import os
from groq import Groq
from utils.logging import logger
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))

class AnalystAgent:
    def __init__(self):
        self.model = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "Performs in-depth analysis on market and research data, identifies risks and opportunities."
        self.instructions = """
            1. Receive market and research data.
            2. Compute key metrics (volatility, growth, risk ratios).
            3. Generate charts and visual summaries.
            4. Identify trends, anomalies, and potential risks.
            5. Prepare actionable insights.
        """

    def analyze(self, market_data: str, research_summary: str) -> str:
        """
        Perform analysis using market data and research summary.
        """
        logger.info("AnalystAgent: Performing analysis")

        prompt = f"""{self.description}

    Instructions:
    {self.instructions}

    Market Data:
    {market_data}

    Research Summary:
    {research_summary}
    """
        try:
            response = self.model.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("AnalystAgent: Analysis complete")
            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"AnalystAgent: Analysis failed — {e}")
            return "Error: Unable to perform analysis at this time."
