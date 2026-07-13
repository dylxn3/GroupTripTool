from datetime import datetime, timedelta
from getdata import search_flights
from models import (
    OriginEntry, OriginResult, TravelerResult, DestinationCheck,
    DestinationResult, OriginFareBreakdown, DestinationSuggestion,
)

CANDIDATE_DESTINATIONS = [
    {"label": "Cancun", "sky_id": "CUNA", "entity_id": "27538100"},
    {"label": "Tokyo", "sky_id": "TYOA", "entity_id": "27537542"},
    {"label": "Rome", "sky_id": "ROMA", "entity_id": "27538000"},
]


# ------------------------------------------------------------
# Airport resolution — every distinct airport actually in use
# ------------------------------------------------------------

def get_origin_airports(origin: OriginEntry) -> list[dict]:
    """
    Returns every DISTINCT airport actually selected within this origin
    (one per traveler for individual entries, or the bulk airport),
    falling back to the city-wide airport when nothing specific was chosen.
    Each entry: {"sky_id", "entity_id", "label"}
    """
    seen = {}

    if origin.entry_type == "individual":
        for t in origin.travelers:
            if t.airport_sky_id:
                seen[t.airport_sky_id] = {
                    "sky_id": t.airport_sky_id,
                    "entity_id": t.airport_entity_id,
                    "label": t.airport_label or t.airport_sky_id,
                }
        if not seen:
            seen[origin.city_sky_id] = {
                "sky_id": origin.city_sky_id,
                "entity_id": origin.city_entity_id,
                "label": origin.origin_city_label,
            }
    else:
        if origin.bulk_airport_sky_id:
            seen[origin.bulk_airport_sky_id] = {
                "sky_id": origin.bulk_airport_sky_id,
                "entity_id": origin.bulk_airport_entity_id,
                "label": origin.bulk_airport_label or origin.bulk_airport_sky_id,
            }
        else:
            seen[origin.city_sky_id] = {
                "sky_id": origin.city_sky_id,
                "entity_id": origin.city_entity_id,
                "label": origin.origin_city_label,
            }

    return list(seen.values())


def get_traveler_airport(traveler, origin: OriginEntry) -> tuple[str, str]:
    """Specific airport for one traveler, falling back to the origin's city-wide ID."""
    if traveler.airport_sky_id:
        return traveler.airport_sky_id, traveler.airport_entity_id
    return origin.city_sky_id, origin.city_entity_id


def get_bulk_airport(origin: OriginEntry) -> tuple[str, str]:
    if origin.bulk_airport_sky_id:
        return origin.bulk_airport_sky_id, origin.bulk_airport_entity_id
    return origin.city_sky_id, origin.city_entity_id


# ------------------------------------------------------------
# Fare cache — avoid duplicate search_flights calls for the same route
# ------------------------------------------------------------

class FareCache:
    def __init__(self, date: str, return_date: str | None):
        self.date = date
        self.return_date = return_date
        self._cache: dict[tuple[str, str], float | None] = {}

    def get_fare(self, origin_sky_id: str, origin_entity_id: str, dest_sky_id: str, dest_entity_id: str) -> float | None:
        key = (origin_sky_id, dest_sky_id)
        if key not in self._cache:
            self._cache[key] = search_flights(
                origin_sky_id, origin_entity_id, dest_sky_id, dest_entity_id, self.date, self.return_date
            )
        return self._cache[key]


def get_min_budget(origin: OriginEntry) -> float:
    if origin.entry_type == "individual":
        return min((t.budget for t in origin.travelers), default=0)
    return origin.bulk_budget or 0


def compute_return_date(departure_date: str, duration_days: int | None) -> str | None:
    if not duration_days:
        return None
    dep = datetime.strptime(departure_date, "%Y-%m-%d")
    ret = dep + timedelta(days=duration_days)
    return ret.strftime("%Y-%m-%d")


# ------------------------------------------------------------
# Fixed-destination mode
# ------------------------------------------------------------

def check_origin(
    destination_sky_id: str,
    destination_entity_id: str,
    date: str,
    return_date: str | None,
    origin: OriginEntry,
    cache: FareCache,
) -> OriginResult:
    if origin.entry_type == "individual":
        traveler_results = []
        any_fare_found = False
        for t in origin.travelers:
            o_sky, o_entity = get_traveler_airport(t, origin)
            fare = cache.get_fare(o_sky, o_entity, destination_sky_id, destination_entity_id)
            if fare is None:
                traveler_results.append(TravelerResult(name=t.name, fare=None, affordable=False, shortfall=None))
                continue
            any_fare_found = True
            affordable = fare <= t.budget
            traveler_results.append(TravelerResult(
                name=t.name, fare=fare, affordable=affordable,
                shortfall=None if affordable else round(fare - t.budget, 2),
            ))

        if not any_fare_found:
            return OriginResult(origin=origin.origin_city_label, error="No flight found for this route")

        compatible_count = sum(1 for r in traveler_results if r.affordable)
        # use the first found fare just for display purposes on the origin summary line
        display_fare = next((r.fare for r in traveler_results if r.fare is not None), None)
        return OriginResult(
            origin=origin.origin_city_label,
            fare=display_fare,
            traveler_results=traveler_results,
            compatible_count=compatible_count,
            total=len(traveler_results),
        )

    # bulk
    o_sky, o_entity = get_bulk_airport(origin)
    fare = cache.get_fare(o_sky, o_entity, destination_sky_id, destination_entity_id)
    if fare is None:
        return OriginResult(origin=origin.origin_city_label, error="No flight found for this route")

    affordable = fare <= (origin.bulk_budget or 0)
    return OriginResult(
        origin=origin.origin_city_label,
        fare=fare,
        headcount=origin.headcount,
        affordable=affordable,
        shortfall=None if affordable else round(fare - origin.bulk_budget, 2),
    )


def all_affordable(origin_results: list[OriginResult]) -> bool:
    for r in origin_results:
        if r.error:
            return False
        if r.traveler_results is not None:
            if r.compatible_count != r.total:
                return False
        elif r.affordable is False:
            return False
    return True


def check_destination_for_origin(dest: dict, cache: FareCache, origin: OriginEntry) -> DestinationCheck:
    result = check_origin(dest["sky_id"], dest["entity_id"], cache.date, cache.return_date, origin, cache)
    return DestinationCheck(
        origin=result.origin,
        fare=result.fare,
        error=result.error,
        traveler_results=result.traveler_results,
        compatible_count=result.compatible_count,
        total=result.total,
        affordable=result.affordable,
        shortfall=result.shortfall,
    )


def find_alternatives_for_trip(origins: list[OriginEntry], date: str, return_date: str | None) -> list[DestinationResult]:
    cache = FareCache(date, return_date)
    results = []
    for dest in CANDIDATE_DESTINATIONS:
        origin_checks = [check_destination_for_origin(dest, cache, o) for o in origins]
        results.append(DestinationResult(destination_label=dest["label"], origin_checks=origin_checks))
    return results


# ------------------------------------------------------------
# Anywhere mode — now airport-aware, one "row" per distinct airport used
# ------------------------------------------------------------

def find_anywhere_trip(origins: list[OriginEntry], date: str, return_date: str | None) -> dict:
    cache = FareCache(date, return_date)

    airport_rows = []
    for origin in origins:
        budget = get_min_budget(origin)
        for airport in get_origin_airports(origin):
            display_label = airport["label"]
            if display_label != origin.origin_city_label:
                display_label = f"{origin.origin_city_label} ({airport['label']})"
            airport_rows.append({
                "origin_city_label": origin.origin_city_label,
                "display_label": display_label,
                "sky_id": airport["sky_id"],
                "entity_id": airport["entity_id"],
                "budget": budget,
            })

    fare_matrix = {}
    for row in airport_rows:
        for dest in CANDIDATE_DESTINATIONS:
            fare_matrix[(row["sky_id"], dest["sky_id"])] = cache.get_fare(
                row["sky_id"], row["entity_id"], dest["sky_id"], dest["entity_id"]
            )

    def build_breakdown(dest: dict) -> list[OriginFareBreakdown]:
        breakdown = []
        for row in airport_rows:
            fare = fare_matrix.get((row["sky_id"], dest["sky_id"]))
            if fare is None:
                continue
            affordable = fare <= row["budget"]
            breakdown.append(OriginFareBreakdown(
                origin=row["display_label"],
                fare=fare,
                budget=row["budget"],
                affordable=affordable,
                shortfall=None if affordable else round(fare - row["budget"], 2),
            ))
        return breakdown

    # Step 1: destinations affordable for EVERYONE — the ideal case
    viable = []
    for dest in CANDIDATE_DESTINATIONS:
        breakdown = build_breakdown(dest)
        if len(breakdown) == len(airport_rows) and all(b.affordable for b in breakdown):
            total_cost = sum(b.fare for b in breakdown)
            checks = [
                DestinationCheck(origin=b.origin, fare=b.fare, affordable=b.affordable, shortfall=b.shortfall)
                for b in breakdown
            ]
            viable.append((total_cost, DestinationResult(destination_label=dest["label"], origin_checks=checks)))

    if viable:
        # Rank affordable options by lowest total combined cost first
        viable.sort(key=lambda x: x[0])
        return {
            "destinations": [v[1] for v in viable],
            "cheapest_per_origin": None,
            "recommended_option": None,
        }

    # Step 2: nothing affordable for everyone — rank ALL candidates by lowest total combined cost,
    # regardless of affordability, and surface the cheapest overall as the recommendation.
    # Spread is included as supporting info, not the deciding factor.
    ranked_candidates = []
    for dest in CANDIDATE_DESTINATIONS:
        breakdown = build_breakdown(dest)
        if len(breakdown) != len(airport_rows):
            continue  # skip destinations missing a fare for any origin
        total_cost = sum(b.fare for b in breakdown)
        fares = [b.fare for b in breakdown]
        spread = round(max(fares) - min(fares), 2)
        ranked_candidates.append((total_cost, spread, dest, breakdown))

    recommended_option = None
    if ranked_candidates:
        ranked_candidates.sort(key=lambda x: x[0])  # lowest total cost wins
        total_cost, spread, dest, breakdown = ranked_candidates[0]
        recommended_option = DestinationSuggestion(
            destination_label=dest["label"],
            anchor_origin=None,
            origin_fares=breakdown,
            fare_spread=spread,
        )

    # Each origin's own individually cheapest destination — kept as supplementary info
    cheapest_per_origin = []
    for row in airport_rows:
        fares = [(dest, fare_matrix.get((row["sky_id"], dest["sky_id"]))) for dest in CANDIDATE_DESTINATIONS]
        fares = [(d, f) for d, f in fares if f is not None]
        if not fares:
            continue
        cheapest_dest, _ = min(fares, key=lambda x: x[1])
        cheapest_per_origin.append(DestinationSuggestion(
            destination_label=cheapest_dest["label"],
            anchor_origin=row["display_label"],
            origin_fares=build_breakdown(cheapest_dest),
        ))

    return {
        "destinations": [],
        "cheapest_per_origin": cheapest_per_origin,
        "recommended_option": recommended_option,
    }