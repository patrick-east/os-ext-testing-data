#!/bin/bash

HOSTNAME=$1

SLAVE_CONF_DIR=/etc/pure-ci
SLAVE_CONF=slave.conf
SLAVE_CONF_TARGET=${SLAVE_CONF_DIR}/${SLAVE_CONF}

sudo mkdir -p ${SLAVE_CONF_DIR}
sudo cp ./${SLAVE_CONF} ${SLAVE_CONF_TARGET}
sudo chmod a+rw ${SLAVE_CONF_TARGET}

sudo apt-get install -y multipath-tools

./prepare_node_devstack.sh "$HOSTNAME"
