# DINAR

**D**inar **I**s **N**ot **A** **R**unbot.

DINAR helps you to configure Github Actions to test and preview Odoo addons.

# Usage

* Fork this repo
* set MY_GITHUB_TOKEN in fork's setting. The token must have access to the repos
* Update repositories list and other settings in config.yml
* Check Actions tab in the fork
* In your repositories: send new PR or rebase existing one

# Repository structure

* ``workflows/`` -- Github Workflows for uploading to target repo

   * ``itpp-runbot-install.yml`` -- workflow that uploads runbot's files to the target repo
   * ``itpp-runbot.yml`` -- workflow that generates Docker images

* ``editable-files/`` -- files to upload to target repo with possibility to modify it by developers
* ``embedded-files/`` -- files are copied in Github Workflow environment on generating Docker images
* ``local-files/`` -- files to download to local machine to work with the dockers
