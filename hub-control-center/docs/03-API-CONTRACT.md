# 03 — Backend API Contract

**API prefix:** `/api/v1`  
**Version:** 1.0 draft contract  
**Status:** implementation target; endpoints are not yet implemented

## 1. General rules

- JSON request and response bodies use UTF-8.
- All timestamps are ISO 8601 UTC strings.
- All endpoints return explicit error objects.
- Responses containing live data include `observed_at`.
- Lists are bounded and paginated where appropriate.
- Unknown fields are ignored only where the schema explicitly permits it.
- No endpoint accepts arbitrary shell commands or arbitrary filesystem paths.
- Mutating endpoints require authentication, authorization, CSRF protection where cookie sessions are used, and audit logging.

Common response envelope for live status:

```json
{
  "data": {},
  "observed_at": "2026-11-21T00:00:00Z",
  "source": "host",
  "stale": false
}
```

Common error shape:

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Docker daemon is not available",
    "request_id": "opaque-request-id"
  }
}
```

## 2. Health and application metadata

### GET `/health`
Liveness check. Does not require Docker or optional integrations.

Example:
```json
{"ok": true, "service": "freezzz-hub-api"}
```

### GET `/ready`
Readiness check for the API process and its required local dependencies. Optional adapters do not make the core API unready.

### GET `/api/v1/meta`
Returns application version, API version, enabled modules and startup time. Never returns secrets or internal environment variables.

## 3. Host telemetry

### GET `/api/v1/system/summary`
Returns normalized overview:
- hostname;
- OS/kernel;
- uptime_seconds;
- cpu_percent;
- load_average;
- memory_total_bytes / memory_used_bytes / memory_percent;
- swap_total_bytes / swap_used_bytes / swap_percent;
- filesystem summary;
- network summary;
- docker daemon state;
- observation timestamp.

### GET `/api/v1/system/cpu`
CPU utilization and load average. CPU temperature/frequency are optional and include a source or unavailable reason.

### GET `/api/v1/system/memory`
RAM and swap values in bytes and percentages.

### GET `/api/v1/system/storage`
Filesystem mounts, capacity, used and available bytes. Sensitive pseudo-filesystems may be filtered.

### GET `/api/v1/system/network`
Interface names, addresses, link state and traffic counters. Do not expose Wi-Fi passwords or private credentials.

### GET `/api/v1/system/ports`
Read-only listening socket summary. Restricted to authorized administrators.

## 4. Docker

### GET `/api/v1/docker/summary`
Docker daemon state and aggregate container counts.

### GET `/api/v1/docker/containers`
Bounded list of containers with:
- id (shortened);
- name;
- image;
- state;
- health;
- started_at / created_at;
- ports;
- CPU and memory when supported;
- compose project and service labels when available.

### GET `/api/v1/docker/containers/{container_id}`
Detailed container information. Validate the identifier against the daemon's current container inventory.

### GET `/api/v1/docker/containers/{container_id}/logs?tail=200`
Read-only logs. Enforce a maximum tail and redact secret-like values.

### POST `/api/v1/docker/containers/{container_id}/actions`
Request:
```json
{"action": "start"}
```
Allowed actions: `start`, `stop`, `restart`.
The backend verifies current state, user permission, configured allow-list and container identity before calling Docker. Return an operation id and final/accepted state. No arbitrary Docker API path is accepted.

No delete, prune, volume mutation or image removal endpoint in release 1.

## 5. systemd services

### GET `/api/v1/services/systemd`
List only selected services or a bounded filtered set.

### GET `/api/v1/services/systemd/{service_name}`
Return status, enabled state, active state and last result.

### POST `/api/v1/services/systemd/{service_name}/actions`
Allowed actions are configured per service. The initial default is read-only; service mutation must be explicitly enabled in server-side policy.

## 6. Infrastructure integrations

### GET `/api/v1/integrations`
Returns detected integrations and their state.

### GET `/api/v1/integrations/{integration_id}/health`
Returns health, check timestamp and a safe diagnostic reason.

Integration identifiers are fixed registry values, not arbitrary URLs.

## 7. Projects and toolchains

### GET `/api/v1/development/toolchains`
Returns detected tool names, versions and executable paths (paths may be hidden from non-admin users).

### GET `/api/v1/development/projects`
Returns repositories found only under configured scan roots.

### GET `/api/v1/development/projects/{project_id}`
Returns project metadata and recognized build profiles.

### POST `/api/v1/development/builds`
Request:
```json
{
  "project_id": "registered-project-id",
  "profile_id": "validated-profile-id"
}
```
The backend resolves the project and command from server-side configuration. The client cannot submit a shell command or arbitrary working directory.

### GET `/api/v1/development/builds/{job_id}`
Returns job state, timestamps and bounded output.

## 8. AI runtime

### GET `/api/v1/ai/runtimes`
Detect local runtimes and safe status.

### GET `/api/v1/ai/models`
Return local model metadata where supported. Do not return API keys.

### GET `/api/v1/ai/providers`
Return provider identifier, provider type, configured state and connectivity state. Secret material is never returned.

## 9. Audit and events

### GET `/api/v1/events?limit=100`
Bounded recent events.

### GET `/api/v1/audit?limit=100`
Administrative action history, restricted to administrators. Do not log secret values or sensitive request bodies.

## 10. Backup

### GET `/api/v1/backups`
List known backup metadata.

### POST `/api/v1/backups`
Create a backup using a fixed server-side backup profile. No client-supplied destination path.

Restore is deliberately excluded from the first API release. It requires a separate design, pre-restore verification and explicit operator confirmation.

## 11. WebSocket

### WS `/ws/v1/events`
Authenticated event stream for:
- host metric updates;
- service state changes;
- job progress;
- warnings.

Requirements:
- bounded event payloads;
- heartbeat/ping;
- reconnect support;
- no secret-bearing events;
- server-side subscription allow-list;
- rate limiting.

The REST API remains authoritative. WebSocket is an optimization, not a required dependency.

## 12. Status semantics

A service response must distinguish:
- `running`: process/container state is running;
- `healthy`: service-specific health check passed;
- `degraded`: service responds but has a warning;
- `unavailable`: adapter or dependency is absent;
- `unknown`: no valid observation;
- `error`: check failed unexpectedly.

Never label a service healthy solely because Docker reports `running`.

## 13. HTTP status policy

- 200: successful read/action completed.
- 202: accepted asynchronous job.
- 400: invalid request.
- 401: unauthenticated.
- 403: authenticated but not permitted.
- 404: resource not found.
- 409: action conflicts with current state.
- 422: schema/validation error.
- 429: rate limit.
- 503: required local dependency unavailable.
- 500: unexpected server error with request id.

## 14. Contract testing

Every endpoint must have:
- schema validation tests;
- authorization tests;
- unavailable-adapter tests;
- error-path tests;
- bounded-response tests;
- secret-redaction tests where applicable.

Mutating endpoints additionally require allow-list tests, audit assertions and invalid-state tests.
