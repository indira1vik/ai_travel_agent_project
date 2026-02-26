from typing import List
from pydantic import BaseModel, Field

class FlightOption(BaseModel):
    provider: str
    airline: str
    price: float
    duration_hours: int

class HotelOption(BaseModel):
    provider: str
    name: str
    price_per_day: float
    rating: float

class ItineraryItem(BaseModel):
    day: int
    plan: str

class TripPlanRequest(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    people_count: int = Field(..., gt=0)
    days: int = Field(..., gt=0)
    budget: float = Field(..., gt=0)

class TripPlanResponse(BaseModel):
    source: str
    destination: str
    days: int
    people_count: int
    budget: float
    flights: List[FlightOption]
    hotels: List[HotelOption]
    itinerary: List[ItineraryItem]