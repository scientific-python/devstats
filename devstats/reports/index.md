---
kernelspec:
  display_name: Python 3
  name: ipython3
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
with open("{{ project }}_issues.json", "r") as fh:
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
```

```{include} prs_filter.md

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
