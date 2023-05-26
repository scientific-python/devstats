### Mergeability of Open PRs

```{code-cell} ipython3
---
tags: [hide-input]
---
open_prs = [pr for pr in prs if pr["state"] == "OPEN"]

# The GraphQL query does not reliably return information on PR mergeability.
# Warn if there are problems
if any([pr["mergeable"] == "UNKNOWN" for pr in open_prs]):
    warnings.warn(
        (
            "\n\nThe data contains PRs with unknown merge status.\n"
            "Please re-download the data to get accurate info about PR mergeability."
        ),
        UserWarning,
        stacklevel=2,
    )

conflicting_prs = [isoparse(pr["createdAt"]) for pr in open_prs if pr["mergeable"] == "CONFLICTING"]
mergeable_prs = [isoparse(pr["createdAt"]) for pr in open_prs if pr["mergeable"] == "MERGEABLE"]

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(
    [conflicting_prs, mergeable_prs],
    bins="auto",
    histtype="bar",
    label=("conflicting", "mergeable"),
    color=("tab:red", "tab:blue"),
)
ax.legend()
ax.set_xlabel("Date of PR creation")
ax.set_ylabel(r"# of conflicting PRs")
fig.autofmt_xdate()
fig.tight_layout();
```
