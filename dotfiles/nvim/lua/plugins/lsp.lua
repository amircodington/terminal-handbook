-- gopls is installed via Homebrew, not Mason. mason-lspconfig's automatic_enable
-- only turns on Mason-installed servers, so enable gopls explicitly through
-- LazyVim's per-server `setup` hook (runs right after vim.lsp.config() for it).
return {
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        gopls = {},
      },
      setup = {
        gopls = function()
          if vim.fn.executable("gopls") == 1 then
            vim.lsp.enable("gopls")
          end
          return false -- let LazyVim run its default handling too
        end,
      },
    },
  },
}
