# app/routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from agents.master_agent import MasterAgent

router = APIRouter()
master_agent = MasterAgent()

class SymbolsRequest(BaseModel):
    symbols: list[str]
    alpha_key: str = None  # optional

@router.get("/full_report/{tickers}")
def get_full_report(tickers: str):
    """
    Endpoint to run the pipeline for a comma-separated list of tickers.
    """
    tickers_list = tickers.split(",")
    return master_agent.execute_pipeline(tickers_list)

@router.post("/run_pipeline/")
def run_pipeline(request: SymbolsRequest):
    """
    Endpoint to run the pipeline for JSON payload.
    """
    master_agent.crawler.symbols = request.symbols
    master_agent.crawler.alpha_key = request.alpha_key
    return master_agent.run_pipeline()
