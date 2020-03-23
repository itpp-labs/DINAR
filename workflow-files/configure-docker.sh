set -ex
DIR="`dirname \"$0\"`"

REF=${GITHUB_BASE_REF:-${GITHUB_REF}}
BRANCH=${REF##*/}
REPO_NAME=${GITHUB_REPOSITORY##*/}
IMAGE_CODE=$REPO_NAME:$BRANCH
IMAGE_DB=${GITHUB_REPOSITORY}/dinar-db-$IMAGE_CODE
IMAGE_ODOO=${GITHUB_REPOSITORY}/dinar-odoo-$IMAGE_CODE
REGISTRY=docker.pkg.github.com
REGISTRY_USERNAME="${GITHUB_ACTOR}"
REGISTRY_PASSWORD="$1"

ODOO_VERSION="$(echo $BRANCH | python $DIR/branch2odoo_version.py)"
echo "ODOO_VERSION=$ODOO_VERSION"

echo "::set-env name=DB_VERSION::10"
echo "::set-env name=ODOO_VERSION::$ODOO_VERSION"
echo "::set-env name=IMAGE_CODE::$IMAGE_CODE"
echo "::set-env name=IMAGE_DB::$IMAGE_DB"
echo "::set-env name=IMAGE_ODOO::$IMAGE_ODOO"
echo "::set-env name=REGISTRY::${REGISTRY}"
echo "::set-env name=REGISTRY_USERNAME::${REGISTRY_USERNAME}"
echo "::set-env name=REGISTRY_PASSWORD::${REGISTRY_PASSWORD}"

# authenticate
if [ ! -z "$REGISTRY_PASSWORD" ]; then
    echo "$REGISTRY_PASSWORD" | docker login -u "$REGISTRY_USERNAME" --password-stdin "$REGISTRY"
fi
