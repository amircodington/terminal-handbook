# Terminal setup — everything `install.sh` installs.
# Works on macOS and on Linux (Homebrew on Linux). macOS-only items sit in the
# `if OS.mac?` block at the bottom.
#   brew bundle --file Brewfile          install
#   brew bundle check --file Brewfile    what is missing

tap "jandedobbeleer/oh-my-posh"
tap "sst/tap"

# Shell & prompt
brew "zsh-autosuggestions"
brew "zsh-syntax-highlighting"
brew "jandedobbeleer/oh-my-posh/oh-my-posh"
brew "direnv"
brew "fzf"
brew "zoxide"

# Core CLI
brew "bat"
brew "curl"
brew "duf"
brew "dust"
brew "eza"
brew "fd"
brew "glow"
brew "jless"
brew "jq"
brew "procs"
brew "sd"
brew "tealdeer"
brew "tokei"
brew "tree"
brew "wget"
brew "xh"
brew "yq"

# Git & GitHub
brew "gh"
brew "git"
brew "git-delta"
brew "git-lfs"
brew "gnupg"
brew "lazygit"

# Editors & multiplexers
brew "neovim"
brew "tree-sitter-cli"
brew "tmux"
brew "zellij"

# Monitoring & benchmarking
brew "btop"
brew "htop"
brew "hyperfine"
brew "watchexec"

# Languages & runtimes
brew "go"
brew "gopls"
brew "uv"
brew "volta"
brew "cmake"
brew "pkgconf"

# Containers & Kubernetes (CLI side; see docs/SETUP.md for the Linux engine)
brew "dive"
brew "hadolint"
brew "helm"
brew "k9s"
brew "kubernetes-cli"
brew "lazydocker"

# Media (also used by LazyVim image preview)
brew "ghostscript"
brew "imagemagick"
brew "libarchive"  # bsdtar, used by extract() for .rar/.7z

# Local AI
brew "llama.cpp"
brew "ollama"
brew "sst/tap/opencode"

if OS.mac?
  # Docker runtime on macOS (Linux uses Docker Engine directly)
  brew "colima"
  brew "docker"
  brew "docker-buildx"
  brew "docker-compose"

  brew "mactop"
  brew "pinentry-mac"
  brew "trash"

  cask "ghostty"
  cask "font-geist-mono-nerd-font"
  cask "font-jetbrains-mono-nerd-font"
  cask "font-vazirmatn"
end
