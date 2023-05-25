```{code-cell}
---
tags: [hide-input]
---

# Filters

# The following filters are applied to the PRs for the following analysis:
#
# - Only PRs to the default development branch (e.g `main`)[^master_to_main]
#  are considered.
# - Only PRs from users with _active_ GitHub accounts are considered. For example,
#   if a user opened a Pull Request in 2016, but then deleted their GitHub account
#   in 2017, then this PR is excluded from the analysis.
# - PRs opened by dependabot are excluded.

# Only look at PRs to the main development branch - ignore backports,
# gh-pages, etc.
default_branches = {"main", "master"}  # Account for default branch update
prs = [pr for pr in prs if pr["baseRefName"] in default_branches]

# Drop data where PR author is unknown (e.g. github account no longer exists)
prs = [pr for pr in prs if pr["author"]]  # Failed author query results in None

# Filter out PRs by bots
bot_filter = {
  "dependabot-preview",
  "github-actions",
  "meeseeksmachine",
  "pre-commit-ci[bot]"
}
prs = [pr for pr in prs if pr["author"]["login"] not in bot_filter]
```
