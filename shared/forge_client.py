"""HTTP client so Oracle, Akasha, and Insight can persist results on Forge."""

from __future__ import annotations

import os
from typing import Any, Optional

import requests

FORGE_BASE_URL = os.getenv("FORGE_BASE_URL", "http://localhost:5000").rstrip("/")


class ForgeClientError(RuntimeError):
    pass


def _headers(service_key: Optional[str]) -> dict[str, str]:
    headers = {"Content-Type": "application/json"}
    if service_key:
        headers["X-Service-Key"] = service_key
    return headers


def forge_enabled() -> bool:
    return os.getenv("FORGE_ENABLED", "true").lower() not in {"0", "false", "no"}


def post_json(path: str, payload: dict[str, Any], service_key: Optional[str]) -> Optional[dict[str, Any]]:
    if not forge_enabled():
        return None
    url = f"{FORGE_BASE_URL}{path}"
    try:
        response = requests.post(url, json=payload, headers=_headers(service_key), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise ForgeClientError(f"Forge POST {path} failed: {exc}") from exc


def get_json(path: str, service_key: Optional[str] = None, params: Optional[dict[str, Any]] = None) -> Optional[dict[str, Any]]:
    if not forge_enabled():
        return None
    url = f"{FORGE_BASE_URL}{path}"
    try:
        response = requests.get(url, params=params, headers=_headers(service_key), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise ForgeClientError(f"Forge GET {path} failed: {exc}") from exc


def submit_disease_prediction(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return post_json("/api/disease/predict-result", payload, os.getenv("ORACLE_SERVICE_KEY"))


def submit_advisory(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return post_json("/api/advisory", payload, os.getenv("ADVISORY_SERVICE_KEY"))


def submit_market_snapshot(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return post_json("/api/market", payload, os.getenv("INSIGHT_SERVICE_KEY"))


def submit_logistics(payload: dict[str, Any]) -> Optional[dict[str, Any]]:
    return post_json("/api/transaction/logistics", payload, os.getenv("INSIGHT_SERVICE_KEY"))
