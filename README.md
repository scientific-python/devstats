# devstats

This repository holds the devstats package. devstats is a command line tool that uses the GitHub GraphQL API to
generate developer statistics and a developer statistics report for a specified
project.

## OAuth key for accessing GitHub

Per the [GitHub GraphQL API docs](https://developer.github.com/v4/guides/forming-calls/),
you need a personal access token with `public_repo` permission to access the GraphQL API.

This code expects the personal access token to be in the environment variable
`GRAPH_API_KEY`.

You can [create a personal access token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) on GitHub. Save the token in a trusted location.

Finally, add the token to your environment using:

`export GRAPH_API_KEY=<yourkey>`

## Query script

The `query.py` script can be used to collect data for other projects like
so: `python query.py <repo_owner> <repo_name>` where `repo_owner` and
`repo_name` are the names of the **org** and **repo** on GitHub, respectively.

First you need to install the required Python packages:

```bash
pip install -r requirements.txt
```

To download the latest data for `pandas` use the following command:

```bash
devstats query.py pandas-dev pandas
```

The command will collect information from GitHub and generate two output files in the same directory where you ran it as follows:

packagename_issues.json: this file contains information about issues for the repository of interest.  
packagename_PRs.json: this file contains information associated with pull requests for the repository of interest.
