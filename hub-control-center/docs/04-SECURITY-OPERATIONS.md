# 04 — Security and Operations

**Version:** 1.0  
**Status:** mandatory design constraints

## 1. Threat model

The control panel can inspect and operate a server. A compromise of its web interface or API could affect containers, projects and local services. The system must therefore assume:
- an untrusted device may reach the LAN;
- browser requests can be forged;
- a compromised frontend must not gain host-level privileges;
- Docker socket access is effectively high privilege;
- logs and configuration may contain credentials;
- public internet connectivity may disappear.

The control panel is intended for a private network, not direct public exposure.

## 2. Privilege separation

- Run the backend as a dedicated unprivileged service account.
- Do not run the entire API as root.
- Do not add `monk` to the `docker` group without explicit authorization.
- Do not mount the Docker socket into the frontend or a browser-facing static server.
- Docker access, if enabled, must be isolated behind a restricted adapter and narrowly scoped operational policy.
- If an operation needs elevated privileges, use a small reviewed helper with fixed commands and strict argument validation. Do not use unrestricted sudo.

Docker daemon access is highly privileged even when invoked through a limited-looking API. Treat it as an administrative capability.

## 3. API security

- Authentication required for remote access.
- Bind to loopback by default until remote access is explicitly configured.
- Use HTTPS for browser access over networks where traffic is not otherwise protected.
- If cookie sessions are used: Secure, HttpOnly and appropriate SameSite policy; CSRF protection on state-changing requests.
- Validate Origin/Host and reject unexpected origins.
- Apply request size limits, rate limits and timeouts.
- Use strict CORS allow-lists; never wildcard credentialed origins.
- Use parameterized SQL queries.
- Validate every identifier against a server-side registry or live inventory.
- No arbitrary URLs, commands, file paths or Docker API routes from clients.

## 4. Network exposure

Default:
- Backend listens on `127.0.0.1`.
- No public internet binding.
- LAN/Tailscale exposure is configured deliberately through a reverse proxy or a controlled bind address.
- Firewall rules are reviewed before enabling remote access.
- Do not assume Tailscale connectivity is available when public internet is down.

The application must display which interface/address it is using and whether remote access is enabled.

## 5. Secrets

- Never commit secrets, tokens, private keys, cookies, database dumps or production configuration.
- Keep secrets outside the repository.
- Restrict file permissions to the service account and administrators.
- Do not include secret values in API responses, logs, error messages or browser storage.
- Support secret rotation without rebuilding the frontend.
- Provide only “configured/not configured” status to the UI.

## 6. Docker operation policy

Initial release permits:
- list containers;
- inspect selected safe metadata;
- bounded log retrieval;
- start/stop/restart for configured containers.

Initial release forbids:
- remove container;
- remove image;
- prune;
- delete volume;
- modify networks;
- execute arbitrary command in a container;
- edit Compose files from the UI;
- expose raw Docker API.

For every state-changing action:
1. Authenticate and authorize.
2. Validate the container against the current inventory.
3. Check configured policy and current state.
4. Record an audit event.
5. Execute the single allow-listed action.
6. Read back actual state.
7. Return the verified result or explicit failure.

## 7. Audit

Record:
- timestamp;
- actor/session identifier;
- action;
- target;
- result;
- request id;
- safe error code.

Do not record passwords, tokens, private keys, full secret-bearing request bodies or raw environment variables.

Audit storage must be bounded and included in backup policy.

## 8. Logging and diagnostics

- Prefer journald for service logs.
- Application logs use structured records.
- Bound log retrieval and retention.
- Redact common token/password patterns.
- Return request ids to users for troubleshooting.
- Do not expose stack traces to remote clients in production.

## 9. Backup and recovery

Backup profiles must define exactly which application data is included:
- HUB configuration excluding secrets unless encrypted;
- SQLite state;
- audit database;
- user-selected project configuration if explicitly requested.

Do not automatically back up container volumes or databases managed by other applications. Those require service-specific backup procedures.

A backup must:
- include timestamp and manifest;
- be written outside the source repository;
- be verified after creation;
- have documented retention;
- never overwrite the only known-good backup.

Restore must be a separate, deliberate workflow with integrity checks and pre-restore backup.

## 10. Installation and upgrade policy

- Do not run a destructive setup script.
- Never wipe an existing directory as an installation shortcut.
- Never overwrite the production Portal.
- Installation must detect existing paths and stop on conflicts.
- Back up changed files before replacement.
- Use a versioned release or commit SHA.
- Validate configuration before restart.
- Restart only the HUB service, not all Docker containers.
- Verify health endpoint and UI after deployment.
- Roll back if health checks fail.

## 11. Offline behavior

- Core UI and API continue without public internet.
- Remote AI providers and remote Git/package operations are marked unavailable, not treated as core failures.
- Local authentication and local state remain available.
- No telemetry or analytics calls to external services.

## 12. Operational runbook

### Check HUB process
`systemctl status freezzz-hub`

### Read HUB logs
`journalctl -u freezzz-hub -n 200 --no-pager`

### Check API liveness
`curl -fsS http://127.0.0.1:<configured-port>/health`

### Check readiness
`curl -fsS http://127.0.0.1:<configured-port>/ready`

The actual port is selected during deployment and documented in the installed configuration. Do not assume a port before inspecting current listeners.

### Safe restart
`sudo systemctl restart freezzz-hub`

Only run after the unit exists and a deployment has been approved.

### Failure handling
1. Capture service status and recent logs.
2. Check configuration validation.
3. Check disk space and permissions.
4. Check only the dependency implicated by the error.
5. Roll back the last HUB release if necessary.
6. Do not restart unrelated production services as a generic troubleshooting step.

## 13. Security acceptance

- No secret in Git history or frontend bundle.
- No arbitrary command endpoint.
- No Docker socket exposed to browser.
- No unauthenticated remote mutation.
- Origin/Host validation tested.
- CSRF protection tested where applicable.
- Read-only mode works without Docker access.
- Audit records every enabled mutation.
- Application remains available when Docker is stopped.
