from langchain_community.tools.tavily_search import TavilySearchResults
import os
from dotenv import load_dotenv
import json

load_dotenv()

tool = TavilySearchResults(max_results=3)

print("--- Run 1 ---")
res1 = tool.invoke("Why is PSNY stock moving today?")
print(json.dumps(res1, sort_keys=True))

print("\n--- Run 2 ---")
res2 = tool.invoke("Why is PSNY stock moving today?")
print(json.dumps(res2, sort_keys=True))

if json.dumps(res1, sort_keys=True) == json.dumps(res2, sort_keys=True):
    print("\n[SUCCESS] Search results are IDENTICAL.")
else:
    print("\n[DIFFERENCE] Search results are DIFFERENT.")
