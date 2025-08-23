# agents/research_agent.py
import os 
import sys
import json
from groq import Groq
from textwrap import dedent
from dotenv import load_dotenv
from utils.logging import logger
from utils.utils import remove_code_blocks  # ✅ import the function

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))

class ResearchAgent:
    """
    ResearchAgent:
    Gathers qualitative and contextual information to enrich the market data summary.
    - Pulls in news, analyst opinions, and macroeconomic signals.
    - Identifies qualitative risks and opportunities.
    - Produces structured briefs for each symbol to support deeper analysis.
    """

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "ResearchAgent: Adds qualitative, context-driven insights to market summaries."
        self.instructions = dedent("""
            Responsibilities:
            1. Use the provided market summary to identify the relevant companies and sectors.
            2. For each ticker/company:
                - Gather insights from at least 5 credible and diverse sources, including:
                    • Recent news articles
                    • Analyst opinions or upgrades/downgrades
                    • Industry or sector trend data
                    • Regulatory updates and macroeconomic factors
            3. Extract key qualitative findings:
                - Significant news or events (earnings, mergers, legal issues, market expansions)
                - Risks (regulatory pressure, lawsuits, leadership instability, market downturns)
                - Opportunities (new contracts, technology breakthroughs, positive market trends)
            4. Summarize findings in a structured, evidence-based report:
                - Section 1: Industry & Macro context
                - Section 2: Company-specific updates
                - Section 3: Risk and opportunity highlights
            5. Maintain a neutral, analytical tone with citations or source mentions when possible.
        """)

    def analyze(self, market_summary: str) -> str:
        """
        Enrich the market summary with qualitative research insights.
        
        Args:
            market_summary (str): Market summary from the MarketAgent.
        
        Returns:
            str: A structured qualitative research report.
        """
        logger.info("ResearchAgent: Performing qualitative research synthesis")

        # ✅ Remove any code blocks before sending to LLM
        # ✅ Convert to string before cleaning
        if isinstance(market_summary, dict):
           market_summary_str = json.dumps(market_summary, indent=2)
        else:
           market_summary_str = str(market_summary)  
        market_summary_clean = remove_code_blocks(market_summary_str)      
        prompt = f"""{self.description}

Instructions:
{self.instructions}

Market Summary:
{market_summary_clean}
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("ResearchAgent: Research complete")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"ResearchAgent: Research failed — {e}")
            return "Error: Unable to perform research at this time."
