import os
import sys
from dotenv import load_dotenv
from groq import Groq
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging import logger
from utils.utils import chunk_text, remove_code_blocks  # ✅ import remove_code_blocks
from textwrap import dedent

load_dotenv("/Users/shima/PycharmProjects/finance-agents/app/.env")

class MarketAgent:
    """
    MarketAgent:
    Handles quantitative market analysis.
    - Processes raw data from Yahoo Finance, Alpha Vantage, Finnhub, etc.
    - Detects technical and statistical signals.
    - Produces structured outputs for downstream analysis.
    """

    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.description = "MarketAgent: Quantitative analysis of market data."
        self.instructions = dedent("""
            Responsibilities:
            1. Clean and normalize market datasets from Yahoo Finance, Alpha Vantage, and Finnhub.
            2. Analyze quantitative signals:
                - Price trends and momentum
                - Volatility levels
                - Volume and liquidity patterns
                - Technical indicators (moving averages, RSI, MACD, etc.)
            3. Detect anomalies or unusual activity (e.g., price spikes, trading surges).
            4. Summarize insights in:
                - Plain language explanation
                - Structured JSON format
                - Visual descriptions for charts
            5. Identify key tickers or patterns that warrant deeper qualitative research.
        """)
        self.max_input_tokens = 10000
        self.output_tokens = 2000

    def analyze_market(self, market_data: dict) -> dict:
        logger.info("MarketAgent: Cleaning and analyzing market data")
        # Convert dict to JSON string
        market_data_str = json.dumps(market_data, indent=2)
        # Remove any code blocks before sending to LLM
        market_data_str = remove_code_blocks(market_data_str)

        chunks = chunk_text(market_data_str, self.max_input_tokens)
        full_content = ""

        for i, chunk in enumerate(chunks):
            prompt = f"{self.description}\n\nInstructions:\n{self.instructions}\n\nData:\n{chunk}"
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                content = response.choices[0].message.content
                full_content += content + "\n\n"
                logger.info(f"MarketAgent: Processed chunk {i+1}/{len(chunks)}")
            except Exception as e:
                logger.error(f"MarketAgent: Groq API error on chunk {i+1} — {e}")
                full_content += f"[Error processing chunk {i+1}]\n\n"

        return {"markdown": full_content.strip()}
