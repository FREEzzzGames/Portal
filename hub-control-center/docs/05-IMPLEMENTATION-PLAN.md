# 05 — Implementation Plan and Acceptance Tests

**Version:** 1.0  
**Status:** delivery baseline

## 1. Delivery principle

Deliver complete, testable milestones. Avoid creating isolated screens that cannot be connected to real data. Each milestone must include implementation, tests, documentation and a verified deployment artifact.

No production deployment is performed merely because code has been committed.

## 2. Required pre-implementation inspection

Before coding integrations or installation scripts:
1. Inspect the current FREEzzz Portal source archive.
2. Inspect current Compose files and service definitions.
3. Read the current collector implementation and API.
4. Verify actual Ubuntu release, CPU, RAM, storage and free space.
5. Detect installed Python/Node versions and available system packages.
6. Inspect current listening ports and firewall rules.
7. Confirm the existing service account and permissions.
8. Identify paths and units used by the existing Portal.
9. Confirm whether the source archive is complete and whether it contains secrets; exclude secrets from repository commits.

Discovery is read-only. No install, upgrade, restart or permission change during this phase.

## 3. Milestones

### M0 — Baseline and compatibility
Deliverables:
- inspected host inventory;
- inspected source archive;
- dependency/version matrix;
- port and path map;
- deployment risk register;
- final runtime configuration proposal.

Exit criteria:
- no unknown path collision;
- no conflict with existing Portal;
- all privileged operations identified;
- dependencies selected based on host evidence.

### M1 — Core application
Deliverables:
- backend application;
- static frontend shell;
- health/readiness endpoints;
- configuration validation;
- SQLite initialization;
- structured logging;
- systemd unit template;
- unit and API tests.

Exit criteria:
- starts independently of Docker;
- no external network request required;
- health and readiness behavior tested;
- service runs unprivileged.

### M2 — HOME and host telemetry
Deliverables:
- responsive HOME dashboard;
- CPU, memory, swap, storage, uptime and network metrics;
- timestamps and stale-state handling;
- API and UI tests.

Exit criteria:
- displayed metrics match host commands within reasonable sampling tolerance;
- unavailable metrics are labelled unavailable;
- mobile layout works at 360 px width.

### M3 — SERVICES
Deliverables:
- Docker daemon detection;
- container inventory;
- status and health display;
- bounded log view;
- allow-listed start/stop/restart for configured containers;
- systemd service read-only inventory.

Exit criteria:
- Docker unavailable does not crash HUB;
- actions read back actual state;
- invalid and unauthorized actions are rejected;
- no destructive endpoint exists.

### M4 — SYSTEM and diagnostics
Deliverables:
- host details;
- storage and network views;
- safe listening-port view;
- Tailscale detection where supported;
- diagnostics page.

Exit criteria:
- no credential leakage;
- interfaces and ports are read-only;
- data sources and timestamps are visible.

### M5 — DEVELOPMENT
Deliverables:
- toolchain detection;
- configured repository discovery;
- build profiles;
- job tracking and bounded logs.

Exit criteria:
- no arbitrary shell command input;
- build paths are constrained to configured roots;
- jobs have timeouts and output limits.

### M6 — SMART HOME and AI adapters
Deliverables:
- optional Home Assistant/MQTT/ESPHome adapters;
- optional local AI runtime detection;
- provider status and secret-safe configuration state.

Exit criteria:
- absent hardware/integrations do not affect core service;
- remote providers are clearly internet-dependent;
- local status works offline.

### M7 — Release hardening
Deliverables:
- mobile and accessibility pass;
- security tests;
- backup/restore design and verification;
- systemd autostart;
- offline test;
- upgrade and rollback procedure;
- final operator documentation.

Exit criteria:
- all release acceptance tests pass;
- production deployment is backed up and verified.

## 4. Test strategy

### Unit tests
- metric normalization;
- state mapping;
- config validation;
- identifier validation;
- authorization policy;
- secret redaction;
- adapter failure isolation.

### API tests
- valid and invalid schemas;
- authentication and authorization;
- rate limits;
- unavailable dependencies;
- bounded log and list responses;
- audit events;
- no secret leakage.

### Frontend tests
- loading/empty/error/stale states;
- navigation;
- action confirmation;
- mobile overflow;
- keyboard focus;
- localization key completeness.

### Integration tests
- backend starts with Docker stopped;
- backend reports Docker unavailable safely;
- Docker adapter reads live container inventory when daemon is available;
- action state is read back;
- systemd service status is reported accurately.

## 5. Release acceptance checklist

### Functional
- [ ] HOME metrics are real and timestamped.
- [ ] Container inventory matches Docker.
- [ ] Service health is not inferred solely from process state.
- [ ] Logs are bounded and secrets redacted.
- [ ] Enabled actions work and are verified by read-back.
- [ ] Optional integrations fail independently.

### Offline
- [ ] Disconnect public internet.
- [ ] Open UI from localhost.
- [ ] Open UI from LAN.
- [ ] Core API and dashboard continue.
- [ ] Local monitoring and local management continue.
- [ ] Remote integrations show a clear unavailable state.
- [ ] No external assets or required API calls appear in browser network log.

### Mobile
- [ ] Android portrait at 360 px and common larger widths.
- [ ] No horizontal overflow.
- [ ] Bottom navigation respects safe areas.
- [ ] Confirmations and status messages are readable.
- [ ] Touch targets are practical.

### Security
- [ ] Backend runs unprivileged.
- [ ] No arbitrary shell or arbitrary path API.
- [ ] No Docker socket in frontend.
- [ ] Remote mutations require authentication.
- [ ] Origin/Host and CSRF protections tested.
- [ ] Secrets absent from Git and frontend.
- [ ] Mutations are audited.

### Operations
- [ ] systemd autostart works.
- [ ] HUB survives Docker outage.
- [ ] HUB restarts cleanly.
- [ ] Backup creation and verification work.
- [ ] Upgrade and rollback are documented.
- [ ] Existing Portal remains unchanged.

## 6. Definition of done

A milestone is complete only when:
- code is committed;
- tests have actually run;
- build output is verified;
- relevant documentation is updated;
- limitations are listed;
- no unverified success claim is made.

A GitHub commit alone is not proof of runtime correctness.
