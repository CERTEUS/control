#!/usr/bin/env python3
from __future__ import annotations

# Thin compatibility shim so that `from security.ra import ...` works
# by delegating to the implementation under `certeus.security.ra`.

from certeus.security.ra import (  # type: ignore
    RAFingerprint,
    extract_fingerprint,
    parse_attestation_json,
    verify_fingerprint,
)

__all__ = [
    "RAFingerprint",
    "extract_fingerprint",
    "parse_attestation_json",
    "verify_fingerprint",
]

