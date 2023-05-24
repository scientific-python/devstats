import os
import sys
from glob import glob


def publisher(project):
    os.makedirs("_generated", exist_ok=True)
    report_files = glob(os.path.join(os.path.dirname(__file__), "reports/*.md"))

    for report in report_files:
        print(f"Generating {project} report...", end="")
        with open(report) as fh:
            template = fh.read()
        with open(f"_generated/{project}.md", "w") as fh:
            fh.write(template.replace("{{ project }}", project))
        print("OK")
