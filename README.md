# devstats

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/scientific-python/devstats/main.svg)](https://results.pre-commit.ci/latest/github/scientific-python/devstats/main)

This repository holds the `devstats` package. `devstats` is a Python command line tool that uses the GitHub GraphQL API to
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
so: `devstats query.py <repo_owner> <repo_name>` where `repo_owner` and
`repo_name` are the names of the **org** and **repo** on GitHub, respectively.

To download the latest data for `pandas` use the following command:

```bash
devstats query.py pandas-dev pandas
```

The command will collect information from GitHub and generate two output files in the same directory where you ran it as follows:

`packagename_issues.json`: this file contains information about issues for the repository of interest.
`packagename_PRs.json`: this file contains information associated with pull requests for the repository of interest.

## Development instructions

If you wish to contribute to devstats:

1. Fork and clone the repository
2. Create a new branch with your proposed feature or change to the package repository

### Code Style / Pre-commit

We use `pre-commit` to ensure the code style is consistent. To install pre-commit locally:

1. First install pre-commit: `pip install pre-commit`
2. Install all of the pre-commit hooks by running `pre-commit install`

Once you have `pre-commit` installed, the code stylers and linters
defined in the `pre-commit-config.yaml` will run each time you
commit modified changes to git locally.

### Precommit.ci Bot

We use the pre-commit CI bot to run linting tests and to auto fix
pull requests. How it works:

- Pre-commit.ci will run the CI checks via a CI run in the PR.
- After the PR is approved but before it's merged, a maintainer can run the bot to apply linting fixes via a commit to the PR. To run the bot write:

`pre-commit.ci autofix` in a comment in the PR. This will trigger another CI run to double check that the linting / code style fixes are as expected. Then you can merge!

NOTE: the pre-commit CI bot CI action will allow you to see what checks pass. It will also remind you of the command to autofix the code in the pr.
