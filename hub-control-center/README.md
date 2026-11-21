# FREEzzz HUB Control Center

Standalone, local-first control panel for the FREEzzz home server.

## Project status

Initial workspace. The existing production portal and its containers are not modified by this project.

## Design constraints

- Offline-first: the UI and backend must work without public internet access.
- Local deployment on Ubuntu; browser access from localhost, LAN and Tailscale.
- Mobile-first responsive interface, including portrait phone layouts.
- No CDN, remote fonts, cloud authentication or required hosted APIs.
- The control panel must start independently of Docker so it remains available when Docker is unavailable.
- Read-only discovery by default. Any system-changing action must be explicit, validated, allow-listed and logged.
- Never expose the Docker socket directly to the browser.
- Do not require adding the Linux user `monk` to the `docker` group.
- Secrets and runtime data must stay outside source control.

## Planned architecture

```text
Browser (local static UI)
        |
     HTTP / WS
        |
Python API service
        |
  adapters / allow-listed actions
        |
Ubuntu / Docker / network / local services
```

## Planned stack

- Frontend: HTML, CSS, TypeScript, Vite.
- Backend: Python, FastAPI, Uvicorn.
- Host metrics: psutil and read-only Linux interfaces.
- Container integration: Docker API through a restricted backend adapter.
- Local state: SQLite.
- Runtime: systemd service, independent of Docker.

Exact versions and installed dependencies will be selected after inspecting the server inventory and the supplied source archive.

## Planned modules

1. HOME — host health, CPU, memory, swap, disk, uptime and service overview.
2. SERVICES — Docker containers, systemd services, health checks and logs.
3. SYSTEM — host, network, storage, security and backup information.
4. DEVELOPMENT — detected repositories, toolchains and controlled build jobs.
5. SMART HOME — Home Assistant, MQTT and device integrations when available.
6. AI CENTER — local model runtimes and optional remote providers.

## Repository layout

```text
hub-control-center/
  frontend/
  backend/
  config/
  docs/
  scripts/
  tests/
  README.md
```

## Development workflow

Changes are developed on the `hub-control-center` branch. The running server is not changed until a release is reviewed, backed up, deployed and verified.

## Next step

Inspect the current server archive and map the existing services and deployment constraints before implementing adapters or deployment scripts.
