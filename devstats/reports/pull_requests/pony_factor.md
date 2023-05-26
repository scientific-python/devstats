### Pony factor

Another way to look at these data is in terms of the
[pony factor](https://ke4qqq.wordpress.com/2015/02/08/pony-factor-math/),
described as:

> The minimum number of contributors whose total contribution constitutes a
> majority of the contributions.

For this analysis, we will consider merged PRs as the metric for contribution.
Considering all merged PRs over the lifetime of the project, the pony factor
is: {glue:text}`{{ project }}_pony_factor`.

% TODO: pandas-ify to improve sorting

```{code-cell} ipython3
---
tags: [hide-input]
---
# Sort by number of merged PRs in descending order
num_merged_prs_per_author.sort()
num_merged_prs_per_author = num_merged_prs_per_author[::-1]

num_merged_prs = num_merged_prs_per_author.sum()
pf_thresh = 0.5
pony_factor = np.searchsorted(
    np.cumsum(num_merged_prs_per_author), num_merged_prs * pf_thresh
) + 1

fig, ax = plt.subplots()
ax.plot(
    np.arange(len(num_merged_prs_per_author)) + 1,
    np.cumsum(num_merged_prs_per_author),
    "."
)
ax.set_title(f"How the pony factor is calculated")
ax.set_xlabel("# unique contributors")
ax.set_xscale("log")
ax.set_ylabel("Cumulative sum of merged PRs / contributor")
ax.hlines(
    xmin=0,
    xmax=len(contributions_by_author),
    y=num_merged_prs * pf_thresh,
    color="tab:green",
    label=f"Pony factor threshold = {100 * pf_thresh:1.0f}%",
)
ax.legend();

glue("{{ project }}_pony_factor", pony_factor)
```

% TODO: Add:
% - Augmented pony factor (only consider contributors active in a time window)
% - pony factor over time, e.g yearly bins

[^master_to_main]: i.e. `master` or `main`.
[^only_active]: This only includes PRs from users with an active GitHub account.
