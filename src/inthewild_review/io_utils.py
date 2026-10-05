"""CSV helpers. Research tables are never rewritten inside data/raw."""

from __future__ import annotations

import csv
from pathlib import Path


class RawDataProtectionError(RuntimeError):
    """Raised when a write would touch an immutable bibliographic export."""


def assert_not_raw_write(path: Path, root: Path) -> None:
    raw = (root / "data" / "raw").resolve()
    resolved = path.resolve()
    if resolved == raw or raw in resolved.parents:
        raise RawDataProtectionError(
            f"Refusing to write inside the raw export directory: {resolved}"
        )


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, str]] = []
        for row in reader:
            rows.append({key: (value or "") for key, value in row.items() if key is not None})
        return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str], root: Path) -> None:
    assert_not_raw_write(path, root)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, "") for name in fieldnames})


def read_text_export(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    return raw.decode("latin-1")
