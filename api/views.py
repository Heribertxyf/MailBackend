# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
#from serializers import TemplateSerializer, HistorySerializer
from db.mail_mod import Log
from rest_framework import status
from ops_mail.config import CONFIG
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from utils.mail_utils import send

# Create your views here.
class MyPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "size"
    max_page_size =200
    page_query_param = "page"

class MailAPI(APIView):
    def post(self, request, format=None):
        print request.data
        cname = request.data.get("name", "")
        cemail = request.data.get("email", "")
        cphone = request.data.get("phone", "")
        ccompany = request.data.get("company", "")
        cmessage = request.data.get("message", "")
	print cname
	mail_user = "cdssupport@cdsglobalcloud.com"
        mail_passwd = "123abc,.;"
        addr = "cdssupport@cdsglobalcloud.com"
        receivers = ["yangfei.xu@capitalonline.net", "han.zhang@capitalonline.net"]
        result_msg = send(mail_user, mail_passwd, addr, receivers, cname, cphone, ccompany, cemail, cmessage)
	print result_msg
        result = {"code": 200, "msg": "success."}
	print result
        return Response(result, status=status.HTTP_200_OK)
