import json
import os
import os.path
import sys

import yaml
from plumbum import FG
from plumbum.cmd import cp, git, mkdir

from .oca_dependencies2configs import main as oca_deps2configs

# TODO: update link to fork
COMMIT_MESSAGE = """:construction_worker_man: sync DINAR

Pushed from  https://github.com/itpp-labs/DINAR/.github/workflows/fork2repos.yml
"""
FORK_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def main(config, bot_token, bot_name, bot_email):
    print("Config:\n")
    print(json.dumps(config, indent=4, sort_keys=True))
    cmd(git["config", "--global", "user.name", bot_name])
    cmd(git["config", "--global", "user.email", bot_email])

    mkdir["-p", "REPOS"] & FG
    branches = config["branches"]
    for repo in config["repos"]:
        for br in branches:
            sync_repo(repo, br, bot_token)


def sync_repo(repo, br, bot_token):
    repo_path = os.path.join("REPOS", repo)
    repo_owner, repo_name = repo.split("/")
    mkdir["-p", repo_path] & FG
    if dir_is_empty(repo_path):
        cmd(
            git[
                "clone",
                "--branch",
                br,
                "https://{}@github.com/{}/{}.git".format(
                    bot_token, repo_owner, repo_name
                ),
                repo_path,  # where to clone
            ]
        )
    else:
        try:
            cmd(git["-C", repo_path, "checkout", "-b", br, "origin/%s" % br])
        except Exception:
            # no such branch
            return

    # STATIC FILES
    static_files_path = os.path.join(FORK_PATH, "static-files")
    cmd(cp["-rTv", os.path.join(static_files_path, "all"), repo_path])
    cmd(cp["-rTv", os.path.join(static_files_path, br), repo_path])

    # EDITABLE FILES
    editable_files_path = os.path.join(FORK_PATH, "editable-files")
    mkdir["-p", os.path.join(repo_path, ".DINAR/image/dependencies/")] & FG
    # copy requirements.txt
    cmd(
        cp[
            "-n",
            os.path.join(repo_path, "requirements.txt"),
            os.path.join(repo_path, ".DINAR/image/dependencies/pip.txt"),
        ]
    )
    # check if oca_dependencies file is not converted to addons.yaml yet
    oca_dependencies_txt = os.path.join(repo_path, "oca_dependencies.txt")
    addons_yaml = os.path.join(repo_path, ".DINAR/image/src/addons.yaml")
    repos_yaml = os.path.join(repo_path, ".DINAR/image/src/repos.yaml")
    run_oca2configs = os.path.exists(oca_dependencies_txt) and not os.path.exists(
        addons_yaml
    )
    # copy other files
    cmd(cp["-rnTv", editable_files_path, repo_path])
    if run_oca2configs:
        # make addons.yaml from oca_dependencies.txt
        oca_deps2configs(oca_dependencies_txt, addons_yaml, repos_yaml)

    # COMMIT
    cmd(git["-C", repo_path, "add", "--all"])
    try:
        cmd(git["-C", repo_path, "commit", "-m", COMMIT_MESSAGE])
    except Exception:
        # nothing to commit
        return
    cmd(git["-C", repo_path, "push"])


def dir_is_empty(path):
    return len(os.listdir(path)) == 0


def cmd(command):
    print(command)
    print(command())


if __name__ == "__main__":
    config_filename = sys.argv[1]
    bot_token = sys.argv[2]
    bot_name = sys.argv[3] or "Github Actions"
    bot_email = sys.argv[4] or "actions@github.com"
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)
    main(config, bot_token, bot_name, bot_email)
