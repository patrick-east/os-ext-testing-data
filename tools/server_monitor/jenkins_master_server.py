from server import Server
import urllib
import re


def jenkins_job_url_path(job_name):
    return '/job/%s/api/python' % job_name


class JenkinsMasterServer(Server):
    def __init__(self, config, reporter, username, host, key_file):
        Server.__init__(self, config, reporter, username, host, key_file)
        self.jenkins_base_url = 'http://%s:%s' % (host, self.config.jenkins_port())
        self.jenkins_job_path = jenkins_job_url_path(self.config.jenkins_job_name())

    def run_checks(self):
        super(JenkinsMasterServer, self).run_checks()
        self.check_zuul_server_online()
        self.check_zuul_merger_online()
        self.check_gearman_online()
        self.check_jenkins_errors()
        self.check_nodepool_image_age()

    def _check_service_running(self, service_name):
        try:
            service_status = self.run_command('sudo service %s status' % service_name)
            if not 'running' in service_status:
                self.reporter.error('Service %s is not running on host %s, status: %s'
                                    % (service_name, self.host, service_status))
        except Exception, e:
            self.reporter.error('Failed to check %s status for host %s: %s'
                                % (service_name, self.host, e.message))

    def check_zuul_server_online(self):
        self._check_service_running('zuul')

    def check_zuul_merger_online(self):
        self._check_service_running('zuul-merger')

    def check_gearman_online(self):
        try:
            gearadmin_status = self.run_command('(echo status ; sleep 0.1) | netcat 127.0.0.1 4730 -w 1')
            if not self.config.jenkins_job_name() in gearadmin_status:
                self.reporter.error('Jenkins job is not registered in gearman! status:\n%s'
                                    % gearadmin_status)
        except Exception, e:
            self.reporter.error('Failed to check gearadmin status for host %s: %s'
                                % (self.host, e.message))

    def check_jenkins_errors(self):
        try:
            target_url = self.jenkins_base_url + self.jenkins_job_path
            jenkins_volume_job = eval(urllib.urlopen(target_url).read())

            if jenkins_volume_job:
                health_score = jenkins_volume_job['healthReport'][0]['score']
                if health_score == 0:
                    self.reporter.warning('Jenkins job health score is %s' % health_score)

        except Exception, e:
            self.reporter.error('Error checking jenkins status for host %s: %s'
                                % (self.host, e.message))

    def check_nodepool_image_age(self):
        try:
            image_list_raw = self.run_command('sudo nodepool image-list')
            image_list_lines = image_list_raw.split('\n')
            newest_image_age = None
            for line in image_list_lines:
                match = re.search('\|\s+(\w+)\s+\|\s+(\d+)\s+\|$', line)
                if match:
                    status = match.group(0)
                    age = match.group(1)
                    if status is 'ready' and (newest_image_age is None or (float(age) < newest_image_age)):
                        newest_image_age = age

            if newest_image_age > 36:  # hours
                self.reporter.error('Nodepool image age is %d hours' % newest_image_age)

        except Exception, e:
            self.reporter.error('Error checking nodepool images for host %s: %s'
                                % (self.host, e.message))
