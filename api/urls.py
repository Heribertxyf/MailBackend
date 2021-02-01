#-*- coding: utf-8 -*-
from django.conf.urls import url, include
from api import views
from utils import mail_utils, mail_input

urlpatterns = [
    url(r'^get_template?$', views.TemplateAPI.as_view()),
    url(r'^get_history?$', views.HistoryAPI.as_view()),
    url(r'^mail/$', mail_utils.MailAPI.as_view()),
]

urlpatterns += [
    url(r'^template/modify?$', mail_input.do_modify_template.as_view()),
    url(r'^template/delete?$', mail_input.do_delete_template.as_view()),
    url(r'^template/input?$', mail_input.input_template.as_view()),
    url(r'^template/input/template$', mail_input.do_input_template.as_view()),
    url(r'^template/modify/(?P<pk>.+?)?$', mail_input.modify_template.as_view()),
    url(r'^template/input/sender$', mail_input.do_input_sender.as_view()),
    url(r'^template/input/receiver$', mail_input.do_input_receiver.as_view()),
    url(r'^template/delete/sender?$', mail_input.do_delete_sender.as_view()),
    url(r'^template/delete/receiver?$', mail_input.do_delete_receiver.as_view()),
]
