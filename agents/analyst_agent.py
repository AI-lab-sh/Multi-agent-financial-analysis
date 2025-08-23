# agents/analyst_agent.py
import os
from groq import Groq
from utils.logging import logger
from dotenv import load_dotenv
from textwrap import dedent


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))

class AnalystAgent:
    """
    AnalystAgent:
    Integrates quantitative (market) and qualitative (research) data.
    - Performs in-depth financial analysis.
    - Calculates risk, growth, and valuation metrics.
    - Identifies actionable insights.
    """

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "AnalystAgent: Deep integration and financial analysis."
        self.instructions = dedent("""
            Responsibilities:
            1. Combine MarketAgent (quantitative) and ResearchAgent (qualitative) outputs.
            2. Compute key metrics:
                - Volatility
                - Growth rates and revenue trends
                - Valuation ratios (P/E, P/B, PEG)
                - Risk-adjusted performance metrics
            3. Compare tickers relative to industry and sector benchmarks.
            4. Detect:
                - Undervalued or overvalued opportunities
                - Potential growth or decline trajectories
                - Significant risk factors or anomalies
            5. Generate outputs:
                - Executive summary (high-level)
                - Detailed structured insights
                - Recommendations for risk mitigation and opportunity exploitation
            6. Include textual descriptions for potential charts or dashboards.
        """)

    def analyze(self, market_data: str, research_summary: str) -> str:
        logger.info("AnalystAgent: Integrating market and research data")
        prompt = f"""{self.description}

Instructions:
{self.instructions}

Market Data:
{market_data}

Research Summary:
{research_summary}
"""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("AnalystAgent: Analysis complete")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AnalystAgent: Analysis failed — {e}")
            return "Error: Unable to perform analysis at this time."