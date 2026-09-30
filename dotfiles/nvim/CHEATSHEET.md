# Neovim (LazyVim) — quick reference

Leader key = **Space**. Press `<Space>` and wait — **which-key** shows every menu.
Full docs: <https://lazyvim.org>. Manage plugins/extras with `:Lazy` and `:LazyExtras`.

## Files & search
| Keys | Action |
|---|---|
| `<Space><Space>` | find files (root) |
| `<Space>ff` / `<Space>fF` | find files (root / cwd) |
| `<Space>fr` | recent files |
| `<Space>/` | live grep (ripgrep) in project |
| `<Space>sw` | grep word under cursor |
| `<Space>fe` / `<Space>e` | file explorer (neo-tree) |
| `<Space>fb` | open buffers |
| `<Space>,` | switch buffer |

## Windows / buffers / tabs
| Keys | Action |
|---|---|
| `<C-h/j/k/l>` | move between splits |
| `<Space>w` then `s` / `v` | split below / right |
| `<Space>wd` | close window |
| `<Space>bd` | close buffer |
| `<S-h>` / `<S-l>` | prev / next buffer |
| `<Space><Tab>` menu | tabs |

## Code / LSP
| Keys | Action |
|---|---|
| `gd` / `gr` | go to definition / references |
| `gD` | declaration · `gI` implementation · `gy` type def |
| `K` | hover docs |
| `<Space>ca` | code action |
| `<Space>cr` | rename symbol |
| `<Space>cf` | format (also on save) |
| `<Space>cd` | line diagnostics |
| `]d` / `[d` | next / prev diagnostic |
| `<Space>ss` | document symbols |
| `<Space>cl` | LSP info |

## Git
| Keys | Action |
|---|---|
| `<Space>gg` | lazygit (full TUI) |
| `<Space>gb` | git blame line |
| `<Space>ghs` / `<Space>ghr` | stage / reset hunk |
| `]h` / `[h` | next / prev hunk |
| `<Space>gf` | file history |

## Edit / move
| Keys | Action |
|---|---|
| `<A-j>` / `<A-k>` | move line/selection down / up |
| `gcc` / `gc` (visual) | toggle comment |
| `<Space>sr` | search & replace in project (grug-far) |
| `<Space>p` (visual) | paste without yanking (yanky) |
| `<Space>P` | yank history |
| `<C-\\>` | toggle terminal |

## Misc
| Keys | Action |
|---|---|
| `<Space>l` | Lazy plugin manager |
| `<Space>cm` | Mason (LSP/formatter installer) |
| `<Space>uh` | toggle inlay hints |
| `<Space>ur` | clear search highlight / redraw |
| `<Space>qq` | quit all |

## This config
```
~/.config/nvim/
  lua/config/lazy.lua       ← LazyVim + language extras list
  lua/config/options.lua    ← editor options
  lua/config/keymaps.lua    ← your keymaps
  lua/plugins/colorscheme.lua ← Tokyo Night Storm, transparent (matches Ghostty)
  lua/plugins/editor.lua    ← extra treesitter parsers + mason tools
```
Enabled extras: TypeScript, Python, Go, JSON, YAML, TOML, Docker, Markdown,
Tailwind, SQL, Prettier, ESLint, fzf, yanky, dotfiles.
Add more with `:LazyExtras` (e.g. `lang.rust` — needs `rustup`/`rust-analyzer` first).

LSP servers via Homebrew (not Mason): `gopls`. Everything else is Mason-managed
(`:Mason` to view/add). `imagemagick` + `ghostscript` power inline image/PDF
preview in Markdown.
