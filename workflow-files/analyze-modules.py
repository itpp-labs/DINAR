# Copyright 2020 IT Projects Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ast
import itertools
import os.path
import sys

import yaml
from plumbum.cmd import cat

try:
    from github import Github
except ImportError:
    pass

MANIFESTS = ["__manifest__.py", "__openerp__.py"]
# https://odoo-development.readthedocs.io/en/latest/admin/server_wide_modules.html
DEFAULT_SERVER_WIDE_MODULES = {
    "13.0": ["base", "web"],
    "12.0": ["base", "web"],
    "11.0": ["web"],
    "10.0": ["web", "web_kanban"],
}


def action_updated(token, repository, pull_number, dinar_odoo_base_modules):
    github = Github(token)
    repo = github.get_repo(repository)
    pr = repo.get_pull(int(pull_number))
    changed_files = [f.filename for f in pr.get_files()]

    other_folders = {}
    root_files = []
    manifests = {}
    for f in changed_files:
        if "/" not in f:
            root_files.append(f)
            continue
        module_name = f.split("/")[0]
        if module_name in manifests:
            # already handled
            continue
        manifest_path = module_name2manifest_path(module_name)
        if manifest_path:
            manifests[module_name] = manifest_path
        else:
            # no manifest in the folder
            other_folders.setdefault(module_name, [])
            other_folders[module_name].append(f)

    addons_config = get_addons_config()
    exclude = addons_config.get("exclude", [])

    modules_data = parse_manifests(manifests)
    modules_data = {
        m: data
        for m, data in modules_data.items()
        if data["manifest"].get("installable", True) and m not in exclude
    }

    set_github_var("PR_MODULES_LOAD", server_wide_modules(modules_data))
    set_github_var("PR_MODULES", ",".join(modules_data.keys()))
    set_github_var(
        "PR_MODULES_DEPS", modules2deps(modules_data, set(), dinar_odoo_base_modules)
    )
    # TODO: set to value "1" if there are changes in .DINAR/image/
    # https://github.com/itpp-labs/DINAR/issues/42
    set_github_var("PR_DEPS", "")


def get_addons_config():
    # TODO: addons.yaml may differs from what base image has.
    try:
        with open(".DINAR/config.yaml") as config_file:
            config = yaml.safe_load(config_file)
    except Exception as e:
        print("Error on parsing .DINAR/config.yaml: %s" % e)
        return {}
    return config.get("addons", {})


def action_all():
    # List all available modules
    ROOT = "."
    folders = [
        name for name in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, name))
    ]
    manifests = {}
    for module_name in folders:
        manifest_path = module_name2manifest_path(module_name)
        if manifest_path:
            manifests[module_name] = manifest_path
    addons_config = get_addons_config()
    include = addons_config.get("include", ["base"])
    exclude = addons_config.get("exclude", [])

    modules_data = parse_manifests(manifests)
    modules_data = {
        m: data
        for m, data in modules_data.items()
        if data["manifest"].get("installable", True) and m not in exclude
    }

    set_github_var("ALL_MODULES_LOAD", server_wide_modules(modules_data))
    set_github_var("ALL_MODULES", ",".join(modules_data.keys()))
    set_github_var("ALL_MODULES_DEPENDENCIES", modules2deps(modules_data, include))


def module_name2manifest_path(module_name):
    for m_py in MANIFESTS:
        manifest_path = os.path.join(module_name, m_py)
        if not os.path.exists(manifest_path):
            # no such manifest
            continue
        return manifest_path


def parse_manifests(manifests):
    modules_data = {}
    for module_name, manifest_path in manifests.items():
        try:
            manifest_data = ast.literal_eval(cat(manifest_path))
        except Exception:
            manifest_data = {"error": "cannot parse"}
        modules_data[module_name] = {"manifest": manifest_data}

    return modules_data


def modules2deps(modules_data, include=None, exclude=None):
    include = include or set()
    exclude = exclude or set()
    dependencies = list(
        itertools.chain.from_iterable(
            m["manifest"].get("depends", []) for m in modules_data.values()
        )
    )
    return ",".join(
        (set(include) | set(dependencies)) - set(modules_data.keys()) - set(exclude)
    )


def server_wide_modules(modules_data):
    odoo_version = os.environ.get("ODOO_VERSION", "13.0")
    mandatory_modules = DEFAULT_SERVER_WIDE_MODULES.get(odoo_version, ["web", "base"])
    addons_config = get_addons_config()
    repo_modules = addons_config.get("server_wide_modules", [])
    return ",".join(
        set(mandatory_modules) | (set(repo_modules) & set(modules_data.keys()))
    )


def cmd(command):
    print(command)
    print(command())


def set_github_var(name, value):
    print("{}={}".format(name, value))
    print("::set-env name={}::{}".format(name, value))


if __name__ == "__main__":
    print(sys.argv)
    action = sys.argv[1]
    if action == "updated":
        token = sys.argv[2]
        repository = sys.argv[3]
        pull_number = sys.argv[4]
        try:
            dinar_odoo_base_modules = sys.argv[5]
            dinar_odoo_base_modules = dinar_odoo_base_modules.split(",")
        except Exception:
            dinar_odoo_base_modules = []
        action_updated(token, repository, pull_number, dinar_odoo_base_modules)
    else:
        action_all()
