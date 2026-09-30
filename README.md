# Terminal Handbook

An offline field guide to working in the terminal on **macOS and Linux**.

<!-- counts:start -->
268 worked command examples across 12 topics, 7 end-to-end workflows, 54 tools
with install instructions, and a learning path in 8 steps.
<!-- counts:end -->

All of it in one self-contained HTML file, with no network calls and no
analytics. A keyboard-shortcut reference comes with it.

**[Open the handbook →](https://amircodington.github.io/terminal-handbook/)**

Or clone it and open `index.html` in a browser. It works with no internet
connection, because everything it needs is inside that file.

<!-- Add a screenshot here: docs/screenshot.png -->

---

## What this is

Most terminal cheat sheets give you a command and no context. This one is built
around a different idea: **you should not run a command you cannot explain.**

So every example carries four things:

| | |
| --- | --- |
| **The command** | Copyable, with placeholders clearly marked |
| **What it does** | Why it works, and what the flags mean |
| **Its effect** | `Inspect` reads · `Write` touches files · `Disruptive` stops something running · `Destructive` cannot be undone |
| **A reference** | A link to the tool's own documentation, not to a blog post |

The commands are organised by topic — shell foundations, files, Git, GitHub,
web development, containers, Python and local AI, data and media, networking,
editors, packages, plus separate **macOS specifics** and **Linux specifics**
sections for the places where the two genuinely differ.

## My terminal setup (optional)

The handbook is only a page, and it never touches your system. Separately, the
repo also holds my own terminal setup. It works on **macOS and Linux**:

- **zsh**: history, completion, fzf, zoxide, autosuggestions, syntax highlighting and aliases
- **Oh My Posh**: the *Grok Red* prompt theme
- **Ghostty**: config and the matching *Grok Red* color theme
- **Git** (delta), **Neovim** (LazyVim), **Zellij**
- a **`Brewfile`** with every tool, the fonts and Ghostty

| Path | What it is |
| --- | --- |
| [`install.sh`](install.sh) | One-command installer: Homebrew, the `Brewfile`, and symlinks for the configs |
| [`Brewfile`](Brewfile) | Every package, with the macOS-only items in one block |
| [`dotfiles/`](dotfiles) | The config files themselves |
| [`docs/SETUP.md`](docs/SETUP.md) | **Step-by-step guide for macOS and Linux** |

Quick start, once you have read [`docs/SETUP.md`](docs/SETUP.md) and `install.sh`:

```bash
git clone https://github.com/amircodington/terminal-handbook.git ~/Workspace/terminal-handbook && cd ~/Workspace/terminal-handbook && ./install.sh
```

Anything the installer would replace is moved to
`~/.config/terminal-backups/` first. Secrets go in `~/.zshrc.local`, which is
never committed.

This setup is personal. Use it as a starting point and read what it does. That
is the same advice the handbook gives about every command.

## What this is *not*

**It is not a complete reference.** It is a curated set of worked examples. For
complete syntax, use `man` and `--help` — which the handbook repeatedly tells
you to do.

## Before you run anything

Read this part. It matters more than the rest of the README.

1. **Every example is a starting point, not a recipe to paste.** Paths such as
   `~/projects/your-app`, names such as `IMAGE:TAG`, and IDs such as `PID` are
   placeholders. Replace them.
2. **Check the effect badge.** Anything marked `Write`, `Disruptive` or
   `Destructive` changes something. `Destructive` means there is no undo.
3. **`sudo` gives a command the power to break your system.** The Linux install
   commands here use it because installing packages requires it. Understand what
   you are elevating before you type your password.
4. **Installer scripts piped from the internet run as you.** A few tools
   (`uv`, `volta`, `ollama`) are most easily installed that way on Linux. Download
   the script and read it first. That advice applies to every project, not just
   these.
5. **Adding yourself to the `docker` group is equivalent to giving yourself
   root.** It is the normal way to use Docker on Linux, but know what it means.

## Installing the tools

The handbook's **Install the toolkit** page lists every tool with the exact
command for each platform. Nothing there is mandatory — the tools are sorted
into three tiers:

- **Essential** — the command library assumes these: `zsh`, `git`, `fzf`,
  `zoxide`, `fd`, `ripgrep`, `jq`, `curl`, `lsof`
- **Recommended** — used across several topics: `eza`, `bat`, `gh`, `git-delta`,
  `btop`, `tealdeer`, `neovim`, `uv`, `volta`, `yq`, `trash`, plus the two zsh plugins
- **Optional** — one topic each: containers, Kubernetes, local AI, media, Go

Check what you already have before installing anything:

```bash
command -v git fzf rg fd jq zoxide
```

The quickest way to get the essentials:

**macOS** — with [Homebrew](https://brew.sh):

```bash
brew install zsh git fzf zoxide fd ripgrep jq curl
```

**Debian / Ubuntu:**

```bash
sudo apt update && sudo apt install -y zsh git fzf zoxide fd-find ripgrep jq curl lsof
```

**Fedora / RHEL:**

```bash
sudo dnf install -y zsh git fzf zoxide fd-find ripgrep jq curl lsof
```

**Arch:**

```bash
sudo pacman -S --needed zsh git fzf zoxide fd ripgrep jq curl lsof
```

### Two Linux gotchas the handbook repeats

On Debian and Ubuntu, two packages install their binary under a different name:

```bash
fdfind --version && batcat --version
```

If you want the usual names, alias them in your `.zshrc` — your decision, not
this repo's:

```bash
echo "alias fd=fdfind" >> ~/.zshrc && echo "alias bat=batcat" >> ~/.zshrc
```

`fzf` and `zoxide` also do nothing until they are hooked into your shell. Both
projects document the one line each needs; the handbook's entry for each links
straight to it.

## Building it yourself

The page is generated. Content lives in Python; the HTML is the output.

```bash
python3 src/build.py
```

No dependencies beyond Python 3.9+ — no pip install, no virtualenv, no build
tooling. It writes `index.html` and `catalog.json` at the repository root.

| File | What it holds |
| --- | --- |
| `src/content.py` | Command examples, workflows, shortcuts and lessons |
| `src/toolkit.py` | Every tool and its per-platform install commands |
| `src/template.html` | Page markup and all the CSS |
| `src/runtime.js` | Search, filtering, bookmarks and progress |
| `src/build.py` | Combines the four into one HTML file, and resolves each example's documentation link and the package that provides its command |

To add a command, add a row to the relevant `rows(...)` block in
`src/content.py` and rebuild. The row format is
`title | command | explanation | level | effect`, and `src/content.py` documents
it at the top. The counts above are regenerated by the build, so they cannot
drift out of date.

`catalog.json` is the same content as plain data, for anyone who would rather
query it than read a web page.

## Contributing

Corrections are especially welcome. If an explanation is wrong, a flag does not
exist on your platform, or a package name has changed on your distribution, open
an issue or a pull request.

Please edit `src/`, not `index.html` — the HTML is generated and your change
would be overwritten on the next build. Run `python3 src/build.py` and commit
the regenerated output along with your source change.

## Honest disclosure: this was vibe coded

This repository was built with an AI coding assistant (Claude), from a terminal
audit of one developer's machine, then rewritten to be general. That shaped it
in ways worth knowing before you trust it:

- **The content was AI-drafted and then checked against each tool's own
  documentation.** Every example links to that documentation so you can verify a
  claim yourself rather than taking the page's word for it.
- **Not every command has been executed on every platform.** The macOS examples
  come from a working macOS machine. The Linux package names and equivalents
  were researched rather than tested on all four distributions. If one is wrong
  where you are, that is a bug — please report it.
- **The tone is confident. Treat it as a well-read colleague's advice, not as
  authority.** `man` is the authority.
- **Nothing here runs automatically.** `install.sh` runs only when you run it,
  and the handbook itself never runs anything. That limits the blast radius of any
  mistake in it to a command you chose to copy. Read before you paste. That is
  the whole point of the handbook anyway.

## Licence

[MIT](LICENSE). The command examples and explanations are yours to reuse. Links
point to each tool's own documentation, which stays under its own licence.
