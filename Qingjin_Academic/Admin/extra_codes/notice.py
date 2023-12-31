from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from numpy import random
from django.template import loader

data = {
    'sender': "olafknowledgegraph@163.com",  # 发送者邮箱，自己用可写死
    'password': "MUVNLBGHOGERATMW",  # 在开启SMTP服务后，可以生成授权码，此处为授权码
    'subject': "AgileScholar事务反馈",  # 邮件主题名，没有违规文字都行
}


class SendEmail:
    def __init__(self, data, receiver, time, affair_name, username, decision, reason):
        self.sender = data.get('sender', '')  # 发送者QQ邮箱
        self.receiver = receiver  # 接收者邮箱
        self.password = data.get('password', '')
        self.subject = data.get('subject', '')
        self.context = {'time': time, 'affair_name': affair_name, 'username': username, 'decision': decision,
                        'reason': reason}

    def load_message(self, type0):
        if type0 == 1:
            template = loader.get_template('notice.html')
        else:
            template = loader.get_template('notice2.html')
        html = template.render(self.context)
        message = MIMEText(html, "html", "utf-8")  # 文本内容，文本格式，编码
        message["Subject"] = Header(self.subject, "utf-8")  # 邮箱主题
        message["From"] = Header(self.sender)  # 发送者
        message["To"] = Header(self.receiver, "utf-8")  # 接收者
        return message

    def send_email(self, type0):
        message = self.load_message(type0)
        smtp = SMTP_SSL("smtp.163.com")  # 需要发送者QQ邮箱开启SMTP服务
        smtp.login(self.sender, self.password)
        smtp.sendmail(self.sender, self.receiver, message.as_string())
