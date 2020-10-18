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
import os
import sys

# TODO: rename analyze-modules.py file
import importlib   
analyze_modules = importlib.import_module("analyze-modules")       
set_github_var = analyze_modules.set_github_var

# TODO: make a python package, say dinarlib, to use local imports
from branch2odoo_version import ODOO_VERSIONS, branch2version

TAGS = {
    "1": "one",
    "2": "two",
    "3": "three",
    "4": "four",
    "5": "five",
    "6": "six",
    "7": "seven",
    "8": "eight",
    "9": "nine",
    "0": "zero",
}

def get_prev_version(version):
    return ODOO_VERSIONS[ODOO_VERSIONS.index(version) + 1]

if __name__ == "__main__":
    print(sys.argv)
    title = sys.argv[1]
    parts = title.split(" ")
    branch = parts[1]
    module = parts[2]
    version = branch2version(branch)
    from_version = get_prev_version(branch)
    branch_tags = ":{}::{}:".format(TAGS[version[0]], TAGS[version[1]])
    from_branch_tags = ":{}::{}:".format(TAGS[from_version[0]], TAGS[from_version[1]])
    set_github_var("PORT_FROM_BRANCH", from_version)
    set_github_var("PORT_TO_BRANCH", branch)
    set_github_var("PORT_TO_BRANCH_TAGS", branch_tags)
    set_github_var("PORT_FROM_BRANCH_TAGS", from_branch_tags)
    set_github_var("PORT_MODULE", module)
