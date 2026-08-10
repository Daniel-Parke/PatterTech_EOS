# Reference

Every flag notecat understands. If you have not run it before, the
[Installing](quickstart.md#install-it) section is the shorter way in.

## `--source DIR`

Directory to read notes from. Only files ending in `.md` are read, and
they are bundled in filename order. Defaults to `notes`.

## `--out-dir DIR`

Directory to write the bundle into. Created if it is not there. The
bundle is always called `notes.md`. Defaults to `build`.

## `--title TEXT`

Heading placed at the top of the bundle. Defaults to `Notes`.

## `--help`

Prints the usage line and exits.

## Exit codes

`0` on success. `1` on any error.
