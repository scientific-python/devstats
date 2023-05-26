### Where contributions come from

There have been a total of {glue:text}`{{ project }}_num_merged_prs_with_known_authors`
merged PRs[^only_active] submitted by {glue:text}`{{ project }}_num_unique_authors_of_merged_prs`
unique authors. {glue:text}`{{ project }}_num_flyby` of these are "fly-by" PRs, i.e.
PRs from users who have contributed to the project once (to-date).

```{code-cell} ipython3
---
tags: [hide-input]
---

# Remap PRs by author
contributions_by_author = defaultdict(list)
for pr in merged_prs:
    author = pr["author"]["login"]
    contributions_by_author[author].append(pr)

num_merged_prs_per_author = np.array(
    [len(prs) for prs in contributions_by_author.values()]
)

num_flybys = np.sum(num_merged_prs_per_author == 1)

glue("{{ project }}_num_merged_prs_with_known_authors", len(merged_prs))
glue("{{ project }}_num_unique_authors_of_merged_prs", len(contributions_by_author))
glue("{{ project }}_num_flyby", percent_val(num_flybys, len(num_merged_prs_per_author)))
```

```{code-cell} ipython3
---
tags: [hide-input]
---

title = "Distribution of number of merged PRs per contributor"

x = ["1", "2", "3", "4", "5", "6 - 10", "10 - 20", "20 - 50", "> 50"]
bedges = np.array([0, 1, 2, 3, 4, 5, 10, 20, 50, sum(num_merged_prs_per_author)]) + 0.5
y, _ = np.histogram(num_merged_prs_per_author, bins=bedges)

p = figure(
    x_range=x,
    y_range=(0, 1.05 * y.max()),
    width=670,
    height=400,
    title=title,
    tooltips=[(r"# PRs merged", "@x"), ("# contributors", f"@top")],
)
p.vbar(x=x, top=y, width=0.8)
p.xaxis.axis_label = "# Merged PRs per user"
p.yaxis.axis_label = "# of unique contributors with N PRs merged"
show(p)
```
