from datetime import datetime


class BasicReporter(object):
    def __init__(self, config):
        self.config = config
        self.log_file_name = '/var/log/%s.log' % config.daemon_name()

    def report(self, message):
        fo = open(self.log_file_name, 'a')
        fo.write(message)
        fo.close()

    def report_with_time(self, message):
        message = '%s: %s' % (str(datetime.now()),  message)
        self.report(message)

    def error(self, message):
        self.report_with_time('ERROR: %s\n' % message)

    def warning(self, message):
        self.report_with_time('WARNING: %s\n' % message)

    def info(self, message):
        self.report_with_time('INFO: %s\n' % message)


class ReporterChain(BasicReporter):
    def __init__(self, config):
        BasicReporter.__init__(self, config)
        self.reporters = []

    def add_reporter(self, reporter):
        self.reporters.append(reporter)
        BasicReporter.report(self, 'Adding reporter: %s\n' % type(reporter))

    def report(self, message):
        for reporter in self.reporters:
            reporter.report(message)
