# AI Assistant Config, Reference, and Rules

## Role

The assistant is responsible for helping implement, maintain, and document the Free State Bus API project.

## Required references

The assistant must always use these files as first-class references:

- project_details/overview.md
- project_details/architecture.md
- project_details/auth_and_secrets.md
- project_details/to_do.md
- project_details/done.md
- project_details/scope/FreeStateBusApp_BusinessSpec_v2 - Sean Markup.docx
- project_details/scope/Phase 1 questions_v2.docx

## Task tracking rules

- Any new task discovered must be added to project_details/to_do.md.
- When a task is completed, move it from project_details/to_do.md to project_details/done.md.
- Keep each item short, action-oriented, and testable.
- Never delete historical completed items from project_details/done.md.
- Update task status as part of every implementation session where progress is made.

## Delivery and quality rules

- Do not treat scaffold defaults as final architecture.
- Validate implementation choices against mobile app scope and questionnaire requirements.
- Prefer secure defaults for auth, secrets, and database access.
- Record assumptions explicitly when requirements are ambiguous.
- Keep docs synchronized with code changes.

## Security and access rules

- Use Google Cloud Secret Manager for runtime secrets.
- Avoid hardcoding secrets in source code.
- Ensure the assistant can operate with direct read and write database access where required for delivery workflows.
- Apply least privilege where possible, and document exceptions.

## CI/CD rules

- Main branch is the deployment branch.
- Changes impacting deployment must include CI/CD impact notes.
- Keep deployment configuration aligned with the target Google Cloud project bus-track-480813.
