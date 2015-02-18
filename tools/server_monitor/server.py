import paramiko
import re
import socket
import subprocess

SSH_TIMEOUT = 10
DISK_USAGE_THRESHOLD = 75  # % used


class Server(object):
    def __init__(self, config, reporter, username, host, key_file):
        self.config = config
        self.reporter = reporter
        self.username = username
        self.host = host
        self.key_file = key_file
        self.ssh_key = None
        if not self._is_localhost():
            try:
                self.ssh_key = paramiko.RSAKey.from_private_key_file(self.key_file)
            except Exception, e:
                self.reporter.error("Failed to initalize host %s with error %s" %
                                    (self.host, e))

    def run_checks(self):
        """
        Primary run method for the server, all checks should be done in here.

        Any subclasses should call the super method to run all checks.
        """
        self.check_disk_space()

    def _is_localhost(self):
        return self.host == socket.gethostname()

    def _run_command_local(self, command):
        try:
            return subprocess.check_output(command, shell=True)
        except Exception, e:
            return e.message

    def _run_command_remote(self, command):
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=self.host,
                               username=self.username,
                               pkey=self.ssh_key,
                               timeout=self.config.ssh_timeout())
            stdin, stdout, stderr = ssh_client.exec_command(command)
            output = stdout.read()
            ssh_client.close()
            return output
        except Exception, e:
            self.reporter.error('failed to run remote command! '
                                '\nhost=%s \ncommand=%s \nerror=%s' %
                                (self.host, command, e))

    def run_command(self, command):
        if self._is_localhost():
            return self._run_command_local(command)
        else:
            return self._run_command_remote(command)

    def _yield_lines(self, data):
        for line in data.split("\n"):
            yield line

    def _line_to_list(self, line):
        return re.sub(' +', ' ', line).split()

    def _get_percent_used(self, dfdata):
        percent_used_list = []
        lines = self._yield_lines(dfdata)
        headers = self._line_to_list(lines.next())
        columns = [list() for i in range(len(headers))]
        for i,h in enumerate(headers):
            columns[i].append(h)

        for line in lines:
            for i,l in enumerate(self._line_to_list(line)):
                columns[i].append(l)

        for column in columns:
            if '%' in column[0]:
                row_iter = iter(column)
                # skip the first one since it will be 'Use%'
                next(row_iter)
                for row in row_iter:
                    percent_used = row[:-1]
                    percent_used_list.append(percent_used)

        return percent_used_list

    def check_disk_space(self):
        try:
            dfdata = self.run_command('df -h')

            # parse out the 'Use%' column and check for high usage
            dfdata = dfdata.replace('Mounted on', 'Mounted_on')
            percent_used_list = self._get_percent_used(dfdata)

            for percent_used in percent_used_list:
                if int(percent_used) > self.config.disk_usage_threshold():
                    self.reporter.error('Disk usage too high for host %s\n%s'
                                        % (self.host, dfdata))
                    return
        except Exception, e:
            self.reporter.error('Failed to get disk usage for host %s: %s'
                                % (self.host, e.message))
