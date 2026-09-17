"""The toolkit the command library assumes, with install commands per platform.

Every entry names the executables it provides so a reader can check what they
already have with `command -v NAME` before installing anything. Linux package
names differ from Homebrew formula names more often than people expect, and a
few packages install the binary under a different name; `binary` records that.

`tier` separates what the handbook depends on from what it merely mentions:

  Essential  - the command library breaks without it
  Recommended- used by several examples; worth installing early
  Optional   - used by one topic (containers, local AI, media)
"""

# Package managers, in the order the README presents them.
MANAGERS = [
    ('macOS', 'Homebrew', 'brew install', 'https://brew.sh'),
    ('Debian / Ubuntu', 'apt', 'sudo apt install -y', 'https://wiki.debian.org/Apt'),
    ('Fedora / RHEL', 'dnf', 'sudo dnf install -y', 'https://dnf.readthedocs.io/'),
    ('Arch', 'pacman', 'sudo pacman -S --needed', 'https://wiki.archlinux.org/title/Pacman'),
]

# name, description, commands, tier, brew, apt, dnf, pacman, url, note
_TOOLS = [
    # --- Shell and prompt -------------------------------------------------
    ('zsh', 'The shell every example in this handbook is written for.', ['zsh'], 'Essential',
     'zsh', 'zsh', 'zsh', 'zsh', 'https://zsh.sourceforge.io/Doc/Release/',
     'Default on macOS since Catalina. On Linux, install it and then run chsh -s "$(command -v zsh)" to make it your login shell.'),
    ('zsh-autosuggestions', 'Suggests the rest of a command from your history as you type.', [], 'Recommended',
     'zsh-autosuggestions', 'zsh-autosuggestions', 'zsh-autosuggestions', 'zsh-autosuggestions',
     'https://github.com/zsh-users/zsh-autosuggestions',
     'A plugin, not a command. It has to be sourced from your .zshrc; the package description prints the path to source.'),
    ('zsh-syntax-highlighting', 'Colours a command line as valid or invalid before you press Enter.', [], 'Recommended',
     'zsh-syntax-highlighting', 'zsh-syntax-highlighting', 'zsh-syntax-highlighting', 'zsh-syntax-highlighting',
     'https://github.com/zsh-users/zsh-syntax-highlighting',
     'Source it last in your .zshrc, after every other plugin, or it will not see later keybindings.'),
    ('direnv', 'Loads and unloads environment variables when you enter or leave a directory.', ['direnv'], 'Optional',
     'direnv', 'direnv', 'direnv', 'direnv', 'https://direnv.net/',
     'Needs a shell hook in your .zshrc. It executes .envrc files, so only allow them in repositories you trust.'),

    # --- Navigation and reading ------------------------------------------
    ('fzf', 'Fuzzy finder. Provides Ctrl+R history search and Ctrl+T file search.', ['fzf'], 'Essential',
     'fzf', 'fzf', 'fzf', 'fzf', 'https://github.com/junegunn/fzf',
     'The key bindings are a separate setup step; see the project README for the line to add to your .zshrc.'),
    ('zoxide', 'Directory jumper that learns where you actually work. Provides z and zi.', ['zoxide'], 'Essential',
     'zoxide', 'zoxide', 'zoxide', 'zoxide', 'https://github.com/ajeetdsouza/zoxide',
     'Needs eval "$(zoxide init zsh)" in your .zshrc. Older Debian and Ubuntu releases ship a version without zi.'),
    ('fd', 'Fast, sensible file finder. A friendlier front end than find.', ['fd'], 'Essential',
     'fd', 'fd-find', 'fd-find', 'fd', 'https://github.com/sharkdp/fd',
     'On Debian and Ubuntu the binary is installed as fdfind; alias fd=fdfind or symlink it.'),
    ('ripgrep', 'Fast recursive content search that respects .gitignore.', ['rg'], 'Essential',
     'ripgrep', 'ripgrep', 'ripgrep', 'ripgrep', 'https://github.com/BurntSushi/ripgrep', ''),
    ('eza', 'Modern ls replacement with colours, icons, tree view and Git status.', ['eza'], 'Recommended',
     'eza', 'eza', 'eza', 'eza', 'https://github.com/eza-community/eza',
     'Not in older Debian and Ubuntu archives; the project documents an apt repository for those releases.'),
    ('bat', 'cat with syntax highlighting, line numbers and paging.', ['bat'], 'Recommended',
     'bat', 'bat', 'bat', 'bat', 'https://github.com/sharkdp/bat',
     'On Debian and Ubuntu the binary is installed as batcat; alias bat=batcat or symlink it.'),
    ('tree', 'Prints a directory as an indented tree.', ['tree'], 'Optional',
     'tree', 'tree', 'tree', 'tree', 'https://oldmanprogrammer.net/source.php?dir=projects/tree', ''),
    ('glow', 'Renders Markdown readably in the terminal.', ['glow'], 'Optional',
     'glow', 'glow', 'glow', 'glow', 'https://github.com/charmbracelet/glow',
     'Packaged on Arch and Fedora; on Debian and Ubuntu use the Charm apt repository or a release binary.'),
    ('tealdeer', 'Fast client for tldr, the community cheat sheets. Provides tldr.', ['tldr'], 'Recommended',
     'tealdeer', 'tealdeer', 'tealdeer', 'tealdeer', 'https://github.com/tealdeer-rs/tealdeer',
     'Run tldr --update once after installing to fetch the page cache.'),

    # --- Text and data ----------------------------------------------------
    ('jq', 'Query and reshape JSON on the command line.', ['jq'], 'Essential',
     'jq', 'jq', 'jq', 'jq', 'https://jqlang.github.io/jq/manual/', ''),
    ('yq', 'The same idea as jq, for YAML, TOML and XML.', ['yq'], 'Recommended',
     'yq', '', '', 'go-yq', 'https://mikefarah.gitbook.io/yq/',
     'Debian, Ubuntu and Fedora package a different, Python-based yq. For the Go yq used here, install the release binary from the project page.'),
    ('jless', 'Pager for large JSON documents. Fold, search and navigate instead of scrolling.', ['jless'], 'Optional',
     'jless', '', '', 'jless', 'https://jless.io/',
     'Not packaged on Debian, Ubuntu or Fedora; install with cargo install jless or a release binary.'),
    ('sd', 'Find and replace with plain syntax. An easier sed for simple substitutions.', ['sd'], 'Optional',
     'sd', 'sd', 'rust-sd', 'sd', 'https://github.com/chmln/sd',
     'sd rewrites files in place. Preview with ripgrep first; it has no undo.'),
    ('tokei', 'Counts lines of code by language.', ['tokei'], 'Optional',
     'tokei', 'tokei', 'tokei', 'tokei', 'https://github.com/XAMPPRocky/tokei', ''),

    # --- Git --------------------------------------------------------------
    ('git', 'Version control. The handbook assumes a recent version.', ['git'], 'Essential',
     'git', 'git', 'git', 'git', 'https://git-scm.com/docs',
     'macOS ships an Xcode version of Git. Installing it via Homebrew keeps it current.'),
    ('gh', 'GitHub from the terminal: pull requests, issues, releases, CI runs.', ['gh'], 'Recommended',
     'gh', 'gh', 'gh', 'github-cli', 'https://cli.github.com/manual/',
     'Debian, Ubuntu and Fedora need the GitHub apt/dnf repository first; the manual documents the exact steps.'),
    ('git-delta', 'Readable, syntax-highlighted diffs for git diff and git log.', ['delta'], 'Recommended',
     'git-delta', 'git-delta', 'git-delta', 'git-delta', 'https://dandavison.github.io/delta/',
     'Configure it as your pager in .gitconfig; installing alone changes nothing.'),
    ('git-lfs', 'Stores large binary files outside the Git history.', ['git-lfs'], 'Optional',
     'git-lfs', 'git-lfs', 'git-lfs', 'git-lfs', 'https://git-lfs.com/',
     'Run git lfs install once per machine after installing.'),
    ('lazygit', 'Full-screen Git interface for staging hunks and reading history.', ['lazygit'], 'Optional',
     'lazygit', '', 'lazygit', 'lazygit', 'https://github.com/jesseduffield/lazygit',
     'Not in the Debian or Ubuntu archives; use the release binary from the project page.'),

    # --- Inspecting a running system --------------------------------------
    ('btop', 'Resource monitor for CPU, memory, disks, network and processes.', ['btop'], 'Recommended',
     'btop', 'btop', 'btop', 'btop', 'https://github.com/aristocratos/btop', ''),
    ('htop', 'The classic interactive process viewer.', ['htop'], 'Optional',
     'htop', 'htop', 'htop', 'htop', 'https://htop.dev/', ''),
    ('procs', 'ps with readable columns, colour and search.', ['procs'], 'Optional',
     'procs', 'procs', 'procs', 'procs', 'https://github.com/dalance/procs', ''),
    ('dust', 'Shows which directories are actually using your disk.', ['dust'], 'Optional',
     'dust', 'du-dust', 'du-dust', 'dust', 'https://github.com/bootandy/dust',
     'The Debian, Ubuntu and Fedora package is named du-dust; the binary is still dust.'),
    ('duf', 'Readable df: free space per filesystem.', ['duf'], 'Optional',
     'duf', 'duf', 'duf', 'duf', 'https://github.com/muesli/duf', ''),
    ('lsof', 'Lists open files and sockets. How you find what is holding a port.', ['lsof'], 'Essential',
     '', 'lsof', 'lsof', 'lsof', 'https://github.com/lsof-org/lsof',
     'Already present on macOS. On Linux, ss -tlnp from iproute2 answers the same port question and is usually installed.'),
    ('hyperfine', 'Benchmarks commands with warmup runs and statistics.', ['hyperfine'], 'Optional',
     'hyperfine', 'hyperfine', 'hyperfine', 'hyperfine', 'https://github.com/sharkdp/hyperfine', ''),
    ('watchexec', 'Re-runs a command when files change.', ['watchexec'], 'Optional',
     'watchexec', '', 'watchexec', 'watchexec', 'https://github.com/watchexec/watchexec',
     'Not in the Debian or Ubuntu archives; use cargo install watchexec-cli or a release binary.'),
    ('trash', 'Deletes to the desktop trash instead of unlinking. A safer rm for interactive use.', ['trash'], 'Recommended',
     'trash', 'trash-cli', 'trash-cli', 'trash-cli', 'https://github.com/sindresorhus/trash-cli',
     'These are two different projects with the same idea. On Linux the command is usually trash-put.'),

    # --- Network ----------------------------------------------------------
    ('curl', 'Transfers data over HTTP and many other protocols.', ['curl'], 'Essential',
     'curl', 'curl', 'curl', 'curl', 'https://curl.se/docs/manpage.html', ''),
    ('wget', 'Downloads files, including recursive mirroring.', ['wget'], 'Optional',
     'wget', 'wget', 'wget', 'wget', 'https://www.gnu.org/software/wget/manual/', ''),
    ('xh', 'Friendly HTTP client for testing APIs. Prints headers and JSON readably.', ['xh'], 'Optional',
     'xh', '', 'xh', 'xh', 'https://github.com/ducaale/xh',
     'Not in the Debian or Ubuntu archives; use the release binary from the project page.'),

    # --- Editor and sessions ----------------------------------------------
    ('neovim', 'The editor the handbook assumes when it says "open the file".', ['nvim'], 'Recommended',
     'neovim', 'neovim', 'neovim', 'neovim', 'https://neovim.io/doc/',
     'Distribution packages lag upstream. If a plugin requires a newer Neovim, use the official AppImage or release archive.'),
    ('tmux', 'Keeps shell sessions alive across disconnects and splits one terminal into panes.', ['tmux'], 'Optional',
     'tmux', 'tmux', 'tmux', 'tmux', 'https://github.com/tmux/tmux/wiki', ''),

    # --- Language runtimes ------------------------------------------------
    ('uv', 'Installs Python versions, manages project environments and runs isolated CLI tools.', ['uv', 'uvx'], 'Recommended',
     'uv', '', '', 'uv', 'https://docs.astral.sh/uv/',
     'On Debian, Ubuntu and older Fedora, use the official installer at https://astral.sh/uv/install.sh after reading it.'),
    ('volta', 'Pins a Node and package-manager version per project, then switches automatically.', ['volta', 'node', 'npm'], 'Recommended',
     'volta', '', '', 'volta', 'https://docs.volta.sh/reference/',
     'On Debian, Ubuntu and Fedora, use the installer at https://get.volta.sh. Volta then installs Node itself: volta install node@22.'),
    ('go', 'The Go toolchain. Needed to build some of the tools listed here from source.', ['go'], 'Optional',
     'go', 'golang', 'golang', 'go', 'https://go.dev/doc/', ''),

    # --- Containers -------------------------------------------------------
    ('docker', 'Builds and runs containers. Provides docker and docker compose.', ['docker'], 'Optional',
     'docker', 'docker.io', 'moby-engine', 'docker', 'https://docs.docker.com/reference/cli/docker/',
     'On Linux the engine runs natively; enable it with sudo systemctl enable --now docker and add yourself to the docker group. On macOS the CLI needs a VM: see colima. Docker\'s own repository usually carries a newer engine than the distribution package.'),
    ('docker-compose', 'Runs multi-container projects from a compose.yaml file.', ['docker compose'], 'Optional',
     'docker-compose', 'docker-compose-v2', 'docker-compose', 'docker-compose', 'https://docs.docker.com/compose/',
     'This is the v2 plugin invoked as docker compose, with a space. The old docker-compose script is a separate, retired project.'),
    ('colima', 'Runs the Linux VM that Docker needs on macOS. macOS only.', ['colima'], 'Optional',
     'colima', '', '', '', 'https://github.com/abiosoft/colima',
     'macOS only, and not needed on Linux, where containers run on the host kernel. An alternative to Docker Desktop.'),
    ('lazydocker', 'Full-screen view of containers, logs and resource use.', ['lazydocker'], 'Optional',
     'lazydocker', '', '', 'lazydocker', 'https://github.com/jesseduffield/lazydocker',
     'Not in the Debian, Ubuntu or Fedora archives; use the release binary from the project page.'),
    ('dive', 'Inspects an image layer by layer to find what is making it large.', ['dive'], 'Optional',
     'dive', '', '', 'dive', 'https://github.com/wagoodman/dive',
     'Not in the Debian, Ubuntu or Fedora archives; the project publishes .deb and .rpm packages.'),
    ('hadolint', 'Lints Dockerfiles for common mistakes.', ['hadolint'], 'Optional',
     'hadolint', '', '', 'hadolint-bin', 'https://github.com/hadolint/hadolint',
     'Packaged on Arch via the AUR; elsewhere use the release binary from the project page.'),
    ('kubernetes-cli', 'Talks to a Kubernetes cluster. Provides kubectl.', ['kubectl'], 'Optional',
     'kubernetes-cli', 'kubectl', 'kubernetes-client', 'kubectl', 'https://kubernetes.io/docs/reference/kubectl/',
     'Debian and Ubuntu need the Kubernetes apt repository first; the documentation covers the steps.'),
    ('k9s', 'Full-screen Kubernetes browser for pods, logs and events.', ['k9s'], 'Optional',
     'k9s', '', '', 'k9s', 'https://k9scli.io/',
     'Not in the Debian, Ubuntu or Fedora archives; use the release binary from the project page.'),
    ('helm', 'Installs and upgrades packaged Kubernetes applications.', ['helm'], 'Optional',
     'helm', '', '', 'helm', 'https://helm.sh/docs/',
     'Debian and Ubuntu need the Helm apt repository; the documentation covers the steps.'),

    # --- Local AI ---------------------------------------------------------
    ('ollama', 'Downloads and runs language models locally.', ['ollama'], 'Optional',
     'ollama', '', '', 'ollama', 'https://ollama.com/',
     'On Debian, Ubuntu and Fedora, use the installer at https://ollama.com/install.sh after reading it. Models are large: check disk space first, and expect memory use in the same order as the model file.'),
    ('llama.cpp', 'Runs GGUF models directly. Provides llama-cli and llama-server.', ['llama-cli', 'llama-server'], 'Optional',
     'llama.cpp', '', '', 'llama.cpp', 'https://github.com/ggml-org/llama.cpp',
     'Most Linux users build it from source to match their GPU; the repository documents the build flags.'),

    # --- Media and documents ----------------------------------------------
    ('imagemagick', 'Converts, resizes and inspects images. Provides magick.', ['magick'], 'Optional',
     'imagemagick', 'imagemagick', 'ImageMagick', 'imagemagick', 'https://imagemagick.org/script/command-line-processing.php', ''),
    ('ghostscript', 'Processes PostScript and PDF. Provides gs.', ['gs'], 'Optional',
     'ghostscript', 'ghostscript', 'ghostscript', 'ghostscript', 'https://www.ghostscript.com/documentation/',
     'If you alias gs to git status, the alias wins. Call the full path to reach Ghostscript.'),
    ('tesseract', 'Extracts text from images (OCR).', ['tesseract'], 'Optional',
     'tesseract', 'tesseract-ocr', 'tesseract', 'tesseract', 'https://tesseract-ocr.github.io/',
     'Each language is a separate data package, for example tesseract-ocr-deu on Debian and Ubuntu.'),
]

# Terminal emulators and fonts are chosen, not required. Kept separate so the
# handbook can say so plainly rather than listing them beside real dependencies.
EXTRAS = [
    ('A terminal emulator', 'Ghostty, WezTerm, Kitty and Alacritty are all GPU-accelerated and cross-platform. macOS Terminal, GNOME Console and Konsole run every command here too.',
     'https://ghostty.org/'),
    ('A Nerd Font', 'Only needed if you want icons in a prompt or file listing. JetBrainsMono Nerd Font is a safe default. Install it, then select it in your terminal settings.',
     'https://www.nerdfonts.com/'),
    ('A prompt', 'Starship and Oh My Posh both show Git state, runtime versions and exit status. Entirely optional: the handbook never depends on your prompt.',
     'https://starship.rs/'),
]


def _tool(row):
    name, description, commands, tier, brew, apt, dnf, pacman, url, note = row
    return dict(name=name, description=description, commands=commands, tier=tier, url=url,
                note=note, install=dict(brew=brew, apt=apt, dnf=dnf, pacman=pacman))


TOOLS = [_tool(row) for row in _TOOLS]
