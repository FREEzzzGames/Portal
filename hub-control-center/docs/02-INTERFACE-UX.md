# 02 — Interface and UX Specification

**Version:** 1.0  
**Status:** baseline for implementation

## 1. Design direction

Visual language: dark sci-fi / industrial control panel. The interface should feel like a compact server console, not a generic SaaS admin template.

Palette:
- Main background: `#0B0C10`
- Secondary background: `#151820`
- Card surface: `#1B2029`
- Cyan accent: `#66FCF1`
- Green/success: `#00FF66`
- Amber/warning: `#FFB703`
- Red/error: `#D90429`
- Primary text: `#E6EDF3`
- Muted text: `#89939F`

Use restrained glow and gradients. Do not use bright neon as the default text color. Status must also be communicated through labels/icons, not color alone.

Typography:
- UI: system sans-serif stack.
- Technical values: system monospace stack.
- Optional bundled Space Mono for technical labels.
- Fonts must be stored locally; no Google Fonts or remote font requests.

## 2. Navigation model

Primary destinations:
1. HOME
2. SERVICES
3. SYSTEM
4. DEVELOPMENT
5. SMART HOME
6. AI CENTER
7. SETTINGS

Desktop:
- Persistent left navigation rail/sidebar.
- Main content area with a maximum readable width.
- Top bar with product identity, connection state and current page title.

Mobile:
- Compact top identity/status row.
- Bottom navigation for the three most-used destinations: HOME, SERVICES, SYSTEM.
- Secondary destinations reachable through a “More” panel or secondary navigation.
- Fixed bottom navigation must respect Android safe-area insets.
- Content must remain scrollable above the navigation bar.

The navigation must never open a chat or unrelated page by default.

## 3. HOME dashboard

### Header
- FREEzzz HUB wordmark.
- Subtitle: PRIVATE SERVER CONTROL.
- Backend connection indicator: ONLINE / DEGRADED / OFFLINE.
- Last successful refresh timestamp.

### Hero status panel
- Current system state.
- Host name.
- Short operational summary.
- Warning count, if any.

### Resource cards
- CPU load percentage and small history indicator.
- RAM used / total and percentage.
- Disk used / total and percentage.
- Swap used / total.
- Uptime.
- Network throughput (RX/TX) when available.

Cards must display actual values and a timestamp. If a metric cannot be read, show “Unavailable”; never substitute a plausible-looking zero.

### Infrastructure overview
Service tiles for detected/configured integrations, for example:
- Matrix
- Tinode
- Home Assistant
- ESPHome
- MQTT
- Kiwix
- other discovered services

Each tile includes:
- display name;
- purpose;
- health state;
- last check time;
- open-details action.

Only discovered or explicitly configured services are shown. No hard-coded “11/11 active” counter.

### Events
Recent warnings, failed health checks, restarts and administrative actions. Each event has timestamp, severity, source and concise description.

## 4. SERVICES screen

### Container list
Each container card/row shows:
- container name;
- image;
- state and health;
- uptime or last transition;
- mapped ports;
- CPU/RAM when available;
- actions supported for that container.

Mobile cards stack vertically. Desktop may use a table with a detail drawer.

### Actions
- Start
- Stop
- Restart
Actions are shown only when valid for the current state and the current user has permission.

Stop/restart requires a confirmation dialog containing the exact container name and action. Show pending state while the backend executes. Refresh state after completion. If the action fails, display the backend error and retain the previous known state with its timestamp.

No remove-container, prune-image, delete-volume or destructive database actions in the first release.

### Details
- Summary
- Health checks
- Ports
- Recent logs
- Compose project/source metadata when it can be determined safely

Logs must be paginated or bounded. Redact known secret patterns before rendering.

## 5. SYSTEM screen

Sections:
- Host overview
- CPU and memory
- Disks and mounts
- Network interfaces
- Listening ports (read-only)
- systemd services
- Tailscale state
- Application diagnostics

Do not expose sensitive environment variables, private keys, passwords or complete process command lines by default.

## 6. DEVELOPMENT screen

- Repository list with path, branch and dirty/clean status.
- Detected compiler/runtime matrix.
- Project details and build profile.
- Build history and output artifact list.
- Explicit build confirmation with project and profile.
- Progress state and bounded logs.

No generic terminal widget. No arbitrary command field.

## 7. SMART HOME screen

- Integration cards: Home Assistant, MQTT, ESPHome.
- Device list only when a real integration provides it.
- Device controls require a separate capability and confirmation policy.
- MQTT monitor has topic filters and bounded message history.
- Clearly distinguish unavailable hardware from a failed service.

## 8. AI CENTER screen

- Local runtime state.
- Installed model list, if available.
- Provider status.
- Remote provider marked “Internet required”.
- Local provider marked “Local”.
- Secret values never displayed; show configured/not configured only.
- Agent controls are not part of the first implementation milestone.

## 9. SETTINGS screen

- Access status and trusted network configuration.
- Refresh intervals.
- Enabled modules.
- Data retention.
- Backup status and restore workflow.
- Application version and diagnostics.

High-impact settings require explicit confirmation and audit logging.

## 10. Responsive layout

Target widths:
- Wide desktop: 1280 px and above.
- Tablet/small laptop: 768–1279 px.
- Phone: 360–767 px.

Rules:
- No horizontal scrolling at 360 px viewport width.
- Touch targets preferably 44×44 CSS px or larger.
- Numeric cards may use two columns on phone; dense tables become cards.
- Buttons must not be placed so close that Stop and Restart are easy to tap accidentally.
- Long container names and paths wrap or truncate with an accessible full-value view.
- Respect reduced-motion preferences.
- Keyboard focus is visible.
- Color contrast must remain readable in dim environments.

## 11. Loading, error and stale states

Every live panel supports:
- initial loading;
- loaded;
- stale data;
- unavailable source;
- request error;
- reconnecting.

A disconnected WebSocket must not blank the page. The UI retains the last known data with a visible stale timestamp and attempts reconnect with exponential backoff and a maximum delay.

## 12. Accessibility and localization

- Semantic HTML and labelled controls.
- Keyboard navigation for desktop.
- Screen-reader names for icon-only controls.
- Status labels in text.
- Russian default language; German and English localization architecture.
- No text embedded in images.
- Date/time displayed in local browser timezone with unambiguous formatting.

## 13. Visual acceptance checklist

- Matches the dark industrial visual direction.
- Mobile HOME is readable without zooming.
- Bottom navigation does not cover content.
- No external network requests are needed to render the UI.
- All metrics show source timestamps.
- Unavailable data is not represented as zero or green/healthy.
- Every destructive or state-changing action has a clear confirmation and result state.
