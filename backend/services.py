from datetime import datetime, timedelta
from getdata import search_flights
from models import OriginEntry, OriginResult, TravelerResult


def compute_return_date(departure_date: str, duration_days: int | None) -> str | None:
    if not duration_days:
        return None
    dep = datetime.strptime(departure_date, "%Y-%m-%d")
    return_date = dep + timedelta(days=duration_days)
    return return_date.strftime("%Y-%m-%d")


def check_origin(
    destination_sky_id: str,
    destination_entity_id: str,
    date: str,
    return_date: str | None,
    origin: OriginEntry,
) -> OriginResult:
    fare = search_flights(
        origin.city_sky_id,
        origin.city_entity_id,
        destination_sky_id,
        destination_entity_id,
        date,
        return_date,
    )

    if fare is None:
        return OriginResult(
            origin=origin.origin_city_label,
            error="No flight found for this route",
        )

    if origin.entry_type == "individual":
        traveler_results = []
        for t in origin.travelers:
            affordable = fare <= t.budget
            traveler_results.append(
                TravelerResult(
                    name=t.name,
                    fare=fare,
                    affordable=affordable,
                    shortfall=None if affordable else round(fare - t.budget, 2),
                )
            )
        compatible_count = sum(1 for r in traveler_results if r.affordable)
        return OriginResult(
            origin=origin.origin_city_label,
            fare=fare,
            traveler_results=traveler_results,
            compatible_count=compatible_count,
            total=len(traveler_results),
        )

    # bulk entry
    affordable = fare <= (origin.bulk_budget or 0)
    shortfall = None if affordable else round(fare - origin.bulk_budget, 2)
    return OriginResult(
        origin=origin.origin_city_label,
        fare=fare,
        headcount=origin.headcount,
        affordable=affordable,
        shortfall=shortfall,
    )