from datetime import date, timedelta

from habitlog import db


def make_conn():
    conn = db.connect(":memory:")
    db.add_habit(conn, "Read")
    return conn


def test_streak_counts_consecutive_days():
    conn = make_conn()
    today = date(2026, 1, 10)
    for i in range(3):
        db.check_in(conn, "Read", today - timedelta(days=i))
    assert db.current_streak(conn, "Read", today) == 3


def test_streak_breaks_on_gap():
    conn = make_conn()
    today = date(2026, 1, 10)
    db.check_in(conn, "Read", today)
    db.check_in(conn, "Read", today - timedelta(days=2))
    assert db.current_streak(conn, "Read", today) == 1


def test_streak_survives_until_end_of_today():
    conn = make_conn()
    today = date(2026, 1, 10)
    db.check_in(conn, "Read", today - timedelta(days=1))
    assert db.current_streak(conn, "Read", today) == 1
