# File will control all FastAPI routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AirportSearchResponse, AirportOption, TripRequest, TripResult
from services import compute_return_date, check_origin
from getdata import search_airports
from services import find_anywhere_trip

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-trip", response_model=TripResult)
def check_trip(trip: TripRequest):
    return_date = compute_return_date(trip.date, trip.duration_days)

    if trip.destination_sky_id:
        origin_results = [check_origin(trip.destination_sky_id, trip.destination_entity_id, trip.date, return_date, o) for o in trip.origins]
        return TripResult(trip_name=trip.trip_name, destination=trip.destination_label, origin_results=origin_results)

    anywhere_results = find_anywhere_trip(trip.origins, trip.date, return_date)
    return TripResult(trip_name=trip.trip_name, destination=None, anywhere_results=anywhere_results)

@app.get("/search-airports", response_model=AirportSearchResponse)
def search_airports_endpoint(query: str):
    results = search_airports(query)
    options = [AirportOption(**r) for r in results]
    return AirportSearchResponse(options=options)


@app.post("/check-trip", response_model=TripResult)
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

    return TripResult(
        trip_name=trip.trip_name,
        destination=trip.destination_label,
        origin_results=origin_results,
    )