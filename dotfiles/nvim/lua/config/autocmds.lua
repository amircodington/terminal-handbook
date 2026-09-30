-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")

-- Persian: display prose files right-to-left (Ghostty has no bidi yet).
-- A text-like buffer is RTL when most letters in its first 100 lines are
-- Arabic-script. Code files are skipped: 'rightleft' also mirrors Latin text.
local rtl_filetypes = { markdown = true, text = true, gitcommit = true, [""] = true }

local function is_persian(buf)
  local text = table.concat(vim.api.nvim_buf_get_lines(buf, 0, 100, false), "\n")
  local _, persian = text:gsub("[\216-\219][\128-\191]", "") -- U+0600–U+06FF
  local _, latin = text:gsub("%a", "")
  return persian > 0 and persian > latin
end

local function apply_rtl(buf, win)
  -- b:persian_rtl is only set by the manual toggle; otherwise detect each time
  -- (this file can load before the buffer's lines are read).
  local rtl = vim.b[buf].persian_rtl
  if rtl == nil then
    rtl = rtl_filetypes[vim.bo[buf].filetype] == true and is_persian(buf)
  end
  vim.wo[win].rightleft = rtl
end

vim.api.nvim_create_autocmd("BufWinEnter", {
  group = vim.api.nvim_create_augroup("persian_rtl", { clear = true }),
  callback = function(ev)
    apply_rtl(ev.buf, vim.api.nvim_get_current_win())
  end,
})

-- This file loads on VeryLazy, after `nvim file.md` already opened the file.
for _, win in ipairs(vim.api.nvim_list_wins()) do
  apply_rtl(vim.api.nvim_win_get_buf(win), win)
end

vim.keymap.set("n", "<leader>uR", function()
  local buf = vim.api.nvim_get_current_buf()
  vim.b[buf].persian_rtl = not vim.wo.rightleft
  vim.wo.rightleft = vim.b[buf].persian_rtl
end, { desc = "Toggle right-to-left (Persian)" })
