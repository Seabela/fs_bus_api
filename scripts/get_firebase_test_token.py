from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.firebase_identity import (
    DEFAULT_FIREBASE_WEB_API_KEY,
    FirebaseIdentityError,
    FirebaseInvalidCredentialsError,
    sign_in_with_email_password,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exchange Firebase email/password credentials for an ID token.",
    )
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument(
        "--api-key",
        default=os.getenv("FIREBASE_WEB_API_KEY", DEFAULT_FIREBASE_WEB_API_KEY),
        help="Firebase Web API key. Defaults to FIREBASE_WEB_API_KEY or the project browser key.",
    )
    parser.add_argument(
        "--id-token-only",
        action="store_true",
        help="Print only the Firebase ID token.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = sign_in_with_email_password(
            api_key=args.api_key,
            email=args.email,
            password=args.password,
        )
    except FirebaseInvalidCredentialsError:
        print("Invalid email or password.")
        return 1
    except FirebaseIdentityError as exc:
        print(str(exc))
        return 2

    if args.id_token_only:
        print(result.id_token)
    else:
        print(json.dumps(result.model_dump(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())