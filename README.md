# 🔍 System Architecture Overview

This project implements a multi-agent financial intelligence platform designed to handle natural language investment queries.
It extracts relevant symbols, gathers market and qualitative data, performs deep analysis, and delivers personalized, actionable recommendations.

The system integrates crawler scripts, multiple LLM-driven agents, and external APIs to deliver high-quality insights for individual investors, analysts, and automated trading tools.

## 📊 True Data Flow Diagram

```mermaid
graph LR
A[User Query] --> B[Master Agent]

%% Master orchestrates all agents
B --> C[Resolver Agent]
B --> D[Crawler]
B --> E[Market Agent]
B --> F[Research Agent]
B --> G[Analyst Agent]
B --> H[Recommender Agent]
B --> I[Final Output]

%% Data flow
C -- "Symbols / Entities" --> D
D -- "Raw Market & Fundamentals" --> E
E -- "Market Summary" --> F
E -- "Market Summary" --> G
F -- "Research Summary" --> G
G -- "Integrated Analysis" --> H
H -- "Recommendations & Portfolio Plan" --> I

%% Styles
style A fill:#e1d5e7,stroke:#9673a6,stroke-width:2px
style B fill:#d5e8d4,stroke:#82b366,stroke-width:2px
style C fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px
style D fill:#fff2cc,stroke:#d6b656,stroke-width:2px
style E fill:#f8cecc,stroke:#b85450,stroke-width:2px
style F fill:#ffe6cc,stroke:#d79b00,stroke-width:2px
style G fill:#e2d5e7,stroke:#9673a6,stroke-width:2px
style H fill:#ffcc99,stroke:#ff9900,stroke-width:2px
style I fill:#c3d6a3,stroke:#3c7e2e,stroke-width:3px
```

## ⚙️ Agents Overview

### 1. Master Agent

* Orchestrates the entire workflow.
* Passes data to all agents and handles errors/retries.
* Aggregates outputs for the Final Report.
* **Inputs**: User query
* **Outputs**: Final consolidated report

### 2. Resolver Agent

* Extracts tickers, sectors, and keywords from natural language queries or direct ticker inputs.
* Validates ticker symbols, detects typos or outdated symbols, and provides updated versions.
* Uses search tools such as **DuckDuckGo**, **Tavily**, and other market databases to ensure correctness.
* Sends only verified symbols to the Crawler.

**Example Output (with updated tickers):**

```json
{
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "entities": ["technology", "software"],
  "updated_symbols": {
    "GOOG": "GOOGL"
  },
  "confidence": 0.98
}
```

### 3. Crawler

* Collects raw market and fundamental data from:

  * Yahoo Finance
  * Alpha Vantage
  * Finnhub
* Sends raw data only to Market Agent.

**Example Output:**

```json
{
  "AAPL": { "ohlcv": [...], "fundamentals": {...} },
  "MSFT": { "ohlcv": [...], "fundamentals": {...} }
}
```

### 4. Market Agent

* Normalizes and analyzes quantitative data.
* Produces:

  * Technical trends, volatility, anomalies
  * Clean summaries
* Sends output to Research Agent and Analyst Agent.

**Example Output:**

```json
{
  "AAPL": { "trend": "up", "volatility": 0.18, "signals": {"rsi": 62} }
}
```

### 5. Research Agent

The ResearchAgent enriches market summaries with qualitative insights.

**Responsibilities:**

* Use Market Summary as input.
* For each symbol:

  * Gather insights from ≥5 sources (news, analyst reports, regulatory updates, sector trends)
  * Identify key events, risks, opportunities
  * Produce structured, neutral report:

    * Section 1: Industry & Macro context
    * Section 2: Company-specific updates
    * Section 3: Risk and opportunity highlights

**Inputs**: Market Summary
**Outputs**: Structured research briefs

**Example Use:**

```python
research_agent = ResearchAgent()
report = research_agent.analyze(market_summary)
print(report)
```

### 6. Analyst Agent

* Integrates Market and Research summaries.
* Performs:

  * Valuation metrics (P/E, EV/EBITDA, growth)
  * Peer and sector comparison
  * Risk assessment and red-flag identification
* Produces integrated analysis for the Recommender Agent.

**Example Output:**

```json
{
  "rankings": ["AAPL", "MSFT", "GOOGL"],
  "valuations": { "AAPL": {"pe": 25.6, "growth": "high"} }
}
```

### 7. Recommender Agent

* Converts analysis into investment strategies.
* Generates:

  * Buy/Hold/Sell recommendations
  * Portfolio weights and allocation suggestions
  * Risk mitigation advice

**Example Output:**

```json
{
  "recommendations": [
    {"symbol": "AAPL", "action": "BUY", "weight": 0.35, "entry": "< 170"}
  ]
}
```

## 🌟 Features

* Master-led orchestration
* Strict data flow separation
* Quantitative + qualitative integration
* Portfolio-aware recommendations
* Structured outputs (JSON + Markdown)
* Robust error handling and logging
* **Advanced Resolver Capabilities**:

  * Handles both natural language queries and direct ticker inputs
  * Detects typos and outdated symbols
  * Updates tickers using DuckDuckGo, Tavily, and other search tools
  * Returns `updated_symbols` mapping when symbols have changed

## 🛠 Technology Stack

* Python 3.10+
* LLM APIs: Groq, Qwen
* Market Data: Yahoo Finance, Alpha Vantage, Finnhub
* Search: DuckDuckGo, Tavily
* Visualization: Mermaid (architecture diagrams)

## 📈 Future Enhancements

* Automated backtesting
* Expanded data sources (Bloomberg, TradingView)
* Options/derivatives support
* Interactive dashboards for insights
* Portfolio simulation and risk modeling
