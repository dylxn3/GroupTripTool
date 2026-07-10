# File will control all FastAPI routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AirportSearchResponse, AirportOption, TripRequest
from services import compute_return_date, check_origin
from getdata import search_airports

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search-airports", response_model=AirportSearchResponse)
def search_airports_endpoint(query: str):
    results = search_airports(query)
    options = [AirportOption(**r) for r in results]
    return AirportSearchResponse(options=options)


@app.post("/check-trip", response_model=TripRequest)
def check_trip(trip: TripRequest):
    return_date = compute_return_date(trip.date, trip.duration_days)

    origin_results = [
        check_origin(
            trip.destination_sky_id,
            trip.destination_entity_id,
            trip.date,
            return_date,
            origin,
        )
        for origin in trip.origins
    ]

    return TripRequest(
        trip_name=trip.trip_name,
        destination=trip.destination_sky_id,  # or store/pass a real destination label if you have one
        origin_results=origin_results,
    )