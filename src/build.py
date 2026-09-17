#!/usr/bin/env python3
"""Build index.html and catalog.json from the content in this directory.

    python3 src/build.py

The page is one self-contained HTML file with no network dependencies: the
template supplies the markup and CSS, runtime.js supplies the behaviour, and
content.py plus toolkit.py supply the data, embedded as inert JSON.

Nothing here reads your machine. The output is identical on any computer, which
is the point: this is a handbook, not an inventory of one person's laptop.
"""
import json
from pathlib import Path

from content import LESSONS, RECIPES, SHORTCUTS, WORKFLOWS
from toolkit import EXTRAS, MANAGERS, TOOLS

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'src'

# Where a recipe's "Reference" link points, keyed by the executable it runs.
# Anything not listed here falls back to the tool's own URL in toolkit.py, and
# then to the shared source declared for its category.
DOC_LINKS = {
    'git': 'https://git-scm.com/docs',
    'gh': 'https://cli.github.com/manual/',
    'pnpm': 'https://pnpm.io/cli/run',
    'npm': 'https://docs.npmjs.com/cli/',
    'volta': 'https://docs.volta.sh/reference/',
    'uv': 'https://docs.astral.sh/uv/reference/cli/',
    'docker': 'https://docs.docker.com/reference/cli/docker/',
    'brew': 'https://docs.brew.sh/Manpage',
    'python3': 'https://docs.python.org/3/using/cmdline.html',
    'systemctl': 'https://www.freedesktop.org/software/systemd/man/systemctl.html',
    'journalctl': 'https://www.freedesktop.org/software/systemd/man/journalctl.html',
    'ss': 'https://man7.org/linux/man-pages/man8/ss.8.html',
    'apt': 'https://manpages.debian.org/stable/apt/apt.8.en.html',
    'dpkg': 'https://manpages.debian.org/stable/dpkg/dpkg.1.en.html',
    'open': 'https://support.apple.com/guide/terminal/open-or-quit-terminal-trml35697/mac',
}

# Executable name -> the package that provides it, where the two differ.
PROVIDED_BY = {
    'rg': 'ripgrep',
    'tldr': 'tealdeer',
    'delta': 'git-delta',
    'nvim': 'neovim',
    'kubectl': 'kubernetes-cli',
    'magick': 'imagemagick',
    'gs': 'ghostscript',
    'z': 'zoxide',
    'zi': 'zoxide',
}

TOOL_URLS = {tool['name']: tool['url'] for tool in TOOLS}
for _tool in TOOLS:
    for _command in _tool['commands']:
        TOOL_URLS.setdefault(_command, _tool['url'])


def executable(command):
    """The program a recipe actually runs, ignoring any `cd ... ;; ` prefix."""
    return Path(command.splitlines()[-1].split()[0]).name


def link_recipes():
    for recipe in RECIPES:
        command = executable(recipe['command'])
        if command in DOC_LINKS:
            recipe['source'] = DOC_LINKS[command]
        elif command in TOOL_URLS:
            recipe['source'] = TOOL_URLS[command]
        if 'wpcli wp' in recipe['command']:
            recipe['source'] = 'https://developer.wordpress.org/cli/commands/'
        recipe['tool'] = PROVIDED_BY.get(command, command)


def build_data():
    link_recipes()
    return dict(
        recipes=RECIPES,
        shortcuts=SHORTCUTS,
        workflows=WORKFLOWS,
        lessons=LESSONS,
        tools=TOOLS,
        managers=MANAGERS,
        extras=EXTRAS,
        categories=list(dict.fromkeys(r['category'] for r in RECIPES)),
    )


def render(data):
    # The data is inert inside a JSON script tag, but escaping the three
    # characters that could close that tag early keeps it inert even if someone
    # later writes an explanation containing markup.
    payload = (json.dumps(data, ensure_ascii=False)
               .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))
    runtime = (SRC / 'runtime.js').read_text()
    if '</script' in runtime.lower():
        raise SystemExit('runtime.js contains a closing script tag and cannot be inlined')
    page = (SRC / 'template.html').read_text()
    for placeholder, value in (('__HANDBOOK_DATA__', payload), ('__HANDBOOK_RUNTIME__', runtime)):
        if placeholder not in page:
            raise SystemExit(f'template.html is missing {placeholder}')
        page = page.replace(placeholder, value)
    return page


def main():
    data = build_data()
    (ROOT / 'index.html').write_text(render(data))
    (ROOT / 'catalog.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f"Built index.html: {len(RECIPES)} commands across {len(data['categories'])} topics, "
          f"{len(TOOLS)} tools, {len(WORKFLOWS)} workflows.")


if __name__ == '__main__':
    main()
