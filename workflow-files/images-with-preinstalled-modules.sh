set -ex
DIR="`dirname \"$0\"`"
docker-compose -p DINAR -f $DIR/docker-compose.yml config
docker-compose -p DINAR -f $DIR/docker-compose.yml up -d
docker-compose -p DINAR -f $DIR/docker-compose.yml exec odoo odoo -i $MODULES --stop-after-init
docker-compose -p DINAR -f $DIR/docker-compose.yml stop

docker commit $(docker inspect --format="{{.Id}}" dinar_db_1) $REGISTRY/$IMAGE_DB
docker commit $(docker inspect --format="{{.Id}}" dinar_odoo_1) $REGISTRY/$IMAGE_ODOO

docker push $REGISTRY/$IMAGE_DB
docker push $REGISTRY/$IMAGE_ODOO
