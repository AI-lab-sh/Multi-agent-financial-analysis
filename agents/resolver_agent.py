import os
import textwrap
import sys
import re
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.tools import DuckDuckGoSearchRun
from tavily import TavilyClient
from langchain.agents import Tool, initialize_agent,AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.logging import logger

# Load env variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.abspath(os.path.join(BASE_DIR, "../app",".env")))


google_api_key = os.environ.get("GOOGLE_API_KEY")
tavily_api_key = os.environ.get("TAVILY_API_KEY")

class ResolverAgent:
    """
    Resolves ticker symbols from a user query.
    Uses Gemini (via LangChain) with DuckDuckGo + Tavily as tools.
    Falls back to Tavily search if LLM fails.
    """

    def __init__(self):
        # Configure Gemini + Tavily
        genai.configure(api_key=google_api_key)
        # self.gemini_model = genai.Model("gemini-2.0-flash")
        self.tavily_client = TavilyClient(api_key=tavily_api_key)

        # LLM wrapper
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.1)

        # Setup tools + agent
        self.tools = self.create_search_tools()
        self.agent = initialize_agent(
    tools=[self.tools["duckduck_search_tool"], self.tools["tavily_search_tool"]],
    llm=self.llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # 👈 this must be inside the executor
)

    def tavily_search(self, query: str) -> str:
        """Run a Tavily search and return joined results as text."""
        result = self.tavily_client.search(query)
        return "\n".join([r["content"] for r in result["results"]])

    def create_search_tools(self) -> dict:
        
        """Create and return search tools."""
        duck_duck_client = DuckDuckGoSearchRun()

        tavily_tool = Tool(
            name="Tavily Search",
            func=self.tavily_search,
            description="Use this tool to search Tavily for current, summarized web results."
        )
        duckduck_tool = Tool(
            name="DuckDuckGo Search",
            func=duck_duck_client.run,
            description="Use this tool to search the internet for current information."
        )

        return {
            "duckduck_search_tool": duckduck_tool,
            "tavily_search_tool": tavily_tool
        }
    def extract_symbols(self,response: str):
        # Match either **TICKER** or standalone uppercase words
        matches = re.findall(r"\*\*([A-Z]{2,6})\*\*|\b([A-Z]{2,6})\b", response)

        # Flatten and filter empty strings
        symbols = [m[0] if m[0] else m[1] for m in matches]

        # Deduplicate while preserving order
        seen = set()
        clean_symbols = []
        for s in symbols:
            if s not in seen:
                seen.add(s)
                clean_symbols.append(s)

        return clean_symbols
    
    def clean_tickers(self,data):
        tickers = []
        for item in data:
            # Remove asterisks, whitespace, and any trailing text
            match = re.search(r'\b[A-Z]{2,6}\b', item)
            if match:
                tickers.append(match.group())
        return tickers

    def resolve(self, user_query: str):
        prompt = textwrap.dedent(f"""
            Find the current ticker symbols for: "{user_query}".
            - Only return ticker symbols (no company names, no exchanges).
            - Format them like this: **XOM**, **CVX**, **COP**
            - At the end, add one line: "Last updated: YYYY-MM-DD"
        """)

        try:
            response = self.agent.invoke({"input": prompt})
            response_text = response["output"]  # agent returns dict
            l1=response_text.split(",")
            print(f"LLM raw response:\n{response_text}\n")
            # print(f"LLM l:\n{l1}\n")
            # l2 = [i.strip("**") for i in l1]
            # print(f"LLM l2:\n{l2}\n")
            # l3=self.clean_tickers(l2)
            # print(f"LLM l3:\n{l3}\n")
            return self.extract_symbols(response_text)

        except Exception as e:
            logger.error(f"LLM failed, falling back to Tavily: {e}")
            fallback_text = self.tavily_search(user_query)
            matches = re.findall(r"\b[A-Z]{2,5}\b", fallback_text)
            return list(set(matches)) if matches else []

# def main():
#     agent = ResolverAgent()

#     # Example queries
#     queries = [
#         "gold mining companies"
#         # "oil and gas stocks",
#         # "Barrick Gold latest ticker",
#         # "technology companies like Apple, Microsoft, and Google"
#     ]

#     for q in queries:
#         print("\n============================")
#         print(f"Query: {q}")
#         try:
#             symbols = agent.resolve(q)
#             print(f"Resolved Symbols: {symbols}")
#         except Exception as e:
#             print(f"Error resolving query '{q}': {e}")

# if __name__ == "__main__":
#     main()
