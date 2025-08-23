# utils/utils.py
import requests
import yfinance as yf
import re
from utils.logging import logger


def alpha_vantage_search(api_key, keyword):
    """
    Search for ticker symbols on Alpha Vantage by keyword.
    """
    if not api_key:
        return []
    try:
        url = "https://www.alphavantage.co/query"
        params = {"function": "SYMBOL_SEARCH", "keywords": keyword, "apikey": api_key}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [
            {"symbol": m.get("1. symbol"), "name": m.get("2. name")}
            for m in data.get("bestMatches", [])
        ]
    except Exception as e:
        logger.warning(f"Alpha Vantage search failed: {e}")
        return []


def yahoo_autocomplete(query):
    """
    Use Yahoo Finance autocomplete API to suggest ticker symbols.
    """
    try:
        url = "https://query1.finance.yahoo.com/v1/finance/search"
        params = {"q": query, "quotesCount": 10, "newsCount": 0}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [
            {"symbol": item["symbol"], "name": item.get("shortname") or item.get("longname")}
            for item in data.get("quotes", [])
            if "symbol" in item
        ]
    except Exception as e:
        logger.warning(f"Yahoo autocomplete failed: {e}")
        return []


def finnhub_search(api_key, query):
    """
    Use Finnhub symbol search to find ticker symbols.
    """
    if not api_key:
        return []
    try:
        url = "https://finnhub.io/api/v1/search"
        params = {"q": query, "token": api_key}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [
            {"symbol": r["symbol"], "name": r.get("description")}
            for r in data.get("result", [])
        ]
    except Exception as e:
        logger.warning(f"Finnhub search failed: {e}")
        return []


def fetch_google_finance(symbol):
    """
    Fetch minimal price data from Google Finance as a fallback.
    """
    try:
        url = f"https://www.google.com/finance/quote/{symbol}:NASDAQ"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None
        match = re.search(r'"price":([0-9.]+)', resp.text)
        if match:
            return {"close": float(match.group(1))}
        return None
    except Exception as e:
        logger.warning(f"Google Finance failed for {symbol}: {e}")
        return None


def fetch_yahoo_finance(symbol):
    """
    Fetch latest price from Yahoo Finance using yfinance.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if hist.empty:
            return None
        return {"close": hist["Close"].iloc[-1]}
    except Exception as e:
        logger.warning(f"Yahoo Finance failed for {symbol}: {e}")
        return None


def alpha_vantage_api_call(api_key, symbol):
    """
    Fetch daily stock data from Alpha Vantage.
    Returns raw JSON from the API.
    """
    try:
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": api_key,
            "outputsize": "compact"
        }
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if "Error Message" in data:
            logger.warning(f"Alpha Vantage API error for {symbol}: {data['Error Message']}")
            return None
        return data
    except Exception as e:
        logger.error(f"Alpha Vantage API call failed for {symbol}: {e}")
        return None


def finnhub_api_call(api_key, symbol):
    """
    Fetch quote data from Finnhub.
    Returns raw JSON from the API.
    """
    try:
        url = f"https://finnhub.io/api/v1/quote"
        params = {"symbol": symbol, "token": api_key}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        logger.error(f"Finnhub API call failed for {symbol}: {e}")
        return None
    
def chunk_text(text: str, max_input_tokens: int = 10000) -> list[str]:
    """
    Splits text into chunks safe for Groq API.
    Leaves room for output tokens.
    """
    max_length = max_input_tokens * 4  # ~40,000 chars
    chunks, current = [], []
    

    for line in text.splitlines():
        if sum(len(c) for c in current) + len(line) > max_length:
            chunks.append("\n".join(current))
            current = []
        current.append(line)

    if current:
        chunks.append("\n".join(current))

    return chunks

def remove_code_blocks(text: str) -> str:
    """
    Removes code blocks and inline code from text.
    """
    # Remove triple-backtick code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Remove indented code blocks (4 spaces at line start)
    text = re.sub(r'(?:\n {4}.*)+', '', text)

    # Remove inline code `like_this`
    text = re.sub(r'`[^`]+`', '', text)

    return text.strip()