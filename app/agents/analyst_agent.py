# agents/analyst_agent.py
from groq import Groq
from utils import logger

class AnalystAgent:
    def __init__(self):
        self.model = Groq(id="llama3-7b-4096")
        self.description = "Performs in-depth analysis on market and research data, identifies risks and opportunities."
        self.instructions = """
            1. Receive market and research data.
            2. Compute key metrics (volatility, growth, risk ratios).
            3. Generate charts and visual summaries.
            4. Identify trends, anomalies, and potential risks.
            5. Prepare actionable insights.
        """

    def analyze(self, market_data, research_summary):
        logger.info("AnalystAgent: Performing analysis")
        prompt = f"{self.description}\nInstructions:\n{self.instructions}\nMarket Data:\n{market_data}\nResearch Summary:\n{research_summary}"
        return self.model.generate(prompt)