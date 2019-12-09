# ITPP Runbot

Docker based runbot-like solution for odoo addons repositories.

Features:

* Allows preview updates
* Runs tests
* Provides instructions to reproduce errors locally by using same docker images and volumes
* Uses Github tools: 

  * *Github Actions* to build docker images
  * *Github Packages* to store docker images

* Tests in pull-requests are run in private server, cause *Github Actions*'
  environment doesn't have access to external resources (e.g. to s3 to upload
  docker volumes). This part of the system is proprietary.

# Repository structure

* ``workflows/`` -- Github Workflows for uploading to target repo

   * ``itpp-runbot-install.yml`` -- workflow that uploads runbot's files to the target repo
   * ``itpp-runbot.yml`` -- workflow that generates Docker images

* ``editable-files/`` -- files to upload to target repo with possibility to modify it by developers
* ``embedded-files/`` -- files are copied in Github Workflow environment on generating Docker images
* ``local-files/`` -- files to download to local machine to work with the dockers
