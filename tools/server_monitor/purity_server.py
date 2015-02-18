import re
from server import Server

PURITY_ERROR_REGEX = re.compile('(error|stop|waiting|not responding)', re.IGNORECASE)


class PurityServer(Server):
    def __init__(self, config, reporter, username, host, key_file):
        Server.__init__(self, config, reporter, username, host, key_file)

    def run_checks(self):
        super(PurityServer, self).run_checks()
        self.check_purity_status()

    def check_purity_status(self):
        try:
            status_data = self.run_command('pureadm status')
            status_lines = status_data.split('\n')
            for line in status_lines:
                if re.search(PURITY_ERROR_REGEX, line):
                    self.reporter.error('Purity system has an error on host %s:\n%s'
                                        % (self.host, status_data))
        except Exception, e:
            self.reporter.error('Unable to check Purity status for host %s: %s'
                                % (self.host, e.message))
