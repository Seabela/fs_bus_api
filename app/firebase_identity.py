from __future__ import annotations

import httpx
from pydantic import BaseModel


FIREBASE_PASSWORD_SIGN_IN_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
)

# Firebase Web API keys are public client configuration, not secrets.
DEFAULT_FIREBASE_WEB_API_KEY = "AIzaSyDh21k62KCpURRdmM_zQXozBtJJQ3HHxhA"


class FirebaseIdentityError(Exception):
    pass


class FirebaseInvalidCredentialsError(FirebaseIdentityError):
    pass


class FirebasePasswordSignInRequest(BaseModel):
    email: str
    password: str


class FirebasePasswordSignInResult(BaseModel):
    provider: str = "firebase"
    id_token: str
    refresh_token: str
    expires_in: int
    email: str | None = None
    local_id: str | None = None
    registered: bool | None = None


def _extract_error_code(response: httpx.Response) -> str:
    try:
        data = response.json()
    except ValueError:
        return ""
    error = data.get("error") if isinstance(data, dict) else None
    if not isinstance(error, dict):
        return ""
    message = error.get("message")
    return message if isinstance(message, str) else ""


def sign_in_with_email_password(
    api_key: str,
    email: str,
    password: str,
    timeout_seconds: float = 10.0,
) -> FirebasePasswordSignInResult:
    if not api_key:
        raise FirebaseIdentityError("Firebase Web API key is not configured.")

    response = httpx.post(
        f"{FIREBASE_PASSWORD_SIGN_IN_URL}?key={api_key}",
        json={
            "email": email,
            "password": password,
            "returnSecureToken": True,
        },
        timeout=timeout_seconds,
    )

    if response.status_code >= 400:
        error_code = _extract_error_code(response)
        if error_code in {
            "INVALID_LOGIN_CREDENTIALS",
            "EMAIL_NOT_FOUND",
            "INVALID_PASSWORD",
            "USER_DISABLED",
        }:
            raise FirebaseInvalidCredentialsError(error_code or "Invalid email or password")
        raise FirebaseIdentityError(error_code or "Firebase sign-in failed.")

    payload = response.json()
    return FirebasePasswordSignInResult(
        id_token=payload["idToken"],
        refresh_token=payload["refreshToken"],
        expires_in=int(payload["expiresIn"]),
        email=payload.get("email"),
        local_id=payload.get("localId"),
        registered=payload.get("registered"),
    )