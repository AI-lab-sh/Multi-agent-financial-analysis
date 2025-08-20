import matplotlib.pyplot as plt
import uuid
import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agents.master_agent import MasterAgent
import json

# Initialize FastAPI app
app = FastAPI(title="Finance Multi-Agent System")

# Paths
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
plots_path = os.path.join(frontend_path, "plots")
os.makedirs(plots_path, exist_ok=True)

# Serve frontend & static
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

master_agent = MasterAgent()

class QueryRequest(BaseModel):
    query: str | None = None
    symbols: list[str] | None = None
    alpha_key: str | None = None
    finnhub_key: str | None = None

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_file = os.path.abspath(os.path.join(frontend_path, "index.html"))
    return FileResponse(index_file)

@app.post("/run_pipeline/")
async def run_pipeline(request: QueryRequest):
    result = master_agent.resolve_and_execute(request.query)

    # Case 1: result is a matplotlib figure
    if isinstance(result, plt.Figure):
        filename = f"{uuid.uuid4().hex}.png"
        filepath = os.path.join(plots_path, filename)
        result.savefig(filepath)
        plt.close(result)
        return JSONResponse(content={"result": {"output": f"/static/plots/{filename}"}})

    # Case 2: result is dict -> pretty JSON
    if isinstance(result, dict):
        result = json.dumps(result, indent=2)

    # Case 3: fallback to string
    elif not isinstance(result, str):
        result = str(result)

    return JSONResponse(content={"result": {"output": result}})
