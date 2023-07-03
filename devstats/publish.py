import os
import sys
from glob import glob
import shutil
import re
import functools

import click


@click.command()
@click.argument("project")
@click.option(
    "-o", "--outdir", default="source", help="Output directory", show_default=True
)
def template(project, outdir):
    """Generate myst report templates

    These templates are copied from `devstats`, and still need to be compiled
    to substitute variables.
    """
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, project), exist_ok=True)

    print(f"Populating [{outdir}] with templates for [{project}] report:", flush=True)

    report_files = glob(os.path.join(os.path.dirname(__file__), "reports/*.md"))
    for f in report_files:
        dest = f"{outdir}/{project}/{os.path.basename(f)}"
        print(f" - {dest}")
        shutil.copyfile(f, dest)


def _include_file(basedir, x):
    fn = x.group(1)
    with open(os.path.join(basedir, fn)) as f:
        return f.read()


@click.command()
@click.argument("project")
@click.option(
    "-t",
    "--templatedir",
    default="source",
    help="Template directory",
    show_default=True,
)
@click.option(
    "-o", "--outdir", default="build", help="Output directory", show_default=True
)
def publish(project, templatedir, outdir):
    """Compile templates (substitute variables) into markdown files ready for sphinx / myst

    Include sections like the following are executed:

    ```
    {include} filename.md
    ```

    Thereafter, the following variables are substituted:

      - `{{ project }}`: Name of the project

    """
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, project), exist_ok=True)

    variables = {"project": project}

    print(f"Templating [{project}] report from [{templatedir}] to [{outdir}]...")

    templatedir = f"{templatedir}/{project}"
    template_files = [f"{templatedir}/index.md"]

    for f in template_files:
        with open(f) as fh:
            template = fh.read()
        dest_dir = f"{outdir}/{project}"
        dest = f"{dest_dir}/{os.path.basename(f)}"
        with open(dest, "w") as fh:
            print(f" - {dest}")
            # Handle myst includes
            template = re.sub(
                r"```{include}\s*(.*)\s*```",
                functools.partial(_include_file, templatedir),
                template,
                flags=re.MULTILINE,
            )

            for v in variables:
                template = template.replace("{{ " + v + " }}", variables[v])

            fh.write(template)
