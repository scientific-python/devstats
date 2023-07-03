---
file_format: mystnb
kernelspec:
  display_name: Python 3
  name: python3
---

# `{{ project }}`

```{include} preamble.md

```

A snapshot of the development on the {{ project }} project.

## Issues

% TODO: query_date should be synced up with the query that generates data,
% rather than specified manually

% TODO improve handling of datetimes (super annoying)

```{code-cell}
query_date = np.datetime64("2020-01-01 00:00:00")

# Load data
with open("devstats-data/{{ project }}_issues.json", "r") as fh:
    issues = [item["node"] for item in json.loads(fh.read())]

glue("devstats-data/{{ project }}_query_date", str(query_date.astype("M8[D]")))
```

```{include} new_issues.md

```

```{include} issue_time_to_response.md

```

```{include} issue_first_responders.md

```

## Pull Requests

```{code-cell}
---
tags: [hide-input]
---
with open("devstats-data/{{ project }}_prs.json", "r") as fh:
    prs = [item["node"] for item in json.loads(fh.read())]

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

```{include} prs_merged_over_time.md

```

```{include} prs_lifetime.md

```

```{include} prs_mergeability.md

```

```{include} prs_participants.md

```

```{include} prs_contributor_origin.md

```

```{include} prs_pony_factor.md

```
