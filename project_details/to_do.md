# To Do

## Platform and cloud wiring

- Validate a DB-backed application path end-to-end against Cloud Run.

## Secrets and configuration

- Validate secret loading behavior in local, CI, and Cloud Run environments.

## Auth and security

- Implement real OAuth2 user authentication flow (replace placeholder login behavior).
- Add persistent user model, credential verification, and password hashing lifecycle.
- Define token claims, expiry strategy, and validation policy for production.

## Data and API surface

- Define canonical data model and database schema from business scope and questionnaire inputs.
- Add migrations workflow for database schema changes.
- Implement canonical API routes required by the mobile app integration scope.
- Add request/response validation and error contracts for mobile integration.

## CI/CD and reliability

- Add GitHub repository secrets for WIF_PROVIDER and WIF_SERVICE_ACCOUNT.
- Add automated tests for authentication, health, and core API routes.
- Add integration testing path against a test database.
- Run a post-deploy smoke test against a DB-backed route or migration path, not only health/auth placeholder routes.

## Documentation and governance

- Refine architecture and overview docs as implementation decisions become final.
- Maintain project_details/to_do.md and project_details/done.md continuously.
