# Implementation status — 0.1.0

## Implemented in GitHub

- FastAPI backend with health, host telemetry, Docker inventory and combined overview endpoints.
- Responsive Russian-language interface with desktop sidebar and Android bottom navigation.
- Live CPU, RAM, swap, root filesystem, uptime, host, kernel and load-average data.
- Read-only Docker container inventory over the Unix socket. Missing socket, daemon errors and permission denial are represented as unavailable.
- Five-second refresh, timestamps, loading/error states and HTML escaping for container metadata.
- Local development runner and a systemd unit template.

## Not enabled in this milestone

- Container start/stop/restart actions.
- Remote/LAN binding, authentication and TLS deployment.
- systemd service mutations, firewall changes or privileged helper.
- Project scanning, build execution, smart-home device control and AI agent execution.

These require host baseline verification and a reviewed security design. The service unit is a template, not an install script. Do not install it without creating and reviewing the dedicated service account, paths and Docker access model. Do not add user `monk` to the `docker` group as a shortcut.

## Local development

From the repository checkout:

```bash
cd hub-control-center
bash scripts/run-dev.sh
```

Open `http://127.0.0.1:8787`. The first run installs the pinned Python dependencies and therefore needs internet access or a pre-populated package cache. Once installed, application runtime is local and does not require public internet.

## API

- `GET /api/v1/health`
- `GET /api/v1/system`
- `GET /api/v1/containers`
- `GET /api/v1/overview`

The backend binds to loopback by default. Docker inventory requires the backend process to have read access to the Docker socket; if it does not, the UI reports Docker as unavailable. No Docker permission changes are performed automatically.

## Verification status

Source files are committed to branch `hub-control-center`. Runtime tests, dependency installation and deployment have not yet been run on the user's Ubuntu host. This is an implementation preview, not a production deployment.


## Additional engineering work

- Added automated backend API smoke tests under `app/tests/`.
- Added GitHub Actions workflow for Python compilation and API tests on branch updates.
- Added the Cardputer ADV push-to-talk voice-control architecture, including offline-first speech recognition, device pairing, allowlisted intents and confirmation requirements.
- Voice control is specified but not implemented; Cardputer hardware/firmware transport must be verified before coding the device integration.
