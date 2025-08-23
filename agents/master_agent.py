import os
from agents.crawler import Crawler
from agents.market_agent import MarketAgent
from agents.research_agent import ResearchAgent
from agents.analyst_agent import AnalystAgent
from agents.recommender_agent import RecommenderAgent
from agents.resolver_agent import ResolverAgent
from dotenv import load_dotenv
from utils.logging import logger
from textwrap import dedent
import json 


# Load .env
#load_dotenv("/Users/shima/PycharmProjects/finance-agents/app/.env")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))


class MasterAgent:
    """
    Top-level orchestrator.
    - Resolves user queries into ticker symbols (via ResolverAgent)
    - Crawls raw data from multiple sources
    - Runs market, research, analyst, and recommender agents
    """

    def __init__(self):
        # API keys (from args or .env)
        self.alpha_key = os.environ.get("ALPHA_VANTAGE_KEY")
        self.finnhub_key = os.environ.get("FINNHUB_KEY")

        # Initialize agents
        self.resolver = ResolverAgent()
        self.crawler = Crawler(alpha_key=self.alpha_key, finnhub_key=self.finnhub_key)
        self.market = MarketAgent()
        self.research = ResearchAgent()
        self.analyst = AnalystAgent()
        self.recommender = RecommenderAgent()

    def resolve_and_execute(self, user_query: str, alpha_key=None, finnhub_key=None) -> str:
        """
        Full pipeline starting from a natural language user query.
        Always resolves query -> symbols, then runs pipeline.
        Always returns a JSON string.
        """
        logger.info(f"MasterAgent: Resolving query -> {user_query}")

        # Step 0: Resolve query into ticker symbols
        symbols = self.resolver.resolve(user_query)
        logger.info(f"MasterAgent: Resolved symbols -> {symbols}")

        if not symbols:
            logger.error(f"MasterAgent: No symbols found for query: {user_query}")
            return json.dumps(
                {"error": "No symbols could be resolved from query", "query": user_query},
                indent=2
            )

        # Step 1+: Continue full pipeline
        result = self.execute_pipeline(symbols, alpha_key=alpha_key, finnhub_key=finnhub_key)

        # Always return as pretty JSON string
        return json.dumps(result, indent=2)

    def execute_pipeline(self, symbols, alpha_key=None, finnhub_key=None) -> dict:
        """
        Orchestrates the full multi-agent pipeline:
        1. Crawl raw data from multiple sources
        2. Market analysis
        3. Research analysis
        4. Analyst deep dive
        5. Recommendations
        """
        # Override API keys if provided at runtime
        if alpha_key:
            self.crawler.alpha_key = alpha_key
        if finnhub_key:
            self.crawler.finnhub_key = finnhub_key

        logger.info(f"MasterAgent: Starting pipeline for symbols: {symbols}")

        # 1. symbols to crawler 
        raw_data = self.crawler.crawl(symbols)
        logger.info("MasterAgent: Crawling complete")

        # 2. Market analysis
        market_summary = self.market.analyze_market(raw_data)
        logger.info("MasterAgent: Market analysis complete")

        # 3. Research analysis
        research_summary = self.research.analyze(market_summary)
        logger.info("MasterAgent: Research analysis complete")

        # 4. Analyst deep dive
        analysis = self.analyst.analyze(research_summary, market_summary)
        logger.info("MasterAgent: Analyst deep dive complete")

        # 5. Recommendations
        recommendations = self.recommender.recommend(analysis)
        logger.info("MasterAgent: Recommendations generated")

        return {
            "symbols": symbols,
            # "raw_data": raw_data,                  
            "market_summary": market_summary,
            "research_summary": research_summary,
            "analysis": analysis,
            "recommendations": recommendations,
        }
