# Reads oca_dependencies.txt file and writes addons.yaml and optionally repos.yaml
#
# for oca_dependencies.txt format see https://github.com/OCA/maintainer-quality-tools/blob/master/travis/clone_oca_dependencies
#
# TODO: it doesn't support recursive generation of dependencies

import sys
import os


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


def addons_config(repo, url=None):
    # works after merging https://github.com/Tecnativa/doodba/pull/261/files
    env = ""
    if url:
        pattern = '%s/{}.git' % '/'.join(url.split('/')[:-1])
        env = """
ENV:
  DEFAULT_REPO_PATTERN: %s
        """ % pattern

    return """
---
%s%s:
  - "*"
""" % (env, repo)

def repos_config(repo, url, branch, commit):
    if not url.endswith('.git'):
        url += '.git'

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
        if commit or branch:
            repos += repos_config(repo, url, branch, commit)
            addons += addons_config(repo)
        elif url:
            addons += addons_config(repo, url)
        else:
            addons += addons_config(repo)
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
            with open(filename, 'w+') as f:
                f.write(content)
