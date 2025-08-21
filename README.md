# 🔍 System Architecture Overview

This project uses a multi-agent architecture to process user queries and generate intelligent recommendations. Below is a flowchart that illustrates the data flow between agents.

## 📊 System Architecture

```mermaid
graph LR
A[User Query] --> B[Master Agent]
B --> C[Resolver Agent]
C -- "Symbols" --> D[Crawler]
D -- "Raw Data" --> E[Market Agent]
E -- "Market Summary" --> F[Research Agent]
F -- "Research Summary" --> G[Analysis Agent]
G -- "Analysis Results" --> H[Recommender Agent]
H -- "Final Recommendations" --> I[Final Output]
B --> D
B --> E
B --> F
B --> G
B --> H
E -- "Market Summary" --> G
C -. "Symbols" .-> I
E -. "Market Summery" .-> I
F -. "Research Summery" .-> I
G -. "Analysis Results" .-> I

style A fill:#e1d5e7,stroke:#9673a6,stroke-width:2px
style B fill:#d5e8d4,stroke:#82b366,stroke-width:2px
style C fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px
style D fill:#fff2cc,stroke:#d6b656,stroke-width:2px
style E fill:#f8cecc,stroke:#b85450,stroke-width:2px
style F fill:#ffe6cc,stroke:#d79b00,stroke-width:2px
style G fill:#e2d5e7,stroke:#9673a6,stroke-width:2px
style H fill:#ffcc99,stroke:#ff9900,stroke-width:2px
style I fill:#c3d6a3,stroke:#3c7e2e,stroke-width:3px
