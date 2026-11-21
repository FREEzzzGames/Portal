# 06 — Current Server Baseline

**Version:** 1.0  
**Purpose:** preserve observed facts and separate them from assumptions  
**Important:** this is a record of user-provided terminal output and screenshots from 21 November 2026, not a live connection to the server.

## 1. Existing Portal control panel

The user-provided screenshots show an existing FREEzzz HUB/Portal control interface accessible through a Tailscale hostname.

Observed interface features:
- HOME, SERVICES and SYSTEM bottom navigation.
- Dark mobile-first design with cyan accent.
- Host resource cards for CPU, RAM and disk.
- Infrastructure tiles for Matrix, Tinode, Home Assistant, ESPHome, Kiwix and Element.
- Container cards with RUNNING state and Start/Stop/Restart controls.
- A server status timestamp.

These are observations of the existing interface, not proof that every listed service is currently healthy.

## 2. Existing API and collector observations

Terminal output supplied by the user showed:
- `GET /api/health` returned HTTP 200 and JSON `{"ok": true}`.
- `GET /api/status` returned a JSON snapshot containing system metrics and container records.
- A systemd timer named `freezzz-portal-collector.timer` was loaded, enabled and active at the time of capture.
- The timer triggered `freezzz-portal-collector.service`.
- The existing backend source path was `/srv/freezzz/portal/backend/server.py`.
- The existing collector source path was `/srv/freezzz/portal/backend/collect.sh`.
- The existing frontend paths included `/srv/freezzz/portal/frontend/index.html` and `nginx.conf`.
- The existing Compose file was `/srv/freezzz/portal/compose.yaml`.

The supplied API snapshot displayed 11 container records, including:
- freezzz-portal
- freezzz-portal-api
- freezzz-esphome
- freezzz-element
- freezzz-matrix
- freezzz-matrix-db
- freezzz-kiwix
- freezzz-homeassistant
- freezzz-tinode
- freezzz-tinode-db
- freezzz-mosquitto

At the capture time, the snapshot represented these containers as running. Some records included a “healthy” state string. This historical output must not be treated as a current health check.

## 3. Existing deployment details observed

The displayed Compose configuration included:
- backend container name `freezzz-portal-api`;
- backend image built from `./backend`;
- backend command `python -u server.py`;
- Docker socket mounted at `/var/run/docker.sock`;
- frontend container name `freezzz-portal`;
- frontend image `nginx:alpine`;
- frontend host binding `127.0.0.1:8090:80`;
- shared project network named `portal`.

The existing backend code shown in a screenshot used a Unix HTTP connection to `/var/run/docker.sock` and supported container actions `start`, `stop`, `restart`. It also showed same-origin checks and JSON content-type checks. This is a visual inspection of a partial code listing, not a full source audit.

## 4. Existing host/network observations

Terminal output showed:
- a Tailscale Serve endpoint on port 8443;
- local proxy listeners on loopback ports 8090 and 8080;
- a Docker proxy listener on loopback port 8090;
- Tailscale listener on port 8443;
- local HTTP response from `127.0.0.1:8090` returned HTTP 200 with `Server: nginx/1.31.8`.

The screenshots include a Tailscale device listing and a phone connected directly to the host over the LAN. IP addresses in those screenshots are historical and should not be copied into configuration without rechecking.

## 5. Update archive

A file named `freezzz-portal-update.tar.gz` was transferred from Termux to the server's `/tmp` directory. Its visible contents included:
- `portal/UPDATE-NOTES.txt`
- `portal/backend/Dockerfile`
- `portal/backend/collect.sh`
- `portal/backend/server.py`
- `portal/compose.yaml`
- `portal/data/status.json`
- `portal/frontend/index.html`
- `portal/frontend/nginx.conf`
- backup copies of frontend files.

The update notes described changes to CPU calculation, swap/max temperature collection, snapshot timestamps, HTML escaping and container action applicability. The notes explicitly stated that this was a file update package, not a live deployment, and that existing files should be backed up before replacement.

A later diff command was run against the extracted archive, but the screenshot shows no diff output. This may mean the compared files matched or the diff command did not produce visible output; it is not sufficient to establish equivalence.

## 6. Known paths

Observed:
- Existing application: `/srv/freezzz/portal`
- Existing Compose file: `/srv/freezzz/portal/compose.yaml`
- Existing backend: `/srv/freezzz/portal/backend/server.py`
- Existing collector: `/srv/freezzz/portal/backend/collect.sh`
- Existing frontend: `/srv/freezzz/portal/frontend/`
- Existing timer: `freezzz-portal-collector.timer`

New project:
- Repository: `FREEzzzGames/Portal`
- Branch: `hub-control-center`
- Project subdirectory: `hub-control-center/`
- This new project must remain separate from `/srv/freezzz/portal` until a deliberate migration decision is made.

## 7. Important safety conclusions

1. The existing Portal already provides a useful monitoring/control surface. The new Control Center must first inspect and reuse verified capabilities rather than duplicate them blindly.
2. The current backend has access to the Docker socket. Treat this as a privileged boundary and audit it before expanding functionality.
3. Existing service containers and the collector timer are production infrastructure. Do not stop, recreate or rename them during development.
4. Do not overwrite `/srv/freezzz/portal` with the new project.
5. Do not assume the update archive has been deployed merely because it was transferred or extracted.
6. Do not assume all 11 services are still running now.

## 8. Items requiring live verification

Before implementation or deployment, verify:
- current host identity, OS release, kernel and CPU;
- current RAM, swap and disk layout;
- current Docker and Compose versions;
- current container inventory and health checks;
- current Compose configuration and project labels;
- current systemd timer and service definitions;
- current listening ports and Tailscale Serve configuration;
- current source archive contents and file checksums;
- current user/group permissions;
- whether the transferred source archive is present and complete;
- whether the update archive was ever deployed.

Until this inspection is complete, no package installation, port change, firewall change, permission change or production restart is authorized by this specification.
