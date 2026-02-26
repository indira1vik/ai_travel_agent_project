from fastapi import FastAPI, HTTPException
from typing import List
from fastapi.middleware.cors import CORSMiddleware

import app.database as db
import app.schema.trip as trip_schema
import app.schema.auth as auth_schema
from app.agents.orchestrator import orchestrated_answers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    db.init_db()

@app.get("/health")
def health_check():
    return { "Status": "OK" }

@app.post("/login", response_model=auth_schema.AuthResponse)
def login(payload: auth_schema.LoginRequest):
    user = db.get_user_by_email(payload.email)
    if user is None:
        raise HTTPException(status_code=401, detail="Email not found")
    if not db.verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")
    return auth_schema.AuthResponse(
        user_id=user["id"],
        name=user["name"],
        email=user["email"],
    )

@app.post("/signup", response_model=auth_schema.AuthResponse)
def signup(payload: auth_schema.NewUserRequest):
    existing = db.get_user_by_email(payload.email)
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_id = db.create_user(
        name=payload.name,
        email=payload.email,
        plain_password=payload.password,
    )
    return auth_schema.AuthResponse(
        user_id=user_id,
        name=payload.name,
        email=payload.email,
    )

@app.post("/plan_trip", response_model=trip_schema.TripPlanResponse)
def plan_trip(request: trip_schema.TripPlanRequest, user_id: int):
    planned_trip = orchestrated_answers(
        source=request.source,
        destination=request.destination,
        budget=request.budget,
        days=request.days,
        people_count=request.people_count,
    )
    db.insert_trip_plan(
        user_id=user_id,
        source=request.source,
        destination=request.destination,
        people_count=request.people_count,
        days=request.days,
        total_budget=request.budget,
        raw_plan=planned_trip,
    )
    return planned_trip

@app.get("/get_trips_of_one_user", response_model=List[trip_schema.TripPlanResponse])
def get_trips_of_one_user(user_id: int):
    return db.get_user_trips(user_id)

@app.get("/get_one_trip_details", response_model=trip_schema.TripPlanResponse)
def get_one_trip_details(user_id: int, trip_id: int):
    return db.get_one_trip_by_id(user_id, trip_id)

