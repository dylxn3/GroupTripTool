# File will control all FastAPI routes from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AffordabilityRequest, AffordabilityResponse, AirportSearchResponse, AirportOption
from services import check_origin_affordability
from getdata import search_airports

app = FastAPI()

# Allow the React dev server to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Live Endpoints 
@app.get("/search-airports", response_model=AirportSearchResponse)
def search_airports_endpoint(query: str):
    results = search_airports(query)
    options = [AirportOption(**r) for r in results]
    return AirportSearchResponse(options=options)

# Mock Endpoints 
@app.post("/check-affordability", response_model=AffordabilityResponse)
def check_affordability(request: AffordabilityRequest):
    results = [
        check_origin_affordability(request.destination, group)
        for group in request.origin_groups
    ]
    return AffordabilityResponse(destination=request.destination, results=results)