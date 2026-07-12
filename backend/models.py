from pydantic import BaseModel
from typing import List, Literal


# ---- Airport search ----

class AirportOption(BaseModel):
    label: str
    sky_id: str
    entity_id: str
    entity_type: str  # "CITY" or "AIRPORT"

class AirportSearchResponse(BaseModel):
    options: List[AirportOption]


# ---- Trip / traveler input models ----

class NamedTraveler(BaseModel):
    name: str
    budget: float
    airport_sky_id: str | None = None
    airport_entity_id: str | None = None
    airport_label: str | None = None

class OriginEntry(BaseModel):
    origin_city_label: str
    city_sky_id: str
    city_entity_id: str
    headcount: int
    entry_type: Literal["individual", "bulk"]
    travelers: List[NamedTraveler] = []
    bulk_airport_sky_id: str | None = None
    bulk_airport_entity_id: str | None = None
    bulk_airport_label: str | None = None
    bulk_budget: float | None = None
    currency: str = "USD"

# ---- Result models ----

class TravelerResult(BaseModel):
    name: str
    fare: float | None = None
    affordable: bool | None = None
    shortfall: float | None = None

class OriginResult(BaseModel):
    origin: str
    fare: float | None = None
    error: str | None = None
    # individual-entry results
    traveler_results: List[TravelerResult] | None = None
    compatible_count: int | None = None
    total: int | None = None
    # bulk-entry results
    headcount: int | None = None
    affordable: bool | None = None
    shortfall: float | None = None

class DestinationCheck(BaseModel):
    origin: str
    fare: float | None = None
    error: str | None = None
    traveler_results: List[TravelerResult] | None = None
    compatible_count: int | None = None
    total: int | None = None
    affordable: bool | None = None
    shortfall: float | None = None

class DestinationResult(BaseModel):
    destination_label: str
    origin_checks: List[DestinationCheck]

class TripResult(BaseModel):
    trip_name: str
    destination: str | None = None
    origin_results: List[OriginResult] | None = None
    anywhere_results: List[DestinationResult] | None = None

class TripRequest(BaseModel):
    trip_name: str
    destination_label: str | None = None
    destination_sky_id: str | None = None
    destination_entity_id: str | None = None
    date: str
    duration_days: int | None = None
    origins: List[OriginEntry]