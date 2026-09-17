# Contributing

Corrections are the most valuable contribution here. A wrong explanation is
worse than a missing one.

## Before you open a pull request

Edit `src/`, never `index.html`. The HTML is generated output and your change
would disappear on the next build.

```bash
python3 src/build.py
```

Commit both your source change and the regenerated `index.html` and
`catalog.json`.

## Adding a command

Add a row to the relevant `rows(...)` block in `src/content.py`:

```
Title of the example | the command | what it does and why | Start | Inspect
```

- Use ` ;; ` to break a command across lines.
- `level` is `Start`, `Intermediate` or `Advanced`.
- `effect` must be honest, because it drives the warning badge in the page:
  `Inspect` (reads only), `Run`, `Write` (touches the filesystem), `Network`,
  `Disruptive` (stops something running), `Destructive` (no undo), or
  `Remote write` (changes something on someone else's server).

Use placeholder paths (`~/projects/your-app`) rather than real ones, and write
the explanation so a reader knows what will happen *before* they press Enter.

## Adding a tool

Add an entry to `_TOOLS` in `src/toolkit.py` with the package name for each of
Homebrew, apt, dnf and pacman. Leave a field empty where no standard package
exists and explain the alternative in `note`. If the installed binary has a
different name from the package, say so in `note` — that trips people up
constantly.

## Platform claims

If you are correcting a Linux package name or a BSD-versus-GNU flag difference,
please say in the pull request which distribution or version you verified it on.
Much of the Linux coverage was researched rather than executed everywhere, so
first-hand confirmation genuinely helps.
