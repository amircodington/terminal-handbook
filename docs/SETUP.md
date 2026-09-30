# Terminal setup — step by step

This sets up the same terminal I use: **zsh** with autosuggestions, syntax
highlighting, fzf and zoxide, the **Oh My Posh "Grok Red"** prompt (plus the "atomic" theme), the
**Ghostty** terminal with a matching theme, plus Git (delta), Neovim
(LazyVim), Zellij, btop, htop, the GitHub CLI settings and the CLI tools in the [`Brewfile`](../Brewfile).

It works on **macOS** and **Linux** (Debian/Ubuntu, Fedora, Arch). Both use
Homebrew, so the same `Brewfile` and the same `.zshrc` work on both.

## What goes where

`install.sh` does not copy files. It **symlinks** them, so the repo stays the
single source of truth: edit a file in the repo, open a new terminal, done.

| In the repo | Linked to |
| --- | --- |
| `dotfiles/zsh/.zshrc` | `~/.zshrc` |
| `dotfiles/zsh/.zshenv` | `~/.zshenv` |
| `dotfiles/ohmyposh/` | `~/.config/ohmyposh/` |
| `dotfiles/ghostty/` (config + `themes/grok-red`) | `~/.config/ghostty/` |
| `dotfiles/git/config`, `dotfiles/git/ignore` | `~/.config/git/` |
| `dotfiles/nvim/` | `~/.config/nvim/` |
| `dotfiles/zellij/` | `~/.config/zellij/` |
| `dotfiles/btop/btop.conf` | `~/.config/btop/btop.conf` |
| `dotfiles/htop/htoprc` | `~/.config/htop/htoprc` |
| `dotfiles/gh/config.yml` | `~/.config/gh/config.yml` (never `hosts.yml`, which holds your login token) |

Anything already at a target is **moved** (not deleted) to
`~/.config/terminal-backups/install-<date>/` first.

Two files are created for you and never tracked by Git:

- `~/.zshrc.local`: secrets (API tokens) and machine-only aliases. `.zshrc`
  sources it.
- `~/.gitconfig`: your Git name and email.

---

## macOS

### 1. Install the Xcode command-line tools

```bash
xcode-select --install
```

This gives you `git`, which you need for the next step. If it says they are
already installed, carry on.

### 2. Clone the repo

```bash
git clone https://github.com/amircodington/terminal-handbook.git ~/Workspace/terminal-handbook
```

```bash
cd ~/Workspace/terminal-handbook
```

Clone it somewhere you will keep it. The links point into this folder, so if
you move or delete it, your shell config goes with it.

### 3. Read the installer, then run it

```bash
less install.sh
```

```bash
./install.sh
```

The installer:

1. installs Homebrew if it is missing (it asks for your password)
2. runs `brew bundle`, which installs every formula, Ghostty and the Nerd Fonts
3. links the config files (see the table above)
4. makes zsh your login shell if it is not already

It is safe to run again. Anything already installed or linked is left alone.

### 4. Open Ghostty

Quit Terminal and open **Ghostty** from Applications. You should see the
Grok Red prompt, with its icons drawn correctly. If you see empty boxes
instead of icons, the font is missing: run `brew bundle --file Brewfile`
again.

### 5. Personal settings

```bash
git config --global user.name "Your Name"
```

```bash
git config --global user.email "you@example.com"
```

Put tokens in `~/.zshrc.local`, never in `.zshrc`:

```bash
echo 'export HF_TOKEN="…"' >> ~/.zshrc.local
```

### 6. Docker (optional)

On macOS, Docker runs inside a small VM managed by Colima:

```bash
colima start
```

```bash
docker run --rm hello-world
```

### 7. Neovim (optional)

```bash
nvim
```

The first launch downloads LazyVim and its plugins. Wait for it to finish,
then restart `nvim`.

---

## Linux

Tested paths: Debian/Ubuntu (`apt`), Fedora (`dnf`), Arch (`pacman`).

### 1. Install git and curl

```bash
sudo apt update && sudo apt install -y git curl
```

On Fedora use `sudo dnf install -y git curl`. On Arch use
`sudo pacman -S --needed git curl`.

### 2. Clone the repo

```bash
git clone https://github.com/amircodington/terminal-handbook.git ~/Workspace/terminal-handbook
```

```bash
cd ~/Workspace/terminal-handbook
```

### 3. Read the installer, then run it

```bash
less install.sh
```

```bash
./install.sh
```

On Linux the installer also:

- installs build tools, `zsh`, `lsof`, `unzip` and `xdg-utils` with your
  distribution's package manager, which needs `sudo` (plus the Vazirmatn font
  for Persian text on Debian/Ubuntu and Fedora)
- installs Homebrew into `/home/linuxbrew/.linuxbrew`, so you get the same
  tool versions as on macOS
- installs the GeistMono Nerd Font into `~/.local/share/fonts` with
  `oh-my-posh font install`
- installs **Ghostty**: `pacman` on Arch, the `scottames/ghostty` COPR on
  Fedora, and Snap elsewhere (Ubuntu)

`chsh` asks for your password. **Log out and back in** for zsh to become your
login shell.

### 4. Open Ghostty

Open **Ghostty** from your app launcher. The installer has already set it up
with the same config, theme and font as on macOS.

If the installer printed "No Ghostty package found", install it using the
official list at <https://ghostty.org/docs/install/binary>. The config is
already in place.

Differences from macOS:

- Ghostty ignores the `macos-*` options on Linux.
- `cmd` in the config means the Super key, so the reload key is
  `super+shift+r`. Ghostty's own `ctrl+shift+,` also reloads.
- The background blur only works on KDE Plasma. Elsewhere you get a
  transparent window without blur.

### 5. Personal settings

Same as step 5 for macOS: set your Git name and email, and put tokens in
`~/.zshrc.local`.

### 6. Docker (optional)

Colima is only needed on macOS. On Linux, install Docker Engine by following
the steps for your distribution at <https://docs.docker.com/engine/install/>,
then:

```bash
sudo usermod -aG docker "$USER"
```

Log out and back in. Be aware that anyone in the `docker` group effectively
has root access.

### 7. Neovim (optional)

Same as macOS: run `nvim` once and let it install.

---

## Day to day

| I want to… | Run |
| --- | --- |
| reload the shell after editing `.zshrc` | `reload` |
| reload Ghostty after editing its config | `cmd+shift+r` (Linux: `super+shift+r`) |
| see which Brewfile packages are missing | `brew bundle check --file Brewfile` |
| update everything | `brew update && brew upgrade` |
| re-link configs only (for example after a `git pull`) | `./install.sh --links-only` |
| undo the setup | delete the symlinks, then move files back from `~/.config/terminal-backups/` |

## Updating the repo from this machine

If you change a config somewhere other than the repo, or install a new tool:

```bash
brew bundle dump --file - --no-vscode
```

This prints what is installed. Add the lines you want to keep to `Brewfile` by
hand, so its sections and the `if OS.mac?` block stay intact.

Once the configs are linked, editing `~/.zshrc` edits the file in the repo
directly. Review it and commit:

```bash
git diff
```

Before every commit, check that no token has slipped into a tracked file:

```bash
git grep -nE '(TOKEN|KEY|SECRET)=' -- dotfiles
```

That command should print nothing.
