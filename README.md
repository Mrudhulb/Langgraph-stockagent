# AI Stock Agent 📈

A multi-agent system built with **LangGraph** that automatically finds trending stocks, performs AI-powered technical and fundamental analysis, and generates a consolidated report.

## 🚀 Features

- **Market Screener**: Scrapes Yahoo Finance to identify top gaining stocks.
- **Parallel Analysts**: Spawns concurrent AI agents to analyze each stock individually.
- **Technical Analysis**: Calculates recent price momentum using `yfinance`.
- **Fundamental Analysis**: Searches the web for breaking news using **Tavily**.
- **AI Reasoning**: Uses **Google Gemini** to generate Buy/Sell/Hold recommendations.
- **Visual Workflow**: Automatically generates a Mermaid diagram of the agentic workflow (`market_agent_graph.png`).

## 🛠️ Tech Stack

- **Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/)
- **LLM**: Google Gemini (via `langchain-google-genai`)
- **Search**: Tavily Search API
- **Data**: `yfinance`, `pandas`

## 📋 Prerequisites

- Python 3.9+
- A [Google AI Studio](https://aistudio.google.com/) API Key.
- A [Tavily](https://tavily.com/) API Key.

## 📦 Installation

1.  **Clone the repository** (if applicable) or download the source code.

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## ⚙️ Configuration

1.  Create a `.env` file in the root directory.
2.  Add your API keys:

    ```ini
    GOOGLE_API_KEY=your_google_api_key_here
    TAVILY_API_KEY=your_tavily_api_key_here
    ```

## ▶️ Usage

Run the main application:

```bash
python app.py
```

### What to Expect
1.  **Graph Generation**: The script will first save the workflow diagram to `market_agent_graph.png`.
2.  **Screener**: It will print the top stocks found (or fallbacks).
3.  **Analysis**: You will see logs from multiple "Analyst" nodes running in parallel.
4.  **Report**: A final "Publisher" block will print a consolidated report to the console.

## 🧩 Project Structure

- `app.py`: Main application logic containing the graph definition and node functions.
- `requirements.txt`: Python package dependencies.
