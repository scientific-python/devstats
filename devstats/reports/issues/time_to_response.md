### Time to response

```{code-cell} ipython3
---
tags: [hide-input]
---
# Remove issues that are less than a day old for the following analysis
newly_created_day_old = [
    iss for iss in newly_created
    if np.datetime64(datetime.datetime.now()) - np.datetime64(iss["createdAt"])
    > np.timedelta64(1, "D")
]

# TODO: really need pandas here
commented_issues = [
    iss for iss in newly_created_day_old
    if any(
        e["node"]["__typename"] == "IssueComment" for e in iss["timelineItems"]["edges"]
    )
]
first_commenters, time_to_first_comment = [], []
for iss in commented_issues:
    for e in iss["timelineItems"]["edges"]:
        if e["node"]["__typename"] == "IssueComment":
            try:
                user = e["node"]["author"]["login"]
            except TypeError as err:
                # This can happen e.g. when a user deletes their GH acct
                user = "UNKNOWN"
            first_commenters.append(user)
            dt = np.datetime64(e["node"]["createdAt"]) - np.datetime64(iss["createdAt"])
            time_to_first_comment.append(dt.astype("m8[m]"))
            break  # Only want the first commenter
time_to_first_comment = np.array(time_to_first_comment)  # in minutes

median_time_til_first_response = np.median(time_to_first_comment.astype(int) / 60)

cutoffs = [
    np.timedelta64(1, "h"),
    np.timedelta64(12, "h"),
    np.timedelta64(24, "h"),
    np.timedelta64(3, "D"),
    np.timedelta64(7, "D"),
    np.timedelta64(14, "D"),
]
num_issues_commented_by_cutoff = np.array(
    [
        np.sum(time_to_first_comment < cutoff) for cutoff in cutoffs
    ]
)

# TODO: Update IssueComment query to include:
#  - whether the commenter is a maintainer
#  - datetime of comment
# This will allow analysis of what fraction of issues are addressed by
# maintainers vs. non-maintainer, and the distribution of how long an issue
# usually sits before it's at least commented on

glue(
    "{{ project }}_num_new_issues_responded",
    percent_val(len(commented_issues), len(newly_created_day_old))
)

glue("{{ project }}_new_issues_at_least_1_day_old", len(newly_created_day_old))
glue("{{ project }}_median_response_time", f"{median_time_til_first_response:1.0f}")
```

Of the {glue:text}`{{ project }}_new_issues_at_least_1_day_old` issues that are at least 24
hours old, {glue:text}`{{ project }}_num_new_issues_responded` of them have been commented
on.
The median time until an issue is first responded to is
{glue:text}`{{ project }}_median_response_time` hours.

```{code-cell} ipython3
---
tags: [hide-input]
---
from bokeh.transform import dodge

title = f"Percentage of issues opened since {query_date} that are commented on within..."

x = [str(c) for c in cutoffs]
y = 100 * num_issues_commented_by_cutoff / len(newly_created_day_old)

p = figure(
    x_range=x,
    y_range=(0, 100),
    width=670,
    height=400,
    title=title,
    tooltips=[(r"%", "@top")],
)
p.vbar(x=x, top=y, width=0.8)
p.xaxis.axis_label = "Time interval"
p.yaxis.axis_label = "Percentage of issues commented on within interval"
show(p)
```
