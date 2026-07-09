from pydantic import BaseModel
from typing import List

class OriginGroup(BaseModel):
    origin: str
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