from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AirportSearchResponse, AirportOption, TripRequest, TripResult
from services import (
    compute_return_date,
    check_origin,
    all_affordable,
    find_alternatives_for_trip,
    find_anywhere_trip,
    FareCache,
)
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


@app.post("/check-trip", response_model=TripResult)
def check_trip(trip: TripRequest):
    return_date = compute_return_date(trip.date, trip.duration_days)

    if trip.destination_sky_id:
        cache = FareCache(trip.date, return_date)
        origin_results = [
            check_origin(trip.destination_sky_id, trip.destination_entity_id, trip.date, return_date, o, cache)
            for o in trip.origins
        ]

        suggested_alternatives = None
        if not all_affordable(origin_results):
            suggested_alternatives = find_alternatives_for_trip(trip.origins, trip.date, return_date)
            suggested_alternatives = [
                alt for alt in suggested_alternatives
                if all(
                    (oc.traveler_results is None or oc.compatible_count == oc.total)
                    and (oc.affordable is not False)
                    and oc.error is None
                    for oc in alt.origin_checks
                )
            ]

        return TripResult(
            trip_name=trip.trip_name,
            destination=None,
            anywhere_results=anywhere_data["destinations"],
            cheapest_per_origin=anywhere_data["cheapest_per_origin"],
            recommended_option=anywhere_data["recommended_option"],
)
    anywhere_data = find_anywhere_trip(trip.origins, trip.date, return_date)
    return TripResult(
        trip_name=trip.trip_name,
        destination=None,
        anywhere_results=anywhere_data["destinations"],
        cheapest_per_origin=anywhere_data["cheapest_per_origin"],
        recommended_option=anywhere_data["recommended_option"],
    )