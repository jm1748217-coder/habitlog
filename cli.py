import argparse
import sqlite3

from . import __version__, db


def build_parser():
    parser = argparse.ArgumentParser(
        prog="habitlog", description="A local-first habit tracker."
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("add", help="Add a habit").add_argument("name")
    sub.add_parser("check", help="Check in today").add_argument("name")
    sub.add_parser("streak", help="Show current streak").add_argument("name")
    sub.add_parser("list", help="List habits")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    conn = db.connect()
    try:
        if args.command == "add":
            db.add_habit(conn, args.name)
            print(f"Added '{args.name}'")
        elif args.command == "check":
            db.check_in(conn, args.name)
            print(f"Checked in '{args.name}' for today")
        elif args.command == "streak":
            n = db.current_streak(conn, args.name)
            print(f"'{args.name}': {n}-day streak")
        elif args.command == "list":
            for name in db.list_habits(conn):
                print(name)
    except sqlite3.IntegrityError:
        print("That habit already exists.")
        return 1
    except ValueError as exc:
        print(exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
