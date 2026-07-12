from datetime import datetime, timedelta
from getdata import search_flights
from models import OriginEntry, OriginResult, TravelerResult, DestinationCheck, DestinationResult

CANDIDATE_DESTINATIONS = [
    {"label": "Cancun", "sky_id": "CUNA", "entity_id": "27538100"},
    {"label": "Tokyo", "sky_id": "TYOA", "entity_id": "27537542"},
    {"label": "Rome", "sky_id": "ROMA", "entity_id": "27538000"},
]


def get_min_budget(origin: OriginEntry) -> float:
    """Lowest effective per-person budget for this origin group."""
    if origin.entry_type == "individual":
        return min((t.budget for t in origin.travelers), default=0)
    return origin.bulk_budget or 0


def find_anchor_origin(origins: list[OriginEntry]) -> OriginEntry:
    """The origin group with the lowest budget — search starts here."""
    return min(origins, key=get_min_budget)


def check_destination_for_origin(dest: dict, date: str, return_date: str | None, origin: OriginEntry) -> DestinationCheck:
    fare = search_flights(origin.city_sky_id, origin.city_entity_id, dest["sky_id"], dest["entity_id"], date, return_date)

    if fare is None:
        return DestinationCheck(origin=origin.origin_city_label, fare=None, affordable=False, shortfall=None, error="No route found")

    if origin.entry_type == "individual":
        traveler_results = []
        for t in origin.travelers:
            affordable = fare <= t.budget
            traveler_results.append(TravelerResult(
                name=t.name, fare=fare, affordable=affordable,
                shortfall=None if affordable else round(fare - t.budget, 2),
            ))
        return DestinationCheck(
            origin=origin.origin_city_label, fare=fare,
            traveler_results=traveler_results,
            compatible_count=sum(1 for r in traveler_results if r.affordable),
            total=len(traveler_results),
        )

    affordable = fare <= (origin.bulk_budget or 0)
    return DestinationCheck(
        origin=origin.origin_city_label, fare=fare, affordable=affordable,
        shortfall=None if affordable else round(fare - origin.bulk_budget, 2),
    )


def find_anywhere_trip(origins: list[OriginEntry], date: str, return_date: str | None) -> list[DestinationResult]:
    anchor = find_anchor_origin(origins)
    anchor_budget = get_min_budget(anchor)

    # Step 1: find destinations the anchor (most budget-constrained) group can afford
    affordable_for_anchor = []
    for dest in CANDIDATE_DESTINATIONS:
        fare = search_flights(anchor.city_sky_id, anchor.city_entity_id, dest["sky_id"], dest["entity_id"], date, return_date)
        if fare is not None and fare <= anchor_budget:
            affordable_for_anchor.append(dest)

    # Step 2: for each of those, check every other origin
    results = []
    for dest in affordable_for_anchor:
        origin_checks = [check_destination_for_origin(dest, date, return_date, o) for o in origins]
        results.append(DestinationResult(destination_label=dest["label"], origin_checks=origin_checks))

    return results

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