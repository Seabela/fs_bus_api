# To Do

## Platform and cloud wiring

- Set Google Cloud project configuration to bus-track-480813 across runtime, docs, and deployment.
- Provision PostgreSQL Cloud SQL instance for the API.
- Finalize Cloud SQL connection strategy for local development and Cloud Run deployment.
- Configure required IAM roles for API runtime, CI/CD deploy identity, and assistant DB access.

## Secrets and configuration

- Create and verify required Secret Manager secrets for API auth and database credentials.
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

- Verify GitHub Actions secrets and deployment values for bus-track-480813.
- Add automated tests for authentication, health, and core API routes.
- Add integration testing path against a test database.

## Documentation and governance

- Refine architecture and overview docs as implementation decisions become final.
- Maintain project_details/to_do.md and project_details/done.md continuously.
