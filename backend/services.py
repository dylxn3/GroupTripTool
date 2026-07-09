from models import OriginGroup, OriginResult
from mock_data import get_mock_fare

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