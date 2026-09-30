-- GitHub Dark Default — matched to Ghostty (theme = "GitHub Dark Default").
return {
  {
    "projekt0n/github-nvim-theme",
    name = "github-theme",
    lazy = false,
    priority = 1000,
    opts = {
      options = {
        transparent = true, -- use Ghostty's #0d1117 background
        styles = { comments = "italic", keywords = "italic" },
      },
    },
    config = function(_, opts)
      require("github-theme").setup(opts)
    end,
  },
  {
    "LazyVim/LazyVim",
    opts = { colorscheme = "github_dark_default" },
  },
}
