#!/usr/bin/env python3
"""Explicit, project-scoped local memory with provenance.

No content is saved automatically. Writes require ORDINARY_CHAT_MEMORY_ALLOW_WRITE=true.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import pathlib
import re
import sqlite3
import sys
import time
import uuid
from collections.abc import Iterator
from typing import Any


def _chmod_private(path: pathlib.Path, mode: int) -> None:
    try:
        path.chmod(mode)
    except OSError:
        pass


def _state_dir() -> pathlib.Path:
    raw = os.environ.get("ORDINARY_CHAT_STATE_DIR", "~/.ordinary-chat-agent")
    path = pathlib.Path(raw).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    _chmod_private(path, 0o700)
    return path


def _memory_dir() -> pathlib.Path:
    directory = _state_dir() / "memory"
    directory.mkdir(parents=True, exist_ok=True)
    _chmod_private(directory, 0o700)
    return directory


def _allowed_roots() -> list[pathlib.Path]:
    roots: list[pathlib.Path] = []
    seen: set[pathlib.Path] = set()
    for item in os.environ.get("ORDINARY_CHAT_ALLOWED_ROOTS", "").split(os.pathsep):
        if not item.strip():
            continue
        root = pathlib.Path(item).expanduser().resolve()
        if root not in seen:
            roots.append(root)
            seen.add(root)
    return roots


def _workspace(value: str) -> pathlib.Path:
    path = pathlib.Path(value).expanduser().resolve()
    if not path.is_dir():
        raise ValueError("workspace_missing")
    for root in _allowed_roots():
        try:
            path.relative_to(root)
            return path
        except ValueError:
            continue
    raise ValueError("workspace_not_allowlisted")


def _db_path(workspace: pathlib.Path) -> pathlib.Path:
    key = hashlib.sha256(str(workspace).encode("utf-8")).hexdigest()[:24]
    return _memory_dir() / f"{key}.sqlite3"


def _harden_db_files(db_path: pathlib.Path) -> None:
    for candidate in (db_path, pathlib.Path(str(db_path) + "-wal"), pathlib.Path(str(db_path) + "-shm")):
        if candidate.exists():
            _chmod_private(candidate, 0o600)


def _ephemeral_ttl_seconds() -> int:
    try:
        value = int(os.environ.get("ORDINARY_CHAT_MEMORY_EPHEMERAL_TTL_SECONDS", "86400"))
    except ValueError:
        value = 86400
    return min(max(value, 60), 604800)


def _purge_expired(db: sqlite3.Connection) -> int:
    cutoff = int(time.time()) - _ephemeral_ttl_seconds()
    cursor = db.execute(
        "DELETE FROM memory_items WHERE retention = 'ephemeral' AND created_at < ?",
        (cutoff,),
    )
    return max(cursor.rowcount, 0)


@contextlib.contextmanager
def _database(workspace: pathlib.Path) -> Iterator[sqlite3.Connection]:
    db_path = _db_path(workspace)
    db = sqlite3.connect(db_path, timeout=5.0)
    db.row_factory = sqlite3.Row
    try:
        db.execute("PRAGMA busy_timeout=5000")
        db.execute("PRAGMA journal_mode=WAL")
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_items (
                id TEXT PRIMARY KEY,
                created_at INTEGER NOT NULL,
                updated_at INTEGER NOT NULL,
                content TEXT NOT NULL,
                source TEXT NOT NULL,
                confidence REAL NOT NULL,
                retention TEXT NOT NULL,
                tags_json TEXT NOT NULL
            )
            """
        )
        db.execute("CREATE INDEX IF NOT EXISTS memory_updated_idx ON memory_items(updated_at DESC)")
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        _harden_db_files(db_path)


def _write_enabled() -> bool:
    return os.environ.get("ORDINARY_CHAT_MEMORY_ALLOW_WRITE") == "true"


def _normalize_tags(tags: list[str]) -> tuple[list[str], str | None]:
    if len(tags) > 30:
        return [], "too_many_tags"
    normalized: list[str] = []
    for tag in tags:
        value = tag.strip()
        if not value or len(value) > 100 or "\x00" in value:
            return [], "tag_invalid"
        if value not in normalized:
            normalized.append(value)
    return normalized, None


def _escape_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def add(workspace: str, content: str, source: str, confidence: float, retention: str, tags: list[str]) -> dict[str, Any]:
    if not _write_enabled():
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "memory_write_disabled"}
    try:
        root = _workspace(workspace)
    except ValueError as exc:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": str(exc)}
    text = content.strip()
    source_text = source.strip()
    if not text:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "content_empty"}
    if len(text) > 20000:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "content_too_large"}
    if not source_text:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "source_empty"}
    if len(source_text) > 2000 or "\x00" in source_text:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "source_invalid"}
    if not (0 <= confidence <= 1):
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "confidence_out_of_range"}
    if retention not in {"ephemeral", "project", "durable"}:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "retention_invalid"}
    normalized_tags, tag_error = _normalize_tags(tags)
    if tag_error:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": tag_error}

    item_id = uuid.uuid4().hex
    now = int(time.time())
    try:
        with _database(root) as db:
            purged = _purge_expired(db)
            db.execute(
                "INSERT INTO memory_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    item_id,
                    now,
                    now,
                    text,
                    source_text,
                    confidence,
                    retention,
                    json.dumps(normalized_tags, ensure_ascii=False),
                ),
            )
    except sqlite3.Error as exc:
        return {"schemaVersion": 1, "result": "FAIL", "reason": f"sqlite_error:{type(exc).__name__}"}
    return {
        "schemaVersion": 1,
        "id": item_id,
        "workspace_sha256": hashlib.sha256(str(root).encode()).hexdigest(),
        "purged_expired": purged,
        "result": "PASS",
    }


def search(workspace: str, query: str, limit: int) -> dict[str, Any]:
    try:
        root = _workspace(workspace)
    except ValueError as exc:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": str(exc), "items": []}
    if not (1 <= limit <= 50):
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "limit_out_of_range", "items": []}
    query_text = query.strip()
    if len(query_text) > 2000 or "\x00" in query_text:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "query_invalid", "items": []}
    db_path = _db_path(root)
    if not db_path.exists():
        return {"schemaVersion": 1, "result": "PASS", "items": [], "purged_expired": 0}
    needle = f"%{_escape_like(query_text)}%"
    try:
        with _database(root) as db:
            purged = _purge_expired(db)
            rows = db.execute(
                """
                SELECT id, created_at, updated_at, content, source, confidence, retention, tags_json
                FROM memory_items
                WHERE content LIKE ? ESCAPE '\\'
                   OR source LIKE ? ESCAPE '\\'
                   OR tags_json LIKE ? ESCAPE '\\'
                ORDER BY updated_at DESC, id ASC
                LIMIT ?
                """,
                (needle, needle, needle, limit),
            ).fetchall()
    except sqlite3.Error as exc:
        return {"schemaVersion": 1, "result": "FAIL", "reason": f"sqlite_error:{type(exc).__name__}", "items": []}

    items = []
    warnings: list[str] = []
    for row in rows:
        try:
            parsed_tags = json.loads(row["tags_json"])
            tags = parsed_tags if isinstance(parsed_tags, list) else []
            if not isinstance(parsed_tags, list):
                warnings.append(f"tags_not_array:{row['id']}")
        except json.JSONDecodeError:
            tags = []
            warnings.append(f"tags_invalid_json:{row['id']}")
        items.append(
            {
                "id": row["id"],
                "created_at": row["created_at"],
                "updated_at": row["updated_at"],
                "content": row["content"],
                "source": row["source"],
                "confidence": row["confidence"],
                "retention": row["retention"],
                "tags": tags,
            }
        )
    return {
        "schemaVersion": 1,
        "workspace": str(root),
        "items": items,
        "purged_expired": purged,
        "warnings": warnings,
        "result": "PASS",
    }


def delete(workspace: str, item_id: str) -> dict[str, Any]:
    if not _write_enabled():
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "memory_write_disabled"}
    if not re.fullmatch(r"[0-9a-f]{32}", item_id):
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "id_invalid"}
    try:
        root = _workspace(workspace)
    except ValueError as exc:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": str(exc)}
    db_path = _db_path(root)
    if not db_path.exists():
        return {"schemaVersion": 1, "deleted": False, "result": "PASS"}
    try:
        with _database(root) as db:
            purged = _purge_expired(db)
            cursor = db.execute("DELETE FROM memory_items WHERE id = ?", (item_id,))
            deleted = cursor.rowcount == 1
    except sqlite3.Error as exc:
        return {"schemaVersion": 1, "result": "FAIL", "reason": f"sqlite_error:{type(exc).__name__}"}
    return {"schemaVersion": 1, "deleted": deleted, "purged_expired": purged, "result": "PASS"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    add_p = sub.add_parser("add")
    add_p.add_argument("--workspace", required=True)
    add_p.add_argument("--source", required=True)
    add_p.add_argument("--confidence", type=float, default=1.0)
    add_p.add_argument("--retention", choices=["ephemeral", "project", "durable"], default="project")
    add_p.add_argument("--tag", action="append", default=[])
    search_p = sub.add_parser("search")
    search_p.add_argument("--workspace", required=True)
    search_p.add_argument("--query", required=True)
    search_p.add_argument("--limit", type=int, default=10)
    delete_p = sub.add_parser("delete")
    delete_p.add_argument("--workspace", required=True)
    delete_p.add_argument("--id", required=True)
    args = parser.parse_args(argv)
    if args.command == "add":
        result = add(args.workspace, sys.stdin.read(), args.source, args.confidence, args.retention, args.tag)
    elif args.command == "search":
        result = search(args.workspace, args.query, args.limit)
    else:
        result = delete(args.workspace, args.id)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result.get("result") == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
