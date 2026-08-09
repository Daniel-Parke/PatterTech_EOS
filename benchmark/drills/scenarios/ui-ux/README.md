# Northbank Water web

The public leak-reporting page, and soon an internal view for the
control room.

## What is here

- `web/` the public page as it stands: hand-written HTML, CSS and a
  little JavaScript.
- `tools/build.py` writes `dist/` from the sources. Everything under
  `dist/` is generated. Do not edit it by hand; change the source and
  run the build again.
- `tools/serve.py` previews `dist/` on <http://localhost:8000>.
- `tests/` plain `unittest`, no plugins.

## Working on it

    python tools/build.py
    python tools/serve.py
    python -m unittest discover -s tests

No package manager and no framework. Everything here runs on a stock
Python and a browser, which is deliberate: the control room machines
are locked down and we cannot install a toolchain on them.

## Conventions

- Anything the build writes is derived. If a derived file and its
  source disagree, the source wins.
- New pages go in their own directory with their own entry point
  rather than growing `web/index.html` further.
