-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

local opt = vim.opt

opt.scrolloff = 8 -- keep more context around the cursor
opt.sidescrolloff = 8
opt.relativenumber = true -- (LazyVim default, kept explicit)
opt.wrap = false
opt.linebreak = true -- when wrap is toggled on, break at word boundaries
opt.confirm = true -- prompt instead of failing on :q with unsaved changes
opt.timeoutlen = 400 -- snappier which-key popup

-- format on save (LazyVim default: true) — explicit so it's discoverable
vim.g.autoformat = true

-- use ripgrep for :grep
if vim.fn.executable("rg") == 1 then
  opt.grepprg = "rg --vimgrep --smart-case"
  opt.grepformat = "%f:%l:%c:%m"
end

-- Disable the legacy remote-plugin providers. No modern Lua plugin uses them;
-- turning them off removes the :checkhealth warnings and speeds startup.
-- Re-enable one by installing its package (e.g. `pipx install pynvim`) and
-- removing the matching line.
vim.g.loaded_node_provider = 0
vim.g.loaded_perl_provider = 0
vim.g.loaded_python3_provider = 0
vim.g.loaded_ruby_provider = 0
