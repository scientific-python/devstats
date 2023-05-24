import os
import requests
import sys
import json
import click
from glob import glob
import re

try:
    token = os.environ["GRAPH_API_KEY"]
except KeyError:
    print("You need to set GRAPH_API_KEY")
    print("But you shouldn't use this yet.")
    sys.exit()

endpoint = r"https://api.github.com/graphql"
headers = {"Authorization": f"bearer {token}"}


def load_query_from_file(fname, repo_owner="numpy", repo_name="numpy"):
    """
    Load an 'issue' query from file and set the target repository, where
    the target repository has the format:

    https://github.com/<repo_owner>/<repo_name>

    Parameters
    ----------
    fname : str
        Path to a text file containing a valid issue query according to the
        GitHub GraphQL schema.
    repo_owner : str
        Owner of target repository on GitHub. Default is 'numpy'.
    repo_name : str
        Name of target repository on GitHub. Default is 'numpy'.

    Returns
    -------
    query : str
        Query loaded from file in text form suitable for ``send_query``.

    Notes
    -----
    This function expects the query to have a specific form and will not work
    for general GitHub GraphQL queries. See ``examples/`` for some valid
    templated issue queries.
    """
    with open(fname) as fh:
        query = fh.read()
        # Set target repo from template
        query = query.replace("_REPO_OWNER_", repo_owner)
        query = query.replace("_REPO_NAME_", repo_name)
    return query


def send_query(query, query_type, cursor=None):
    """
    Send a GraphQL query via requests.post

    No validation is done on the query before sending. GitHub GraphQL is
    supported with the `cursor` argument.

    Parameters
    ----------
    query : str
        The GraphQL query to be sent
    query_type : {"issues", "pullRequests"}
        The object being queried according to the GitHub GraphQL schema.
        Currently only issues and pullRequests are supported
    cursor : str, optional
        If given, then the cursor is injected into the query to support
        GitHub's GraphQL pagination.

    Returns
    -------
    dict
        The result of the query (json) parsed by `json.loads`

    Notes
    -----
    This is intended mostly for internal use within `get_all_responses`.
    """
    # TODO: Expand this, either by parsing the query type from the query
    # directly or manually adding more query_types to the set
    if query_type not in {"issues", "pullRequests"}:
        raise ValueError(
            "Only 'issues' and 'pullRequests' queries are currently supported"
        )
    # TODO: Generalize this
    # WARNING: The cursor injection depends on the specific structure of the
    # query, this is the main reason why query types are limited to issues/PRs
    if cursor is not None:
        cursor_insertion_key = query_type + "("
        cursor_ind = query.find(cursor_insertion_key) + len(cursor_insertion_key)
        query = query[:cursor_ind] + f'after:"{cursor}", ' + query[cursor_ind:]
    # Build request payload
    payload = {"query": "".join(query.split("\n"))}
    response = requests.post(endpoint, json=payload, headers=headers)
    return json.loads(response.content)


def get_all_responses(query, query_type):
    """
    Helper function to bypass GitHub GraphQL API node limit.
    """
    # Get data from a single response
    print(f"Retrieving first page...", end="", flush=True)
    initial_data = send_query(query, query_type)
    data, last_cursor, total_count = parse_single_query(initial_data, query_type)

    # Continue requesting data (with pagination) until all are acquired
    while len(data) < total_count:
        rdata = send_query(query, query_type, cursor=last_cursor)
        pdata, last_cursor, _ = parse_single_query(rdata, query_type)
        data.extend(pdata)
        print(
            f"OK\nRetrieving {len(data)} out of {total_count} values...",
            end="",
            flush=True,
        )
    print("OK")
    return data


def parse_single_query(data, query_type):
    """
    Parse the data returned by `send_query`

    .. warning::

       Like `send_query`, the logic here depends on the specific structure
       of the query (e.g. it must be an issue or PR query, and must have a
       total count).
    """
    try:
        total_count = data["data"]["repository"][query_type]["totalCount"]
        data = data["data"]["repository"][query_type]["edges"]
        last_cursor = data[-1]["cursor"]
    except KeyError as e:
        print(data)
        raise e
    return data, last_cursor, total_count


class GithubGrabber:
    """
    Pull down data via the GitHub APIv.4 given a valid GraphQL query.
    """

    def __init__(self, query_fname, query_type, repo_owner="numpy", repo_name="numpy"):
        """
        Create an object to send/recv queries related to the issue tracker
        for the given repository via the GitHub API v.4.

        The repository to query against is given by:
        https://github.com/<repo_owner>/<repo_name>

        Parameters
        ----------
        query_fname : str
            Path to a valid GraphQL query conforming to the GitHub GraphQL
            schema
        query_type : {"issues", "pullRequests"}
            Type of object that is being queried according to the GitHub GraphQL
            schema. Currently only "issues" and "pullRequests" are supported.
        repo_owner : str
            Repository owner. Default is "numpy"
        repo_name : str
            Repository name. Default is "numpy"
        """
        self.query_fname = query_fname
        self.query_type = query_type  # TODO: Parse this directly from query
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.raw_data = None
        self.load_query()

    def load_query(self):
        self.query = load_query_from_file(
            self.query_fname, self.repo_owner, self.repo_name
        )

    def get(self):
        """
        Get JSON-formatted raw data from the query.
        """
        self.raw_data = get_all_responses(self.query, self.query_type)

    def dump(self, outfile):
        """
        Dump raw json to `outfile`.
        """
        if not self.raw_data:
            raise ValueError("raw_data is currently empty, nothing to dump")

        with open(outfile, "w") as outf:
            print(f"Writing [{outfile}]")
            json.dump(self.raw_data, outf)


@click.command()
@click.argument("repo_owner")
@click.argument("repo_name")
def main(repo_owner, repo_name):
    """Download and save issue and pr data for `repo_owner`/`repo_name`."""

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
            repo_owner=repo_owner,
            repo_name=repo_name,
        )
        data.get()
        ftype = {"issues": "issues", "pullRequests": "PRs"}
        data.dump(f"{repo_name}_{ftype.get(qtype, qtype)}.json")


if __name__ == "__main__":
    main()
