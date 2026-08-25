#!/usr/bin/env python3
"""Explicit, project-scoped local memory with provenance.

No content is saved automatically. Writes require ORDINARY_CHAT_MEMORY_ALLOW_WRITE=true.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import sqlite3
import sys
import time
import uuid
from typing import Any


def _state_dir() -> pathlib.Path:
    raw = os.environ.get("ORDINARY_CHAT_STATE_DIR", "~/.ordinary-chat-agent")
    path = pathlib.Path(raw).expanduser().resolve()
    path.mkdir(parents=True, exist_ok=True)
    return path


def _allowed_roots() -> list[pathlib.Path]:
    return [
        pathlib.Path(item).expanduser().resolve()
        for item in os.environ.get("ORDINARY_CHAT_ALLOWED_ROOTS", "").split(os.pathsep)
        if item.strip()
    ]


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
    directory = _state_dir() / "memory"
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{key}.sqlite3"


def _connect(workspace: pathlib.Path) -> sqlite3.Connection:
    db = sqlite3.connect(_db_path(workspace))
    db.row_factory = sqlite3.Row
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
    return db


def _write_enabled() -> bool:
    return os.environ.get("ORDINARY_CHAT_MEMORY_ALLOW_WRITE") == "true"


def add(workspace: str, content: str, source: str, confidence: float, retention: str, tags: list[str]) -> dict[str, Any]:
    if not _write_enabled():
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "memory_write_disabled"}
    try:
        root = _workspace(workspace)
    except ValueError as exc:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": str(exc)}
    text = content.strip()
    if not text:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "content_empty"}
    if len(text) > 20000:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "content_too_large"}
    if not (0 <= confidence <= 1):
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "confidence_out_of_range"}
    if retention not in {"ephemeral", "project", "durable"}:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "retention_invalid"}
    item_id = uuid.uuid4().hex
    now = int(time.time())
    with _connect(root) as db:
        db.execute(
            "INSERT INTO memory_items VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (item_id, now, now, text, source, confidence, retention, json.dumps(sorted(set(tags)), ensure_ascii=False)),
        )
    return {
        "schemaVersion": 1,
        "id": item_id,
        "workspace_sha256": hashlib.sha256(str(root).encode()).hexdigest(),
        "result": "PASS",
    }


def search(workspace: str, query: str, limit: int) -> dict[str, Any]:
    try:
        root = _workspace(workspace)
    except ValueError as exc:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": str(exc), "items": []}
    if not (1 <= limit <= 50):
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "limit_out_of_range", "items": []}
    db_path = _db_path(root)
    if not db_path.exists():
        return {"schemaVersion": 1, "result": "PASS", "items": []}
    needle = f"%{query.strip()}%"
    with _connect(root) as db:
        rows = db.execute(
            """
            SELECT id, created_at, updated_at, content, source, confidence, retention, tags_json
            FROM memory_items
            WHERE content LIKE ? OR source LIKE ? OR tags_json LIKE ?
            ORDER BY updated_at DESC
            LIMIT ?
            """,
            (needle, needle, needle, limit),
        ).fetchall()
    items = []
    for row in rows:
        items.append({
            "id": row["id"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "content": row["content"],
            "source": row["source"],
            "confidence": row["confidence"],
            "retention": row["retention"],
            "tags": json.loads(row["tags_json"]),
        })
    return {"schemaVersion": 1, "workspace": str(root), "items": items, "result": "PASS"}


def delete(workspace: str, item_id: str) -> dict[str, Any]:
    if not _write_enabled():
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": "memory_write_disabled"}
    try:
        root = _workspace(workspace)
    except ValueError as exc:
        return {"schemaVersion": 1, "result": "BLOCKED", "reason": str(exc)}
    with _connect(root) as db:
        cursor = db.execute("DELETE FROM memory_items WHERE id = ?", (item_id,))
    return {"schemaVersion": 1, "deleted": cursor.rowcount == 1, "result": "PASS"}


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
