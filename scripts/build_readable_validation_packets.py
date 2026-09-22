#!/usr/bin/env python3
"""Build derived human-readable CliniProof validation packets from frozen JSON."""

from __future__ import annotations

from app.services.readable_packets import main

if __name__ == "__main__":
    raise SystemExit(main())
