import ast
import sys
import os.path
from plumbum.cmd import git, cat
from plumbum import FG, BG

MANIFESTS=[
    "__manifest__.py",
    "__openerp__.py"
]

def main(base_branch):
    git["fetch", "origin", base_branch] & FG
    changed_files = git(
        "diff",
        "--name-only",
        "origin/%s...HEAD" % base_branch
    ).split("\n")
    changed_files = filter(None, changed_files)

    modules = {}
    other_folders = {}
    root_files = []
    for f in changed_files:
        if '/' not in f:
            root_files.append(f)
            continue
        module_name = f.split('/')[0]
        for manifest in MANIFESTS:
            manifest_path = os.path.join(module_name, manifest)
            if not os.path.exists(manifest_path):
                continue
            try:
                manifest_data = ast.literal_eval()
            except:
                manifest_data = {
                    "error": "cannot parse"
                }
            modules[module_name] = {
                "manifest": cat(manifest_path)
            }
            break
        else:
            other_folders.setdefault(module_name, [])
            other_folders[module_name].append(f)

    # TODO: filter installable modules
    set_github_var('PR_UPDATED_MODULES_INSTALLABLE', ','.join(modules.keys()))

def set_github_var(name, value):
    print ("%s=%s" % (name, value))
    print ("::set-env name=%s::%s" % (name, value))

if __name__ == '__main__':
    print (sys.argv)
    base_branch = sys.argv[1]
    main(base_branch)
