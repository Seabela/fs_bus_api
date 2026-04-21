# Current Architecture and Status

## Current baseline

- FastAPI service scaffold exists with entry point in app/main.py.
- Basic middleware and health endpoint exist.
- OAuth2 bearer token scaffolding exists, with JWT encode/decode helpers.
- The token issue endpoint exists but currently returns not implemented for real authentication.
- SQLAlchemy database engine and session setup exist for PostgreSQL.
- Configuration supports loading secrets from environment variables and Google Cloud Secret Manager.
- Dockerfile and docker-compose are present for local API plus Cloud SQL Proxy style development.
- GitHub Actions workflow exists for test, build, and deploy on main branch pushes.

## Important caveat

- This is a generated baseline architecture and should be treated as starter scaffolding.
- Cloud resources, IAM, secrets, database provisioning, and production auth are not fully finalized.
- Existing routes and implementation details are not yet canonical and must be validated against project scope.

## Source inputs to align against

- project_details/scope/FreeStateBusApp_BusinessSpec_v2 - Sean Markup.docx
- project_details/scope/Phase 1 questions_v2.docx

## Architecture direction

- Keep FastAPI as API runtime.
- Use Cloud SQL for PostgreSQL as the system database.
- Use Secret Manager for secrets and sensitive runtime values.
- Implement OAuth2-compliant auth flow with production-grade token issuance and validation.
- Use CI/CD on main branch as the deployment trigger.
