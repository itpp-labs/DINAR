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
SHARE=$1
mkdir -p $SHARE

for NAME in db odoo
do
    CONTAINER=$(docker inspect --format="{{.Id}}" dinar_${NAME}_1)
    docker commit $CONTAINER ${NAME}-image
    TMP=${NAME}-image.save/
    mkdir $TMP
    docker save ${NAME}-image | tar -C $TMP -xf -
    LAYER=$TMP/$(jq '.[0].Layers[-1]' $TMP/manifest.json --raw-output)
    cp $LAYER $SHARE/${NAME}-layer.tar
    docker diff $CONTAINER > $SHARE/${NAME}-diff.txt
done
