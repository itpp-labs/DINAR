import ast
import os.path
import sys

from github import Github
from plumbum.cmd import cat

MANIFESTS = ["__manifest__.py", "__openerp__.py"]


def main(token, repository, pull_number):
    github = Github(token)
    repo = github.get_repo(repository)
    pr = repo.get_pull(int(pull_number))
    changed_files = [f.filename for f in pr.get_files()]

    modules = {}
    other_folders = {}
    root_files = []
    for f in changed_files:
        if "/" not in f:
            root_files.append(f)
            continue
        module_name = f.split("/")[0]
        for manifest in MANIFESTS:
            manifest_path = os.path.join(module_name, manifest)
            if not os.path.exists(manifest_path):
                continue
            try:
                manifest_data = ast.literal_eval(cat(manifest_path))
            except Exception:
                manifest_data = {"error": "cannot parse"}
            modules[module_name] = {"manifest": manifest_data}
            break
        else:
            other_folders.setdefault(module_name, [])
            other_folders[module_name].append(f)

    # TODO: filter installable modules
    set_github_var("PR_UPDATED_MODULES_INSTALLABLE", ",".join(modules.keys()))


def cmd(command):
    print(command)
    print(command())


def set_github_var(name, value):
    print("{}={}".format(name, value))
    print("::set-env name={}::{}".format(name, value))


if __name__ == "__main__":
    print(sys.argv)
    token = sys.argv[1]
    repository = sys.argv[2]
    pull_number = sys.argv[3]
    main(token, repository, pull_number)
