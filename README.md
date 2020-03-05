# DINAR

**D**INAR **I**s **N**ot **A** **R**unbot.

DINAR helps you to configure Github Actions to test and preview Odoo addons.

# Usage

- Fork [DINAR](https://github.com/itpp-labs/DINAR/)
- [Set secrets](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-and-using-encrypted-secrets#creating-encrypted-secrets)

  - `BOT_TOKEN` -- [github token](https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line) with push access to the repos
  - `BOT_NAME` -- Optional. Default `Github Actions`
  - `BOT_EMAIL` -- Optional. Default `actions@github.com`

- Make `config.yml` file to list repositories and set other settings. See [`config.example.yml`](config.example.yml) for details.
- Check Actions tab in the fork
- In your repositories: set secrets:

  - `DINAR_TOKEN` -- with access `write:packages`, `read:packages`

- In your repositories: send new PR or rebase existing one

# Repository structure

- `.github/workflows/':

  - [`DINAR2fork.yml`](.github/workflows/DINAR2fork.yml) -- checks for updates in DINAR and makes PR to your fork
  - [`fork2repos.yml`](.github/workflows/fork2repos.yml) -- Github Workflow to install forked DINAR to your repositories

- `static-files/` -- **copy** and **push** to a repo **with overwriting**. Mandatory files to make the system work.

  - `all/` -- files for any version
  - `10.0/`, `11.0/`, etc -- version specific files

- `editable-files/` -- **copy** and **push** to a repo **without overwriting**. The files can be modified per repository.
- `embedded-files/` -- **copy** to a repo **without overwriting**. The files used on generating Docker images and normally shall not be modified per repository.
- `workflow-files/` -- scripts that can be used from workflows without coping.
- `local-files/` -- files to download to maintainer's machine to work with the dockers locally

# Docker images

DINAR builds and push docker images to Github Packages. Examples for 12.0 branch of `repo-name` repository:

- `dinar-odoo-base-repo-name:12.0` - base odoo image with dependencies: installs packages and fetches repositories. It uses settings from [`.DINAR/image/`](editable-files/.DINAR/image/dependencies/).
- Odoo and postgres images with preinstalled modules specified in manifest's `depends` attribute plus modules listed in `addons.include` attribute of [`.DINAR/config.yaml`](editable-files/.DINAR/config.yaml).

  - `dinar-odoo-repo-name:12.0`, `dinar-db-repo-name:12.0` -- modules are installed with demo data
  - `dinar-odoo-repo-name:12.0-nodemo`, `dinar-db-nodemo-repo-name:12.0-nodemo` -- modules are installed without demo data
