#-*- coding: utf-8 -*-
from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^mail$', views.MailAPI.as_view()),
]
