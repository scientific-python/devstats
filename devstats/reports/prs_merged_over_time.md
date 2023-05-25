### Merged PRs over time

A look at merged PRs over time.

```{code-cell}
---
tags: [hide-input]
---

# All contributors
merged_prs = [pr for pr in prs if pr['state'] == 'MERGED']
merge_dates = np.array([pr['mergedAt'] for pr in merged_prs], dtype=np.datetime64)
binsize = np.timedelta64(30, "D")
date_bins = np.arange(merge_dates[0], merge_dates[-1], binsize)
h_all, bedges = np.histogram(merge_dates, date_bins)
bcenters = bedges[:-1] + binsize / 2
smoothing_interval = 4  # in units of bin-width

# First-time contributors
first_time_contributor = []
prev_contrib = set()
for record in merged_prs:
    try:
        author = record['author']['login']
    except TypeError:  # Author no longer has GitHub account
        first_time_contributor.append(None)
        continue
    if author not in prev_contrib:
        first_time_contributor.append(True)
        prev_contrib.add(author)
    else:
        first_time_contributor.append(False)
# Object dtype for handling None
first_time_contributor = np.array(first_time_contributor, dtype=object)
# Focus on first time contributors
ftc_mask = first_time_contributor == True
ftc_dates = merge_dates[ftc_mask]

h_ftc, bedges = np.histogram(ftc_dates, date_bins)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))
for ax, h, whom in zip(
    axes.ravel(), (h_all, h_ftc), ("all contributors", "first-time contributors")
):
    ax.bar(bcenters, h, width=binsize, label="Raw")
    ax.plot(
        bcenters,
        np.convolve(h, np.ones(smoothing_interval), 'same') / smoothing_interval,
        label=f"{binsize * smoothing_interval} moving average",
        color='tab:orange',
        linewidth=2.0,
    )

    ax.set_title(f'{whom}')
    ax.legend()

fig.suptitle("Merged PRs from:")
axes[0].set_xlabel('Time')
axes[0].set_ylabel(f'# Merged PRs / {binsize} interval')
axes[1].set_ylim(axes[0].get_ylim())
fig.autofmt_xdate()

# TODO: Replace this with `glue` once the glue:figure directive supports
# alt-text
import os
os.makedirs("thumbs", exist_ok=True)
plt.savefig("thumbs/{{ project }}.png", bbox_inches="tight")
```
