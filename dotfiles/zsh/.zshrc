# ==============================================================================
# ZSH CONFIGURATION
# ==============================================================================
# macOS / Linux development environment
# Homebrew • Volta • Git • Docker • Kubernetes • Python/uv • pnpm
# fzf • zoxide • eza • bat • Oh My Posh
# ==============================================================================


# ------------------------------------------------------------------------------
# 1. Environment
# ------------------------------------------------------------------------------

# Default editor: VS Code when installed, otherwise Neovim.
if command -v code >/dev/null 2>&1; then
    export EDITOR="code --wait"
else
    export EDITOR="nvim"
fi
export VISUAL="$EDITOR"

# Language / Unicode
export LANG="en_US.UTF-8"
export LC_ALL="en_US.UTF-8"

# bat + delta use the terminal's (GitHub Dark) ANSI palette.
export BAT_THEME="ansi"

# Disable Homebrew environment hints
export HOMEBREW_NO_ENV_HINTS=1

# Huggingface
export HF_HUB_ENABLE_HF_TRANSFER=1
export HF_XET_HIGH_PERFORMANCE=1
# ------------------------------------------------------------------------------
# 2. PATH
# ------------------------------------------------------------------------------

# Keep PATH entries unique, including after reload.
typeset -U path PATH

# Homebrew (Apple Silicon, Intel Mac or Linux); sets HOMEBREW_PREFIX.
for _brew in /opt/homebrew/bin/brew /usr/local/bin/brew /home/linuxbrew/.linuxbrew/bin/brew; do
    if [[ -x "$_brew" ]]; then
        eval "$("$_brew" shellenv)"
        break
    fi
done
unset _brew

# Prefer Homebrew curl over the system curl
export PATH="$HOMEBREW_PREFIX/opt/curl/bin:$PATH"


# Volta — Node.js / npm / pnpm
export VOLTA_HOME="$HOME/.volta"
export PATH="$VOLTA_HOME/bin:$PATH"


# ------------------------------------------------------------------------------
# 3. Zsh Function / Completion Paths
# ------------------------------------------------------------------------------

# Custom completions
mkdir -p "$HOME/.zfunc"
typeset -U fpath
fpath=("$HOME/.zfunc" "$HOMEBREW_PREFIX/share/zsh/site-functions" $fpath)


# ------------------------------------------------------------------------------
# 4. History
# ------------------------------------------------------------------------------

HISTFILE="$HOME/.zsh_history"

# Number of commands kept in memory
HISTSIZE=100000

# Number of commands persisted to disk
SAVEHIST=100000

# Append instead of replacing history
setopt APPEND_HISTORY

# Share history between terminal sessions
setopt SHARE_HISTORY

# Remove duplicate history entries
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_SAVE_NO_DUPS

# Remove unnecessary whitespace
setopt HIST_REDUCE_BLANKS

# Show history command before execution when using history expansion
setopt HIST_VERIFY

# Do not save commands beginning with a space
setopt HIST_IGNORE_SPACE


# ------------------------------------------------------------------------------
# 5. General Zsh Behavior
# ------------------------------------------------------------------------------

# Automatically cd into a directory by typing its name
setopt AUTO_CD

# Allow comments in interactive shell
setopt INTERACTIVE_COMMENTS

# Better directory stack behavior
setopt AUTO_PUSHD
setopt PUSHD_IGNORE_DUPS
setopt PUSHD_SILENT

# Prevent accidental overwrite using >
setopt NO_CLOBBER


# ------------------------------------------------------------------------------
# 6. Completion
# ------------------------------------------------------------------------------

autoload -Uz compinit

# Cache completion initialization for faster startup
ZSH_COMPDUMP="${ZDOTDIR:-$HOME}/.zcompdump"

if [[ ! -f "$ZSH_COMPDUMP" || "${ZDOTDIR:-$HOME}/.zshrc" -nt "$ZSH_COMPDUMP" || -n "$ZSH_COMPDUMP"(#qN.mh+24) ]]; then
    compinit -d "$ZSH_COMPDUMP"
else
    compinit -C -d "$ZSH_COMPDUMP"
fi

# Interactive completion menu
zstyle ':completion:*' menu select

# Case-insensitive completion
zstyle ':completion:*' matcher-list \
    'm:{a-zA-Z}={A-Za-z}' \
    'r:|[._-]=* r:|=*'

# Group completion results
zstyle ':completion:*' group-name ''

# Better completion descriptions
zstyle ':completion:*:descriptions' format '%F{yellow}-- %d --%f'

# Process completion
zstyle ':completion:*:*:*:*:processes' command \
    'ps -u $USER -o pid,user,comm -w -w'

# Completion caching
zstyle ':completion:*' use-cache on
zstyle ':completion:*' cache-path "$HOME/.zsh/cache"
mkdir -p "$HOME/.zsh/cache"


# ------------------------------------------------------------------------------
# 7. Key Bindings
# ------------------------------------------------------------------------------

# Emacs-style shell editing
bindkey -e

# Home / End
bindkey '^[[H' beginning-of-line
bindkey '^[[F' end-of-line

# Delete
bindkey '^[[3~' delete-char

# Ctrl + Left / Right — jump between words
bindkey '^[[1;5D' backward-word
bindkey '^[[1;5C' forward-word

# Up / Down — search history based on current input
autoload -Uz up-line-or-beginning-search
autoload -Uz down-line-or-beginning-search

zle -N up-line-or-beginning-search
zle -N down-line-or-beginning-search

bindkey '^[[A' up-line-or-beginning-search
bindkey '^[[B' down-line-or-beginning-search


# ------------------------------------------------------------------------------
# 8. FZF
# ------------------------------------------------------------------------------

if command -v fzf >/dev/null 2>&1; then
    source <(fzf --zsh)

    # Better default fuzzy-search behavior
    export FZF_DEFAULT_OPTS="
        --height=60%
        --layout=reverse
        --border
        --info=inline
        --preview-window=right:60%
    "

    # Use fd instead of find when available
    if command -v fd >/dev/null 2>&1; then
        export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
        export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
        export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
    fi
fi


# ------------------------------------------------------------------------------
# 9. Zoxide
# ------------------------------------------------------------------------------

if command -v zoxide >/dev/null 2>&1; then
    eval "$(zoxide init zsh)"
fi


# ------------------------------------------------------------------------------
# 10. GitHub CLI Completion
# ------------------------------------------------------------------------------

# Homebrew provides _gh in site-functions; compinit loads it on demand.


# ------------------------------------------------------------------------------
# 11. Navigation Aliases
# ------------------------------------------------------------------------------

alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."

alias home="cd ~"

# Quick access to development workspace
alias dev="cd ~/Workspace"
alias work="cd ~/Workspace"


# ------------------------------------------------------------------------------
# 12. File & Directory Aliases
# ------------------------------------------------------------------------------

if command -v eza >/dev/null 2>&1; then
    alias ls="eza --icons=always"
    alias l="eza --icons=always"
    alias ll="eza -lah --icons=always --git"
    alias la="eza -a --icons=always"
    alias lt="eza --tree --level=2 --icons=always"
    alias ltt="eza --tree --level=3 --icons=always"
fi

if command -v bat >/dev/null 2>&1; then
    alias ccat="bat"
fi


# ------------------------------------------------------------------------------
# 12b. Editor (Neovim / LazyVim)
# ------------------------------------------------------------------------------

if command -v nvim >/dev/null 2>&1; then
    alias v="nvim"
    alias vi="nvim"
    alias vim="nvim"
    alias lg="lazygit"
fi


# ------------------------------------------------------------------------------
# 13. Git Aliases
# ------------------------------------------------------------------------------

alias g="git"

alias gs="git status"
alias gss="git status --short"

alias ga="git add"
alias gaa="git add ."

alias gc="git commit"
alias gcm="git commit -m"

alias gp="git push"
alias gpf="git push --force-with-lease"

alias gl="git pull"

alias gd="git diff"
alias gds="git diff --staged"

alias gb="git branch"
alias gba="git branch --all"

alias gco="git checkout"
alias gsw="git switch"

alias glog="git log --oneline --graph --decorate"
alias gloga="git log --oneline --graph --decorate --all"

alias gr="git restore"
alias grs="git restore --staged"

alias gst="git stash"
alias gstp="git stash pop"


# ------------------------------------------------------------------------------
# 14. Docker Aliases
# ------------------------------------------------------------------------------

alias d="docker"

alias dc="docker compose"

alias dps="docker ps"
alias dpa="docker ps -a"

alias di="docker images"

alias dex="docker exec -it"

alias dcu="docker compose up"
alias dcud="docker compose up -d"

alias dcd="docker compose down"

alias dcl="docker compose logs"
alias dclf="docker compose logs -f"

alias dcb="docker compose build"
alias dcps="docker compose ps"

# Clean dangling Docker resources
alias dprune="docker system prune"


# ------------------------------------------------------------------------------
# 15. Kubernetes Aliases
# ------------------------------------------------------------------------------

alias k="kubectl"

alias kgp="kubectl get pods"
alias kgpa="kubectl get pods -A"

alias kgs="kubectl get services"
alias kgn="kubectl get nodes"

alias kctx="kubectl config current-context"
alias kcontexts="kubectl config get-contexts"

alias kdesc="kubectl describe"
alias klogs="kubectl logs"


# ------------------------------------------------------------------------------
# 16. Python / uv
# ------------------------------------------------------------------------------

alias py="python3"
alias py3="python3"

alias uvrun="uv run"
alias uvadd="uv add"
alias uvsync="uv sync"
alias uvlock="uv lock"


# ------------------------------------------------------------------------------
# 17. Node / pnpm
# ------------------------------------------------------------------------------

alias p="pnpm"

alias pi="pnpm install"
alias pd="pnpm dev"
alias pb="pnpm build"
alias pt="pnpm test"

alias px="pnpm exec"


# ------------------------------------------------------------------------------
# 18. Utility Aliases
# ------------------------------------------------------------------------------

alias cls="clear"

alias path='echo $PATH | tr ":" "\n"'

alias ports="lsof -iTCP -sTCP:LISTEN -n -P"

alias myip="curl -s https://api.ipify.org && echo"

alias reload="source ~/.zshrc"

alias zshconfig="\${EDITOR%% *} ~/.zshrc"


# ------------------------------------------------------------------------------
# 19. Useful Functions
# ------------------------------------------------------------------------------

# Create directory and enter it
mkcd() {
    if [[ -z "$1" ]]; then
        echo "Usage: mkcd <directory>"
        return 1
    fi

    mkdir -p -- "$1" && cd -- "$1"
}


# Extract most common archive formats
extract() {
    if [[ ! -f "$1" ]]; then
        echo "'$1' is not a valid file."
        return 1
    fi

    case "$1" in
        *.tar.bz2) tar xjf "$1" ;;
        *.tar.gz)  tar xzf "$1" ;;
        *.tar.xz)  tar xJf "$1" ;;
        *.bz2)     bunzip2 "$1" ;;
        *.rar)     "$HOMEBREW_PREFIX/opt/libarchive/bin/bsdtar" -xf "$1" ;;
        *.gz)      gunzip "$1" ;;
        *.tar)     tar xf "$1" ;;
        *.tbz2)    tar xjf "$1" ;;
        *.tgz)     tar xzf "$1" ;;
        *.zip)     unzip "$1" ;;
        *.7z)      "$HOMEBREW_PREFIX/opt/libarchive/bin/bsdtar" -xf "$1" ;;
        *)
            echo "Unsupported archive format: $1"
            return 1
            ;;
    esac
}


# Find process using a TCP port
port() {
    if [[ -z "$1" ]]; then
        echo "Usage: port <port-number>"
        return 1
    fi

    lsof -iTCP:"$1" -sTCP:LISTEN -n -P
}


# Stop all processes listening on one TCP port (SIGTERM, not SIGKILL).
killport() {
    if [[ "$#" != 1 || "$1" != <1-65535> ]]; then
        print -u2 -- "Usage: killport <1-65535>"
        return 2
    fi
    local -a pids
    pids=("${(@f)$(command lsof -tiTCP:"$1" -sTCP:LISTEN)}")
    pids=("${(@)pids:#}")
    if (( ! ${#pids} )); then
        print -- "No process is listening on port $1"
        return 0
    fi
    print -- "Sending SIGTERM to PID(s): ${pids[*]}"
    kill -- "${pids[@]}"
}


# ------------------------------------------------------------------------------
# 20. Zsh Autosuggestions
# ------------------------------------------------------------------------------

if [[ -f "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh" ]]; then
    source "$HOMEBREW_PREFIX/share/zsh-autosuggestions/zsh-autosuggestions.zsh"
fi


# ------------------------------------------------------------------------------
# 21. Oh My Posh
# ------------------------------------------------------------------------------

# direnv must hook in before Oh My Posh so the prompt sees DIRENV_DIR.
if command -v direnv >/dev/null 2>&1; then
    eval "$(direnv hook zsh)"
fi

# Background job count for the prompt; must run before Oh My Posh's precmd.
_omp_jobs() { export OMP_JOBS=${#jobstates} }
precmd_functions+=(_omp_jobs)

if command -v oh-my-posh >/dev/null 2>&1; then
    eval "$(oh-my-posh init zsh --config "$HOME/.config/ohmyposh/grok-red.omp.json")"
fi


# ------------------------------------------------------------------------------
# 22. Syntax Highlighting
# ------------------------------------------------------------------------------
# IMPORTANT:
# zsh-syntax-highlighting should be loaded as close to the END of .zshrc as
# possible so it can correctly wrap previously-defined widgets and bindings.

# Loaded after all integrations below.


# ==============================================================================
# END OF ZSH CONFIGURATION
# ==============================================================================

# Hugging Face model cache
export HF_HOME="$HOME/.cache/huggingface"

# pnpm globals; Volta owns the pnpm executable and stays first in PATH.
if [[ "$OSTYPE" == darwin* ]]; then
    export PNPM_HOME="$HOME/Library/pnpm"
else
    export PNPM_HOME="$HOME/.local/share/pnpm"
fi
path=("$VOLTA_HOME/bin" $path "$PNPM_HOME" "$PNPM_HOME/bin")

# Run WP-CLI inside a running site's container, from its compose directory.
wpdc() {
    command docker compose exec wpcli wp "$@"
}


# Open the offline command handbook from this repo (.zshrc is a symlink into it).
_handbook="${${(%):-%x}:A:h:h:h}/index.html"
if [[ "$OSTYPE" == darwin* ]]; then
    alias cheats="open ${(q)_handbook}"
else
    alias cheats="xdg-open ${(q)_handbook}"
fi
unset _handbook

# Explicit UTF-8 Python per-project workflows remain managed by uv.
# Convenient file preview in Ctrl+T; only runs when the picker is open.
if command -v bat >/dev/null 2>&1; then
    export FZF_CTRL_T_OPTS="--preview 'bat --color=always --style=numbers --line-range=:200 {}'"
fi

# Secrets (API tokens) and machine-only aliases; never committed.
[[ -f "$HOME/.zshrc.local" ]] && source "$HOME/.zshrc.local"

# Syntax highlighting must follow widgets and shell hooks.
if [[ -f "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" ]]; then
    source "$HOMEBREW_PREFIX/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh"
fi
