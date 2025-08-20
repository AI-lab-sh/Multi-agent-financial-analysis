import os
import sys
from dotenv import load_dotenv
from groq import Groq
import json 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging import logger
from utils.utils import chunk_text   # ✅ imported here

load_dotenv("/Users/shima/PycharmProjects/finance-agents/app/.env")

class MarketAgent:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "Analyzes market data and trends to provide actionable insights."
        self.instructions = """
            1. Collect data from Yahoo Finance and Alpha Vantage.
            2. Identify trends, anomalies, and risk factors.
            3. Summarize insights in plain language with charts.
        """
        self.max_input_tokens = 10000
        self.output_tokens = 2000

    def analyze_market(self, market_data):
        logger.info("MarketAgent: Analyzing market data")
        market_data_str = json.dumps(market_data, indent=2)  # nicely formatted
        chunks = chunk_text(market_data_str, self.max_input_tokens)
        full_content = ""

        for i, chunk in enumerate(chunks):
            prompt = f"{self.description}\nInstructions:\n{self.instructions}\nData:\n{chunk}"
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    
                )
                content = response.choices[0].message.content
                full_content += content + "\n\n"
                logger.info(f"Processed chunk {i + 1}/{len(chunks)}")
            except Exception as e:
                logger.error(f"Groq API error on chunk {i + 1}: {e}")
                full_content += f"[Error processing chunk {i + 1}]\n\n"

        return {"markdown": full_content.strip()}
