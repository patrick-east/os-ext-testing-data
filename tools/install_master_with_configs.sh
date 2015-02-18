#!/bin/sh

SCRIPT_DIR=$(dirname $0)

CONFIG_DIR_SOURCE=$1

LOG_SERVER_CONFIG=log-server.conf
ZUUL_LAYOUT_YAML=layout.yaml
SLAVE_VARS=slave.conf
SERVER_MONITOR_CONFIG=server-monitor.cfg
SERVER_MONITOR_DEFAULT_CONFIG=server-monitor-defaults.cfg

LOG_SERVER_CONFIG_SOURCE=${CONFIG_DIR_SOURCE}/${LOG_SERVER_CONFIG}
ZUUL_LAYOUT_YAML_SOURCE=${CONFIG_DIR_SOURCE}/${ZUUL_LAYOUT_YAML}
SERVER_MONITOR_CONFIG_SOURCE=${CONFIG_DIR_SOURCE}/${SERVER_MONITOR_CONFIG}

ZUUL_CONFIG_DIR=${SCRIPT_DIR}/../etc/zuul
ZUUL_LAYOUT_YAML_TARGET=${ZUUL_CONFIG_DIR}/${ZUUL_LAYOUT_YAML}

SLAVE_SCRIPT_DIR=${SCRIPT_DIR}/../etc/nodepool/scripts
SLAVE_VARS_SOURCE=${CONFIG_DIR_SOURCE}/${SLAVE_VARS}

CONFIG_DIR_TARGET=/etc/pure-ci
SERVER_MONITOR_CONFIG_TARGET=${CONFIG_DIR_TARGET}/${SERVER_MONITOR_CONFIG}

SERVER_MONITOR_DEFAULT_CONFIG_SOURCE=${SCRIPT_DIR}/../configs/defaults/${SERVER_MONITOR_DEFAULT_CONFIG}
SERVER_MONITOR_DEFAULT_CONFIG_TARGET=${CONFIG_DIR_TARGET}/${SERVER_MONITOR_DEFAULT_CONFIG}

# We only need to copy the vars into etc/nodepool/scripts, puppet will do the rest
cp ${SLAVE_VARS_SOURCE} ${SLAVE_SCRIPT_DIR}

mkdir -p ${ZUUL_CONFIG_DIR}
cp ${ZUUL_LAYOUT_YAML_SOURCE} ${ZUUL_LAYOUT_YAML_TARGET}

# Source the log server config so that we can pick up the log server host name
. ${LOG_SERVER_CONFIG_SOURCE}

bash install_master.sh

echo Installing server_monitor
sudo mkdir -p ${CONFIG_DIR_TARGET}

cp ${SCRIPT_DIR}/../pure_root ~/.ssh/pure_root
chmod 600 ~/.ssh/pure_root

cp ${SCRIPT_DIR}/../jenkins_key ~/.ssh/jenkins_key
chmod 600 ~/.ssh/jenkins_key

cp ${SCRIPT_DIR}/../cinder-diste41-vms.pem ~/.ssh/cinder-diste41-vms.pem
chmod 600 ~/.ssh/cinder-diste41-vms.pem

sudo cp ${SERVER_MONITOR_CONFIG_SOURCE} ${SERVER_MONITOR_CONFIG_TARGET}
sudo chmod a+r ${SERVER_MONITOR_CONFIG_TARGET}

sudo cp ${SERVER_MONITOR_DEFAULT_CONFIG_SOURCE} ${SERVER_MONITOR_DEFAULT_CONFIG_TARGET}
sudo chmod a+r ${SERVER_MONITOR_DEFAULT_CONFIG_TARGET}

sudo ${SCRIPT_DIR}/server_monitor/install.sh
sudo /etc/init.d/server_monitor.sh restart
