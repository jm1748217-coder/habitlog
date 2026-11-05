# habitlog

A local-first command-line habit tracker. Add habits, check them off each day,
and see your current streak. All data stays in a SQLite file on your machine.

## Who it's for
People who want a fast, private, no-account habit tracker in the terminal.

## Built with
Python 3.9+, SQLite (standard library only), pytest for tests.

## Install and run

```bash
git clone https://github.com/YOUR-USERNAME/habitlog.git
cd habitlog
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

```bash
habitlog add "Read 20 pages"
habitlog check "Read 20 pages"
habitlog list
habitlog streak "Read 20 pages"
```

Data is stored in `~/.habitlog/habits.db`.

## Run the tests

```bash
pip install pytest
pytest
```

## Roadmap
See [ROADMAP.md](ROADMAP.md) and the open issues.

## License
MIT. See [LICENSE](LICENSE).
