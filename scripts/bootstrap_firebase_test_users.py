from __future__ import annotations

import argparse
import json
import secrets

from firebase_admin import auth, get_app, initialize_app


ROLE_USERS = (
    ("Monitor", "monitor.test@fsbus.example.com", "FS Bus Monitor Test"),
    ("Supervisor", "supervisor.test@fsbus.example.com", "FS Bus Supervisor Test"),
    ("Admin", "admin.test@fsbus.example.com", "FS Bus Admin Test"),
)


def get_or_initialize_app(project_id: str):
    try:
        return get_app()
    except ValueError:
        return initialize_app(options={"projectId": project_id})


def generate_password() -> str:
    return secrets.token_urlsafe(18)


def upsert_user(project_id: str, role: str, email: str, display_name: str, reset_password: bool) -> dict[str, str]:
    get_or_initialize_app(project_id)

    password = generate_password() if reset_password else None
    created = False

    try:
        user = auth.get_user_by_email(email)
    except auth.UserNotFoundError:
        user = auth.create_user(
            email=email,
            email_verified=True,
            password=password or generate_password(),
            display_name=display_name,
            disabled=False,
        )
        created = True
        if password is None:
            password = "generated-on-create"

    update_kwargs = {
        "display_name": display_name,
        "disabled": False,
        "email_verified": True,
    }
    if reset_password:
        update_kwargs["password"] = password
    user = auth.update_user(user.uid, **update_kwargs)
    auth.set_custom_user_claims(user.uid, {"role": role})

    return {
        "role": role,
        "email": email,
        "uid": user.uid,
        "status": "created" if created else "updated",
        "password": password or "unchanged",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or update Firebase test users for each role.")
    parser.add_argument("--project-id", default="bus-track-480813")
    parser.add_argument(
        "--reset-passwords",
        action="store_true",
        help="Generate and apply a new random password for each role user.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    results = [
        upsert_user(args.project_id, role, email, display_name, args.reset_passwords)
        for role, email, display_name in ROLE_USERS
    ]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()