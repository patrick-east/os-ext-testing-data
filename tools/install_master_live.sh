#!/bin/sh

SCRIPT_DIR=$(dirname $0)

CONF_DIR=${SCRIPT_DIR}/../configs/live

${SCRIPT_DIR}/install_master_with_configs.sh ${CONF_DIR}