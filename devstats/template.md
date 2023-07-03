---
jupytext:
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.13.6
kernelspec:
  display_name: Python 3
  language: python
  name: python3
orphan: true
---

# `{{ project }}`

```{code-cell} ipython3
---
tags: [remove-cell]
---

import json
import functools
import datetime
from dateutil.parser import isoparse
import warnings
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from myst_nb import glue

glue = functools.partial(glue, display=False)

def percent_val(val, denom):
    return f"{val} ({100 * val / denom:1.0f}%)"

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message="parsing timezone"
)
```

```{code-cell} ipython3
# For interactive plots
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import TeX
output_notebook()
```

%TODO improve handling of datetimes (super annoying)

A snapshot of the development on the {{ project }} project.

## Issues

%TODO: query_date should be synced up with the query that generates data, rather
%than specified manually

```{code-cell} ipython3
query_date = np.datetime64("2020-01-01 00:00:00")

# Load data
with open("../devstats-data/{{ project }}_issues.json", "r") as fh:
    issues = [item["node"] for item in json.loads(fh.read())]

glue("{{ project }}_query_date", str(query_date.astype("M8[D]")))
```

{{ new_issues }}

{{ time_to_response }}

{{ first_responders }}

## Pull Requests

```{code-cell} ipython3
---
tags: [hide-input]
---

with open("../devstats-data/{{ project }}_prs.json", "r") as fh:
    prs = [item["node"] for item in json.loads(fh.read())]

### Filters

# Only look at PRs to the main development branch - ignore backports, gh-pages,
# etc.
default_branches = {"main", "master"}  # Account for default branch update
prs = [pr for pr in prs if pr["baseRefName"] in default_branches]

# Drop data where PR author is unknown (e.g. github account no longer exists)
prs = [pr for pr in prs if pr["author"]]  # Failed author query results in None

# Filter out PRs by bots
bot_filter = {"dependabot-preview", "github-actions", "meeseeksmachine", "pre-commit-ci[bot]"}
prs = [pr for pr in prs if pr["author"]["login"] not in bot_filter]
```

The following filters are applied to the PRs for the following analysis:

- Only PRs to the default development branch (e.g `main`)[^master_to_main]
  are considered.
- Only PRs from users with _active_ GitHub accounts are considered. For example,
  if a user opened a Pull Request in 2016, but then deleted their GitHub account
  in 2017, then this PR is excluded from the analysis.
- PRs opened by dependabot are excluded.

{{ merged_prs_over_time }}

{{ pr_lifetime }}

{{ mergeability_of_open_prs }}

{{ number_of_pr_participants }}

{{ where_contributions_come_from }}

{{ pony_factor }}
