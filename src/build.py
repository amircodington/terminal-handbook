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
    'pnpm': 'https://pnpm.io/cli/run',
    'npm': 'https://docs.npmjs.com/cli/',
    'uv': 'https://docs.astral.sh/uv/reference/cli/',
    'brew': 'https://docs.brew.sh/Manpage',
    'python3': 'https://docs.python.org/3/using/cmdline.html',
    'systemctl': 'https://www.freedesktop.org/software/systemd/man/systemctl.html',
    'journalctl': 'https://www.freedesktop.org/software/systemd/man/journalctl.html',
    'ss': 'https://man7.org/linux/man-pages/man8/ss.8.html',
    'apt': 'https://manpages.debian.org/stable/apt/apt.8.en.html',
    'dpkg': 'https://manpages.debian.org/stable/dpkg/dpkg.1.en.html',
    'wp': 'https://developer.wordpress.org/cli/commands/',
    'open': 'https://support.apple.com/guide/terminal/open-or-quit-terminal-trml35697/mac',
}

# Executable name -> the tool that provides it, and that tool's documentation.
# Both are derived from toolkit.py so there is one place to record a new tool.
TOOL_URLS = {tool['name']: tool['url'] for tool in TOOLS}
PROVIDED_BY = {}
for _tool in TOOLS:
    for _command in _tool['commands']:
        TOOL_URLS.setdefault(_command, _tool['url'])
        PROVIDED_BY.setdefault(_command, _tool['name'])

# Words that stand in front of the command actually being demonstrated.
WRAPPERS = ('sudo', 'command', 'time')


def executable(command):
    """The program a recipe demonstrates.

    Ignores a leading `cd ... ;; ` line, skips wrapper words that are not the
    point of the example, and looks through `docker compose exec SERVICE` so a
    containerised command links to its own documentation rather than Docker's.
    """
    words = command.splitlines()[-1].split()
    while words and words[0] in WRAPPERS:
        words = words[1:]
    if words[:3] == ['docker', 'compose', 'exec']:
        words = words[4:]          # docker compose exec SERVICE COMMAND ...
    elif words[:2] == ['docker', 'exec']:
        words = words[3:]          # docker exec CONTAINER COMMAND ...
    return Path(words[0]).name if words else ''


def link_recipes():
    for recipe in RECIPES:
        command = executable(recipe['command'])
        recipe['source'] = DOC_LINKS.get(command) or TOOL_URLS.get(command) or recipe['source']
        recipe['tool'] = PROVIDED_BY.get(command, command)


def ordered(values):
    """Distinct values in first-seen order."""
    return list(dict.fromkeys(values))


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
        categories=ordered(r['category'] for r in RECIPES),
        # The filter dropdowns follow the data, so a new level, effect or tier
        # cannot become unreachable by being added in only one of two places.
        levels=ordered(r['level'] for r in RECIPES),
        effects=ordered(r['effect'] for r in RECIPES),
        tiers=ordered(t['tier'] for t in TOOLS),
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


def update_readme_counts(data, summary):
    """Keep the README's headline numbers in step with what was just built."""
    readme = ROOT / 'README.md'
    text = readme.read_text()
    start, end = '<!-- counts:start -->', '<!-- counts:end -->'
    if start not in text or end not in text:
        return
    head, rest = text.split(start, 1)
    _, tail = rest.split(end, 1)
    readme.write_text(f'{head}{start}\n{summary}\n{end}{tail}')


def main():
    data = build_data()
    (ROOT / 'index.html').write_text(render(data))
    (ROOT / 'catalog.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    summary = (f"{len(RECIPES)} worked command examples across {len(data['categories'])} topics, "
               f"{len(WORKFLOWS)} end-to-end workflows, {len(TOOLS)} tools\n"
               f"with install instructions, and a learning path in {len(LESSONS)} steps.")
    update_readme_counts(data, summary)
    print('Built index.html: ' + summary.replace('\n', ' '))


if __name__ == '__main__':
    main()
