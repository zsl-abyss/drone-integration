#! /usr/bin/env python
import sys

import yaml


def main(
    git_repository: str,
    git_branch: str,
    git_commit: str,
):
    # Load instance template.
    with open("drone-worker-template.yaml") as fo:
        instance = yaml.safe_load(fo)

    # Set instance name.
    tag = next(
        filter(
            lambda el: el["Key"] == "Name",
            instance["TagSpecifications"][0]["Tags"],
        )
    )
    tag["Value"] = f"drone-worker-{git_repository}-{git_branch}-{git_commit}"

    # Set git repository, branch and commit hash.
    tag = next(
        filter(
            lambda el: el["Key"] == "Git Repository",
            instance["TagSpecifications"][0]["Tags"],
        )
    )
    tag["Value"] = git_repository
    tag = next(
        filter(
            lambda el: el["Key"] == "Git Branch",
            instance["TagSpecifications"][0]["Tags"],
        )
    )
    tag["Value"] = git_branch
    tag = next(
        filter(
            lambda el: el["Key"] == "Git Commit",
            instance["TagSpecifications"][0]["Tags"],
        )
    )
    tag["Value"] = git_commit

    # Set user data.
    with open("cloud-config.yaml") as fo:
        config = yaml.safe_load(fo)
        user_data = "#cloud-config\n" + yaml.safe_dump(config)

    instance["UserData"] = user_data

    # Save instance cli input yaml file.
    with open("cli-input.yaml", "w") as fo:
        yaml.safe_dump(instance, fo)


if __name__ == "__main__":
    git_repository = sys.argv[1]
    git_branch = sys.argv[2]
    git_commit = sys.argv[3]
    main(
        git_repository=git_repository,
        git_branch=git_branch,
        git_commit=git_commit,
    )
