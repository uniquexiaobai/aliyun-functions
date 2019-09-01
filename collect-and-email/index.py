from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import make_msgid
from email.utils import formatdate
from ssl import create_default_context
from smtplib import SMTP_SSL
import requests
import logging
import datetime

def sendEmail(title, content):
	host_port = 465
	host_server = 'smtpdm.aliyun.com'
	sender_mail = '<发件人邮箱>'
	sender_passwd = '<发件人邮箱密码>'
	receiver_mail = '<收件人邮箱>'

	message = MIMEMultipart('alternative')
	message['Subject'] = title
	message['From'] = sender_mail
	message['To'] = receiver_mail
	message['Message-id'] = make_msgid()
	message['Date'] = formatdate()
	message.attach(MIMEText(content, 'html', 'utf-8'))

	with SMTP_SSL(host_server, host_port) as server:
		server.login(sender_mail, sender_passwd)
		server.sendmail(sender_mail, receiver_mail, message.as_string())
		server.quit()
		print('send success')

def fetchEchojsData():
	res = requests.get('https://top-api.lokibai.com/?target=echojs')
	return res.json()['list']

def createHtml(data):
	li = '<li style="margin-mottom: 10px"><a href="{url}">{title}</a></li>'
	ret = '<ol style="font-size: 15px">'
	for item in data:
		ret += li.format(**item)
	ret += '</ol>'
	return ret

def handler(event, context):
    logger = logging.getLogger()
    echojsData = fetchEchojsData()
    now = datetime.datetime.now().isoformat()
    title = 'Echojs top news'
    logger.info(now)
    html = createHtml(echojsData)
    sendEmail(title, html)
    return now