import ConfigParser

DEFAULT_CONFIG_FILE = '/etc/pure-ci/server-monitor-defaults.cfg'
CONFIG_FILE = '/etc/pure-ci/server-monitor.cfg'
CONFIG_SECTION = 'server-monitor'


class Config:
    def __init__(self):
        self._cfg = ConfigParser.ConfigParser()
        self._cfg.readfp(open(DEFAULT_CONFIG_FILE))
        self._cfg.read(CONFIG_FILE)

    def _value(self, option):
        if self._cfg.has_option(CONFIG_SECTION, option):
            return self._cfg.get(CONFIG_SECTION, option)
        return None

    def _int_value(self, option):
        if self._cfg.has_option(CONFIG_SECTION, option):
            return self._cfg.getint(CONFIG_SECTION, option)
        return None

    def _float_value(self, option):
        if self._cfg.has_option(CONFIG_SECTION, option):
            return self._cfg.getfloat(CONFIG_SECTION, option)
        return None

    # TODO: automatically generate all of the below items somehow
    #       and keep the keys in sync between this and defaults.cfg

    def smtp_server(self):
        return self._value('SMTP_SERVER')

    def email_subject(self):
        return self._value('EMAIL_SUBJECT')

    def email_from(self):
        return self._value('EMAIL_FROM')

    def email_to(self):
        return self._value('EMAIL_TO')

    def email_time_threshold(self):
        return self._int_value('EMAIL_TIME_THRESHOLD')

    def jenkins_port(self):
        return self._value('JENKINS_PORT')

    def jenkins_job_name(self):
        return self._value('JENKINS_JOB_NAME')

    def jenkins_slave_name(self):
        return self._value('JENKINS_SLAVE_NAME')

    def max_restart_wait_attempts(self):
        return self._int_value('MAX_RESTART_WAIT_ATTEMPTS')

    def restart_sleep_between_retry(self):
        return self._int_value('RESTART_SLEEP_BETWEEN_RETRY')

    def max_job_completion_wait_attempts(self):
        return self._int_value('MAX_JOB_COMPLETION_WAIT_ATTEMPTS')

    def job_completion_sleep_between_retry(self):
        return self._int_value('JOB_COMPLETION_SLEEP_BETWEEN_RETRY')

    def shared_memory_threshold(self):
        return self._float_value('SHARED_MEMORY_THRESHOLD')

    def disk_usage_threshold(self):
        return self._int_value('DISK_USAGE_THRESHOLD')

    def ssh_timeout(self):
        return self._int_value('SSH_TIMEOUT')

    def jenkins_master_username(self):
        return self._value('JENKINS_MASTER_USERNAME')

    def jenkins_master_host(self):
        return self._value('JENKINS_MASTER_HOST')

    def jenkins_master_key_file(self):
        return self._value('JENKINS_MASTER_KEY_FILE')

    def log_file_server_username(self):
        return self._value('LOG_FILE_SERVER_USERNAME')

    def log_file_server_host(self):
        return self._value('LOG_FILE_SERVER_HOST')

    def log_file_server_key_file(self):
        return self._value('LOG_FILE_SERVER_KEY_FILE')

    def purity_username(self):
        return self._value('PURITY_USERNAME')

    def purity_host(self):
        return self._value('PURITY_HOST')

    def purity_key_file(self):
        return self._value('PURITY_KEY_FILE')

    def daemon_name(self):
        return self._value('DAEMON_NAME')

    def check_delay(self):
        return self._int_value('CHECK_DELAY')

    def openstack_provider_host(self):
        return self._value('OPENSTACK_PROVIDER_HOST')

    def openstack_provider_user(self):
        return self._value('OPENSTACK_PROVIDER_USER')

    def openstack_provider_key_file(self):
        return self._value('OPENSTACK_PROVIDER_KEY_FILE')
