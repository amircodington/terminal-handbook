"""The handbook content: worked examples, workflows, shortcuts and lessons.

Each row is `title | command | explanation | level | effect`, with ` ;; ` marking a
line break inside a command. A command may contain literal pipes; an explanation
may not (see `rows`). `effect` drives the badge colour in the page, so it has to
stay honest: Inspect reads, Write touches the filesystem, Disruptive stops
something running, Destructive cannot be undone.

The category label that shares a row block also picks the fallback documentation
link for every row in it; build.py refines that per command where it can.

Examples use placeholder paths such as ~/projects/your-app. Replace them.
"""
import re

_IDS = set()
RECIPES = []


def slug(text):
    """A stable id for a recipe, so saved bookmarks survive new rows landing above."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def rows(category, source, text):
    """Parse one block of `title | command | explanation | level | effect` rows.

    The command may contain literal pipes: the title is split from the left and
    the last three fields from the right, so everything between them is the
    command. The explanation must not contain ` | ` for the same reason.
    """
    for line in text.strip().splitlines():
        if not line.strip():
            continue
        title, remainder = line.split(' | ', 1)
        command, explanation, level, effect = remainder.rsplit(' | ', 3)
        recipe_id = f'{slug(category)}-{slug(title)}'
        assert recipe_id not in _IDS, f'duplicate recipe id: {recipe_id}'
        _IDS.add(recipe_id)
        RECIPES.append(dict(id=recipe_id, category=category, title=title,
                            command=command.replace(' ;; ', '\n'),
                            explanation=explanation, level=level, effect=effect, source=source))

rows('Shell foundations', 'https://zsh.sourceforge.io/Doc/Release/',r'''
Know where you are | pwd | Print your current directory before running project commands. Relative paths start here. | Start | Inspect
Find what a command really is | whence -va python3 pnpm git ls | Shows aliases, functions and every executable match, in the order zsh would pick them. This is how you discover that ls is really an alias for eza. | Start | Inspect
Read your PATH | print -l -- $path | zsh exposes PATH as an array. The first matching executable wins. | Start | Inspect
Learn the command you already have | man zshbuiltins | Local manuals match the installed operating system. Press / to search and q to quit. | Start | Inspect
Inspect an alias | alias gs | gs expands to git status. Run alias with no arguments to list aliases. | Start | Inspect
Inspect a shell function | functions precmd | Read a function's implementation before relying on it. Run functions with no arguments to list every function your shell has defined. | Intermediate | Inspect
Look up recent commands | fc -l -20 | Read the last 20 history entries. Ctrl+R opens your fuzzy history picker. | Start | Inspect
Quote paths with spaces | ls -ld "$HOME/Library/Application Support" | Double quotes preserve spaces and expand variables. Single quotes preserve literal text. | Start | Inspect
Capture command output | project_root=$(git rev-parse --show-toplevel) ;; print -r -- "$project_root" | Command substitution captures stdout. Use this inside a Git repository. | Intermediate | Inspect
Act only after success | pnpm lint && pnpm typecheck | && runs the second command only if the first exits successfully. Run in a project with both scripts. | Intermediate | Run
Count tracked source files | git ls-files '*.ts' '*.tsx' | Count or inspect tracked files without searching node_modules. Add a pipe to wc -l for the count. | Intermediate | Inspect
Build a pipeline | git ls-files '*.ts' '*.tsx' | wc -l | A pipe sends one command's stdout into the next. This counts tracked TypeScript files without walking node_modules. | Intermediate | Inspect
Understand pipe failures | (setopt pipefail; false | cat; print -r -- "exit=$?") | Without pipefail, cat succeeds and hides the failure from false, so the pipeline reports success. The subshell keeps the option local. | Advanced | Run
Inspect a pipeline's statuses | printf 'hello\n' | wc -c | Every command returns an exit status, where 0 means success. Immediately after a pipeline, print -l -- $pipestatus shows the status of each stage. | Intermediate | Run
Write output without clobbering | printf '%s\n' 'hello' > terminal-practice.txt | If you have set NO_CLOBBER (setopt noclobber), > refuses to replace an existing file. Use a fresh filename. | Start | Write
Append a line | printf '%s\n' 'another line' >> terminal-practice.txt | >> appends. Use >| only when you deliberately want to overwrite despite NO_CLOBBER. | Start | Write
Keep spaces safe when iterating | for file in *.md(N); do print -r -- "$file"; done | (N) makes an unmatched zsh glob expand to nothing. Quote the variable on use. | Advanced | Inspect
See shell jobs | jobs -l | Ctrl+Z suspends a foreground job; fg resumes it. Ctrl+C asks the foreground process to stop. | Start | Inspect
Resume a suspended job | fg | Return the most recently suspended shell job to the foreground. | Start | Run
Check shell syntax | zsh -n ~/.zshrc | Parse the config without executing it. This catches syntax errors, not every runtime problem. | Intermediate | Inspect
Start a clean shell | zsh -f | Start a shell without your normal startup files. Type exit to leave. Useful for isolating config bugs. | Intermediate | Run
Show completion paths | print -l -- $fpath | These directories contain completion functions, including Homebrew's site-functions directory. | Intermediate | Inspect
Open this handbook | open index.html | Opens the handbook in your browser. It is a single file and works offline. On Linux, use xdg-open index.html. | Start | Run
''')

rows('Find & navigate', 'https://github.com/sharkdp/fd',r'''
Save a jump as an alias | alias work='cd ~/projects' | An alias is a saved command. Add the line to your .zshrc to keep it after this session, then open a new shell. | Start | Run
Jump by remembered name | z your-app | zoxide learns visited directories. zi opens an interactive picker. Visit the directory with cd first if it is unknown. | Start | Run
See files with Git status | eza -lah --git --icons=auto | A detailed directory listing. Your ll alias does the same with icons always enabled. | Start | Inspect
Explore a small tree | eza --tree --level=2 --git-ignore | Keep output shallow. --git-ignore removes entries ignored by Git. | Start | Inspect
Find files by name | fd -e ts -e tsx | fd respects ignore files by default. It searches names, while rg searches file contents. | Start | Inspect
Find hidden config files | fd --hidden --exclude .git '^\.env' | Lists names only; avoids printing secrets stored inside environment files. | Intermediate | Inspect
Find directories | fd --type d 'components' | Narrow by type to locate component directories quickly. | Start | Inspect
Find text in source | rg -n 'TODO|FIXME' -g '*.{ts,tsx,php,py}' | Show line numbers for matching source files. Quoting prevents the shell from interpreting the pattern. | Start | Inspect
Search literal punctuation | rg -n -F 'process.env.' | -F treats the pattern as literal text, rather than a regular expression. | Start | Inspect
List matching files only | rg -l 'use client' -g '*.tsx' | Useful before opening files in your editor. -l prints each matching filename once. | Intermediate | Inspect
Count matches | rg -c 'TODO' -g '*.ts' | Counts matching lines per file. Use --count-matches to count individual matches instead. | Intermediate | Inspect
Search an ignored file deliberately | rg --no-ignore -n 'pattern' path/to/file | Replace the example path and pattern. Scope this tightly; searching every dependency is usually noise. | Intermediate | Inspect
Choose a file interactively | fzf | Your fd default feeds ignored-aware file names into fzf. Ctrl+T inserts a selected path into the current command. | Start | Inspect
Jump with a directory picker | zi | Interactive zoxide selector for directories you have already visited. Alt+C is fzf's directory picker. | Start | Run
Inspect file with highlighting | bat --paging=never package.json | bat adds highlighting. ccat is your alias; ordinary cat remains available for scripts. | Start | Inspect
Read just part of a file | bat --line-range 1:100 package.json | Useful when reviewing a large source file or config. | Start | Inspect
Plain portable directory tree | tree -L 2 -I 'node_modules|vendor|.git' | tree is also installed. The exclusion expression prevents huge dependency listings. | Start | Inspect
Count your codebase | tokei . --exclude node_modules --exclude vendor | Shows source line counts by language. Size is a navigation aid, not a quality score. | Intermediate | Inspect
''')

rows('Git & GitHub', 'https://git-scm.com/docs',r'''
Understand current changes | git status --short --branch | Your gss alias gives short status; gs gives the detailed version. | Start | Inspect
Review unstaged changes | git diff | delta is already your configured pager. q exits; n and N navigate files when navigation is active. | Start | Inspect
Review what will be committed | git diff --staged | Always check staged content before committing. gds is your alias. | Start | Inspect
Stage only intended hunks | git add -p | Review and select individual changes. Type ? at a hunk prompt for the available choices. | Intermediate | Write
Make a focused commit | git commit -m "Explain the behavior changed" | Commit the staged changes with a concrete message. Replace the example message. | Start | Write
Start a feature branch | git switch -c feature/terminal-practice | Creates and switches to a branch. Choose a name appropriate to the actual change. | Start | Write
See recent history | git log --oneline --graph --decorate -15 | Your glog alias shows a similar graph. A compact history helps before a rebase or merge. | Start | Inspect
Fetch remote changes | git fetch --prune | Updates remote-tracking refs and prunes stale ones. It does not merge into your working branch. | Intermediate | Write
Understand upstream differences | git log --oneline --left-right HEAD...@{upstream} | Requires a configured upstream. Left entries are local-only; right entries are upstream-only. | Intermediate | Inspect
Unstage without losing edits | git restore --staged path/to/file | Replace the example path. This changes the index and preserves working-tree content. | Start | Write
Discard a file's local edits | git restore -- path/to/file | Replaces uncommitted working-tree content. Inspect git diff first; ordinary Git may not recover these edits. | Intermediate | Destructive
Find when a line changed | git blame -L 1,60 -- path/to/file | Replace the path. Follow up with git show COMMIT to understand the reason for a change. | Intermediate | Inspect
Search the history of a string | git log -S 'functionName' --oneline --all | Finds commits that change the number of occurrences of the string. Use -G for regex diff matching. | Advanced | Inspect
Recover a moved branch tip | git reflog --date=relative -20 | Read recent ref movements before trying recovery. Create a rescue branch from the desired commit. | Advanced | Inspect
Create a parallel checkout | git worktree add ../project-review -b review/local | Adds a separate checkout and new branch without disturbing current work. Run inside the intended repo. | Advanced | Write
List parallel checkouts | git worktree list | Useful when reviewing work while a development server runs in another checkout. | Intermediate | Inspect
Check whitespace errors | git diff --check | Detects whitespace problems and conflict markers in changes. | Intermediate | Inspect
Use a Git dashboard | lazygit | Interactive status, hunk staging, history and branches. Read on-screen bindings before performing actions. | Start | Run
Inspect large-file tracking | git lfs ls-files | Lists files tracked by Git LFS. LFS stores pointers in Git and file content separately. | Intermediate | Inspect
Check GitHub login | gh auth status | Reports authentication status without requesting token output. | Start | Inspect
List your pull requests | gh pr list --author @me | Run in the relevant GitHub repository. | Start | Inspect
Review a pull request locally | gh pr diff 123 | Replace 123 with a real PR number; prints its patch. | Intermediate | Inspect
Check CI for a PR | gh pr checks 123 | Shows check status. Use gh run list to explore recent workflow runs. | Intermediate | Inspect
Inspect failed CI logs | gh run view RUN_ID --log-failed | Replace RUN_ID with a real run ID from gh run list. Logs may contain sensitive project details. | Intermediate | Inspect
Create a draft PR | gh pr create --draft | Opens an interactive draft-PR flow and sends content to GitHub. Review title, body and target branch. | Intermediate | Remote write
''')

rows('Web development', 'https://pnpm.io/cli/run',r'''
Check runtime selection | volta list | Shows the default Node and the tools Volta manages. Without Volta, use node --version and which -a node. | Start | Inspect
See the actual Node binary | volta which node | Shows the executable Volta would select in the current project. | Intermediate | Inspect
List project scripts | pnpm run | With no script, pnpm lists the scripts declared in package.json. Use this before assuming test or dev exists. | Start | Inspect
Install the locked dependencies | pnpm install --frozen-lockfile | Run in a pnpm project with a current lockfile. Refuses changes to the lockfile; installs dependencies. | Intermediate | Write
Start a development server | cd ~/projects/your-app ;; pnpm dev | Starts the project's dev script. Databases and environment variables still need to be available. Ctrl+C stops it. | Start | Run
Match the project's package manager | ls pnpm-lock.yaml package-lock.json yarn.lock 2>/dev/null | The lockfile tells you which package manager the project uses. Mixing them produces inconsistent installs. | Start | Inspect
Check types | pnpm typecheck | Runs TypeScript without emitting JavaScript, if the project declares the script. pnpm run lists what exists. | Start | Run
Lint project code | pnpm lint | Runs the project's linter. Fix the underlying issue rather than suppressing the rule globally. | Start | Run
Build for production | pnpm build | Runs the project's build, writing output such as .next. A build can require services and environment variables. | Intermediate | Run
Run unit tests | pnpm test | Executes the project's test script. Read package.json to see which runner it uses. | Intermediate | Run
Run browser tests | pnpm test:e2e | Runs end-to-end tests where the project declares them. Browsers, test data and a running server usually have to be set up first. | Intermediate | Run
Explain a dependency | pnpm why react | Find which dependency brings a package into the graph. Better than adding duplicate global packages. | Intermediate | Inspect
Inspect direct versions | pnpm list --depth 0 | Lists top-level packages in the current project. | Start | Inspect
Inspect outdated dependencies | pnpm outdated | Read the available versions before choosing an upgrade. A nonzero exit can indicate outdated packages. | Intermediate | Inspect
Use a project executable | pnpm exec tsc --noEmit | Runs the locally installed executable. It does not install a new CLI like pnpm dlx may do. | Intermediate | Run
Pin Node intentionally | volta pin node@22 | Writes a Volta pin into package.json so everyone on the project gets that Node. Agree on it with the repository first. | Advanced | Write
Run any declared script | pnpm run build:types | Replace build:types with a script from pnpm run. Generated output is written into the project. | Intermediate | Write
Inspect npm globals | npm list -g --depth=0 | A diagnostic inventory. Keep application dependencies in their projects. | Intermediate | Inspect
''')

rows('Containers & WordPress', 'https://docs.docker.com/reference/cli/docker/compose/',r'''
Check the VM (macOS) | colima status | On macOS, Docker needs a Linux VM. Colima reports its CPU, memory and mount settings. On Linux there is no VM: containers use the host kernel. | Start | Inspect
Check Docker's destination | docker context show | Shows which engine your docker commands reach. A context name is not proof that anything is running. | Start | Inspect
List Docker contexts | docker context ls | Verify the target before running commands, especially if remote contexts are added later. | Intermediate | Inspect
Start the container VM (macOS) | colima start | Starts the Colima profile. It does not start your project stacks. The Linux equivalent is sudo systemctl start docker. | Start | Run
Stop the container VM (macOS) | colima stop | Stops every container in that VM. Useful when you want the memory back for something else; save running work first. | Intermediate | Disruptive
List running containers | docker ps | Add -a to include stopped containers. Nothing running is a valid result. | Start | Inspect
See project service names | docker compose config --services | Run from the compose directory. Unlike full config output, this does not print interpolated environment secrets. | Start | Inspect
Validate Compose config | docker compose config --quiet | Checks the project's resolved configuration without printing it. | Intermediate | Inspect
Start a WordPress site | cd ~/projects/your-wordpress-site ;; docker compose up -d | Starts the project's services, downloading images and creating volumes if needed. The site's .env has to be configured first. | Start | Run
Check one site's status | docker compose ps | Run from that site's directory. | Start | Inspect
Follow recent site logs | docker compose logs --tail=100 -f wordpress | Ctrl+C leaves the log stream without stopping the containers. Logs can contain request details. | Start | Inspect
Check WordPress plugins | docker compose exec wpcli wp plugin list | Assumes the stack defines a wpcli service. Running WP-CLI in the container keeps the PHP and WordPress versions aligned with the site. | Start | Inspect
Check WordPress core | docker compose exec wpcli wp core version | Runs in the matching container environment, avoiding global PHP-version drift. | Start | Inspect
List WordPress options selectively | docker compose exec wpcli wp option get siteurl | Query one known option; avoid dumping all options, which can contain secrets. | Intermediate | Inspect
Preview a URL migration | docker compose exec wpcli wp search-replace 'https://old.example' 'https://new.example' --all-tables-with-prefix --skip-columns=guid --dry-run | Replace the example URLs. Keep --dry-run until you have reviewed the result and backed up the database. | Advanced | Inspect
Export a WordPress database | docker compose exec wpcli wp db export db-seed/manual-backup.sql | Writes a potentially sensitive SQL backup to the mounted db-seed directory. Choose a new filename and keep it out of Git. | Intermediate | Write
Stop a project, keep its data | docker compose stop | Stops containers without removing them or volumes. up -d starts them again. | Start | Disruptive
Remove stopped project containers | docker compose down | Removes project containers and networks. Do not add --volumes unless deliberately deleting database volumes. | Intermediate | Disruptive
Inspect Docker disk use | docker system df -v | Reports images, containers, volumes and cache. Reclaimable volumes may still hold important databases. | Intermediate | Inspect
Inspect live container resources | docker stats --no-stream | Takes a single CPU/memory snapshot of running containers. | Intermediate | Inspect
Inspect image layers | dive IMAGE:TAG | Replace IMAGE:TAG with an image listed by docker image ls. Helps find oversized layers. | Advanced | Inspect
Lint a Dockerfile | hadolint Dockerfile | Runs the installed Dockerfile linter on the local file. | Intermediate | Inspect
Inspect the build engine | docker buildx ls | Lists builders and platforms before a multi-platform build. | Intermediate | Inspect
Docker dashboard | lazydocker | Interactive container/log/resource UI. It includes actions that can stop or remove workloads. | Start | Run
Inspect Kubernetes context | kubectl config current-context | Tells you which cluster the next kubectl command would hit. An error here usually means no kubeconfig, not a broken install. | Intermediate | Inspect
Inspect Kubernetes workloads | kubectl get pods -A | Contacts the active cluster and lists pods in every namespace. Check the context before you run it. | Intermediate | Inspect
List Helm releases | helm list --all-namespaces | Read-only cluster query; requires a configured reachable Kubernetes cluster. | Intermediate | Inspect
Kubernetes dashboard | k9s --readonly | Opens the read-only dashboard for the selected context. | Advanced | Inspect
''')

rows('Python & local AI', 'https://docs.astral.sh/uv/',r'''
List installed Python runtimes | uv python list --only-installed | A machine usually has several Pythons: the system one, a package-manager one and uv's. They are not interchangeable. | Start | Inspect
List isolated Python tools | uv tool list | Tools installed with uv tool install each get their own environment, so a CLI cannot break your projects. | Start | Inspect
Use a project's environment | uv run python --version | In a uv project, respects the project's environment and Python requirements; may create or sync the environment. | Start | Run
Create a virtual environment | uv venv --python 3.12 .venv | Creates .venv in the current directory. uv downloads that Python version if it is missing. | Start | Write
Activate a virtual environment | source .venv/bin/activate | Run deactivate to leave. uv run avoids needing this at all, which is usually the better habit. | Start | Run
Sync a uv project | uv sync --locked | Uses the existing lockfile and fails if it needs updating. Run only in a uv project. | Intermediate | Write
Run a Python script | uv run python script.py | Replace script.py with your actual script. Dependencies belong in the project. | Start | Run
Inspect dependency relationships | uv tree | Prints the current project's dependency graph. | Intermediate | Inspect
Add a declared dependency | uv add httpx | Changes pyproject.toml, lockfile and environment. Use only when your project needs this dependency. | Intermediate | Write
Find the Python interpreter | python3 -c 'import sys; print(sys.executable); print(sys.version)' | Use uv run python for the project-specific interpreter rather than assuming global python3 is the correct one. | Intermediate | Inspect
Find the uv cache | uv cache dir | Inspect before cleaning. uv cache prune is a separate mutation and cache cleanup means future downloads. | Intermediate | Inspect
List local Ollama models | ollama list | Shows downloaded models and their size on disk. Disk size is a rough floor for memory use, not a promise. | Start | Inspect
See loaded AI models | ollama ps | Shows models currently in memory. An empty list means the service is idle, not that Ollama is missing. | Start | Inspect
Run a model | ollama run llama3.1:8b | Downloads the model on first use, then loads it into memory. Stop containers and other heavy work first on a small machine. /bye exits the chat. | Intermediate | Run
Release a loaded model | ollama stop llama3.1:8b | Unloads the model from memory. It does not delete the downloaded files. | Start | Run
Inspect model metadata | ollama show llama3.1:8b | Read the architecture, parameter count and context length before choosing settings. | Intermediate | Inspect
Inspect llama.cpp options | llama-cli --help | Runs GGUF models directly, without a model manager. Start with conservative context sizes. | Advanced | Inspect
Run a local GGUF model | llama-cli -m /path/to/model.gguf -p 'Explain this project' -n 128 -c 2048 | Replace the file path. Context size and GPU offload settings decide how much memory this takes. | Advanced | Run
''')

rows('Data, files & media', 'https://jqlang.org/manual/',r'''
Read a JSON field | jq '.scripts' package.json | Print just the scripts object. jq is for structured data; rg is for textual searching. | Start | Inspect
Get raw JSON text | jq -r '.name' package.json | -r outputs the string without JSON quotation marks. | Start | Inspect
Validate JSON | jq empty package.json | A successful exit confirms valid JSON; it does not validate an application-specific schema. | Intermediate | Inspect
Browse large JSON interactively | jless package.json | Navigate structured data without printing a giant document. q quits. | Start | Inspect
Read Compose service names from YAML | yq '.services | keys' docker-compose.yml | Reads the raw YAML without Compose's variable interpolation. This is Mike Farah's Go yq, not the Python one. | Intermediate | Inspect
Read Markdown nicely | glow README.md | Renders Markdown in the terminal. Helpful for project instructions. | Start | Inspect
Preview a text substitution | printf '%s\n' 'old-name' | sd 'old-name' 'new-name' | Transform piped text first to see the result. Passing a filename to sd instead edits that file in place, with no undo. | Intermediate | Inspect
Edit a known string in one file | sd 'old-name' 'new-name' path/to/file | Replace placeholders; edits in place. Review git diff afterwards and use a narrow path. | Intermediate | Write
Watch files and rerun tests | watchexec -e py -- uv run pytest | Runs tests after Python files change. Requires pytest in that project. Ctrl+C stops the watcher. | Intermediate | Run
Benchmark two read-only commands | hyperfine --warmup 2 'rg TODO . -g *.ts' 'rg -F TODO . -g *.ts' | Example comparison of regex vs literal search. Run in a suitable repo; benchmark commands execute repeatedly. | Advanced | Run
Move a file to Trash | trash ./unwanted-file.txt | Sends the file to the desktop Trash instead of unlinking it, so you can get it back. On Linux the trash-cli command is usually trash-put. | Start | Write
Inspect an archive before extraction | bsdtar -tf archive.7z | libarchive's bsdtar reads zip, 7z, rar and more. Always read the filenames before extracting. | Intermediate | Inspect
Extract into a fresh folder | mkdir -p extracted ;; bsdtar -xf archive.7z -C extracted | Extracting into an empty directory stops a badly built archive from scattering files over your working directory. | Intermediate | Write
Inspect image dimensions | magick identify image.png | Reports format, dimensions and colour depth without modifying the file. | Start | Inspect
Make a web-sized image | magick input.jpg -auto-orient -resize '1600x1600>' -strip output.webp | Creates a new WebP and removes metadata. The > prevents upscaling. Keep the original file. | Intermediate | Write
Extract text from an image | tesseract screenshot.png stdout | Runs OCR locally, with no upload. Non-English text needs that language's data package installed. | Intermediate | Run
List OCR languages | tesseract --list-langs | Check what is installed before assuming a language works. Each one is a separate package. | Start | Inspect
Reach a command an alias is shadowing | command gs --version | If gs is an alias for git status, command skips the alias and runs the real executable. whence -va gs shows both. | Intermediate | Inspect
Hash a downloaded file | shasum -a 256 download.tar.gz | Compare with the publisher's checksum through a trusted channel. The hash alone does not prove provenance. | Intermediate | Inspect
Inspect a SQLite database read-only | sqlite3 -readonly database.sqlite '.tables' | Replace the file path. Read-only mode prevents accidental database writes. | Intermediate | Inspect
Show SQLite schema | sqlite3 -readonly database.sqlite '.schema' | Read structure before querying. Do not point this at an unknown production database file. | Intermediate | Inspect
Check native build tools | cmake --version | Many tools compile from source when there is no binary for your platform. Keep build output in a per-project directory. | Intermediate | Inspect
Find a native library's flags | pkg-config --cflags --libs libpng | Returns the compiler and linker flags for an installed library. pkgconf provides the pkg-config command on most systems. | Advanced | Inspect
Check a Go project | go test ./... | Run in a Go module. Tests may execute arbitrary project code and access configured resources. | Intermediate | Run
Inspect Go environment paths | go env GOPATH GOMOD GOROOT | Select only needed fields instead of dumping all environment variables. | Intermediate | Inspect
Check a language server | gopls version | Language servers power editor completion and diagnostics. They normally run through the editor, not by hand. | Intermediate | Inspect
Inspect a tree-sitter grammar | tree-sitter --help | Parser tooling behind modern syntax highlighting. The library and the CLI are separate packages. | Advanced | Inspect
''')

rows('Networking & processes', 'https://curl.se/docs/manpage.html',r'''
Check HTTP headers | curl -I https://example.com | Sends a HEAD request. Useful for redirects, caching and content type without downloading the page body. | Start | Network
Inspect a local web app | curl -sS -o /dev/null -w '%{http_code}\n' http://localhost:3000 | Prints the HTTP status code. It fails if no service is listening. | Intermediate | Network
Read a local JSON API | xh GET http://localhost:3000/api/health | Friendly HTTP client. Replace with an endpoint your application actually implements. | Start | Network
Download to an explicit file | curl --fail --location --output download.zip https://example.com/download.zip | Example URL must be replaced. --fail makes HTTP errors fail the command; --location follows redirects. | Intermediate | Write
Continue an interrupted download | wget -c https://example.com/large-file.zip | Replace the URL. Resumes if the server supports it and writes into the current directory. | Intermediate | Write
Find a port listener | lsof -nP -iTCP:3000 -sTCP:LISTEN | Identify the process holding a port before stopping anything. On Linux, ss -tlnp answers the same question. | Start | Inspect
See all listening TCP ports | lsof -nP -iTCP -sTCP:LISTEN | -nP skips DNS and service-name lookups, so the output is fast and literal. | Start | Inspect
Stop a stuck local dev server | kill $(lsof -nP -iTCP:3000 -sTCP:LISTEN -t) | Sends SIGTERM to every listener on that port. Try Ctrl+C in the owning terminal first; this discards unsaved work in that process. | Intermediate | Disruptive
Look up DNS | dig example.com | Shows DNS answers, not an HTTP response. Useful when the browser cannot find a host. | Intermediate | Network
Inspect a TLS handshake | openssl s_client -connect example.com:443 -servername example.com </dev/null | Uses SNI for the correct certificate. Check verification output; the handshake alone is not an application health check. | Advanced | Network
Open the current directory | open . | Opens the directory in Finder on macOS. The Linux equivalent is xdg-open . | Start | Run
Copy a file to the clipboard | pbcopy < README.md | macOS clipboard. Replaces its contents. On Linux use xclip -selection clipboard or wl-copy. Never pipe secrets into a synced clipboard. | Start | Write
Read clipboard text | pbpaste | Prints the macOS text clipboard. On Linux use xclip -o -selection clipboard or wl-paste. | Start | Inspect
Keep a long job awake | caffeinate -i pnpm build | Prevents idle sleep only while the command runs. Does not permanently change power settings. | Intermediate | Run
Check battery and power source | pmset -g batt | Read-only power status. | Start | Inspect
Check memory pressure | memory_pressure | macOS memory statistics. Never use its pressure-generation options for a routine check. On Linux, read free -h and /proc/pressure/memory. | Intermediate | Inspect
Check swap use | sysctl vm.swapusage | Snapshot of swap usage; sustained pressure matters more than a single number. | Intermediate | Inspect
Inspect CPU and memory interactively | btop | Full-screen resource dashboard. q exits. htop is the lighter classic alternative. | Start | Inspect
Use the macOS process monitor | top -l 1 -o cpu -n 10 | One snapshot sorted by CPU. macOS top flags differ from Linux top. | Intermediate | Inspect
Inspect processes with procs | procs | A more readable ps. macOS permissions limit what any tool can see about other users' processes. | Start | Inspect
Alternative process dashboard | htop | The classic interactive process viewer. F10 or q exits. | Start | Inspect
Check disk capacity | duf | Shows mounted filesystem space in a table. df -h is the built-in alternative. | Start | Inspect
Find a directory's large children | dust -d 2 ~/projects | Read-only size scan, two levels deep. Point it at a directory rather than scanning the whole disk. | Intermediate | Inspect
See macOS version | sw_vers | Reports installed macOS version and build. | Start | Inspect
Inspect hardware | system_profiler SPHardwareDataType | macOS hardware summary. It includes serial identifiers: redact them before sharing the output. On Linux use lscpu and free -h. | Start | Inspect
Check developer tools | xcode-select -p | Prints the active macOS developer-tools directory. Many Homebrew builds need Apple's Command Line Tools. | Start | Inspect
Review an SSH host config | ssh -G example-host | Prints effective SSH configuration for a host alias without connecting. Replace the alias; output may include private network paths. | Advanced | Inspect
Preview a directory sync | rsync -avhn source/ destination/ | -n is a dry run. A trailing slash on the source copies its contents rather than the directory itself. Read the plan before removing -n. | Advanced | Inspect
List GPG public keys | gpg --list-keys | Read-only inventory of public keys. Never export secret keys just to debug signing. | Intermediate | Inspect
Inspect a file type | file path/to/file | Useful before deciding whether a file is text, binary, an archive or an executable. | Start | Inspect
''')

rows('Editors & sessions', 'https://github.com/tmux/tmux/wiki',r'''
Open a project in VS Code | code . | Opens the current directory, if the code command is on your PATH. Set EDITOR="code --wait" so Git waits for the window to close. | Start | Run
Open a terminal editor | nvim README.md | Neovim with no configuration is already usable. Distributions such as LazyVim add language support on top. | Start | Run
Learn Vim interactively | nvim +Tutor | Opens Neovim's tutorial. Esc returns to normal mode; :q exits, :w saves. | Start | Run
Start a named session | tmux new -s dev | Creates a terminal session that survives terminal disconnection. Default prefix is Ctrl+B. | Start | Run
List sessions | tmux ls | Shows saved sessions; no server running is normal if you have never started tmux. | Start | Inspect
Reattach a session | tmux attach -t dev | Return to the named dev session. Ctrl+B then D detaches without stopping processes. | Start | Run
Inspect tmux bindings | tmux list-keys | Available once a server exists. Default prefix shortcuts: % split vertically, double quote split horizontally, c new window. | Intermediate | Inspect
Validate a terminal config | ghostty +validate-config | Checks the config file for errors before you reload. On macOS the binary lives inside the app bundle: /Applications/Ghostty.app/Contents/MacOS/ghostty. | Intermediate | Inspect
Read every terminal option | ghostty +show-config --default --docs | Prints the documented defaults for the installed build. Pipe it into less; it is long. | Intermediate | Inspect
Check direnv state | direnv status | Shows whether this directory's environment is loaded and permitted. direnv needs a hook in your .zshrc to do anything. | Intermediate | Inspect
Allow a reviewed environment | direnv allow . | Executes the directory's .envrc as shell code. Read it first, especially in a newly cloned repository. | Intermediate | Run
''')

rows('Packages & maintenance', 'https://docs.brew.sh/Manpage',r'''
Get short practical help | tldr tar | tealdeer provides the tldr executable. If its cache is missing, tldr --update downloads examples. | Start | Inspect
Read full help | rg --help | Almost every tool answers --help. Use man for system commands, and SUBCOMMAND --help for nested CLIs such as git or docker. | Start | Inspect
Inspect a package | brew info ripgrep | Shows version, description, dependencies and installation details. Package name ripgrep provides executable rg. | Start | Inspect
List installed command packages | brew list --formula | Includes libraries and transitive dependencies, not just user-facing CLIs. | Start | Inspect
List installed desktop packages | brew list --cask | macOS GUI apps and fonts installed through Homebrew. Fonts provide no commands of their own. | Start | Inspect
Understand why a library exists | brew uses --installed libpng | Shows installed packages that depend on libpng. Avoid manually deleting dependency directories. | Intermediate | Inspect
List leaf packages | brew leaves | Packages not required by other installed formulae. A leaf is not necessarily unused. | Intermediate | Inspect
Check missing dependencies | brew missing | No output is the good result: every installed formula has what it declares. | Intermediate | Inspect
Run Homebrew diagnostics | brew doctor | Reports common installation problems. Read each warning before acting; never answer a permissions warning with a recursive sudo chown. | Intermediate | Inspect
Refresh package metadata | brew update | Downloads current metadata; does not upgrade all installed formulae. | Intermediate | Network
Review available updates | brew outdated | Run after brew update. Read the list before upgrading; a major version bump can change a tool's flags. | Intermediate | Inspect
Upgrade one selected tool | brew upgrade ripgrep | Updates only the selected formula and any needed dependencies. Verify your workflow after upgrading. | Intermediate | Write
Preview cache cleanup | brew cleanup --dry-run | Lists what would be removed without deleting anything. Drop --dry-run only after reading the list. | Intermediate | Inspect
Preview unused dependency removal | brew autoremove --dry-run | Read the proposed list before considering a real removal. | Intermediate | Inspect
Locate a package's files | brew list libarchive | Lists files installed by a package, including executables that may not be linked into PATH. | Intermediate | Inspect
Export a reproducible package list | brew bundle dump --file=./Brewfile | Writes a Brewfile listing what you installed. It refuses to overwrite an existing file unless forced. This is how you rebuild a machine. | Advanced | Write
Check a Brewfile | brew bundle check --file=./Brewfile | Compares a manifest with installed dependencies. It does not install missing packages. | Intermediate | Inspect
Inspect a cask | brew info --cask ghostty | Shows a GUI app's version, install path and upstream site. Casks are macOS-only. | Start | Inspect
Update an isolated Python tool | uv tool upgrade ruff | Upgrades that tool's own environment and nothing else. Replace ruff with a tool from uv tool list. | Advanced | Write
See local pnpm storage | pnpm store path | Prints the shared content-addressed store location. Do not delete it while installs run. | Intermediate | Inspect
Check Git settings with origins | git config --show-origin --get-regexp '^(core.pager|fetch.prune|pull.rebase|delta\.)' | Shows which file each setting came from. A narrow pattern avoids dumping credentials and private remote URLs. | Advanced | Inspect
''')

rows('Shell foundations', 'https://www.gnu.org/software/coreutils/manual/',r'''
Read a file without decorations | command cat README.md | Plain text is best for pipelines and scripts; bat is useful for interactive reading. | Start | Inspect
Read the beginning of a log | head -n 40 app.log | Replace the example filename. Avoid printing entire large logs or files containing secrets. | Start | Inspect
Follow a rotating log | tail -F app.log | Follows the filename across replacement or rotation. Ctrl+C stops watching. | Intermediate | Inspect
Extract a range of lines | sed -n '20,40p' README.md | Prints a line range without editing the file. macOS ships BSD sed, Linux ships GNU sed, and their in-place editing flags differ. | Intermediate | Inspect
Count lines, words and bytes | wc README.md | Reports basic text counts. wc -l selects lines; wc -c selects bytes. | Start | Inspect
Sort and deduplicate text | printf '%s\n' beta alpha beta | sort | uniq -c | Produces a sorted frequency table. uniq only combines adjacent duplicate lines, so sorting matters. | Intermediate | Inspect
Select a delimited column | cut -d, -f1 simple.csv | Works for simple delimiter-separated text. Quoted CSV fields need a proper CSV parser, not cut. | Intermediate | Inspect
Compute with awk | printf 'alpha 2\nbeta 3\n' | awk '{sum += $2} END {print sum}' | Accumulates the second whitespace-separated field. Start with small sample input to understand the transformation. | Intermediate | Inspect
Pass filenames without splitting spaces | fd -0 -e md --type f | xargs -0 -I{} printf 'Found: %s\n' '{}' | NUL-delimited records preserve spaces and most unusual filenames. This example only prints a preview. | Advanced | Inspect
Compare two files | diff -u old.txt new.txt | Unified diff. Exit 1 means files differ; it is not necessarily a tool failure. | Intermediate | Inspect
Read long output in a pager | git log --oneline | less | Space scrolls a page, / searches, n advances and q quits. | Start | Inspect
Inspect file permissions | stat -f '%Sp %Su %Sg %N' README.md | Shows mode, owner, group and name. This is BSD syntax for macOS; GNU stat on Linux uses stat -c '%A %U %G %n'. | Intermediate | Inspect
Understand an executable permission | ls -l script.zsh | Inspect before changing modes. chmod u+x script.zsh adds execute permission for the owner only. | Intermediate | Inspect
''')

rows('macOS specifics', 'https://support.apple.com/guide/terminal/welcome/mac',r'''
Search with Spotlight | mdfind -onlyin ~/projects 'kMDItemFSName == "README.md"' | Uses the Spotlight index, so an empty result is not proof a file is absent. fd reads the directory itself. | Intermediate | Inspect
Inspect mounted disks | diskutil list | Lists disks and partitions without modifying them. Disk erase and repair subcommands are separate operations. | Intermediate | Inspect
Inspect network interfaces | networksetup -listallhardwareports | Maps hardware ports to device names such as en0. Does not change network configuration. | Intermediate | Inspect
Inspect macOS DNS configuration | scutil --dns | Useful when VPN or split DNS behaves differently from a direct dig query. Output can reveal internal network names. | Advanced | Inspect
Inspect proxy configuration | scutil --proxy | Read-only check for system HTTP/SOCKS proxy settings. Individual CLI tools may also use environment variables. | Intermediate | Inspect
Check one preference domain | defaults read com.apple.finder AppleShowAllFiles | Reads a single Finder preference. A missing key means there is no explicit user override. | Intermediate | Inspect
Validate a property list | plutil -lint ~/Library/LaunchAgents/com.example.agent.plist | Checks plist syntax only. Valid XML does not mean the program it points at will start. | Intermediate | Inspect
Inspect a launch agent | launchctl print gui/$(id -u)/com.example.agent | Reports registration and last-exit status for a per-user agent. The Linux equivalent is systemctl --user status. | Advanced | Inspect
Check update availability | softwareupdate --list | Contacts Apple's update service and lists available updates without installing them. May take a while. | Intermediate | Network
Create a screenshot file | screencapture -i ~/Desktop/terminal-example.png | Opens macOS interactive capture and writes your selection. Review the visible content before sharing the image. | Start | Write
Show recent app log events | log show --last 5m --style compact --predicate 'process == "Ghostty"' | Narrows the macOS unified log to one process and a short window. Logs can contain private content. journalctl is the Linux counterpart. | Advanced | Inspect
Check backup status | tmutil status | Reports Time Machine's current operation. An idle result does not prove a recent backup exists. | Intermediate | Inspect
Read archive contents | tar -tf archive.tar.gz | Lists what an archive holds without extracting it. Always look before extracting an archive you did not create. | Start | Inspect
Create a project-note archive | tar -czf notes-backup.tar.gz README.md docs | Writes an archive from explicit files and folders. Choose a new output path and exclude secrets. | Intermediate | Write
Connect using SSH | ssh user@example-host | Replace with your account and host. Verify a new host's fingerprint through a trusted channel before accepting it. | Intermediate | Network
Copy one file over SSH | scp ./report.txt user@example-host:/path/to/destination/ | Replace the example user, host and directory. Uploads the file to that host and may overwrite an existing destination file. | Intermediate | Remote write
Check the selected editor | print -r -- "$EDITOR" | Git and other tools open this. A value such as code --wait makes them wait for the window to close. | Start | Inspect
''')

rows('Linux specifics', 'https://www.freedesktop.org/software/systemd/man/',r'''
Identify the distribution | cat /etc/os-release | Tells you which package manager and package names apply. Scripts should read ID and VERSION_ID rather than guessing. | Start | Inspect
See listening ports | ss -tlnp | The Linux answer to lsof for ports. Process names for other users' processes need sudo. | Start | Inspect
Check a service | systemctl status docker | Shows whether a service is enabled, running and what it last logged. Replace docker with any unit name. | Start | Inspect
Start a service now and at boot | sudo systemctl enable --now docker | Two things at once: start it, and start it on every boot. Use disable --now to undo both. | Intermediate | Disruptive
Read a service's logs | journalctl -u docker -n 100 --no-pager | The last 100 lines for one unit. Add -f to follow. Add --since '10 min ago' to bound it by time. | Intermediate | Inspect
Read your own user services | systemctl --user list-units --type=service | Per-user services, the counterpart to macOS launch agents. | Intermediate | Inspect
Check memory and swap | free -h | Human-readable totals. The available column matters more than free: Linux deliberately uses spare memory for cache. | Start | Inspect
Check memory pressure | cat /proc/pressure/memory | Pressure stall information: how much time tasks spent waiting on memory. Better evidence than a single free number. | Advanced | Inspect
Describe the CPU | lscpu | Cores, threads, architecture and flags. lscpu | rg 'Model name' narrows it to one line. | Start | Inspect
Check disk space | df -h | Built-in and always present. duf prints the same data in a friendlier table. | Start | Inspect
Search installed packages | apt list --installed | Debian and Ubuntu. Fedora uses dnf list installed; Arch uses pacman -Q. | Start | Inspect
Find which package owns a file | dpkg -S "$(command -v git)" | Debian and Ubuntu. Fedora uses dnf provides; Arch uses pacman -Qo. | Intermediate | Inspect
Read a package's description | apt show ripgrep | Version, size, dependencies and homepage, before installing anything. | Start | Inspect
Refresh and inspect updates | sudo apt update ;; apt list --upgradable | update refreshes metadata only. Nothing is upgraded until you run apt upgrade. | Intermediate | Network
Make zsh your login shell | chsh -s "$(command -v zsh)" | Takes effect at your next login, not in this terminal. Install zsh first or you will be locked out of a working shell. | Intermediate | Write
Copy to the clipboard | printf '%s\n' hello | xclip -selection clipboard | X11. On Wayland use wl-copy. macOS uses pbcopy. | Intermediate | Write
Open a file with the desktop default | xdg-open README.md | The Linux counterpart to macOS open. Needs a desktop session. | Start | Run
Check your kernel | uname -srm | Kernel name, release and machine architecture. Some tools ship separate arm64 and x86_64 builds. | Start | Inspect
Inspect a user's groups | id -nG | Shows your groups. Running Docker without sudo requires membership in the docker group, which is equivalent to root access. | Intermediate | Inspect
''')


SHORTCUTS = [
('zsh','Ctrl+A / Ctrl+E','Move to start / end of command'),('zsh','Ctrl+U / Ctrl+K','Cut text before / after cursor'),
('zsh','Ctrl+W / Ctrl+Y','Cut previous word / paste cut text'),('zsh','Ctrl+R','Fuzzy-search command history'),
('zsh','Ctrl+T','Find and insert a file path (fzf)'),('zsh','Alt+C','Pick a directory with fzf'),
('zsh','↑ / ↓','Search history using your current input'),('zsh','→','Accept autosuggestion when at the end of input'),
('zsh','Tab / Shift+Tab','Complete a command or navigate completion choices'),('zsh','Ctrl+C','Interrupt the foreground command'),
('zsh','Ctrl+Z → fg','Suspend, then resume a job'),('zsh','Ctrl+L','Redraw the terminal screen'),
('Ghostty','Cmd+D / Cmd+Shift+D','Split right / split down'),('Ghostty','Cmd+[ / Cmd+]','Previous / next split'),
('Ghostty','Cmd+Shift+Enter','Zoom the active split'),('Ghostty','Cmd+T','Open a tab'),
('Ghostty','Cmd+Shift+[ / ]','Previous / next tab'),('Ghostty','Cmd+Shift+R','Reload the Ghostty configuration'),
('Ghostty','Cmd+plus / minus / zero','Increase / decrease / reset font size'),('Ghostty','Cmd+K','Clear scrollback'),
('tmux','Ctrl+B, D','Detach; the session keeps running'),('tmux','Ctrl+B, C','New tmux window'),
('tmux','Ctrl+B, % / "','Split side by side / stacked'),('Neovim','Esc → :w / :q / :wq','Normal mode → save / quit / save and quit'),
('Neovim','/text → n / N','Search → next / previous match'),('Neovim','Space','Open LazyVim leader-key hints')]

WORKFLOWS = [
dict(title='A deliberate start to a coding session',tag='Daily',intro='Establish context before changing anything. Tools become far more predictable once the directory, branch and runtime are explicit rather than assumed.',steps=[
('Go to the project','cd ~/projects/your-app'),('Check your branch and edits','git status --short --branch'),('Check runtime and available scripts','node --version\npnpm --version\npnpm run'),('Start development','pnpm dev')],finish='Open a second split or tab for Git and tests. Keep the dev server visible so you notice failures when they happen, not ten minutes later.'),
dict(title='Diagnose “port 3000 is already in use”',tag='Debugging',intro='Find the owner before killing anything. A port conflict is often an old dev server, but it can just as easily be a different project you still need. On Linux, ss -tlnp replaces lsof.',steps=[
('Identify the listener','lsof -nP -iTCP:3000 -sTCP:LISTEN'),('Inspect the owner','ps -p PID -o pid,ppid,etime,command'),('Stop it intentionally','kill $(lsof -nP -iTCP:3000 -sTCP:LISTEN -t)'),('Restart your intended server','pnpm dev')],finish='Replace PID with the real number. Prefer Ctrl+C in the terminal that owns the server. kill sends SIGTERM, which asks a process to stop and discards its unsaved work.'),
dict(title='Bring up and inspect a WordPress site',tag='WordPress',intro='Run WordPress through the project\u2019s containers so PHP, WordPress and the database versions stay aligned. This assumes the stack defines a wpcli service.',steps=[
('Enter the site directory','cd ~/projects/your-wordpress-site'),('Validate before starting','docker compose config --quiet'),('Start and check services','docker compose up -d\ndocker compose ps'),('Inspect WordPress','docker compose exec wpcli wp core version\ndocker compose exec wpcli wp plugin list'),('Follow application logs','docker compose logs --tail=100 -f wordpress')],finish='Ctrl+C exits logs. docker compose stop preserves the containers and volumes. Database export files are sensitive and should stay out of Git.'),
dict(title='Review a change like a senior engineer',tag='Git',intro='Review behavior, boundaries and failure modes. Commit only changes you can explain.',steps=[
('Understand scope','git status --short\ngit diff --stat\ngit diff'),('Run the project checks','pnpm lint && pnpm typecheck'),('Choose hunks','git add -p'),('Review staged content','git diff --staged\ngit diff --staged --check'),('Commit the intent','git commit -m "Describe the behavior changed"')],finish='Run the relevant test script where it exists. A formatter or passing test suite alone does not prove the change solves the right problem.'),
dict(title='Switch from web development to local AI',tag='Memory',intro='A language model, a container VM and a browser all want the same RAM. On a 16\u201324 GB machine you have to choose between them rather than run everything.',steps=[
('Inspect current workloads','docker ps\nollama ps'),('Stop the container VM if you no longer need it','colima stop'),('Start an inference session','ollama run llama3.1:8b'),('Unload after use','ollama stop llama3.1:8b'),('Restore the VM when you need it again','colima start')],finish='Stopping the VM interrupts every container, so finish their work first. If memory is tight, choose a smaller model or a shorter context. A model\u2019s file size is a floor for its memory use, not a measurement of it. On Linux, replace the colima steps with systemctl start/stop docker.'),
dict(title='Maintain packages without surprise upgrades',tag='Weekly',intro='Refresh metadata, read the proposed changes, then upgrade deliberately. Dependency libraries are part of the toolchain, not clutter to be pruned. Homebrew here; apt, dnf and pacman have the same three phases.',steps=[
('Check package health','brew missing\nbrew doctor'),('Refresh and inspect updates','brew update\nbrew outdated'),('Inspect one candidate','brew info ripgrep'),('Upgrade that tool','brew upgrade ripgrep'),('Preview cleanup','brew cleanup --dry-run\nbrew autoremove --dry-run')],finish='Never answer a permissions warning with a recursive sudo chown on a package directory. Upgrade one tool at a time when a project depends on its behaviour, and read release notes for anything that crosses a major version.'),
dict(title='Turn a one-off command into reliable automation',tag='Advanced',intro='Start with a read-only preview, understand filenames and exit codes, then write the smallest script that does the job. ShellCheck targets sh and bash; zsh -n is the syntax check for zsh scripts.',steps=[
('Create a practice directory','mkdir -p ~/terminal-practice\ncd ~/terminal-practice'),('List targets first',"fd -e txt --type f"),('Handle spaces and empty matches',"for file in *.txt(N); do print -r -- \"$file\"; done"),('Check a zsh script before running it','zsh -n script.zsh')],finish='Quote variable expansions, use -- before user-provided paths, check failures, and never parse ls output. For filename pipelines use null separators, such as fd -0 with xargs -0, and preview the action first.')]

LESSONS = [
('1','Move confidently','Use pwd, cd, z, ll, fd and Ctrl+R without guessing where you are.','Find a source file in one project, preview it with bat, then return with cd -.',['pwd','fd','zoxide']),
('2','Read command structure','Understand command, subcommand, flags, arguments, quotes and exit status.','Explain every token in: rg -n -F "process.env." -g "*.ts" .',['rg','zsh']),
('3','Compose small tools','Use stdout, stderr, pipes, command substitution and redirection intentionally.','Count tracked TypeScript files with git ls-files and wc; explain why node_modules is excluded.',['git','zsh']),
('4','Inspect before changing','Use dry-runs, diffs, explicit paths and narrow queries.','Stage two separate hunks with git add -p and inspect git diff --staged.',['git','rsync']),
('5','Debug from evidence','Check directory, executable, runtime, environment, port, logs and resource pressure.','Diagnose a failed dev-server start using whence -va, lsof and the project log.',['lsof','pnpm']),
('6','Manage repeatable environments','Understand which layer owns what: the system package manager, the runtime manager, the project manager and containers.','Explain which layer owns Node, React, Python, PHP and WordPress on your machine, and what breaks if two layers install the same thing.',['uv','Volta','Docker']),
('7','Automate and recover','Write small scripts, check exits, preserve backups, use worktrees and document operations.','Create a read-only project-health script and test it in a directory whose name contains spaces.',['zsh','git']),
('8','Measure improvements','Compare real workloads, change one thing at a time, and be honest about what a measurement proves.','Use hyperfine on two harmless searches, then explain what the result does and does not prove.',['hyperfine'])]
