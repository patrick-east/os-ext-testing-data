
import datetime
from email.mime.text import MIMEText
from reporter import BasicReporter
import smtplib


class EmailReporter(BasicReporter):
    def __init__(self, config):
        BasicReporter.__init__(self, config)
        self.last_sent = None
        self.host_server_name = config.jenkins_master_host()

    def _should_email(self, message):
        if 'INFO' in message:
            return False

        if self.last_sent is None:
            return True
        else:
            # Prevent spamming about errors
            time_delta = datetime.datetime.now() - self.last_sent
            return time_delta.total_seconds() / 60 > self.config.email_time_threshold()

    def report(self, message):
        if self._should_email(message):
            self._send_email(self.config.email_from(),
                             self.config.email_to(),
                             self.config.email_subject(),
                             message)

    def _send_email(self, message_from, message_to, subject, message):
        try:
            msg = MIMEText(message)
            msg['Subject'] = "%s - %s" % (subject, self.host_server_name)
            msg['From'] = message_from
            msg['To'] = str(message_to)

            smtp = smtplib.SMTP(self.config.smtp_server())
            smtp.sendmail(message_from, message_to, msg.as_string())
            smtp.quit()

            self.last_sent = datetime.datetime.now()
        except Exception, e:
            super(EmailReporter, self).report('Error sending email: %s'
                                              % e.message)
