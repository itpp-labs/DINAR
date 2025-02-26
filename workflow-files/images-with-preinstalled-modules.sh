# Copyright 2020 IT Projects Labs
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
set -ex
DIR="`dirname \"$0\"`"
IMAGE_DB=$1
IMAGE_ODOO=$2
docker compose -p dinar -f $DIR/docker-compose-DINAR.yml config
docker compose -p dinar -f $DIR/docker-compose-DINAR.yml up --abort-on-container-exit

docker commit $(docker inspect --format="{{.Id}}" dinar_db_1) $REGISTRY/$IMAGE_DB
docker commit $(docker inspect --format="{{.Id}}" dinar_odoo_1) $REGISTRY/$IMAGE_ODOO

docker push $REGISTRY/$IMAGE_DB
docker push $REGISTRY/$IMAGE_ODOO

docker compose -p dinar -f $DIR/docker-compose-DINAR.yml down
