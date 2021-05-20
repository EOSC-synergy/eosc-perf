import os
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import jinja2
import configparser

from ..model.data_types import Report


class ReportMailer:
    @dataclass
    class Configuration:
        host: str
        port: int
        from_address: str
        to_address: str
        username: str
        password: str

    def __init__(self):
        host = os.environ['MAIL_HOST']
        port = int(os.environ['MAIL_PORT'])
        sender = os.environ['MAIL_FROM']
        receiver = os.environ['MAIL_TO']

        credentials = configparser.ConfigParser()
        credentials.read('/run/secrets/email_credentials')

        if 'Mail' not in credentials:
            raise ValueError("malformed email credentials file")
        if 'Username' not in credentials['Mail']:
            raise ValueError("missing username in mail credentials")
        if 'Password' not in credentials['Mail']:
            raise ValueError("missing password in mail credentials")

        username = credentials['Mail']['Username']
        password = credentials['Mail']['Password']

        self.config = ReportMailer.Configuration(host=host, port=port, from_address=sender, to_address=receiver,
                                                 username=username, password=password)
        self.jinja = jinja2.Environment(loader=jinja2.FileSystemLoader('eosc_perf/controller/'))

    def _new_mail(self, subject: str):
        multipart = MIMEMultipart()
        multipart['From'] = formataddr(('Notification service', self.config.from_address))
        multipart['To'] = self.config.to_address
        multipart['Subject'] = subject
        return multipart

    def _init_smtp(self):
        self.smtp = smtplib.SMTP(self.config.host, self.config.port)
        self.smtp.starttls()
        self.smtp.login(self.config.username, self.config.password)

    def _finalize_smtp(self):
        self.smtp.quit()

    def send_mail(self, message: str, subject: str = 'Notification'):
        multipart = self._new_mail(subject)

        multipart.attach(MIMEText(message, 'plain'))
        self._init_smtp()
        self.smtp.send_message(multipart)
        self._finalize_smtp()

    def send_mail_html(self, html_message: str, subject: str = 'Notification'):
        multipart = self._new_mail(subject)

        multipart.attach(MIMEText(html_message, 'html'))
        self._init_smtp()
        self.smtp.send_message(multipart)
        self._finalize_smtp()

    def mail_entry(self, report_type: int, message: str, uuid: str):
        titles = {
            Report.SITE: "New site submitted",
            Report.RESULT: "Result reported",
            Report.BENCHMARK: "New benchmark submitted"
        }
        domains = {
            Report.SITE: "https://" + os.environ["DOMAIN"] + "/review/site?uuid=",
            Report.RESULT: "https://" + os.environ["DOMAIN"] + "/review/result?uuid=",
            Report.BENCHMARK: "https://" + os.environ["DOMAIN"] + "/review/benchmark?uuid=",
        }
        title = "New report: {}".format(titles[report_type])
        body = message
        template = self.jinja.get_template('email_template.html.jinja')
        text = template.render(title=title, body=body, link=domains[report_type] + uuid)
        self.send_mail_html(text, title)
