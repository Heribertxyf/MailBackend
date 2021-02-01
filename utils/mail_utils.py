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
from db.mail_mod import Template, Term, History, Receiver,Sender
from rest_framework import status
from rest_framework.response import Response
from ops_mail.config import CONFIG


# SMTP
def get_sender(template):
    user = template.sender.name
    passwd = template.sender.password
    addr = template.sender.email_addr
    return user, passwd, addr


def get_receiver(template):
    receivers = []
    ids = json.loads(template.receivers)
    for id in ids:
        receivers.append(Receiver.objects.get(id=id).email_addr)
    return receivers


def get_terms(template):
    terms_name = []
    pic = []
    is_html = False
    terms_ids = json.loads(template.terms)
    for term in terms_ids:
        t = Term.objects.get(id=term)
        terms_name.append(t.name)
        if t.type == "picture":
            pic.append(t.name)
        if t.type == "html":
            is_html = True
    return terms_name, pic, is_html


def send(template, variates, receivers, pic_names, is_html):
    try:
        print "================== start  ==================="
        mail_user, mail_passwd, addr = get_sender(template)
        if pic_names:
            for pic_name in pic_names:
                body = str(template.body).replace("{%s}" % pic_name, '<img src="cid:imageid" alt="imageid">').format(**variates)
            body_pic = '<html><body><pre style=”word-wrap: break-word; white-space: pre-wrap; white-space: -moz-pre-wrap”>'+body+'</pre></body></html>'
            content = MIMEText(body_pic, 'html', 'utf-8')
            msg = MIMEMultipart('related')
            msg.attach(content)
            for pic_name in pic_names:
                img_data = base64.b64decode(variates[pic_name].split(',')[1])
                img = MIMEImage(img_data)
                img.add_header('Content-ID', "imageid")
                msg.attach(img)
        elif is_html:
            body = template.body.format(**variates)
            msg = MIMEText(body, 'html', 'utf-8')
        else:
            body = template.body.format(**variates)  # 内容
            msg = MIMEText(body, 'plain','utf-8')


        msg['From'] = Header(addr, 'utf-8')
        msg['To'] = ', '.join(receivers)
        msg['Date'] = formatdate(localtime=True)
        subject = template.title.format(**variates)    # 标题
        msg['Subject'] = Header(subject, 'utf-8')

        # print "============="
        # print CONFIG.MAIL_HOST
        # print addr
        # print receivers
        # print msg.as_string()

        smtpObj = smtplib.SMTP()
        smtpObj.connect(CONFIG.MAIL_HOST, 587)
        smtpObj.starttls()
        smtpObj.login(mail_user, mail_passwd)
        smtpObj.sendmail(addr, receivers, msg.as_string())
        smtpObj.quit()
        # print "邮件发送成功"
        result = {"status": True, "msg": "发送成功"}
        History.objects.create(sender=addr, title=subject, body=body, receivers=msg['To'])
    except Exception, e:
        print Exception, e
        # print "邮件发送失败"
        result = {"status": False, "msg": "发送失败，请查看模板变量与内容是否对应填写正确，以及发件人用户名，密码是否正确"}
    finally:
        return result


def is_valid(template_name, variates, receivers):
    if not template_name or not variates:
        result = {"status": False, "msg": "API格式错误！"}
        return result
    if Template.objects.filter(name=template_name).first():
        template = Template.objects.get(name=template_name)
        terms, pic_names, is_html = get_terms(template)
        for term in terms:
            if term not in variates:
                result = {"status": False, "msg": "变量不完整！"}
                return result
        default_receivers = get_receiver(template)
        if receivers:
            receivers.extend(default_receivers)
        else:
            receivers = default_receivers
        result = send(template, variates, receivers, pic_names, is_html)
    else:
        result = {"status": False, "msg": "未找到模板！"}
    return result


class MailAPI(APIView):
    def post(self, request, format=None):
        print request.data
        template = request.data.get("template", "")
        variates = request.data.get("variates", "")
        print variates
        receivers = request.data.get("receivers", "")
        # print "request====", template, variates, receivers
        result = is_valid(template, variates, receivers)
        return Response(result, status=status.HTTP_200_OK)
