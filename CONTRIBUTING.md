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
`catalog.json`. The build also rewrites the count line in `README.md`, so that
may appear in your diff too.

## Adding a command

Add a row to the relevant `rows(...)` block in `src/content.py`:

```
Title of the example | the command | what it does and why | Start | Inspect
```

- Use ` ;; ` to break a command across lines.
- The command may contain literal pipes. The **explanation** may not contain
  ` | ` — the parser splits the last three fields from the right, so a pipe in
  the explanation would be read as a field separator.
- Titles become the example's id, and ids are what a reader's saved bookmarks
  are keyed on. The build fails on a duplicate title within a topic.
- `level` is `Start`, `Intermediate` or `Advanced`.
- `effect` must be honest, because it drives the warning badge in the page:
  `Inspect` (reads only), `Run`, `Write` (touches the filesystem), `Network`,
  `Disruptive` (stops something running), `Destructive` (no undo), or
  `Remote write` (changes something on someone else's server).

Use placeholder paths (`~/projects/your-app`) rather than real ones, and write
the explanation so a reader knows what will happen *before* they press Enter.

## Adding a tool

Add a `tool(...)` entry to `TOOLS` in `src/toolkit.py`. Only `brew` is required:
`apt`, `dnf` and `pacman` default to the same name, so pass them only where the
distribution differs. Pass `''` where no standard package exists and explain the
alternative in `note`. If the installed binary has a different name from the
package, say so in `note` — that trips people up constantly.

List every executable the tool provides in `commands`. The build uses that list
to label examples with the package that provides them and to link each example
to the tool's documentation, so an omission there shows up on the page.

## Platform claims

If you are correcting a Linux package name or a BSD-versus-GNU flag difference,
please say in the pull request which distribution or version you verified it on.
Much of the Linux coverage was researched rather than executed everywhere, so
first-hand confirmation genuinely helps.
