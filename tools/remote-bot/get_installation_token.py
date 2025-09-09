#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import time
from pathlib import Path
from typing import Any

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def b64u(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def load_env_from_file(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.strip().startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip()
    return out


def make_jwt(app_id: str, pem_path: Path) -> str:
    now = int(time.time())
    header = {"alg": "RS256", "typ": "JWT"}
    payload: dict[str, Any] = {"iat": now - 60, "exp": now + 540, "iss": int(app_id) if app_id.isdigit() else app_id}
    h = b64u(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    p = b64u(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{h}.{p}".encode("ascii")
    sk = serialization.load_pem_private_key(pem_path.read_bytes(), password=None)
    sig = sk.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    return f"{h}.{p}.{b64u(sig)}"


def main() -> int:
    root = Path.cwd()
    env = load_env_from_file(root / ".env")
    app_id = os.getenv("GH_APP_ID") or env.get("GH_APP_ID")
    inst_id = os.getenv("GH_APP_INSTALLATION_ID") or env.get("GH_APP_INSTALLATION_ID")
    pem_path = os.getenv("GH_APP_PRIVATE_KEY_PATH") or env.get("GH_APP_PRIVATE_KEY_PATH")
    if not app_id or not inst_id or not pem_path:
        raise SystemExit("Missing GH_APP_ID/GH_APP_INSTALLATION_ID/GH_APP_PRIVATE_KEY_PATH")
    jwt = make_jwt(str(app_id), Path(pem_path))
    r = requests.post(
        f"https://api.github.com/app/installations/{inst_id}/access_tokens",
        headers={"Authorization": f"Bearer {jwt}", "Accept": "application/vnd.github+json"},
        timeout=20,
    )
    r.raise_for_status()
    print(r.json()["token"])  # stdout only token
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

