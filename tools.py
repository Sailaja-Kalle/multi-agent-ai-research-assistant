from tavily import TavilyClient
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def quick_answer(query):
    print(f"⚡ Quick answer for: {query}")
    try:
        response = client.search(
            query=query,
            max_results=3,
            search_depth="basic"
        )
        answers = []
        for r in response["results"]:
            answers.append(r["content"])
        return " ".join(answers[:2])
    except Exception as e:
        return f"Could not get quick answer: {str(e)}"

def search_web(query, limit=5):
    print(f"🔍 Searching web: {query}")
    try:
        response = client.search(
            query=query,
            max_results=limit,
            search_depth="basic"
        )
        results = []
        for r in response["results"]:
            results.append({
                "title": r["title"],
                "url": r["url"],
                "content": r["content"]
            })
        return results
    except Exception as e:
        return []

def search_and_scrape(query, limit=3):
    print(f"🔍 Search + Scrape: {query}")
    try:
        response = client.search(
            query=query,
            max_results=limit,
            search_depth="advanced"
        )
        results = []
        for r in response["results"]:
            scraped = scrape_url(r["url"])
            results.append({
                "title": r["title"],
                "url": r["url"],
                "content": r["content"],
                "scraped": scraped
            })
        return results
    except Exception as e:
        return []

def scrape_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]
    except Exception as e:
        return f"Could not scrape: {str(e)}"