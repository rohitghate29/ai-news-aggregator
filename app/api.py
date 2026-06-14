"""
FastAPI application for managing user preferences (provider subscriptions).

Run with:  uvicorn app.api:app --reload
Docs at:   http://localhost:8000/docs
"""
import os
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

from app.database.repository import Repository

# ---------------------------------------------------------------------------
# Valid provider keys — must match the `type` values used in repository.py
# ---------------------------------------------------------------------------
VALID_PROVIDERS = {
    "youtube",
    "openai",
    "anthropic",
    "huggingface",
    "claude",
    "google_ai",
    "groq",
    "mistral",
    "ollama",
    "perplexity",
    "xai",
}

# ---------------------------------------------------------------------------
# Pydantic Schemas
# ---------------------------------------------------------------------------

class CreateUserRequest(BaseModel):
    email: str
    name: str
    providers: List[str] = []

    @field_validator("providers")
    @classmethod
    def validate_providers(cls, v: List[str]) -> List[str]:
        normalized = [p.strip().lower() for p in v]
        invalid = [p for p in normalized if p and p not in VALID_PROVIDERS]
        if invalid:
            raise ValueError(
                f"Unknown providers: {invalid}. "
                f"Valid options: {sorted(VALID_PROVIDERS)}"
            )
        return normalized


class UpdateProvidersRequest(BaseModel):
    providers: List[str]

    @field_validator("providers")
    @classmethod
    def validate_providers(cls, v: List[str]) -> List[str]:
        normalized = [p.strip().lower() for p in v]
        invalid = [p for p in normalized if p and p not in VALID_PROVIDERS]
        if invalid:
            raise ValueError(
                f"Unknown providers: {invalid}. "
                f"Valid options: {sorted(VALID_PROVIDERS)}"
            )
        return normalized


class UserPreferenceResponse(BaseModel):
    email: str
    name: str
    providers: List[str]
    created_at: str
    updated_at: str


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _to_response(pref) -> UserPreferenceResponse:
    """Convert a UserPreference ORM object to the API response shape."""
    providers = [p for p in (pref.providers or "").split(",") if p]
    return UserPreferenceResponse(
        email=pref.email,
        name=pref.name,
        providers=providers,
        created_at=pref.created_at.isoformat() if pref.created_at else "",
        updated_at=pref.updated_at.isoformat() if pref.updated_at else "",
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI News Aggregator — Preferences API",
    description="Manage per-user RSS provider subscriptions for the daily digest.",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/providers", summary="List all valid provider keys")
def list_providers():
    """Return every provider key that can be used in preferences."""
    return {"providers": sorted(VALID_PROVIDERS)}


@app.post("/users", response_model=UserPreferenceResponse, status_code=201,
          summary="Register a user or update an existing one")
def create_user(body: CreateUserRequest):
    """
    Create a new user with their preferred providers.
    If the email already exists the record is **upserted** (name + providers updated).
    Pass an empty `providers` list to subscribe to **all** sources.
    """
    repo = Repository()
    pref = repo.create_user_preference(
        email=body.email,
        name=body.name,
        providers=body.providers,
    )
    return _to_response(pref)


@app.get("/users/{email}", response_model=UserPreferenceResponse,
         summary="Get a user's preferences")
def get_user(email: str):
    """Fetch preferences for a single user by email."""
    repo = Repository()
    pref = repo.get_user_preference(email=email)
    if not pref:
        raise HTTPException(status_code=404, detail=f"User '{email}' not found.")
    return _to_response(pref)


@app.get("/users", response_model=List[UserPreferenceResponse],
         summary="List all registered users")
def list_users():
    """Return every registered user and their preferences."""
    repo = Repository()
    prefs = repo.get_all_user_preferences()
    return [_to_response(p) for p in prefs]


@app.put("/users/{email}/providers", response_model=UserPreferenceResponse,
         summary="Update a user's provider list")
def update_providers(email: str, body: UpdateProvidersRequest):
    """
    Replace the provider list for a user.
    Send an empty list to subscribe to **all** sources (no filter).
    """
    repo = Repository()
    pref = repo.update_user_providers(email=email, providers=body.providers)
    if not pref:
        raise HTTPException(status_code=404, detail=f"User '{email}' not found.")
    return _to_response(pref)


@app.delete("/users/{email}", status_code=204,
            summary="Remove a user")
def delete_user(email: str):
    """Permanently delete a user's preference record."""
    repo = Repository()
    deleted = repo.delete_user_preference(email=email)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"User '{email}' not found.")
    return None
