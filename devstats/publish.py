import os
import sys
from glob import glob
import click


@click.command()
@click.argument("project")
@click.option(
    '-o', '--outdir',
    default='build', help='Output directory', show_default=True
)
def publish(project, outdir):
    """Generate myst report for `repo_owner`/`repo_name`."""
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, project), exist_ok=True)

    report_files = glob(os.path.join(os.path.dirname(__file__), "reports/*.md"))

    variables = {
        'project': project
    }

    print(f"Generating [{project}] report in [{outdir}]...", end="", flush=True)

    for report in report_files:
        with open(report) as fh:
            template = fh.read()
        with open(f"{outdir}/{project}/{os.path.basename(report)}", "w") as fh:
            for v in variables:
                template = template.replace('{{ ' + v + ' }}', variables[v])
            fh.write(template)

    print("OK")
