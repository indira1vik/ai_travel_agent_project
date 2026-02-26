from app.agents.flight import search_flights
from app.agents.hotel import search_hotels
from app.agents.itinerary import setup_itinerary


def orchestrated_answers(source: str, destination: str, days: int, budget: int, people_count):
    flights = search_flights()
    hotels = search_hotels()
    itinerary = setup_itinerary()
    return {
        "source": source,
        "destination": destination,
        "days": days,
        "people_count": people_count,
        "budget": budget,
        "flights": flights,
        "hotels": hotels,
        "itinerary": itinerary,
    }