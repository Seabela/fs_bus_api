# Free State Bus API Overview

This is an app for the API of the Free State Bus Project.

This service will run as a FastAPI application, with its database hosted in Google Cloud project ID: bus-track-480813.

The app will use Google Cloud Secret Manager for applicable secrets.

We need to create a PostgreSQL Cloud SQL instance and connect the API to it.

The API needs to use OAuth2, and we need to set up the necessary components for that.

The AI assistant should have direct read and write access to the database.

The workflow needs CI/CD deployment on the main branch.

Scope details from the mobile app team, including their questionnaire, are included in project_details/scope.

The current architecture was initially set up by a GitHub repository setup assistant. Nothing is fully wired into Google Cloud yet, and required details and routes are not yet canonical.
