from utils.finance_api import get_yahoo_finance, get_alpha_vantage
from utils.logging import logger

class CrawlerAgent:
    def fetch(self, symbols):
        logger.info(f"CrawlerAgent: Fetching data for {symbols}")
        all_data = {}
        for s in symbols:
            yahoo_data = get_yahoo_finance(s)
            alpha_data = get_alpha_vantage(s)
            all_data[s] = {"yahoo": yahoo_data, "alpha": alpha_data}
        logger.info("CrawlerAgent: Data fetched")
        return all_data