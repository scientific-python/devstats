```{code-cell}
---
tags: [remove-cell]
---

import json
import functools
import datetime
from dateutil.parser import isoparse
import warnings
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from myst_nb import glue

glue = functools.partial(glue, display=False)

def percent_val(val, denom):
    return f"{val} ({100 * val / denom:1.0f}%)"

warnings.filterwarnings(
    "ignore", category=DeprecationWarning, message="parsing timezone"
)
```

```{code-cell}
# For interactive plots
from bokeh.plotting import figure, show, output_notebook
from bokeh.models import TeX
output_notebook()
```
