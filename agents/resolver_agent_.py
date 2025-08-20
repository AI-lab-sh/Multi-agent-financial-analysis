import json
import os
import textwrap
from utils.utils import alpha_vantage_search, yahoo_autocomplete, finnhub_search
from utils.logging import logger
from dotenv import load_dotenv
from groq import Groq

load_dotenv("/Users/shima/PycharmProjects/finance-agents/app/.env")

class ResolverAgent:
    """
    Resolves user queries into stock ticker symbols.
    Collects results from Alpha Vantage, Yahoo Finance, and Finnhub,
    then asks the LLM to consolidate into a final list.
    """

    def __init__(self):
        # self.alpha_key = alpha_key
        # self.finnhub_key = finnhub_key
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def resolve(self, user_query):
        """
        Collect candidates from utils functions, then refine with LLM.
        Returns only a JSON list of ticker symbols.
        """
        candidates = []
        candidates.extend(alpha_vantage_search(self.alpha_key, user_query))
        candidates.extend(yahoo_autocomplete(user_query))
        candidates.extend(finnhub_search(self.finnhub_key, user_query))

        if not candidates:
            logger.error(f"No symbol candidates found for query: {user_query}")
            return []

        try:
            prompt = textwrap.dedent(f"""
                You are a financial assistant.
                The user asked: "{user_query}".

                Candidate ticker symbols:
                {candidates}

                Task:
                - For example, if the user enters "EXOM" you should infer he means XOM.
                - For "APPLE company" return AAPL.
                - For "oil and gas", return a list of representative companies in that industry.
                - Return ONLY a valid JSON array of ticker symbols, e.g. ["XOM", "CVX", "BP"].
                - If no relevant symbols are found, return an empty array [].
                - Pick the most relevant ticker symbols for this query.
                - If it's an industry, collect a representative list of companies.
                - If the query is ambiguous, return the most common symbols.
                - If the query is a company name, return its ticker symbol.
                - If the query is a stock index, return its ticker symbol.
                - If the query is a sector, return a representative list of companies.
                - If the query is a cryptocurrency, return its ticker symbol.
                - If the query is a commodity, return its ticker symbol.
                - If the query is a currency, return its ticker symbol.
                - If the query is a bond, return its ticker symbol.
                - If the query is a mutual fund, return its ticker symbol.
                - If the query is an ETF, return its ticker symbol.
                - If the query is a REIT, return its ticker symbol.
                - If the query is a foreign stock, return its ticker symbol.
                - Output ONLY a valid JSON array of ticker symbols, e.g. ["XOM", "CVX", "BP"].
            """)

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.choices[0].message["content"]
            symbols = json.loads(content)
            return symbols

        except Exception as e:
            logger.error(f"LLM failed to resolve symbols: {e}")
            return [c["symbol"] for c in candidates if "symbol" in c]
