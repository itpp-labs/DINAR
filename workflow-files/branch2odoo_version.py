# reads branch name from input
# prints odoo version to output
import fileinput

ODOO_VERSIONS = ["master", "14.0", "13.0", "12.0", "11.0", "10.0", "9.0", "8.0", "7.0"]


def branch2version(branch):
    branch = branch.rstrip()
    if branch in ODOO_VERSIONS:
        return branch

    for v in ODOO_VERSIONS:
        if branch.startswith("%s-" % v):
            return v

    return ODOO_VERSIONS[0]


if __name__ == "__main__":
    for line in fileinput.input():
        version = branch2version(line)
        print(version)
        break
