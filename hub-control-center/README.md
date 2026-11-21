# FREEzzz HUB Control Center

**Project:** local control plane for the FREEzzz home server  
**Status:** specification baseline; implementation not yet started  
**Working branch:** `hub-control-center`

FREEzzz HUB Control Center is a self-hosted, offline-first administration interface for the Ubuntu host and its local infrastructure. It is a separate application from the existing FREEzzz Portal.

## Documentation

1. [Product and system architecture](docs/01-PRODUCT-ARCHITECTURE.md)
2. [Interface and UX specification](docs/02-INTERFACE-UX.md)
3. [Backend API contract](docs/03-API-CONTRACT.md)
4. [Security and operations](docs/04-SECURITY-OPERATIONS.md)
5. [Implementation plan and acceptance tests](docs/05-IMPLEMENTATION-PLAN.md)
6. [Known server baseline](docs/06-CURRENT-BASELINE.md)

## Non-negotiable requirements

- Local-first and offline-first. No required external APIs, CDNs, remote fonts or cloud authentication.
- Runs on Ubuntu and remains available if Docker is stopped.
- Browser access through localhost, LAN and Tailscale, subject to network availability.
- Responsive desktop and mobile layouts; phone portrait mode is a first-class target.
- Read-only discovery by default. Mutating actions are explicit, allow-listed and audited.
- The browser never receives direct access to the Docker socket.
- Do not add Linux user `monk` to the `docker` group without explicit authorization.
- No arbitrary shell endpoint, arbitrary file path endpoint or unrestricted command execution.
- Backups and secrets are never committed to Git.
- Existing production portal and services must not be changed by development or installation scripts.

## Technology direction

- Frontend: TypeScript, Vite, semantic HTML and CSS.
- Backend: Python, FastAPI and Uvicorn.
- Host telemetry: psutil plus read-only Linux interfaces.
- Docker integration: restricted backend adapter.
- Persistent application state: SQLite.
- Runtime: systemd service, independent of Docker.
- Tests: backend tests, frontend typecheck/build, API integration tests and deployment smoke tests.

Exact dependency versions and deployment permissions must be selected after the current host and source code have been inspected.

## Repository layout

```text
hub-control-center/
├── README.md
├── docs/
├── frontend/
├── backend/
├── config/
├── scripts/
└── tests/
```

## Change and release policy

All work is committed to `hub-control-center`. The production system is not updated directly from an unreviewed working tree. A release requires a backup, a reviewed change set, successful tests, controlled deployment and post-deployment verification.

## Current state

The repository contains the project documentation baseline. The documents define the target system; they do not claim that the new application has been implemented. The known state of the existing server is recorded separately in [06-CURRENT-BASELINE.md].
