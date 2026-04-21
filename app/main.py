"""
FS Bus API — main application entry-point.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse

from app.auth import (
    Token,
    expand_role_permissions,
    get_current_user,
    normalize_role,
    TokenData,
)
from app.config import Settings, get_settings
from app.firebase_identity import (
    FirebaseIdentityError,
    FirebaseInvalidCredentialsError,
    FirebasePasswordSignInRequest,
    sign_in_with_email_password,
)

# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="FS Bus API",
    description="API for capturing data for the FS bus tracking application.",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
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

from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def _serialize_user(current_user: TokenData) -> dict[str, object]:
    return {
        "sub": current_user.sub,
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role,
        "permissions": list(expand_role_permissions(current_user.role)),
    }


def _require_docs_user(
    current_user: Annotated[TokenData, Depends(get_current_user)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> TokenData:
    required_role = normalize_role(settings.docs_required_role)
    if required_role is None:
        return current_user
    if required_role not in expand_role_permissions(current_user.role):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )
    return current_user


def _build_docs_html(settings: Settings) -> str:
    required_role = settings.docs_required_role or "any authenticated user"
    return f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{app.title} Docs</title>
    <link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css\" />
    <style>
        body {{
            margin: 0;
            font-family: "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #f3f7f4, #dce9df);
            color: #17301f;
        }}
        .docs-shell {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px;
        }}
        .gate {{
            background: rgba(255, 255, 255, 0.92);
            border: 1px solid #b7cabd;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 14px 30px rgba(23, 48, 31, 0.08);
            margin-bottom: 20px;
        }}
        .gate h1 {{
            margin-top: 0;
            font-size: 1.7rem;
        }}
        .gate p {{
            margin: 0 0 12px;
            line-height: 1.5;
        }}
        .gate label {{
            display: block;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .gate textarea {{
            width: 100%;
            min-height: 110px;
            border-radius: 12px;
            border: 1px solid #8ea795;
            padding: 12px;
            font: inherit;
            box-sizing: border-box;
        }}
        .gate button {{
            margin-top: 12px;
            border: 0;
            border-radius: 999px;
            padding: 12px 18px;
            background: #17301f;
            color: #fff;
            font: inherit;
            cursor: pointer;
        }}
        .gate code {{
            background: #eef4ef;
            padding: 2px 6px;
            border-radius: 6px;
        }}
        #status {{
            margin-top: 10px;
            min-height: 24px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class=\"docs-shell\">
        <section class=\"gate\">
            <h1>{app.title} API Docs</h1>
            <p>OpenAPI access is protected by the same Firebase bearer-token flow as the API.</p>
            <p>Minimum role: <code>{required_role}</code>.</p>
            <label for=\"token\">Firebase ID token</label>
            <textarea id=\"token\" placeholder=\"Paste a Firebase ID token here\"></textarea>
            <button id=\"load-docs\" type=\"button\">Load Protected Docs</button>
            <div id=\"status\"></div>
        </section>
        <div id=\"swagger-ui\"></div>
    </div>
    <script src=\"https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js\"></script>
    <script>
        const tokenInput = document.getElementById('token');
        const statusNode = document.getElementById('status');
        const loadButton = document.getElementById('load-docs');

        async function loadDocs() {{
            const token = tokenInput.value.trim();
            if (!token) {{
                statusNode.textContent = 'A Firebase ID token is required.';
                return;
            }}

            statusNode.textContent = 'Loading protected OpenAPI schema...';
            const response = await fetch('/openapi.json', {{
                headers: {{ Authorization: `Bearer ${{token}}` }},
            }});

            if (!response.ok) {{
                const body = await response.text();
                statusNode.textContent = `Schema request failed: ${{response.status}} ${{body}}`;
                return;
            }}

            const spec = await response.json();
            statusNode.textContent = 'Docs loaded.';
            window.ui = SwaggerUIBundle({{
                spec,
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [SwaggerUIBundle.presets.apis],
                requestInterceptor: (request) => {{
                    request.headers = request.headers || {{}};
                    request.headers.Authorization = `Bearer ${{token}}`;
                    return request;
                }},
            }});
        }}

        loadButton.addEventListener('click', () => {{
            loadDocs().catch((error) => {{
                statusNode.textContent = `Failed to load docs: ${{error}}`;
            }});
        }});
    </script>
</body>
</html>
"""


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


@auth_router.get("/test/whoami", summary="Validate Firebase bearer token")
def auth_test_whoami(
    current_user: Annotated[TokenData, Depends(get_current_user)],
):
    return {
        "provider": "firebase",
        "user": _serialize_user(current_user),
    }


@auth_router.post(
    "/test/token",
    summary="Exchange email/password for a Firebase ID token (testing only)",
)
def auth_test_token(
    request: FirebasePasswordSignInRequest,
    settings: Annotated[Settings, Depends(get_settings)],
):
    if not settings.enable_test_auth_endpoints:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test auth endpoints are disabled.",
        )

    try:
        return sign_in_with_email_password(
            api_key=settings.firebase_web_api_key,
            email=request.email,
            password=request.password,
        )
    except FirebaseInvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        ) from exc
    except FirebaseIdentityError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


app.include_router(auth_router)


@app.get("/openapi.json", include_in_schema=False)
def openapi_schema(
    current_user: Annotated[TokenData, Depends(_require_docs_user)],
):
    return JSONResponse(
        get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
    )


@app.get("/docs", include_in_schema=False)
def docs_index(settings: Annotated[Settings, Depends(get_settings)]):
    return HTMLResponse(_build_docs_html(settings))


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
    return _serialize_user(current_user)
