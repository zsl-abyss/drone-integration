#! /usr/bin/env python3

"""
This scrip reads content of the `drone-worker-template.yaml' and
`cloud-config.yaml' files and creates a `cli-input.yaml' so it can be be
provided as the `--cli-input-yaml' option of the AWS CLI command `aws ec2
run-instances'. For example:
  aws ec2 run-instances --cli-input-yaml file://cli-input.yaml
"""


import argparse

import __main__
import yaml


def main(
    git_repository: str,
    git_branch: str,
    git_commit: str,
    drone_build_number: str,
):
    # Load instance template.
    with open("./drone/drone-worker-template.yaml") as fo:
        instance = yaml.safe_load(fo)

    # Set tags for: git repository, branch, commit hash, build number and
    # instance name.
    instance_name = (
        f"drone-worker:{git_repository}:{git_branch}:{git_commit}:{drone_build_number}"
    )
    metadata = dict(
        (
            ("Git Repository", git_repository),
            ("Git Branch", git_branch),
            ("Git Commit", git_commit),
            ("Drone Build Number", drone_build_number),
            ("Name", instance_name),
        ),
    )
    for key, value in metadata.items():
        tag = next(
            filter(
                lambda el: el["Key"] == key,
                instance["TagSpecifications"][0]["Tags"],
            )
        )
        tag["Value"] = value

    # Set user data.
    with open("./drone/cloud-config.yaml") as fo:
        config = yaml.safe_load(fo)
        user_data = "#cloud-config\n" + yaml.safe_dump(config)

    instance["UserData"] = user_data

    # Save instance cli input yaml file.
    with open("cli-input.yaml", "w") as fo:
        yaml.safe_dump(instance, fo)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__main__.__doc__,
    )
    parser.add_argument(
        "git_repository",
        nargs="?",
        default="{git-repository}",
        help="Full name of the repository, e.g. 'abyss/abyss-fabric'",
    )
    parser.add_argument(
        "git_branch",
        nargs="?",
        default="{git-branch}",
        help="Branch name, e.g. 'master'",
    )
    parser.add_argument(
        "git_commit",
        nargs="?",
        default="{git-commit}",
        help="Commit hash, e.g. 'a1b2c3d4'",
    )
    parser.add_argument(
        "drone_build_number",
        nargs="?",
        default="{drone-build-number}",
        help="Build number, e.g. '42'",
    )
    args = parser.parse_args()

    git_repository = args.git_repository
    git_branch = args.git_branch
    git_commit = args.git_commit
    drone_build_number = args.drone_build_number

    main(
        git_repository=git_repository,
        git_branch=git_branch,
        git_commit=git_commit,
        drone_build_number=drone_build_number,
    )
