# agents/research_agent.py
import os 
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from langchain.agents import Agent
from groq import Groq
from textwrap import dedent
from dotenv import load_dotenv
from utils.logging import logger
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))

class ResearchAgent:
    """LLM-based research agent with instructions."""
    def __init__(self):
        self.client=Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description="Elite financial research agent"
        self.instructions=dedent("""\
                1. Collect top 5 sources per symbol
                2. Extract trends, risks, news
                3. Summarize in structured report
            """)
    def analyze(self, market_summary: str) -> str:
        logger.info("MarketAgent: Starting market analysis")

        prompt = f"Analyze the following market data:\n{market_summary}"

        try:
            response = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            logger.info("MarketAgent: Analysis complete")
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"MarketAgent: Analysis failed — {e}")
            return "Error: Unable to analyze market data."

        

