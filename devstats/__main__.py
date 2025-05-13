import collections
import datetime
import json
import os
import re
import sys
from glob import glob

import click
import requests

from .publish import publish, template
from .query import GithubGrabber


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super().__init__(name, commands, **attrs)
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
def cli():
    pass


@cli.command("query")
@click.argument("repo_owner")
@click.argument("repo_name")
@click.option(
    "-o",
    "--outdir",
    default="devstats-data",
    help="Output directory",
    show_default=True,
)
@click.option(
    "-d",
    "--start-date",
    default="2020-01-01T00:00:00Z",
    help="Start date for query",
    show_default=True,
)
def query(repo_owner, repo_name, outdir, start_date):
    """Download and save issue and pr data for `repo_owner`/`repo_name`"""
    os.makedirs(outdir, exist_ok=True)

    try:
        token = os.environ["GRAPH_API_KEY"]
    except KeyError:
        print("You need to set GRAPH_API_KEY")
        sys.exit()

    headers = {"Authorization": f"bearer {token}"}
    query_files = glob(os.path.join(os.path.dirname(__file__), "queries/*.gql"))

    for n, query in enumerate(query_files):
        if n != 0:
            print()

        print(f"Query: [{os.path.basename(query)}] on [{repo_owner}/{repo_name}]")
        # Parse query type from gql
        gql = open(query).read()
        qtype_match = re.match(
            r"query\s*{\s*repository\(.*?\)\s*{\s*(pullRequests|issues)",
            gql,
            flags=re.MULTILINE,
        )
        if qtype_match is None:
            print(f"Could not determine gql query type for {query}")
            sys.exit(-1)
        else:
            qtype = qtype_match.group(1)

        qname, qext = os.path.splitext(query)
        data = GithubGrabber(
            query,
            qtype,
            headers,
            repo_owner=repo_owner,
            repo_name=repo_name,
            start_date=start_date,
        )
        data.get()
        ftype = {"issues": "issues", "pullRequests": "PRs"}
        data.dump(f"{outdir}/{repo_name}_{ftype.get(qtype, qtype)}.json")

    # get stars over time
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/stargazers"
    headers = {
        "Accept": "application/vnd.github.v3.star+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        stargazers = response.json()
    else:
        print(
            "Request failed for collecting start with status code "
            f"{response.status_code}"
        )

    with open(f"{outdir}/{repo_name}_misc.json", "w") as outf:
        misc_data = {}
        misc_data["repo_owner"] = repo_owner
        misc_data["repo_name"] = repo_name
        misc_data["query_start_date"] = start_date
        misc_data["query_end_date"] = str(datetime.datetime.now())
        misc_data["repo_stars"] = [
            {"starred_at": user["starred_at"], "login": user["user"]["login"]}
            for user in stargazers
        ]
        json.dump(misc_data, outf)


cli.add_command(template)
cli.add_command(publish)
