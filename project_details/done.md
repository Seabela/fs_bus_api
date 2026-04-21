# Done

## Existing implementation baseline

- FastAPI application scaffold created with API metadata and startup flow.
- CORS configuration wiring added.
- Health endpoint implemented.
- OAuth2 bearer scheme and JWT helper functions implemented.
- Auth token endpoint scaffold created as a placeholder for real auth.
- Settings management created with environment-first and Secret Manager fallback loading.
- SQLAlchemy engine and session setup implemented for PostgreSQL.
- Dockerfile created for containerized API runtime.
- docker-compose stack created with API service and Cloud SQL Proxy service for local use.
- start.sh script created for local startup workflow.
- Initial GitHub Actions CI/CD workflow created for test, build, and deploy path on main branch.
- Scope artifacts added under project_details/scope.

## Cloud bootstrap completed (africa-south1)

- Google Cloud project defaults set to bus-track-480813 with regional defaults in africa-south1.
- Required GCP APIs enabled for compute, Cloud SQL, Secret Manager, Cloud Run, Artifact Registry, IAM, Resource Manager, and Service Networking.
- Service accounts provisioned: fs-bus-api-runtime and fs-bus-cicd.
- IAM role bindings applied for runtime and CI/CD service accounts.
- Cloud SQL PostgreSQL instance provisioned in africa-south1 and upgraded to POSTGRES_17.
- Application database created: fs_bus_api.
- Application database user created: fs_bus_user.
- Secret Manager secret containers created and initialized: api-secret-key, db-password, db-name, db-user.
- Database user password rotated and synchronized into db-password secret.

## Deployment and CI wiring completed

- Runtime database URL handling updated to support Cloud SQL Unix socket paths in Cloud Run.
- Default application GCP project updated to bus-track-480813.
- GitHub Actions workflow updated to use Workload Identity Federation instead of static service account keys.
- Cloud Run service bus-track-api configured to use runtime service account fs-bus-api-runtime.
- Cloud Run service bus-track-api configured with Cloud SQL instance bus-track-480813:africa-south1:fs-bus-db.
- Cloud Run service bus-track-api configured with Secret Manager-backed environment values for DB and JWT secrets.
- Artifact Registry repository bus-track-mcomm verified in africa-south1.
- GitHub Workload Identity Pool and Provider created for macrocomm-dev/fs_bus_api.
- Workload identity binding applied to fs-bus-cicd for GitHub Actions OIDC.
- GitHub deployment configuration moved to repository variables and redundant GitHub secrets were removed.
- Temporary manual token-creator grant used for smoke testing was removed after validation.
- Application startup failure on Cloud Run fixed by moving CORS middleware registration out of startup lifecycle.
- Current workspace image built, pushed to Artifact Registry, and deployed to Cloud Run successfully.

## Smoke checks completed

- Cloud Run health endpoint validated successfully with HTTP 200.
- Protected /me endpoint validated to reject invalid credentials with HTTP 401.
- Placeholder auth token endpoint validated to return HTTP 501 until real auth is implemented.
- Secret Manager latest-version access validated for api-secret-key, db-password, db-name, and db-user.
- Direct external PostgreSQL connection probe from local environment timed out against the instance public IP, so DB-backed application behavior is not yet fully validated end-to-end.

## Auth implementation started

- API bearer-token validation switched from local placeholder JWT decoding to Firebase token verification.
- Firebase configuration fields added to application settings and local environment template.
- Current authenticated user response expanded to expose sub, name, email, role, and derived permissions.
- Role hierarchy modeled in code for Monitor, Supervisor, and Admin, including inherited capabilities.
- Focused automated tests added for auth helpers and the /me protected route.

## Notes

- Items in this file represent work already present in the repository baseline.
- Completed tasks from project_details/to_do.md must be moved here as they are finished.
