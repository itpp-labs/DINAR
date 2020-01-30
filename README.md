# DINAR

**D**INAR **I**s **N**ot **A** **R**unbot.

DINAR helps you to configure Github Actions to test and preview Odoo addons.

# Usage

* Fork this repo
* set `MY_GITHUB_TOKEN` in fork's setting. The token must have access to the repos
* Make `config.yml` file to list repositories and set other settings. See [`config.example.yml`](config.example.yml) for details.
* Check Actions tab in the fork
* In your repositories: send new PR or rebase existing one

# Repository structure

* [`.github/workflows/sync.yml`](.github/workflows/sync.yml) -- Github Workflow to install DINAR to your repositories
* `static-files/` -- **copy** and **push** to a repo **with overwriting**. Mandatory files to make the system work.
* `editable-files/` -- **copy** and **push** to a repo **without overwriting**. The files can be modified settings per repository.
* `embedded-files/` -- **copy** to a repo **without overwriting**. The files used on generating Docker images and normally shall not be modified per repository.
* `workflow-files/` -- scripts that can be used from workflows without coping.
* `local-files/` -- files to download to maintainer's machine to work with the dockers locally

# Docker images

DINAR builds and push docker images to Github Packages. Examples for 12.0 branch:

* `DINAR-dependencies:12.0` - base odoo image with dependencies: installs packages and fetches repositories. It uses settings from [`.DINAR/image/`](editable-files/.DINAR/image/dependencies/).
* Odoo and postgres images with preinstalled base modules. It uses `base-addons` settings from [`.DINAR/volumes/addons.yaml`](editable-files/.DINAR/volumes/addons.yaml). 

  * `DINAR-odoo:12.0`, `DINAR-db:12.0` -- modules are installed with demo data
  * `DINAR-odoo:12.0-nodemo`, `DINAR-db:12.0-nodemo` -- modules are installed without demo data 
