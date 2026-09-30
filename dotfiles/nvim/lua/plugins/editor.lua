-- Small quality-of-life overrides on top of LazyVim defaults.
-- lazygit is available at <leader>gg (LazyVim default) and uses the terminal config.
return {
  -- Extra Treesitter parsers for this machine's stack.
  -- (nvim-treesitter `main` branch: this only takes effect if opts.ensure_installed
  -- is a list; harmless otherwise. LazyVim's lang extras install the rest.)
  {
    "nvim-treesitter/nvim-treesitter",
    opts = function(_, opts)
      if type(opts.ensure_installed) == "table" then
        vim.list_extend(opts.ensure_installed, {
          "bash",
          "css",
          "dockerfile",
          "go",
          "javascript",
          "json",
          "lua",
          "markdown",
          "markdown_inline",
          "python",
          "sql",
          "toml",
          "tsx",
          "typescript",
          "vue",
          "yaml",
        })
      end
    end,
  },

  -- Extra Mason tools (formatters).
  {
    "mason-org/mason.nvim",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}
      vim.list_extend(opts.ensure_installed, {
        "stylua",
        "shfmt",
        "prettier",
      })
    end,
  },

  -- Inline image / PDF preview in Markdown (needs imagemagick + ghostscript,
  -- both installed via Homebrew). Ghostty supports the graphics protocol.
  {
    "folke/snacks.nvim",
    opts = {
      image = { enabled = true },
    },
  },
}
