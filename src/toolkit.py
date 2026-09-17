"""The toolkit the command library assumes, with install commands per platform.

Every entry names the executables it provides so a reader can check what they
already have with `command -v NAME` before installing anything. Linux package
names differ from Homebrew formula names more often than people expect, and a
few packages install the binary under a different name, which the entry's `note`
says explicitly.

`tier` separates what the handbook depends on from what it merely mentions:

  Essential  - the command library breaks without it
  Recommended- used by several examples; worth installing early
  Optional   - used by one topic (containers, local AI, media)
"""

# Package managers, in the order the README presents them. The last field is the
# key into each tool's `install` dict, so the page builds every install command
# from this one table rather than repeating the flags per tool.
MANAGERS = [
    ('macOS', 'Homebrew', 'brew install', 'https://brew.sh', 'brew'),
    ('Debian / Ubuntu', 'apt', 'sudo apt install -y', 'https://wiki.debian.org/Apt', 'apt'),
    ('Fedora / RHEL', 'dnf', 'sudo dnf install -y', 'https://dnf.readthedocs.io/', 'dnf'),
    ('Arch', 'pacman', 'sudo pacman -S --needed', 'https://wiki.archlinux.org/title/Pacman', 'pacman'),
]


def tool(name, tier, description, commands, url, brew, apt=None, dnf=None, pacman=None, note=''):
    """One entry in the toolkit.

    `brew` is the Homebrew formula. `apt`, `dnf` and `pacman` default to that
    same name, which is right for most tools; pass a different name where the
    distribution uses one, or `''` where there is no standard package and the
    note explains the alternative.
    """
    return dict(
        name=name, tier=tier, description=description, commands=commands, url=url, note=note,
        install=dict(brew=brew,
                     apt=brew if apt is None else apt,
                     dnf=brew if dnf is None else dnf,
                     pacman=brew if pacman is None else pacman),
    )

TOOLS = [
    # --- Shell and prompt -------------------------------------------------
    tool('zsh', 'Essential', 'The shell every example in this handbook is written for.',
         commands=['zsh'], url='https://zsh.sourceforge.io/Doc/Release/',
         brew='zsh',
         note='Default on macOS since Catalina. On Linux, install it and then run chsh -s '
              '"$(command -v zsh)" to make it your login shell.'),
    tool('zsh-autosuggestions', 'Recommended',
         'Suggests the rest of a command from your history as you type.',
         commands=[], url='https://github.com/zsh-users/zsh-autosuggestions',
         brew='zsh-autosuggestions',
         note='A plugin, not a command. It has to be sourced from your .zshrc; the package '
              'description prints the path to source.'),
    tool('zsh-syntax-highlighting', 'Recommended',
         'Colours a command line as valid or invalid before you press Enter.',
         commands=[], url='https://github.com/zsh-users/zsh-syntax-highlighting',
         brew='zsh-syntax-highlighting',
         note='Source it last in your .zshrc, after every other plugin, or it will not see '
              'later keybindings.'),
    tool('direnv', 'Optional',
         'Loads and unloads environment variables when you enter or leave a directory.',
         commands=['direnv'], url='https://direnv.net/',
         brew='direnv',
         note='Needs a shell hook in your .zshrc. It executes .envrc files, so only allow '
              'them in repositories you trust.'),
    # --- Navigation and reading ------------------------------------------
    tool('fzf', 'Essential', 'Fuzzy finder. Provides Ctrl+R history search and Ctrl+T file search.',
         commands=['fzf'], url='https://github.com/junegunn/fzf',
         brew='fzf',
         note='The key bindings are a separate setup step; see the project README for the '
              'line to add to your .zshrc.'),
    tool('zoxide', 'Essential',
         'Directory jumper that learns where you actually work. Provides z and zi.',
         commands=['zoxide', 'z', 'zi'], url='https://github.com/ajeetdsouza/zoxide',
         brew='zoxide',
         note='Needs eval "$(zoxide init zsh)" in your .zshrc. Older Debian and Ubuntu '
              'releases ship a version without zi.'),
    tool('fd', 'Essential', 'Fast, sensible file finder. A friendlier front end than find.',
         commands=['fd'], url='https://github.com/sharkdp/fd',
         brew='fd', apt='fd-find', dnf='fd-find',
         note='On Debian and Ubuntu the binary is installed as fdfind; alias fd=fdfind or '
              'symlink it.'),
    tool('ripgrep', 'Essential', 'Fast recursive content search that respects .gitignore.',
         commands=['rg'], url='https://github.com/BurntSushi/ripgrep',
         brew='ripgrep'),
    tool('eza', 'Recommended',
         'Modern ls replacement with colours, icons, tree view and Git status.',
         commands=['eza'], url='https://github.com/eza-community/eza',
         brew='eza',
         note='Not in older Debian and Ubuntu archives; the project documents an apt '
              'repository for those releases.'),
    tool('bat', 'Recommended', 'cat with syntax highlighting, line numbers and paging.',
         commands=['bat'], url='https://github.com/sharkdp/bat',
         brew='bat',
         note='On Debian and Ubuntu the binary is installed as batcat; alias bat=batcat or '
              'symlink it.'),
    tool('tree', 'Optional', 'Prints a directory as an indented tree.',
         commands=['tree'], url='https://oldmanprogrammer.net/source.php?dir=projects/tree',
         brew='tree'),
    tool('glow', 'Optional', 'Renders Markdown readably in the terminal.',
         commands=['glow'], url='https://github.com/charmbracelet/glow',
         brew='glow',
         note='Packaged on Arch and Fedora; on Debian and Ubuntu use the Charm apt '
              'repository or a release binary.'),
    tool('tealdeer', 'Recommended',
         'Fast client for tldr, the community cheat sheets. Provides tldr.',
         commands=['tldr'], url='https://github.com/tealdeer-rs/tealdeer',
         brew='tealdeer',
         note='Run tldr --update once after installing to fetch the page cache.'),
    # --- Text and data ----------------------------------------------------
    tool('jq', 'Essential', 'Query and reshape JSON on the command line.',
         commands=['jq'], url='https://jqlang.github.io/jq/manual/',
         brew='jq'),
    tool('yq', 'Recommended', 'The same idea as jq, for YAML, TOML and XML.',
         commands=['yq'], url='https://mikefarah.gitbook.io/yq/',
         brew='yq', apt='', dnf='', pacman='go-yq',
         note='Debian, Ubuntu and Fedora package a different, Python-based yq. For the Go yq '
              'used here, install the release binary from the project page.'),
    tool('jless', 'Optional',
         'Pager for large JSON documents. Fold, search and navigate instead of scrolling.',
         commands=['jless'], url='https://jless.io/',
         brew='jless', apt='', dnf='',
         note='Not packaged on Debian, Ubuntu or Fedora; install with cargo install jless or '
              'a release binary.'),
    tool('sd', 'Optional',
         'Find and replace with plain syntax. An easier sed for simple substitutions.',
         commands=['sd'], url='https://github.com/chmln/sd',
         brew='sd', dnf='rust-sd',
         note='sd rewrites files in place. Preview with ripgrep first; it has no undo.'),
    tool('tokei', 'Optional', 'Counts lines of code by language.',
         commands=['tokei'], url='https://github.com/XAMPPRocky/tokei',
         brew='tokei'),
    # --- Git --------------------------------------------------------------
    tool('git', 'Essential', 'Version control. The handbook assumes a recent version.',
         commands=['git'], url='https://git-scm.com/docs',
         brew='git',
         note='macOS ships an Xcode version of Git. Installing it via Homebrew keeps it '
              'current.'),
    tool('gh', 'Recommended', 'GitHub from the terminal: pull requests, issues, releases, CI runs.',
         commands=['gh'], url='https://cli.github.com/manual/',
         brew='gh', pacman='github-cli',
         note='Debian, Ubuntu and Fedora need the GitHub apt/dnf repository first; the '
              'manual documents the exact steps.'),
    tool('git-delta', 'Recommended', 'Readable, syntax-highlighted diffs for git diff and git log.',
         commands=['delta'], url='https://dandavison.github.io/delta/',
         brew='git-delta',
         note='Configure it as your pager in .gitconfig; installing alone changes nothing.'),
    tool('git-lfs', 'Optional', 'Stores large binary files outside the Git history.',
         commands=['git-lfs'], url='https://git-lfs.com/',
         brew='git-lfs',
         note='Run git lfs install once per machine after installing.'),
    tool('lazygit', 'Optional', 'Full-screen Git interface for staging hunks and reading history.',
         commands=['lazygit'], url='https://github.com/jesseduffield/lazygit',
         brew='lazygit', apt='',
         note='Not in the Debian or Ubuntu archives; use the release binary from the project '
              'page.'),
    # --- Inspecting a running system --------------------------------------
    tool('btop', 'Recommended', 'Resource monitor for CPU, memory, disks, network and processes.',
         commands=['btop'], url='https://github.com/aristocratos/btop',
         brew='btop'),
    tool('htop', 'Optional', 'The classic interactive process viewer.',
         commands=['htop'], url='https://htop.dev/',
         brew='htop'),
    tool('procs', 'Optional', 'ps with readable columns, colour and search.',
         commands=['procs'], url='https://github.com/dalance/procs',
         brew='procs'),
    tool('dust', 'Optional', 'Shows which directories are actually using your disk.',
         commands=['dust'], url='https://github.com/bootandy/dust',
         brew='dust', apt='du-dust', dnf='du-dust',
         note='The Debian, Ubuntu and Fedora package is named du-dust; the binary is still '
              'dust.'),
    tool('duf', 'Optional', 'Readable df: free space per filesystem.',
         commands=['duf'], url='https://github.com/muesli/duf',
         brew='duf'),
    tool('lsof', 'Essential', 'Lists open files and sockets. How you find what is holding a port.',
         commands=['lsof'], url='https://github.com/lsof-org/lsof',
         brew='', apt='lsof', dnf='lsof', pacman='lsof',
         note='Already present on macOS. On Linux, ss -tlnp from iproute2 answers the same '
              'port question and is usually installed.'),
    tool('hyperfine', 'Optional', 'Benchmarks commands with warmup runs and statistics.',
         commands=['hyperfine'], url='https://github.com/sharkdp/hyperfine',
         brew='hyperfine'),
    tool('watchexec', 'Optional', 'Re-runs a command when files change.',
         commands=['watchexec'], url='https://github.com/watchexec/watchexec',
         brew='watchexec', apt='',
         note='Not in the Debian or Ubuntu archives; use cargo install watchexec-cli or a '
              'release binary.'),
    tool('trash', 'Recommended',
         'Deletes to the desktop trash instead of unlinking. A safer rm for interactive use.',
         commands=['trash'], url='https://github.com/sindresorhus/trash-cli',
         brew='trash', apt='trash-cli', dnf='trash-cli', pacman='trash-cli',
         note='These are two different projects with the same idea. On Linux the command is '
              'usually trash-put.'),
    # --- Network ----------------------------------------------------------
    tool('curl', 'Essential', 'Transfers data over HTTP and many other protocols.',
         commands=['curl'], url='https://curl.se/docs/manpage.html',
         brew='curl'),
    tool('wget', 'Optional', 'Downloads files, including recursive mirroring.',
         commands=['wget'], url='https://www.gnu.org/software/wget/manual/',
         brew='wget'),
    tool('xh', 'Optional',
         'Friendly HTTP client for testing APIs. Prints headers and JSON readably.',
         commands=['xh'], url='https://github.com/ducaale/xh',
         brew='xh', apt='',
         note='Not in the Debian or Ubuntu archives; use the release binary from the project '
              'page.'),
    # --- Editor and sessions ----------------------------------------------
    tool('neovim', 'Recommended', 'The editor the handbook assumes when it says "open the file".',
         commands=['nvim'], url='https://neovim.io/doc/',
         brew='neovim',
         note='Distribution packages lag upstream. If a plugin requires a newer Neovim, use '
              'the official AppImage or release archive.'),
    tool('tmux', 'Optional',
         'Keeps shell sessions alive across disconnects and splits one terminal into panes.',
         commands=['tmux'], url='https://github.com/tmux/tmux/wiki',
         brew='tmux'),
    # --- Language runtimes ------------------------------------------------
    tool('uv', 'Recommended',
         'Installs Python versions, manages project environments and runs isolated CLI tools.',
         commands=['uv', 'uvx'], url='https://docs.astral.sh/uv/',
         brew='uv', apt='', dnf='',
         note='On Debian, Ubuntu and older Fedora, use the official installer at '
              'https://astral.sh/uv/install.sh after reading it.'),
    tool('volta', 'Recommended',
         'Pins a Node and package-manager version per project, then switches automatically.',
         commands=['volta', 'node', 'npm'], url='https://docs.volta.sh/reference/',
         brew='volta', apt='', dnf='',
         note='On Debian, Ubuntu and Fedora, use the installer at https://get.volta.sh. '
              'Volta then installs Node itself: volta install node@22.'),
    tool('go', 'Optional',
         'The Go toolchain. Needed to build some of the tools listed here from source.',
         commands=['go'], url='https://go.dev/doc/',
         brew='go', apt='golang', dnf='golang'),
    # --- Containers -------------------------------------------------------
    tool('docker', 'Optional', 'Builds and runs containers. Provides docker and docker compose.',
         commands=['docker'], url='https://docs.docker.com/reference/cli/docker/',
         brew='docker', apt='docker.io', dnf='moby-engine',
         note="On Linux the engine runs natively; enable it with sudo systemctl enable --now "
              "docker and add yourself to the docker group. On macOS the CLI needs a VM: see "
              "colima. Docker's own repository usually carries a newer engine than the "
              "distribution package."),
    tool('docker-compose', 'Optional', 'Runs multi-container projects from a compose.yaml file.',
         commands=['docker compose'], url='https://docs.docker.com/compose/',
         brew='docker-compose', apt='docker-compose-v2',
         note='This is the v2 plugin invoked as docker compose, with a space. The old '
              'docker-compose script is a separate, retired project.'),
    tool('colima', 'Optional', 'Runs the Linux VM that Docker needs on macOS. macOS only.',
         commands=['colima'], url='https://github.com/abiosoft/colima',
         brew='colima', apt='', dnf='', pacman='',
         note='macOS only, and not needed on Linux, where containers run on the host kernel. '
              'An alternative to Docker Desktop.'),
    tool('lazydocker', 'Optional', 'Full-screen view of containers, logs and resource use.',
         commands=['lazydocker'], url='https://github.com/jesseduffield/lazydocker',
         brew='lazydocker', apt='', dnf='',
         note='Not in the Debian, Ubuntu or Fedora archives; use the release binary from the '
              'project page.'),
    tool('dive', 'Optional', 'Inspects an image layer by layer to find what is making it large.',
         commands=['dive'], url='https://github.com/wagoodman/dive',
         brew='dive', apt='', dnf='',
         note='Not in the Debian, Ubuntu or Fedora archives; the project publishes .deb and '
              '.rpm packages.'),
    tool('hadolint', 'Optional', 'Lints Dockerfiles for common mistakes.',
         commands=['hadolint'], url='https://github.com/hadolint/hadolint',
         brew='hadolint', apt='', dnf='', pacman='hadolint-bin',
         note='Packaged on Arch via the AUR; elsewhere use the release binary from the '
              'project page.'),
    tool('kubernetes-cli', 'Optional', 'Talks to a Kubernetes cluster. Provides kubectl.',
         commands=['kubectl'], url='https://kubernetes.io/docs/reference/kubectl/',
         brew='kubernetes-cli', apt='kubectl', dnf='kubernetes-client', pacman='kubectl',
         note='Debian and Ubuntu need the Kubernetes apt repository first; the documentation '
              'covers the steps.'),
    tool('k9s', 'Optional', 'Full-screen Kubernetes browser for pods, logs and events.',
         commands=['k9s'], url='https://k9scli.io/',
         brew='k9s', apt='', dnf='',
         note='Not in the Debian, Ubuntu or Fedora archives; use the release binary from the '
              'project page.'),
    tool('helm', 'Optional', 'Installs and upgrades packaged Kubernetes applications.',
         commands=['helm'], url='https://helm.sh/docs/',
         brew='helm', apt='', dnf='',
         note='Debian and Ubuntu need the Helm apt repository; the documentation covers the '
              'steps.'),
    # --- Local AI ---------------------------------------------------------
    tool('ollama', 'Optional', 'Downloads and runs language models locally.',
         commands=['ollama'], url='https://ollama.com/',
         brew='ollama', apt='', dnf='',
         note='On Debian, Ubuntu and Fedora, use the installer at '
              'https://ollama.com/install.sh after reading it. Models are large: check disk '
              'space first, and expect memory use in the same order as the model file.'),
    tool('llama.cpp', 'Optional', 'Runs GGUF models directly. Provides llama-cli and llama-server.',
         commands=['llama-cli', 'llama-server'], url='https://github.com/ggml-org/llama.cpp',
         brew='llama.cpp', apt='', dnf='',
         note='Most Linux users build it from source to match their GPU; the repository '
              'documents the build flags.'),
    # --- Media and documents ----------------------------------------------
    tool('imagemagick', 'Optional', 'Converts, resizes and inspects images. Provides magick.',
         commands=['magick'], url='https://imagemagick.org/script/command-line-processing.php',
         brew='imagemagick', dnf='ImageMagick'),
    tool('ghostscript', 'Optional', 'Processes PostScript and PDF. Provides gs.',
         commands=['gs'], url='https://www.ghostscript.com/documentation/',
         brew='ghostscript',
         note='If you alias gs to git status, the alias wins. Call the full path to reach '
              'Ghostscript.'),
    tool('tesseract', 'Optional', 'Extracts text from images (OCR).',
         commands=['tesseract'], url='https://tesseract-ocr.github.io/',
         brew='tesseract', apt='tesseract-ocr',
         note='Each language is a separate data package, for example tesseract-ocr-deu on '
              'Debian and Ubuntu.'),
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

