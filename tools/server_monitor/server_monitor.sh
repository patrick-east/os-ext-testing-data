#!/bin/bash

SERVER_MONITOR_HOME=/home/ubuntu/os-ext-testing-data/tools/server_monitor

start() {
        $SERVER_MONITOR_HOME/server_monitor.py start
        return
}

stop() {
        $SERVER_MONITOR_HOME/server_monitor.py stop
        return
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    *)
        echo "Usage:  {start|stop|restart}"
        exit 1
        ;;
esac
exit 0