cat << EOF
To try updates execute:

    WORKDIR=/tmp/DINAR/$GITHUB_REPOSITORY-$PR_NUM/
    mkdir -p \$WORKDIR
    cd \$WORKDIR
    curl https://raw.githubusercontent.com/$DINAR_REPO/master/workflow-files/docker-compose-DINAR-pr.yml > docker-compose.yml
    curl https://raw.githubusercontent.com/$DINAR_REPO/DINAR/master/local-files/docker-compose.override.yml > docker-compose.override.yml
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
EOF

if [ "$VERSION" == "10.0" ]; then
cat << 'EOF'

    # workaround for odoo 10.0
    docker-compose up -d odoo
    docker-compose exec odoo click-odoo -i
    # EXEC:
    # env['ir.module.module'].update_list()
    # env.cr.commit()
    # exit()
    docker-compose stop odoo

EOF

fi

cat << 'EOF'
    docker-compose up
EOF
