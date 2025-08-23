📊 System Flow

graph LR
A[User Query] --> B[Master Agent]

%% Master orchestrates but does not pass data between agents
B --> C[Resolver Agent]
B --> D[Crawler]
B --> E[Market Agent]
B --> F[Research Agent]
B --> G[Analyst Agent]
B --> H[Recommender Agent]
B --> I[Final Output]

%% True data flow
C -- "Symbols / Entities" --> D
D -- "Raw Market & Fundamentals" --> E
E -- "Market Summary" --> F
E -- "Market Summary" --> G
F -- "Research Summary" --> G
G -- "Integrated Analysis" --> H
H -- "Recommendations & Portfolio Plan" --> I
