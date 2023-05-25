### Number of PR participants

% TODO: Similar analysis, but replace num participants with some metrics of
% how "big" the PR is; num LOC changed, etc.

```{code-cell}
---
tags: [hide-input]
---
# Get the lifetimes and number of participants for merged PRs
lifetimes = np.array(
    [isoparse(pr["mergedAt"]) - isoparse(pr["createdAt"]) for pr in merged_prs],
    dtype="m8[h]",
)
num_participants = np.array([pr["participants"]["totalCount"] for pr in merged_prs])

title = "Distribution of lifetimes for merged PRs based on the number of participants"

p = figure(width=600, height=300, title=title)
p.xgrid.grid_line_color = None
p.xaxis.ticker = sorted(np.unique(num_participants))
p.yaxis.axis_label = "PR lifetime (hours)"
p.scatter(x=num_participants, y=lifetimes.astype(int), size=9, alpha=0.4)
show(p)
```
