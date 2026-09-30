#!/usr/bin/env bash
# Install the terminal setup on macOS or Linux.
#   ./install.sh               packages + config links
#   ./install.sh --links-only  only (re)link the config files
# Safe to re-run. Existing files are moved to ~/.config/terminal-backups/.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOT="$REPO/dotfiles"
BACKUP="$HOME/.config/terminal-backups/install-$(date +%Y%m%d-%H%M%S)"
OS="$(uname -s)"

say() { printf '\n\033[1;31m==>\033[0m %s\n' "$*"; }

linux_prereqs() {
  say "Installing Linux prerequisites (needs sudo)"
  if command -v apt-get >/dev/null; then
    sudo apt-get update && sudo apt-get install -y build-essential procps curl file git zsh lsof unzip bzip2 xdg-utils
    sudo apt-get install -y fonts-vazirmatn || true  # Persian glyphs; not in older releases
  elif command -v dnf >/dev/null; then
    sudo dnf install -y @development-tools procps-ng curl file git zsh lsof unzip bzip2 xdg-utils
    sudo dnf install -y vazirmatn-fonts || true
  elif command -v pacman >/dev/null; then
    sudo pacman -S --needed --noconfirm base-devel procps-ng curl file git zsh lsof unzip bzip2 xdg-utils
  else
    echo "Unknown package manager: install build tools, curl, git and zsh yourself, then re-run." >&2
    exit 1
  fi
}

# Homebrew has no Ghostty for Linux; use the distro's package (ghostty.org/docs/install/binary).
linux_ghostty() {
  command -v ghostty >/dev/null && return
  say "Installing Ghostty"
  if command -v pacman >/dev/null; then
    sudo pacman -S --needed --noconfirm ghostty
  elif command -v dnf >/dev/null; then
    sudo dnf copr enable -y scottames/ghostty && sudo dnf install -y ghostty
  elif command -v snap >/dev/null; then
    sudo snap install ghostty --classic
  else
    echo "  No Ghostty package found for this system; see docs/SETUP.md."
  fi
}

homebrew() {
  local b
  for b in /opt/homebrew/bin/brew /usr/local/bin/brew /home/linuxbrew/.linuxbrew/bin/brew; do
    [[ -x $b ]] && { eval "$("$b" shellenv)"; return; }
  done
  say "Installing Homebrew"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  homebrew
}

# link <source in dotfiles/> <target>: skip if missing in repo, back up whatever is there.
link() {
  local src="$DOT/$1" dst="$2"
  [[ -e $src ]] || { echo "  skip  $1 (not in repo)"; return; }
  if [[ -L $dst && "$(readlink "$dst")" == "$src" ]]; then
    echo "  ok    $dst"; return
  fi
  if [[ -e $dst || -L $dst ]]; then
    mkdir -p "$BACKUP"
    mv "$dst" "$BACKUP/"
    echo "  saved $dst -> $BACKUP/"
  fi
  mkdir -p "$(dirname "$dst")"
  ln -s "$src" "$dst"
  echo "  link  $dst"
}

links() {
  say "Linking config files"
  link zsh/.zshrc          "$HOME/.zshrc"
  link zsh/.zshenv         "$HOME/.zshenv"
  link ohmyposh            "$HOME/.config/ohmyposh"
  link ghostty             "$HOME/.config/ghostty"
  link git/config          "$HOME/.config/git/config"
  link git/ignore          "$HOME/.config/git/ignore"
  link nvim                "$HOME/.config/nvim"
  link zellij              "$HOME/.config/zellij"
  link btop/btop.conf      "$HOME/.config/btop/btop.conf"
  link htop/htoprc         "$HOME/.config/htop/htoprc"
  link gh/config.yml       "$HOME/.config/gh/config.yml"  # never hosts.yml: it holds your login token

  # Machine-only settings and secrets live here, never in the repo.
  [[ -e $HOME/.zshrc.local ]] || printf '# Secrets and machine-only settings (not in Git).\n' > "$HOME/.zshrc.local"
  # Keeps `git config --global user.*` out of the linked file in the repo.
  touch "$HOME/.gitconfig"
}

if [[ ${1:-} == --links-only ]]; then links; exit; fi

[[ $OS == Linux ]] && linux_prereqs
homebrew

say "Installing packages from Brewfile"
brew bundle --file "$REPO/Brewfile"

if [[ $OS == Linux ]]; then
  say "Installing Nerd Font (GeistMono)"
  oh-my-posh font install GeistMono || echo "  font install failed; see docs/SETUP.md"
  linux_ghostty
fi

links

if [[ "$(basename "${SHELL:-}")" != zsh ]]; then
  say "Making zsh your login shell"
  chsh -s "$(command -v zsh)"
fi

say "Done. Open a new terminal (Ghostty) to load everything."
[[ $OS == Linux ]] && echo "Docker Engine is installed separately on Linux: see docs/SETUP.md."
exit 0
