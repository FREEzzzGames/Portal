# 01 — Product and System Architecture

**Product:** FREEzzz HUB Control Center  
**Document type:** system requirements and architecture  
**Version:** 1.0  
**Status:** baseline for implementation

## 1. Purpose

Provide one private, self-hosted control surface for inspecting and administering the FREEzzz server from the host itself or an authorized phone/computer on the local network.

The application consolidates host monitoring, container operations, system services, network visibility, development environments, smart-home integrations and local AI runtime status. It must remain useful without public internet access.

This application is not the Telegram Mini App and is not a replacement for FREEzzz Portal. It is a separate administrative application.

## 2. Product goals

1. Show the actual state of the host and infrastructure, not static/demo values.
2. Make common monitoring and service operations usable from a phone.
3. Keep the control plane independent from Docker and the services it manages.
4. Work without public internet after installation.
5. Discover installed tools and services without silently installing or reconfiguring them.
6. Provide a stable API so new modules can be added without rewriting the core.
7. Preserve operational safety: no broad root access and no arbitrary command execution.

## 3. Non-goals

- Replacing Ubuntu, Docker Compose, systemd or existing service-specific administration tools.
- Becoming a public multi-tenant SaaS.
- Exposing management endpoints to the public internet.
- Automatically installing every optional subsystem.
- Acting as a general-purpose remote shell.
- Modifying production containers during initial discovery.
- Requiring a cloud AI provider for core operation.

## 4. Operating environment

Known host details are recorded in document 06. They are historical observations and must be revalidated before deployment.

Primary target:
- Ubuntu Desktop on HP EliteDesk.
- x86-64 Linux.
- 16 GB RAM reported previously.
- LAN access and Tailscale access.
- Android phone browser as a primary remote client.

The exact CPU model, storage layout, available disk space, Ubuntu release, Docker version and installed runtimes must be read from the live host before selecting pinned dependencies or resource limits.

## 5. System context

```text
Phone / Desktop Browser
        |
        | HTTPS where configured; otherwise trusted local-network HTTP
        v
FREEzzz HUB Frontend
        |
        | versioned HTTP API + WebSocket
        v
FREEzzz HUB Backend (systemd)
        |
        +-- Host telemetry adapter
        +-- Docker adapter
        +-- systemd adapter
        +-- Network adapter
        +-- Storage adapter
        +-- Project/toolchain discovery
        +-- Smart-home adapters
        +-- AI runtime adapters
        +-- SQLite / audit log
```

The backend is the only component allowed to communicate with host management interfaces. The frontend receives normalized, permission-filtered data.

## 6. Architectural boundaries

### 6.1 Frontend

Responsibilities:
- Render dashboards, lists, detail views and action confirmations.
- Display loading, stale, unavailable and error states.
- Call only documented API endpoints.
- Reconnect to the event stream with bounded backoff.
- Never store API secrets.
- Never access Docker socket, host files or privileged host interfaces.

### 6.2 Backend

Responsibilities:
- Collect and normalize host and service telemetry.
- Enforce authentication, authorization, validation and rate limits.
- Expose versioned API contracts.
- Run only predefined, allow-listed operations.
- Record administrative actions and their outcomes.
- Isolate optional adapters so an unavailable integration cannot take down the core API.

### 6.3 Adapters

Each integration implements a common lifecycle:
- `detect()`: determine whether the integration exists.
- `health()`: return current health and observation timestamp.
- `read()`: return normalized read-only data.
- `execute()`: optional, allow-listed operations only.

An unavailable adapter returns `unavailable` with a reason. It must not crash the dashboard.

### 6.4 Persistence

SQLite stores application-specific state only:
- user/session metadata as required by the selected authentication design;
- dashboard preferences;
- service display configuration;
- audit events;
- job metadata;
- backup metadata.

Do not duplicate entire Docker or service databases. Do not store raw API keys in SQLite unless encrypted with a separately managed key; prefer root/service-readable secret files outside the repository.

## 7. Functional modules

### HOME
- Host online state and observation timestamp.
- CPU usage and load average.
- RAM and swap used/total.
- Filesystem usage by mount point.
- Uptime.
- Network interfaces and connectivity state.
- Docker daemon state.
- Summary of configured services and health checks.
- Recent warnings and administrative events.

### SERVICES
- Docker container inventory.
- Container state, image, uptime, health, exposed/bound ports.
- Start, stop and restart for explicitly supported containers.
- Container logs with bounded time/line limits.
- systemd service inventory and status.
- Service-specific health checks.
- No volume deletion or container removal in the initial release.

### SYSTEM
- OS and kernel information.
- CPU, memory, disks and filesystems.
- Network interfaces, routes and listening sockets (read-only).
- Tailscale presence and state when its local CLI/API is available.
- Storage and backup status.
- Application diagnostics.

### DEVELOPMENT
- Git repository discovery from configured roots.
- Toolchain detection: Git, Python, Node/npm, GCC/G++, CMake, Java, Android SDK, PlatformIO, Arduino CLI and ESP-IDF when present.
- Project inventory and build configuration inspection.
- Build jobs only through reviewed project profiles.
- Build artifacts and logs.
- No free-form shell command execution from the browser.

### SMART HOME
Optional adapters for Home Assistant, MQTT/Mosquitto, ESPHome and future ESP32/M5Stack devices.
- Show detected integrations and their health.
- MQTT topic monitoring must be opt-in and bounded.
- Device control is added only after the physical devices and access model are confirmed.
- The absence of hardware must not affect core startup.

### AI CENTER
- Detect local model runtimes such as Ollama if installed.
- Show provider connectivity and configured model inventory.
- Remote API providers are optional and clearly marked as internet-dependent.
- Secrets remain server-side.
- Agent orchestration is a later phase; initial release is status and configuration visibility only.

### SETTINGS
- Application identity and version.
- Access policy and trusted network configuration.
- Module enable/disable configuration.
- Polling intervals.
- Backup/restore controls.
- Diagnostics and audit history.
- No UI option may weaken host firewall or expose management ports without explicit confirmation.

## 8. Availability and state model

All health states must include observation time and source.

Canonical states:
- `online`
- `healthy`
- `degraded`
- `starting`
- `stopping`
- `offline`
- `unavailable`
- `unknown`
- `error`

Do not infer health from a container existing or a process running alone. Use service-specific checks where possible. Distinguish “process running” from “service responding”.

## 9. Offline-first requirements

The following must work with the public internet disconnected:
- UI loading and navigation.
- Host monitoring.
- Local API and database.
- Docker and systemd status, if local daemons are available.
- Local logs and project discovery.
- Local builds using already installed dependencies.
- Local backup and restore.
- Local model runtime status.

The following may become unavailable:
- Remote AI APIs.
- Package downloads and updates.
- Remote Git operations.
- Tailscale connectivity if its coordination/network path is unavailable.

All UI assets, fonts and scripts are bundled locally. No required external DNS, CDN, telemetry or cloud login.

## 10. Performance and resource policy

The machine is a small home server, so the control plane must remain lightweight:
- Avoid heavyweight frontend frameworks unless justified by implementation needs.
- Do not poll every metric at sub-second intervals.
- Default host metric refresh: 3–5 seconds, configurable.
- Default service health refresh: 10–30 seconds, configurable.
- Docker logs are fetched on demand, not continuously.
- Bound response sizes and history retention.
- Avoid persistent high-frequency CPU or disk sampling.
- Establish real memory/CPU budgets after measuring the host baseline.

## 11. Deployment model

Preferred deployment:
- Frontend built to static files.
- Backend runs as a dedicated unprivileged systemd service.
- Backend binds to loopback by default.
- Reverse proxy or controlled bind configuration provides LAN/Tailscale access.
- Docker integration is optional and must not be required for HUB startup.

Do not use Docker Compose to host the control plane in the first deployment if that would make the control plane unavailable when Docker fails.

## 12. Configuration and data paths

Proposed paths (final ownership and permissions are set during deployment):
- Source: `/srv/freezzz/hub-control-center`
- Runtime configuration: `/etc/freezzz-hub/`
- Persistent state: `/var/lib/freezzz-hub/`
- Logs: journald, with optional bounded application log files.
- Backups: a dedicated path outside the Git working tree.

The service account must have only the read permissions and narrowly scoped operational permissions required by enabled adapters.

## 13. Extension rules

- Each module has an explicit capability declaration.
- Optional integrations are loaded independently.
- API response schemas are versioned.
- Configuration is validated at startup.
- A module failure is isolated and visible.
- New privileged actions require a threat review and tests.
