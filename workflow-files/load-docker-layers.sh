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

for NAME in db odoo
do
    CONTAINER=dinar_${NAME}_1
    LAYER=$SHARE/${NAME}-layer.tar
    DIFF_FILE=$SHARE/${NAME}-diff.txt
    LAYER_FILES=${NAME}-layer/
    mkdir -p $LAYER_FILES
    tar -C $LAYER_FILES -xf $LAYER
    if grep "^D " ${DIFF_FILE}; then
        docker start $CONTAINER
        for name in $(awk -F' ' '{if ($1 == "D") print $2; }' ${DIFF_FILE})
        do
            echo "rm -rf $CONTAINER:$name"
            docker exec $CONTAINER rm -rf $name
        done
        docker stop $CONTAINER
    fi
    # "docker cp -a" doesn't work due to this bug https://github.com/moby/moby/issues/34142
    docker cp $LAYER_FILES/. $CONTAINER:/
done
