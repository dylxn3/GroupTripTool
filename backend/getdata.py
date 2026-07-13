# getdata.py

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

# ============================================================
# TOGGLE — flip this to False once RapidAPI quota resets
# ============================================================
USE_MOCK_DATA = True


# ============================================================
# MOCK DATA (used while USE_MOCK_DATA = True)
# ============================================================

MOCK_AIRPORTS = {
    "toronto": {
        "country": "canada",
        "options": [
            {"label": "Toronto (Any)", "sky_id": "YTOA", "entity_id": "27536640", "entity_type": "CITY"},
            {"label": "Toronto Pearson International (YYZ)", "sky_id": "YYZ", "entity_id": "95673353", "entity_type": "AIRPORT"},
            {"label": "Toronto Island (YTZ)", "sky_id": "YTZ", "entity_id": "95673352", "entity_type": "AIRPORT"},
        ],
    },
    "tokyo": {
        "country": "japan",
        "options": [
            {"label": "Tokyo (Any)", "sky_id": "TYOA", "entity_id": "27537542", "entity_type": "CITY"},
            {"label": "Narita International (NRT)", "sky_id": "NRT", "entity_id": "95673400", "entity_type": "AIRPORT"},
            {"label": "Haneda (HND)", "sky_id": "HND", "entity_id": "95673401", "entity_type": "AIRPORT"},
        ],
    },
    "osaka": {
        "country": "japan",
        "options": [
            {"label": "Osaka (Any)", "sky_id": "OSAA", "entity_id": "27537550", "entity_type": "CITY"},
            {"label": "Kansai International (KIX)", "sky_id": "KIX", "entity_id": "95673410", "entity_type": "AIRPORT"},
            {"label": "Osaka Itami (ITM)", "sky_id": "ITM", "entity_id": "95673411", "entity_type": "AIRPORT"},
        ],
    },
    "nagoya": {
        "country": "japan",
        "options": [
            {"label": "Nagoya (Any)", "sky_id": "NGOA", "entity_id": "27537560", "entity_type": "CITY"},
            {"label": "Chubu Centrair International (NGO)", "sky_id": "NGO", "entity_id": "95673420", "entity_type": "AIRPORT"},
        ],
    },
    "sapporo": {
        "country": "japan",
        "options": [
            {"label": "Sapporo (Any)", "sky_id": "SPKA", "entity_id": "27537570", "entity_type": "CITY"},
            {"label": "New Chitose (CTS)", "sky_id": "CTS", "entity_id": "95673430", "entity_type": "AIRPORT"},
        ],
    },
    "manila": {
        "country": "philippines",
        "options": [
            {"label": "Manila (Any)", "sky_id": "MNLA", "entity_id": "27537999", "entity_type": "CITY"},
            {"label": "Ninoy Aquino International (MNL)", "sky_id": "MNL", "entity_id": "95673500", "entity_type": "AIRPORT"},
        ],
    },
    "rome": {
        "country": "italy",
        "options": [
            {"label": "Rome (Any)", "sky_id": "ROMA", "entity_id": "27538000", "entity_type": "CITY"},
            {"label": "Fiumicino (FCO)", "sky_id": "FCO", "entity_id": "95673600", "entity_type": "AIRPORT"},
        ],
    },
    "milan": {
        "country": "italy",
        "options": [
            {"label": "Milan (Any)", "sky_id": "MILA", "entity_id": "27538010", "entity_type": "CITY"},
            {"label": "Malpensa (MXP)", "sky_id": "MXP", "entity_id": "95673610", "entity_type": "AIRPORT"},
        ],
    },
    "cancun": {
        "country": "mexico",
        "options": [
            {"label": "Cancun (Any)", "sky_id": "CUNAA", "entity_id": "27538100", "entity_type": "CITY"},
            {"label": "Cancun International (CUNA)", "sky_id": "CUNA", "entity_id": "95673700", "entity_type": "AIRPORT"},
        ],
    },
}

MOCK_FARES = {
    # Toronto Pearson (YYZ) as origin
    ("YYZ", "CUNA"): 450,     # Cancunfro
    ("YYZ", "TYOA"): 1100,   # Tokyo
    ("YYZ", "ROMA"): 850,    # Rome

    # Narita (NRT) as origin
    ("NRT", "CUNA"): 700,    # Cancun
    ("NRT", "ROMA"): 1050,   # Rome

    # keep existing city-wide entries too, so "Any" origin selections still work
    ("YTOA", "CUNA"): 450,
    ("YTOA", "TYOA"): 1100,
    ("YTOA", "ROMA"): 850,
    ("TYOA", "CUNA"): 1150,
    ("TYOA", "ROMA"): 950,
    ("MNL", "TYOA"): 300,
    ("MNL", "CUNA"): 1200,
    ("MNL", "ROMA"): 1350,
    ("FCO", "TYOA"): 1300,
    ("FCO", "CUNA"): 900,
    ("ROMA", "TYOA"): 1300,
    ("ROMA", "CUNA"): 900,
}

def _mock_search_flights_raw_response(origin_sky_id, destination_sky_id, date, return_date=None) -> dict:
    """
    Simulates the real searchFlights response shape.
    NOTE: response structure below is a best-guess based on common Skyscanner
    itinerary conventions — unconfirmed until tested live. Only the fields
    _real_search_flights actually reads (price.raw) need to match reality;
    everything else here is just for realism/future use.
    """
    base_fare = MOCK_FARES.get((origin_sky_id, destination_sky_id))

    if base_fare is None:
        return {"data": {"itineraries": []}}

    fare = round(base_fare * 1.7, 2) if return_date else base_fare

    return {
        "data": {
            "itineraries": [
                {
                    "id": f"{origin_sky_id}-{destination_sky_id}-{date}",
                    "price": {"raw": fare, "formatted": f"${fare:.2f}"},
                    "legs": [
                        {
                            "origin": {"skyId": origin_sky_id},
                            "destination": {"skyId": destination_sky_id},
                            "departure": date,
                        }
                    ],
                }
            ]
        }
    }

def _mock_search_flights(origin_sky_id, origin_entity_id, destination_sky_id, destination_entity_id, date, return_date=None) -> float | None:
    """Public-facing mock — parses the simulated raw response the same way _real_search_flights will."""
    raw = _mock_search_flights_raw_response(origin_sky_id, destination_sky_id, date, return_date)
    try:
        return raw["data"]["itineraries"][0]["price"]["raw"]
    except (KeyError, IndexError, TypeError):
        return None

def _mock_search_airports(query: str) -> list[dict]:
    key = query.strip().lower()

    for city_key, entry in MOCK_AIRPORTS.items():
        if city_key.startswith(key) or key in city_key:
            return entry["options"]

    matches = []
    for city_key, entry in MOCK_AIRPORTS.items():
        if entry["country"].startswith(key) or key in entry["country"]:
            matches.extend(entry["options"])

    return matches


# ============================================================
# REAL DATA (used while USE_MOCK_DATA = False)
# ============================================================

def _real_search_airports(query: str) -> list[dict]:
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

def _real_search_flights(origin_sky_id, origin_entity_id, destination_sky_id, destination_entity_id, date, return_date=None):
    """Real searchFlights call — response parsing still unconfirmed, verify once tested live."""
    url = f"https://{RAPIDAPI_HOST}/api/v1/flights/searchFlights"
    params = {
        "originSkyId": origin_sky_id,
        "destinationSkyId": destination_sky_id,
        "originEntityId": origin_entity_id,
        "destinationEntityId": destination_entity_id,
        "date": date,
        "adults": 1,
        "currency": "USD",
        "market": "en-US",
        "countryCode": "US",
    }
    if return_date:
        params["returnDate"] = return_date

    response = httpx.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    try:
        return data["data"]["itineraries"][0]["price"]["raw"]
    except (KeyError, IndexError, TypeError):
        return None


# ============================================================
# PUBLIC FUNCTIONS — these are what main.py / services.py import
# ============================================================

def search_airports(query: str) -> list[dict]:
    if USE_MOCK_DATA:
        return _mock_search_airports(query)
    return _real_search_airports(query)

def search_flights(origin_sky_id, origin_entity_id, destination_sky_id, destination_entity_id, date, return_date=None):
    if USE_MOCK_DATA:
        return _mock_search_flights(origin_sky_id, origin_entity_id, destination_sky_id, destination_entity_id, date, return_date)
    return _real_search_flights(origin_sky_id, origin_entity_id, destination_sky_id, destination_entity_id, date, return_date)