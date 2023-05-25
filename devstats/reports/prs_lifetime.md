### PR lifetime

The following plot shows the "survival" of PRs over time.
That means, the plot shows how many PRs are open for at least these many days.
This is seperated into PRs that are merged and those that are still open
(closed but unmerged PRs are not included currently).

```{code-cell}
---
tags: [hide-input]
---

merged_prs = [pr for pr in prs if pr['state'] == 'MERGED']
lifetimes_merged = np.array(
    [isoparse(pr["mergedAt"]) - isoparse(pr["createdAt"]) for pr in merged_prs],
    dtype="m8[m]").view("int64") / (60 * 24)  # days
lifetimes_merged.sort()

#closed_prs = [pr for pr in prs if pr['state'] == 'CLOSED']
#lifetimes_closed = np.array(
#    [isoparse(pr["mergedAt"]) - isoparse(pr["createdAt"]) for pr in closed_prs],
#    dtype="m8[m]").view("int64") / (60 * 24)  # days
#lifetimes_closed.sort()


# Use the newest issue to guess a time when the data was generated.
# Can this logic be improved?
current_time = isoparse(max(iss["createdAt"] for iss in issues))

open_prs = [pr for pr in prs if pr['state'] == 'OPEN']
age_open = np.array(
    [current_time - isoparse(pr["createdAt"]) for pr in open_prs],
    dtype="m8[m]").view("int64") / (60 * 24)  # days
age_open.sort()

fig, ax = plt.subplots(figsize=(6, 4))
number_merged = np.arange(1, len(lifetimes_merged)+1)[::-1]
ax.step(lifetimes_merged, number_merged, label="Merged")

#ax.step(lifetimes_closed, np.arange(1, len(lifetimes_closed)+1)[::-1])

number_open = np.arange(1, len(age_open)+1)[::-1]
ax.step(age_open, number_open, label="Open")

# Find the first point where closed have a bigger survival than open PRs:
all_lifetimes = np.concatenate([lifetimes_merged, age_open])
all_lifetimes.sort()

number_merged_all_t = np.interp(all_lifetimes, lifetimes_merged, number_merged)
number_open_all_t = np.interp(all_lifetimes, age_open, number_open)

first_idx = np.argmax(number_merged_all_t < number_open_all_t)
first_time = all_lifetimes[first_idx]

ax.vlines(
        [first_time], 0, 1, transform=ax.get_xaxis_transform(), colors='k',
        zorder=0, linestyle="--")

ax.annotate(
    f"{round(first_time)} days",
    xy=(first_time, number_open_all_t[first_idx]),
    xytext=(5, 5), textcoords="offset points",
    va="bottom", ha="left")

ax.legend()
ax.set_xlabel("Time until merged or time open [days]")
ax.set_ylabel(r"# of PRs open this long or longer")
ax.set_xscale("log")
fig.autofmt_xdate()
fig.tight_layout();
```
