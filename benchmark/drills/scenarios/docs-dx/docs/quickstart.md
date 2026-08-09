# Quickstart

notecat turns a folder of notes into one file you can read or print.
This takes about two minutes.

## Installing

There is nothing to install. Clone the repository and check that Python
can see the script:

```bash
python cli.py --help
```

You should see the usage line.

## Bundling your first notes

The repository ships a `notes/` folder with two files in it. Bundle
them into a `build/` folder:

```bash
python cli.py --outdir build --source notes
```

Open `build/notes.md` and you will find both notes under one heading.

## Changing the title

The heading at the top of the bundle comes from `--title`:

```bash
python cli.py --title "Week 12" --source notes
```

Every flag is listed in the [reference](reference.md).
