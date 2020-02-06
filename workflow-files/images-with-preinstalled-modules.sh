set -ex
DIR="`dirname \"$0\"`"
docker-compose -p DINAR -f $DIR/docker-compose.yml config
docker-compose -p DINAR -f $DIR/docker-compose.yml up --abort-on-container-exit

docker commit $(docker inspect --format="{{.Id}}" dinar_db_1) $REGISTRY/$IMAGE_DB
docker commit $(docker inspect --format="{{.Id}}" dinar_odoo_1) $REGISTRY/$IMAGE_ODOO

docker push $REGISTRY/$IMAGE_DB
docker push $REGISTRY/$IMAGE_ODOO

docker-compose -p DINAR -f $DIR/docker-compose.yml down
