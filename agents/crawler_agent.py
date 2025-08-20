# agents/crawler_agent.py
from utils.utils import fetch_yahoo_finance , alpha_vantage_api_call, finnhub_api_call, fetch_google_finance
from utils.logging import logger
import yfinance as yf


class CrawlerAgent:
    """
    Fetches market and financial data from multiple sources:
    Yahoo Finance, Alpha Vantage, Finnhub, and Google Finance (fallback).
    """
    def __init__(self, alpha_key=None, finnhub_key=None):
        self.alpha_key = alpha_key
        self.finnhub_key = finnhub_key

    def crawl(self, symbols):
        all_data = {}

        for sym in symbols:
            symbol_data = {}

            # 1️⃣ Yahoo Finance
            try:
                yahoo_data = fetch_yahoo_finance(sym)
                if yahoo_data:
                    symbol_data["yahoo"] = yahoo_data
                    logger.info(f"Crawled Yahoo Finance for {sym}")
            except Exception as e:
                logger.warning(f"Yahoo Finance failed for {sym}: {e}")

            # 2️⃣ Alpha Vantage
            if self.alpha_key:
                try:
                    av_data = alpha_vantage_api_call(self.alpha_key, sym)
                    if av_data:
                        symbol_data["alpha_vantage"] = av_data
                        logger.info(f"Crawled Alpha Vantage for {sym}")
                except Exception as e:
                    logger.warning(f"Alpha Vantage failed for {sym}: {e}")

            # 3️⃣ Finnhub
            if self.finnhub_key:
                try:
                    fh_data = finnhub_api_call(self.finnhub_key, sym)
                    if fh_data:
                        symbol_data["finnhub"] = fh_data
                        logger.info(f"Crawled Finnhub for {sym}")
                except Exception as e:
                    logger.warning(f"Finnhub failed for {sym}: {e}")

            # 4️⃣ Google Finance (fallback)
            try:
                gf_data = fetch_google_finance(sym)
                if gf_data:
                    symbol_data["google_finance"] = gf_data
                    logger.info(f"Crawled Google Finance for {sym}")
            except Exception as e:
                logger.warning(f"Google Finance failed for {sym}: {e}")

            if not symbol_data:
                logger.error(f"No market data found for {sym}. Symbol may be delisted or unavailable.")

            all_data[sym] = symbol_data

        return all_data
