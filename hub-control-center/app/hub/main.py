from __future__ import annotations

import http.client
import json
import os
import platform
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / "web"
APP_VERSION = "0.1.0"
STARTED = time.time()
DOCKER_SOCKET = os.getenv("FREEZZ_HUB_DOCKER_SOCKET", "/var/run/docker.sock")

app = FastAPI(title="FREEzzz HUB Control Center", version=APP_VERSION, docs_url=None, redoc_url=None)


class UnixHTTPConnection(http.client.HTTPConnection):
    def __init__(self, socket_path: str, timeout: float = 2.0):
        super().__init__("localhost", timeout=timeout)
        self.socket_path = socket_path

    def connect(self) -> None:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        sock.connect(self.socket_path)
        self.sock = sock


def docker_get(path: str) -> tuple[int, Any]:
    if not os.path.exists(DOCKER_SOCKET):
        return 503, {"available": False, "reason": "Docker socket not found"}
    try:
        conn = UnixHTTPConnection(DOCKER_SOCKET, timeout=2.5)
        conn.request("GET", path, headers={"Host": "localhost"})
        response = conn.getresponse()
        raw = response.read(2_000_000)
        conn.close()
        if response.status != 200:
            return response.status, {"available": False, "reason": raw[:500].decode("utf-8", "replace")}
        return 200, json.loads(raw.decode("utf-8"))
    except (OSError, TimeoutError, ValueError, http.client.HTTPException) as exc:
        return 503, {"available": False, "reason": str(exc)[:300]}


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def system_snapshot() -> dict[str, Any]:
    vm = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage("/")
    cpu = psutil.cpu_percent(interval=None)
    net = psutil.net_io_counters()
    boot = psutil.boot_time()
    return {
        "observed_at": stamp(),
        "host": socket.gethostname(),
        "platform": platform.platform(),
        "kernel": platform.release(),
        "uptime_seconds": max(0, int(time.time() - boot)),
        "cpu": {"percent": cpu, "logical_cores": psutil.cpu_count(logical=True), "physical_cores": psutil.cpu_count(logical=False)},
        "memory": {"total": vm.total, "used": vm.used, "available": vm.available, "percent": vm.percent},
        "swap": {"total": swap.total, "used": swap.used, "percent": swap.percent},
        "storage": {"root_total": disk.total, "root_used": disk.used, "root_free": disk.free, "root_percent": disk.percent},
        "network": {"bytes_sent": net.bytes_sent, "bytes_recv": net.bytes_recv},
        "load_average": list(os.getloadavg()) if hasattr(os, "getloadavg") else None,
    }


def container_snapshot() -> dict[str, Any]:
    status, payload = docker_get("/containers/json?all=1")
    if status != 200 or not isinstance(payload, list):
        reason = payload.get("reason", "Docker unavailable") if isinstance(payload, dict) else "Docker unavailable"
        return {"available": False, "observed_at": stamp(), "reason": reason, "containers": []}
    items = []
    for item in payload:
        names = item.get("Names") or []
        items.append({
            "id": (item.get("Id") or "")[:12],
            "name": names[0].lstrip("/") if names else "unnamed",
            "image": item.get("Image", "unknown"),
            "state": item.get("State", "unknown"),
            "status": item.get("Status", "unknown"),
            "ports": item.get("Ports") or [],
        })
    return {"available": True, "observed_at": stamp(), "containers": items}


@app.get("/api/v1/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "freezzz-hub", "version": APP_VERSION, "uptime_seconds": int(time.time() - STARTED), "observed_at": stamp()}


@app.get("/api/v1/system")
def system() -> dict[str, Any]:
    try:
        return system_snapshot()
    except Exception as exc:
        return JSONResponse(status_code=503, content={"error": "system_metrics_unavailable", "detail": str(exc)[:200], "observed_at": stamp()})


@app.get("/api/v1/containers")
def containers() -> dict[str, Any]:
    return container_snapshot()


@app.get("/api/v1/overview")
def overview() -> dict[str, Any]:
    return {"system": system_snapshot(), "docker": container_snapshot(), "observed_at": stamp()}


if WEB.exists():
    app.mount("/assets", StaticFiles(directory=WEB / "assets", check_dir=False), name="assets")


@app.get("/")
def index():
    index_file = WEB / "index.html"
    if not index_file.exists():
        return JSONResponse(status_code=503, content={"error": "frontend_not_built"})
    return FileResponse(index_file)


@app.get("/{path:path}")
def spa_fallback(path: str):
    candidate = (WEB / path).resolve()
    if WEB.resolve() not in candidate.parents or not candidate.is_file():
        return FileResponse(WEB / "index.html")
    return FileResponse(candidate)
