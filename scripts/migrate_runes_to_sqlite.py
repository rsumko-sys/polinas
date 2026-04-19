#!/usr/bin/env python3
"""Migration helper: move `src/data/runes.json` into a simple SQLite DB.

Usage:
  python3 scripts/migrate_runes_to_sqlite.py

This creates `src/data/runes.db` with a `runes` table (id TEXT PRIMARY KEY,
name TEXT, effect TEXT, raw JSON TEXT). Re-running will be idempotent and
will upsert existing rows.
"""
import json
import os
import sqlite3


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "src", "data")
JSON_PATH = os.path.join(DATA_DIR, "runes.json")
DB_PATH = os.path.join(DATA_DIR, "runes.db")


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def migrate(json_path, db_path):
    items = load_json(json_path)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS runes (
            id TEXT PRIMARY KEY,
            name TEXT,
            effect TEXT,
            raw JSON
        )
        """
    )
    for it in items:
        _id = it.get("id")
        name = it.get("name")
        effect = it.get("effect")
        raw = json.dumps(it, ensure_ascii=False)
        cur.execute(
            "INSERT OR REPLACE INTO runes(id,name,effect,raw) VALUES (?,?,?,?)",
            (_id, name, effect, raw),
        )
    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("Migrating runes.json -> runes.db")
    migrate(JSON_PATH, DB_PATH)
    print("Done. DB at:", DB_PATH)
