# FREEzzz HUB Control Center

**Project:** local control plane for the FREEzzz home server  
**Status:** MVP source committed; host deployment and runtime verification pending  
**Working branch:** `hub-control-center`

FREEzzz HUB Control Center is a separate, self-hosted, offline-first administration interface for the Ubuntu host and its local infrastructure. It is not the existing FREEzzz Portal and does not replace it.

## Current MVP

- Responsive dark industrial dashboard (Russian UI; desktop and Android portrait layouts).
- Live host telemetry: CPU, RAM, swap, root filesystem, uptime, kernel and load average.
- Read-only Docker container inventory through the backend Unix-socket adapter.
- FastAPI backend with versioned API endpoints.
- Local static frontend; no CDN, remote fonts, analytics or cloud authentication.
- Loopback-only backend binding by default.
- Docker absence or permission errors are shown as unavailable; no automatic permission changes.

## Documentation

1. [Product and system architecture](docs/01-PRODUCT-ARCHITECTURE.md)
2. [Interface and UX specification](docs/02-INTERFACE-UX.md)
3. [Backend API contract](docs/03-API-CONTRACT.md)
4. [Security and operations](docs/04-SECURITY-OPERATIONS.md)
5. [Implementation plan and acceptance tests](docs/05-IMPLEMENTATION-PLAN.md)
6. [Known server baseline](docs/06-CURRENT-BASELINE.md)
7. [Implementation status and run instructions](IMPLEMENTATION-STATUS.md)

## Run locally

From the repository root:

```bash
cd hub-control-center
bash scripts/run-dev.sh
```

Then open `http://127.0.0.1:8787`.

The first run creates a Python virtual environment and installs pinned dependencies. It requires internet access or an existing package cache. Once installed, the runtime is local and does not require public internet.

## API

- `GET /api/v1/health`
- `GET /api/v1/system`
- `GET /api/v1/containers`
- `GET /api/v1/overview`

## Security boundaries

- The browser never accesses the Docker socket.
- The backend binds to `127.0.0.1` by default.
- No arbitrary shell or file-path API exists.
- No container mutation endpoints are included in this MVP.
- Do not add Linux user `monk` to the `docker` group without explicit authorization.
- Do not commit secrets, tokens, production environment files or backups.
- Do not change or restart the existing production Portal or its containers during this project.

The systemd unit under `deploy/` is a template only. It must be reviewed and adapted after checking the live host, service account, filesystem paths and Docker access policy.

## Repository layout

```text
hub-control-center/
├── app/                 # FastAPI backend
├── web/                 # Static offline-capable UI
├── deploy/              # systemd unit template
├── scripts/             # local runner
├── docs/                # full technical specification
├── IMPLEMENTATION-STATUS.md
└── README.md
```

## Verification status

The source is committed to GitHub. It has not yet been installed or tested on the user's Ubuntu host. A Git commit is not proof of deployment correctness. The next step is to pull this branch on the server, run the local development instance, verify the API and UI, then decide the safe production deployment model.
