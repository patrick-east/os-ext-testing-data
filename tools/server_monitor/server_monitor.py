#!/usr/bin/env python

from config import Config
from daemon import Daemon
from email_reporter import EmailReporter
from jenkins_master_server import JenkinsMasterServer
from purity_server import PurityServer
from log_server import LogServer
from reporter import BasicReporter, ReporterChain
from server import Server
import sys
import time


class ServerMonitor(Daemon):
    def run(self):
        config = Config()

        reporter = ReporterChain(config)
        reporter.add_reporter(BasicReporter(config))
        reporter.add_reporter(EmailReporter(config))

        servers = [
            Server(config,
                   reporter,
                   config.openstack_provider_user(),
                   config.openstack_provider_host(),
                   config.openstack_provider_key_file()),
            LogServer(config,
                      reporter,
                      config.log_file_server_username(),
                      config.log_file_server_host(),
                      config.log_file_server_key_file()),
            JenkinsMasterServer(config,
                                reporter,
                                config.jenkins_master_username(),
                                config.jenkins_master_host(),
                                config.jenkins_master_key_file()),
            PurityServer(config,
                         reporter,
                         config.purity_username(),
                         config.purity_host(),
                         config.purity_key_file())
        ]
        reporter.info('Started Server Monitor')
        while True:
            reporter.info('Running checks for %d servers...' % len(servers))
            for server in servers:
                server.run_checks()
            reporter.info('Done!')
            time.sleep(config.check_delay())


def show_usage_and_exit():
    print 'Usage: %s start|stop|restart' % __file__
    exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        show_usage_and_exit()

    app = ServerMonitor('/var/run/server_monitor.pid')
    action = sys.argv[1]

    if action == 'start':
        app.start()
    elif action == 'stop':
        app.stop()
    elif action == 'restart':
        app.restart()
    else:
        print 'unknown option: %s' % action
        show_usage_and_exit()
