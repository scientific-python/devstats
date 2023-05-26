### First responders

```{code-cell} ipython3
---
tags: [hide-input]
---
```

```{code-cell} ipython3
---
tags: [hide-input]
---
first_commenter_tab = pd.DataFrame(
    {
        k: v
        for k, v in zip(
            ("Contributor", "# of times commented first"),
            np.unique(first_commenters, return_counts=True),
        )
    }
)
first_commenter_tab.sort_values(
    "# of times commented first", ascending=False
).head(10)
```
