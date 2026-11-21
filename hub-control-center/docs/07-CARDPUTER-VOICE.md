# Cardputer voice control — architecture

## Goal

Use the M5Stack Cardputer ADV as a physical push-to-talk voice terminal for FREEzzz HUB. The Cardputer is an input device, not the server and not a trusted administrator.

## Data flow

```text
Cardputer ADV microphone + PTT
  -> local Wi-Fi
  -> authenticated HUB voice endpoint
  -> speech-to-text adapter (local engine preferred)
  -> intent parser
  -> allowlisted command router
  -> service adapters (Home Assistant / MQTT / approved HUB actions)
  -> result returned to Cardputer display / speaker
```

## Modes

1. **Offline mode:** only if a local speech engine is installed and configured. No cloud API is required at runtime.
2. **Command mode:** Cardputer sends a compact, explicitly recognized command/intent over local Wi-Fi; suitable for a small fixed vocabulary.
3. **Optional online mode:** a provider can be configured later, but it must never be required for core operation.

The exact Cardputer audio transport and recognition approach must be validated against the installed firmware and available memory before implementation. Do not assume continuous audio streaming is reliable on the device.

## Safety model

- Push-to-talk; no always-on microphone.
- Device identity and per-device token.
- Local network only by default.
- Strict allowlist of intents; never execute arbitrary shell text.
- Read-only queries can execute immediately.
- Device controls require explicit target resolution.
- Destructive actions (delete, reboot, stop critical services, unlock doors) require confirmation on the Cardputer and/or trusted UI.
- Every accepted/rejected command is written to the local audit log.
- Voice commands cannot change security settings, credentials, firewall rules, or user permissions.

## Initial command vocabulary

- "Статус сервера" — report CPU/RAM/disk and service state.
- "Статус Docker" — list container states.
- "Включи свет [комната]" / "Выключи свет [комната]" — only after Home Assistant/MQTT device discovery.
- "Громкость [значение]" — only after audio endpoint discovery.
- "Отмена" — cancel current interaction.

## UI requirements

AI Center / Voice panel will show:
- Cardputer connection and last-seen timestamp.
- Microphone/PTT state (never silently listening).
- Recognition engine and offline/online state.
- Last recognized phrase and parsed intent.
- Command result and audit history.
- Device pairing/revocation.

## Implementation sequence

1. Discover Cardputer model/firmware, Wi-Fi transport and microphone capabilities.
2. Implement authenticated pairing and a harmless status command.
3. Add local STT only after measuring CPU/RAM usage on the HP EliteDesk.
4. Integrate Home Assistant/MQTT after confirming the existing service state.
5. Add the allowlisted device-control intents and confirmation UX.

No voice control endpoint is exposed in the current MVP. This document defines the approved design boundary, not a claim that voice control is already working.
