# Fake fare lookup: (origin, destination) -> fare in USD
MOCK_FARES = {
    ("Toronto", "Cancun"): 450,
    ("Rome", "Cancun"): 900,
    ("Manila", "Cancun"): 1200,
    ("Toronto", "Lisbon"): 600,
    ("Rome", "Lisbon"): 150,
    ("Manila", "Lisbon"): 1400,
}

def get_mock_fare(origin: str, destination: str) -> float | None:
    return MOCK_FARES.get((origin, destination))