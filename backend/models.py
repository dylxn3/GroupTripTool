from pydantic import BaseModel
from typing import List

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