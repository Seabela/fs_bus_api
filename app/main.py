"""
FS Bus API — main application entry-point.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app.auth import (
    Token,
    expand_role_permissions,
    get_current_user,
    TokenData,
)
from app.config import Settings, get_settings

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="FS Bus API",
    description="API for capturing data for the FS bus tracking application.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


def _get_cors_origins(settings: Settings) -> list[str]:
    return [o.strip() for o in settings.cors_origins.split(",") if o.strip()]


app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_cors_origins(get_settings()),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Auth router
# ---------------------------------------------------------------------------

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=Token, summary="Obtain an access token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
):
    """Placeholder endpoint retained only for explicit non-support messaging.

    Production login is expected to happen through the configured identity
    provider rather than this API endpoint.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Login is not handled by this API. "
            "Authenticate through the configured identity provider and call the API with a Bearer token."
        ),
    )


app.include_router(auth_router)

# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health", tags=["health"], summary="Health check")
def health():
    """Returns ``{"status": "ok"}`` when the service is running."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Protected example route
# ---------------------------------------------------------------------------


@app.get("/me", tags=["users"], summary="Current authenticated user")
def read_current_user(
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    """Return the identity of the currently authenticated caller."""
    return {
        "sub": current_user.sub,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "permissions": list(expand_role_permissions(current_user.role)),
    }
