import sqlite3
from datetime import date, timedelta
from pathlib import Path

DEFAULT_DB = Path.home() / ".habitlog" / "habits.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS habits (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS checkins (
    id INTEGER PRIMARY KEY,
    habit_id INTEGER NOT NULL REFERENCES habits(id),
    day TEXT NOT NULL,
    UNIQUE (habit_id, day)
);
"""


def connect(path=DEFAULT_DB):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def add_habit(conn, name):
    with conn:
        conn.execute("INSERT INTO habits (name) VALUES (?)", (name,))


def list_habits(conn):
    return [r[0] for r in conn.execute("SELECT name FROM habits ORDER BY name")]


def _habit_id(conn, name):
    row = conn.execute("SELECT id FROM habits WHERE name = ?", (name,)).fetchone()
    if row is None:
        raise ValueError(f"No habit named '{name}'")
    return row[0]


def check_in(conn, name, day=None):
    day = day or date.today()
    habit_id = _habit_id(conn, name)
    with conn:
        conn.execute(
            "INSERT OR IGNORE INTO checkins (habit_id, day) VALUES (?, ?)",
            (habit_id, day.isoformat()),
        )


def current_streak(conn, name, today=None):
    today = today or date.today()
    habit_id = _habit_id(conn, name)
    rows = conn.execute(
        "SELECT day FROM checkins WHERE habit_id = ?", (habit_id,)
    ).fetchall()
    days = {date.fromisoformat(r[0]) for r in rows}
    cursor = today if today in days else today - timedelta(days=1)
    streak = 0
    while cursor in days:
        streak += 1
        cursor -= timedelta(days=1)
    return streak
