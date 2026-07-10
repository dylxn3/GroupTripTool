from models import OriginGroup, OriginResult
from mock_data import get_mock_fare
from datetime import datetime, timedelta
from getdata import search_flights

def compute_return_date(departure_date: str, duration_days: int | None) -> str | None:
    if not duration_days:
        return None
    dep = datetime.strptime(departure_date, "%Y-%m-%d")
    return_date = dep + timedelta(days=duration_days)
    return return_date.strftime("%Y-%m-%d")


def check_origin(destination_sky_id, destination_entity_id, date, return_date, origin):
    fare = search_flights(
        origin.city_sky_id,
        origin.city_entity_id,
        destination_sky_id,
        destination_entity_id,
        date,
        return_date,   
    )
    
def check_origin_affordability(destination: str, group: OriginGroup) -> OriginResult:
    per_person_budget = group.budget / group.group_size
    fare = get_mock_fare(group.origin, destination)

    if fare is None:
        return OriginResult(
            origin=group.origin,
            per_person_budget=per_person_budget,
            fare=None,
            affordable=None,
            shortfall=None,
            error="No route found for this origin/destination",
        )

    if fare <= per_person_budget:
        return OriginResult(
            origin=group.origin,
            per_person_budget=per_person_budget,
            fare=fare,
            affordable=True,
            shortfall=None,
        )

    shortfall = fare - per_person_budget
    return OriginResult(
        origin=group.origin,
        per_person_budget=per_person_budget,
        fare=fare,
        affordable=False,
        shortfall=round(shortfall, 2),
    )