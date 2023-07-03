### New issues

%TODO: should probably use pandas for this

```{code-cell} ipython3
---
tags: [hide-input]
---

newly_created = [
    iss for iss in issues if np.datetime64(iss["createdAt"]) > query_date
]
new_issues_closed = [iss for iss in newly_created if iss["state"] == "CLOSED"]

new_issue_lifetime = np.array(
    [
        np.datetime64(iss["closedAt"]) - np.datetime64(iss["createdAt"])
        for iss in new_issues_closed
    ],
).astype("m8[h]")  # in hours

glue("{{ project }}_num_new_issues", len(newly_created))
glue("{{ project }}_num_new_issues_closed", percent_val(len(new_issues_closed), len(newly_created)))
glue("{{ project }}_new_issue_median_lifetime", f"{np.median(new_issue_lifetime)}")
```

{glue:text}`{{ project }}_num_new_issues` new issues have been opened since
{glue:text}`{{ project }}_query_date`, of which {glue:text}`{{ project }}_num_new_issues_closed` have been
closed.

The median lifetime of new issues that were created and closed in this period
is {glue:text}`{{ project }}_new_issue_median_lifetime`.

% TODO: replace with bokeh or some other live-plot
% TODO: for any remaining static/mpl plots, set default params for things
% like fontsize in a mplstyle file.

%TODO: query_date should be synced up with the query that generates data, rather
%than specified manually

```{code-cell}
query_date = np.datetime64("2020-01-01 00:00:00")

# Load data
with open("devstats-data/{{ project }}_issues.json", "r") as fh:
    issues = [item["node"] for item in json.loads(fh.read())]

glue("{{ project }}_query_date", str(query_date.astype("M8[D]")))
```

```{code-cell}
---
tags: [hide-input]
---
title = (
    f"Lifetime of issues created and closed in the last "
    f"{(np.datetime64(datetime.datetime.now()) - query_date).astype('m8[D]')}"
)
h, bedges = np.histogram(
    new_issue_lifetime.astype("m8[D]").astype(int), bins=np.arange(30)
)

p = figure(
    width=670,
    height=400,
    title=title,
    tooltips=[("lifetime", "@right days"), (r"# issues", "@top")],
)
p.quad(top=h, bottom=0, left=bedges[:-1], right=bedges[1:])
p.xaxis.axis_label = "Issue lifetime (days)"
p.yaxis.axis_label = "# Issues"
show(p)
```
