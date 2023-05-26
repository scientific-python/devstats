import os
import sys
from glob import glob
from pathlib import Path


def publisher(project):
    print(f"Generating {project} report...", end="")
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "template.md")) as fh:
        template = fh.read()
 
    issues = glob(os.path.join(basedir, "reports/issues/*.md"))
    for issue in issues:
        with open(issue) as fh:
            issue_text = fh.read()
        issue_name = Path(issue).stem
        template = template.replace(f"{{{{ {issue_name} }}}}", issue_text)

    prs = glob(os.path.join(basedir, "reports/pull_requests/*.md"))
    for pr in prs:
        with open(pr) as fh:
            pr_text = fh.read()
        pr_name = Path(pr).stem
        template = template.replace(f"{{{{ {pr_name} }}}}", pr_text)

    template = template.replace("{{ project }}", project)

    os.makedirs("_generated", exist_ok=True)
    with open(f"_generated/{project}.md", "w") as fh:
        fh.write(template)

    print("OK")
