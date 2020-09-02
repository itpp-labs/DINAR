GITHUB_TOKEN=$1

cat << EOF

# Once per device make access token with "read:packages" access
# https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

    USERNAME=YOUR_USERNAME_HERE
    TOKEN=YOUR_TOKEN_HERE
    # Authentication for docker packages access ("docker pull" command):
    docker login docker.pkg.github.com -u \$USERNAME -p \$TOKEN

    # Authentication for api access (it's used to get artifact url)
    (test ! -f \$HOME/.netrc || test ! -z "\$(grep -L 'api.github.com' \$HOME/.netrc)" ) && cat <<- EOOF >> \$HOME/.netrc
        machine api.github.com
        login \$USERNAME
        password \$TOKEN

    EOOF
    chmod 600 \$HOME/.netrc
    # Check the authentication with the following command:
    curl --netrc https://api.github.com/user
    # (If it doesn't work check your ~/.netrc file)

# To try updates execute:

    WORKDIR=/tmp/DINAR/$GITHUB_REPOSITORY-$PR_NUM/
    mkdir -p \$WORKDIR
    cd \$WORKDIR
    curl https://raw.githubusercontent.com/$DINAR_REPO/master/workflow-files/docker-compose-DINAR-pr.yml > docker-compose.yml
    curl https://raw.githubusercontent.com/$DINAR_REPO/master/local-files/docker-compose.override.yml > docker-compose.override.yml
    export REGISTRY=docker.pkg.github.com REPOSITORY=$GITHUB_REPOSITORY VERSION=$VERSION IMAGE_ODOO=$IMAGE_ODOO IMAGE_DB=$IMAGE_DB
    git clone --depth=1 --branch \$VERSION git@github.com:$GITHUB_REPOSITORY pr-files
    # Version in PR
    REVISION=$REVISION_PR
    # Version after merging
    REVISION=pull/$PR_NUM/merge
    git -C pr-files fetch origin \$REVISION
    git -C pr-files checkout FETCH_HEAD
    docker-compose pull
    export PR_FILES=./pr-files/
    export MODULES=$MODULES
    export LOAD_MODULES=$LOAD_MODULES
    export ODOO_EXTRA_ARG=$ODOO_EXTRA_ARG
EOF

if [ "$ARTIFACT" != "empty" ]; then

    cat << EOF

    # get artifact URL
    API_URL="https://api.github.com/repos/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID/artifacts"
    API_RESPONSE=\$(curl -s \$API_URL)
    ARTIFACT_URL=\$(echo \$API_RESPONSE | \
    jq --raw-output '.artifacts[] | select(.name == "new-deps") | .archive_download_url')

    # download artifact
    curl --location --netrc \$ARTIFACT_URL > new-deps.zip
    # unpack
    mkdir new-deps
    unzip new-deps.zip  -d new-deps
    # download script
    DINAR_REPO="$DINAR_REPO"
    curl https://raw.githubusercontent.com/\$DINAR_REPO/master/workflow-files/load-docker-layers.sh > load-docker-layers.sh
    # apply script
    export PROJECT_NAME=\$(basename \$(pwd))
    docker-compose up --no-start
    bash load-docker-layers.sh new-deps/

EOF
else

cat << 'EOF'
    docker-compose up --no-start
EOF

fi


if [ "$VERSION" == "10.0" ]; then
cat << 'EOF'

    # workaround for odoo 10.0
    docker-compose start odoo
    docker-compose exec odoo click-odoo -i
    # EXEC:
    # env['ir.module.module'].update_list()
    # env.cr.commit()
    # exit()

EOF

fi

cat << 'EOF'
    docker-compose start && docker-compose logs --follow odoo
EOF
