from fastapi import APIRouter
import requests

router = APIRouter()

NEWS_API_KEY = "YOUR_NEWSAPI_KEY"

@router.get("/")
def get_latest_news():
    url = f"https://newsapi.org/v2/everything?q=stock%20market&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    news_data = response.json()
    if "articles" in news_data:
        return news_data["articles"][:5]
    return {"error": "No news available"}
