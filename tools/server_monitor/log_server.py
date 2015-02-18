from server import Server


class LogServer(Server):
    def __init__(self, config, reporter, username, host, key_file):
        Server.__init__(self, config, reporter, username, host, key_file)

    def run_checks(self):
        super(LogServer, self).run_checks()
        # TODO: we need to clean out old logs... this command currently hangs
        #self.clean_older_logs()

    def clean_older_logs(self):
        try:
            self.run_command('find /srv/static/logs/* -mtime +35 -exec sudo rm -rf {} \;')
        except Exception, e:
            self.reporter.error('Unable to delete older logs from host %s: %s'
                                % (self.host, e.message))
