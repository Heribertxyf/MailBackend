# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import json
from serializers import TemplateSerializer, HistorySerializer
from db.mail_mod import Template, Term, Receiver, Sender, History
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.
class MyPageNumberPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "size"
    max_page_size =200
    page_query_param = "page"


class HistoryAPI(APIView):
    def get(self, request, *args, **kwargs):
        data = []
        status = True
        msg = ""
        page = request.GET.get('page',1)
        size = request.GET.get('size',1)
        search = request.GET.get('search', None)
        if search:
            search_filter = Q(sender__contains=search) | Q(title__contains=search) | Q(body__contains=search) | Q(receivers__contains=search) | Q(created_at__contains=search)
            historys = History.objects.filter(search_filter).order_by('created_at').reverse()
        else:
            historys = History.objects.all().order_by('created_at').reverse()
        pg = MyPageNumberPagination()
        history = pg.paginate_queryset(queryset=historys, request=request, view=self)
        ser = HistorySerializer(instance=history, many=True)
        for info in ser.data:
            data.append([info['created_at'], info['sender'], info['receivers'], info['title'], info['body']])
        return Response({"status": status, "msg": msg, "data": data, "total": len(historys), "size": size, "page": page})


class TemplateAPI(APIView):
    def get(self, request, *args, **kwargs):
        data = []
        receivers = []
        terms = []
        status = True
        msg = ""
        page = request.GET.get('page',1)
        size = request.GET.get('size',1)
        search = request.GET.get('search', None)
        if search:
            search_filter = Q(name__contains=search) | Q(title__contains=search) | Q(body__contains=search)
            templates = Template.objects.filter(search_filter).order_by('id').reverse()
        else:
            templates = Template.objects.all().order_by('id').reverse()
        pg = MyPageNumberPagination()
        template = pg.paginate_queryset(queryset=templates, request=request, view=self)
        ser = TemplateSerializer(instance=template, many=True)
        for info in ser.data:
            data.append({"id": info['id'], "name": info['name'], "sender": info['sender'], "receivers": info['receivers'], "title": info['title'], "body": info['body'], "terms": info['terms']})
        return Response({"status": status, "msg": msg, "data": data, "total": len(templates), "size": size, "page": page})