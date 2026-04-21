import unittest
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.auth import TokenData, expand_role_permissions, require_role
from app.main import app


client = TestClient(app)


class AuthTests(unittest.TestCase):
    def test_expand_role_permissions_respects_hierarchy(self):
        self.assertEqual(
            expand_role_permissions("Admin"),
            ("Monitor", "Supervisor", "Admin"),
        )
        self.assertEqual(
            expand_role_permissions("Supervisor"),
            ("Monitor", "Supervisor"),
        )

    def test_require_role_accepts_inherited_permissions(self):
        dependency = require_role("Monitor")
        current_user = TokenData(sub="user-123", role="Admin")

        returned_user = dependency(current_user)

        self.assertEqual(returned_user, current_user)

    def test_require_role_rejects_insufficient_permissions(self):
        dependency = require_role("Admin")
        current_user = TokenData(sub="user-123", role="Monitor")

        with self.assertRaises(HTTPException) as raised:
            dependency(current_user)

        self.assertEqual(raised.exception.status_code, 403)
        self.assertEqual(raised.exception.detail, "Insufficient permissions")

    def test_me_returns_firebase_identity_claims(self):
        payload = {
            "uid": "user-123",
            "name": "Ada Lovelace",
            "email": "ada@example.com",
            "role": "Supervisor",
        }

        with patch("app.auth.firebase_auth.verify_id_token", return_value=payload), patch(
            "app.auth.get_firebase_app", return_value=object()
        ):
            response = client.get(
                "/me",
                headers={"Authorization": "Bearer firebase-token"},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "sub": "user-123",
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "role": "Supervisor",
                "permissions": ["Monitor", "Supervisor"],
            },
        )

    def test_me_requires_bearer_token(self):
        response = client.get("/me")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Could not validate credentials")


if __name__ == "__main__":
    unittest.main()