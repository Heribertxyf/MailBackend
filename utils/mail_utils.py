#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from rest_framework.views import APIView
from email.header import Header
import smtplib
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.utils import formatdate
from db.mail_mod import Log
from rest_framework import status
from rest_framework.response import Response
from ops_mail.config import CONFIG


# SMTP
def send(mail_user, mail_passwd, addr, receivers, cname, cphone, ccompany, cemail, cmessage):
    try:
        print "================== start  ==================="
	template = '''
	Customer Name    : {cname};
	Customer Phone   : {cphone};
	Customer Company : {ccompany};
	Customer Email   : {cemail};
	Customer Message :
	{cmessage} 
	'''
	body = template.format(cname=cname, cphone=cphone, ccompany=ccompany, cemail=cemail, cmessage=cmessage)  # 内容
        msg = MIMEText(body, 'plain','utf-8')
        


	msg['From'] = Header(addr, 'utf-8')
        msg['To'] = ', '.join(receivers)
        msg['Date'] = formatdate(localtime=True)
        #subject = template.title.format(**variates)    # 标题
        subject = "Online Customer Contact"
        msg['Subject'] = Header(subject, 'utf-8')

        smtpObj = smtplib.SMTP()
        smtpObj.connect(CONFIG.MAIL_HOST, 587)
        smtpObj.starttls()
        smtpObj.login(mail_user, mail_passwd)
        smtpObj.sendmail(addr, receivers, msg.as_string())
        smtpObj.quit()
        # print "邮件发送成功"
        result = {"status": True, "msg": "发送成功"}
	### add Log create
    except Exception, e:
        print Exception, e
        # print "邮件发送失败"
        result = {"status": False, "msg": "发送失败，请查看模板变量与内容是否对应填写正确，以及发件人用户名，密码是否正确"}
    finally:
        return result
#
#if __name__ == "__main__":
#    mail_user = "cdssupport@cdsglobalcloud.com"
#    mail_password = "123abc,.;"
#    addr = "cdssupport@cdsglobalcloud.com"
#    receivers = ["yangfei.xu@capitalonline.net", "han.zhang@capitalonline.net"]
#    cname = "evan"
#    cphone = "123123"
#    cemail = "evan.xy@163.com"
#    ccompany = "CDS"
#    cmessage = "asdfasdfasdf"
#    result = send(mail_user, mail_passwd, addr, receivers, cname, cphone, ccompany, cemail, cmessage)
