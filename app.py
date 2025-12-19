import operator
import os
from dotenv import load_dotenv

load_dotenv()
from typing import Annotated, List, TypedDict
import requests
import pandas as pd
from io import StringIO

import yfinance as yf
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END, START
from langgraph.types import Send

# --- VISUALIZATION LIBRARY ---
# You need 'grandalf' or 'pygraphviz' installed for draw_mermaid_png to work perfectly,
# but usually it works with default dependencies if you output raw mermaid.
try:
    from IPython.display import Image, display
except ImportError:
    pass

# --- CONFIGURATION ---
# os.environ["GOOGLE_API_KEY"] = "your_google_api_key"
# os.environ["TAVILY_API_KEY"] = "your_tavily_api_key"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
)

search_tool = TavilySearchResults(max_results=3)

# --- STATE DEFINITIONS ---

class AnalystState(TypedDict):
    ticker: str

class GraphState(TypedDict):
    n_stocks: int
    tickers: List[str]
    # operator.add appends results from parallel nodes into a single list
    results: Annotated[List[str], operator.add] 

# --- NODE FUNCTIONS ---

def market_screener_node(state: GraphState):
    n = state.get("n_stocks", 3)
    print(f"--- [Screener] Finding top {n} market movers (Yahoo Finance) ---")
    
    tickers = []
    try:
        url = "https://finance.yahoo.com/gainers"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Parse table using pandas
        tables = pd.read_html(StringIO(response.text))
        if tables:
            df = tables[0]
            # Assumes 'Symbol' is the column name
            tickers = df['Symbol'].head(n).tolist()
    except Exception as e:
        print(f"Error scraping Yahoo Finance: {e}")
        # Fallback if scraping fails
        tickers = ["NVDA", "TSLA"]

    print(f"--- [Screener] Found tickers: {tickers} ---")
    return {"tickers": tickers}

def stock_analyst_node(state: AnalystState):
    ticker = state["ticker"]
    print(f"--- [Analyst] Analyzing {ticker} ---")
    
    # 1. Fetch Technicals
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        pct_change = ((hist["Close"].iloc[-1] - hist["Close"].iloc[-2]) / hist["Close"].iloc[-2]) * 100 if len(hist) >= 2 else 0.0
    except:
        pct_change = 0.0

    # 2. Fetch News
    news = search_tool.invoke(f"Why is {ticker} stock moving today?")
    news_ctx = "\n".join([r["content"] for r in news])
    
    # 3. Reason & Recommend
    prompt = f"""
    Stock: {ticker}, Move: {pct_change:.2f}%
    News: {news_ctx}
    Task: 1 sentence reason + Buy/Sell/Hold recommendation.
    Format: "Ticker: {ticker} | Rec: [REC] | Reason: ..."
    """
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"results": [response.content]}

def publisher_node(state: GraphState):
    print("--- [Publisher] Compiling Report ---")
    final_report = "\n\n".join(state["results"])
    print("\n" + "="*30)
    print(final_report)
    print("="*30 + "\n")
    return {"results": []} # Clear state if needed

# --- GRAPH CONSTRUCTION ---

builder = StateGraph(GraphState)

builder.add_node("screener", market_screener_node)
builder.add_node("analyst", stock_analyst_node)
builder.add_node("publisher", publisher_node)

builder.add_edge(START, "screener")

# Conditional Edge: Map (One-to-Many)
def continue_to_analysts(state: GraphState):
    # This triggers the parallel execution
    return [Send("analyst", {"ticker": t}) for t in state["tickers"]]

builder.add_conditional_edges("screener", continue_to_analysts, ["analyst"])

# Fan-In: Many-to-One
builder.add_edge("analyst", "publisher")
builder.add_edge("publisher", END)

graph = builder.compile()

# --- VISUALIZATION LOGIC ---

def save_graph_image():
    """Generates the architecture diagram"""
    print("--- Generating Graph Image ---")
    try:
        # Get the Mermaid definition
        mermaid_png = graph.get_graph().draw_mermaid_png()
        
        # Save to file
        output_file = "market_agent_graph.png"
        with open(output_file, "wb") as f:
            f.write(mermaid_png)
        print(f"Graph saved as '{output_file}'")
        
    except Exception as e:
        print(f"Graph visualization failed. Install pygraphviz or similar: {e}")
        # Fallback: Print ASCII representation
        print("ASCII Graph Representation:")
        graph.get_graph().print_ascii()

if __name__ == "__main__":
    # 1. Generate the visual graph first
    save_graph_image()
    
    # 2. Run the agent
    print("--- Starting Agent Execution ---")
    graph.invoke({"n_stocks": 2, "results": []})