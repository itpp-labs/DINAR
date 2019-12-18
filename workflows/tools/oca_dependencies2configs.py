# Reads oca_dependencies.txt file and writes addons.yaml and optionally repos.yaml
#
# for oca_dependencies.txt format see https://github.com/OCA/maintainer-quality-tools/blob/master/travis/clone_oca_dependencies
#
# TODO: it doesn't support recursive generation of dependencies

import sys


def parse_depfile(depfile):
    deps = []
    for line in depfile:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split()
        num_parts = len(parts)
        repo, url, branch, commit = [
            num_parts > i and parts[i] for i in range(4)]
        deps.append((repo, url, branch, commit))
    return deps


def addons_config(repo, url=None, branch=None):
    # works after merging https://github.com/Tecnativa/doodba/pull/261/files
    pattern_line = ""
    if url:
        parts = url.split('/')
        pattern = '%s/{}.git' % '/'.join(parts[:-1])
        pattern_line = "  DEFAULT_REPO_PATTERN: %s\n" % pattern

        # Note: this will not work if the repo name is already occupied
        # The solution could be moving such repositories to repos.yaml
        repo = parts[-1]
        if repo.endswith('.git'):
            repo = repo.split('.git')[0]

    branch_line = ""
    if branch:
        branch_line = "  ODOO_VERSION: %s\n" % branch
    ENV = "ENV:\n" if pattern_line or branch_line else ""
    return """
---
%s%s%s
%s:
  - "*"
""" % (ENV, pattern_line, branch_line, repo)


def repos_config(repo, url, branch, commit):
    if not url:
        # TODO: change to OCA once we make the tool available publicly
        # url = 'https://github.com/OCA/%s.git' % repo
        url = 'https://github.com/it-projects-llc/%s.git' % repo

    if not url.endswith('.git'):
        url += '.git'

    if not branch:
        branch = '$ODOO_VERSION'

    commit_line = ""
    if commit:
        commit_line = "\n    - origin %s" % commit

    return """
---
{repo}:
  defaults:
    depth: $DEPTH_MERGE
  remotes:
    origin: {origin}
  target: origin {branch}
  merges:
    - origin {branch}{commit_line}
""".format(repo=repo, origin=url, branch=branch, commit_line=commit_line)


def deps2configs(deps):
    addons = ''
    repos = ''
    for repo, url, branch, commit in deps:
        if commit:
            repos += repos_config(repo, url, branch, commit)
            addons += addons_config(repo)
        else:
            addons += addons_config(repo, url, branch)
    return addons, repos


if __name__ == '__main__':
    depfilename = sys.argv[1]
    addons_filename = sys.argv[2]
    repos_filename = sys.argv[3]
    with open(depfilename) as depfile:
        deps = parse_depfile(depfile)
    addons, repos = deps2configs(deps)
    for content, filename in [
            (addons, addons_filename),
            (repos, repos_filename),
    ]:
        if content:
            with open(filename, 'a+') as f:
                f.write(content)
