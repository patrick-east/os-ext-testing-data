#!/bin/bash

# Use this script to install the server_monitor on an Ubuntu host
# it will then run the monitor on startup but relies on the source
# being at /home/jenkins/data
#
# Must be run as root (or with sudo)

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
pip install -r $SCRIPT_DIR/requirements.txt
cp $SCRIPT_DIR/server_monitor.sh /etc/init.d/
chmod +x /etc/init.d/server_monitor.sh
update-rc.d server_monitor.sh defaults
