from pydantic import BaseModel
from typing import List, Literal

class OriginGroup(BaseModel):
    origin_label: str       # display name, e.g. "Toronto Pearson International (YYZ)"
    sky_id: str              # e.g. "YYZ"
    entity_id: str            # e.g. "95673353"
    group_size: int
    budget: float
    currency: str = "USD"

class AffordabilityRequest(BaseModel):
    destination: str
    origin_groups: List[OriginGroup]

class OriginResult(BaseModel):
    origin: str
    per_person_budget: float
    fare: float | None = None
    affordable: bool | None = None
    shortfall: float | None = None
    error: str | None = None

class AffordabilityResponse(BaseModel):
    destination: str
    results: List[OriginResult]

class AirportOption(BaseModel):
    label: str
    sky_id: str
    entity_id: str
    entity_type: str  # "CITY" or "AIRPORT"

class AirportSearchResponse(BaseModel):
    options: List[AirportOption]

class NamedTraveler(BaseModel):
    name: str
    budget: float
    airport_sky_id: str | None = None      # None = use city-wide default
    airport_entity_id: str | None = None
    airport_label: str | None = None        # e.g. "Toronto Pearson International (YYZ)"

class OriginEntry(BaseModel):
    origin_city_label: str      # e.g. "Toronto"
    city_sky_id: str             # e.g. "YTOA"
    city_entity_id: str
    headcount: int
    entry_type: Literal["individual", "bulk"]
    travelers: List[NamedTraveler] = []
    bulk_airport_sky_id: str | None = None   # shared airport choice for bulk groups
    bulk_airport_entity_id: str | None = None
    bulk_airport_label: str | None = None
    bulk_budget: float | None = None
    currency: str = "USD"

class TripRequest(BaseModel):
    trip_name: str
    destination_sky_id: str
    destination_entity_id: str
    date: str                        # departure date
    duration_days: int | None = None  # used to compute return date
    origins: List[OriginEntry]