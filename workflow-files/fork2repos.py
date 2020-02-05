import yaml
import ast
import sys
import os
import os.path
import json
from plumbum.cmd import git, mkdir, cp
from plumbum import FG, BG


# TODO: update link to fork
COMMIT_MESSAGE=""":construction_worker_man: sync DINAR

Pushed from  https://github.com/itpp-labs/DINAR/.github/workflows/fork2repos.yml
"""
FORK_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))



def main(token, config):
    print("Config:\n")
    print(json.dumps(config, indent=4, sort_keys=True))
    mkdir["-p", "REPOS"] & FG
    branches = config['branches']
    for repo in config['repos']:
        for br in branches:
            sync_repo(repo, br, token)


def sync_repo(repo, br, token):
    repo_path = os.path.join("REPOS", repo)
    repo_owner, repo_name = repo.split('/')
    mkdir["-p", repo_path] & FG
    if dir_is_empty(repo_path):
        cmd(git[
            "clone",
            "--branch", br,
            "https://%s@github.com/%s/%s.git" % (token, repo_owner, repo_name),
            repo_path  # where to clone
        ])
    else:
        try:
            cmd(git[
                "-C", repo_path,
                "checkout",
                "-b", br,
                "origin/%s" % br
            ])
        except:
            # no such branch
            return

    static_files_path = os.path.join(FORK_PATH, "static-files")
    cmd(cp[
        "-rTv",
        static_files_path,
        repo_path
    ])
    cmd(git[
        "-C", repo_path,
        "add",
        "--all"
    ])
    try:
        cmd(git[
            "-C", repo_path,
            "commit",
            "-m",
            COMMIT_MESSAGE
        ])
    except:
        # nothing to commit
        return
    cmd(git[
        "-C", repo_path,
        "push"
    ])

def dir_is_empty(path):
    return len(os.listdir(path)) == 0

def cmd(command):
    print(command)
    command & FG


if __name__ == '__main__':
    token = sys.argv[1]
    config_filename= sys.argv[2]
    with open(config_filename) as config_file:
        config = yaml.safe_load(config_file)
    main(token, config)
