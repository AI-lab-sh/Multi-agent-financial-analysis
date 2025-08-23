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

# 🔍 Multi-Agent Financial Intelligence Platform

This project implements a **multi-agent financial intelligence system** designed to handle **natural language investment queries**.  
It extracts relevant symbols, gathers market and qualitative data, performs deep analysis, and delivers **personalized, actionable recommendations**.

The system integrates:
- 📡 Crawler scripts  
- 🧠 Multiple LLM-driven agents  
- 🔗 External APIs  

---

## 📊 System Architecture

### High-Level Flow




