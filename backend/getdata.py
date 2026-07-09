import os
import httpx
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST")

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST,
}

def search_airports(query: str) -> list[dict]:
    """Return all matching locations (city + every airport) for a search query."""
    url = f"https://{RAPIDAPI_HOST}/api/v1/flights/searchAirport"
    params = {"query": query, "locale": "en-US"}

    response = httpx.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    return [
        {
            "label": r["presentation"]["suggestionTitle"],
            "sky_id": r["navigation"]["relevantFlightParams"]["skyId"],
            "entity_id": r["navigation"]["relevantFlightParams"]["entityId"],
            "entity_type": r["navigation"]["entityType"],
        }
        for r in data.get("data", [])
    ]