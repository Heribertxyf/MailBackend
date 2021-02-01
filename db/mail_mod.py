#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.


class Sender(models.Model):
    name = models.CharField(max_length=255,default='',unique=True,null=False)
    password = models.CharField(max_length=255,default='',unique=False,null=False)
    email_addr = models.CharField(max_length=255,default='',unique=False,null=False)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'mail_sender'
        verbose_name = 'mail_sender'


class Template(models.Model):
    name = models.CharField(max_length=255,default='',unique=True,null=False)
    terms = models.TextField(default='[]')
    title = models.TextField(default='',null=False)
    body = models.TextField(default='',null=False)
    sender = models.ForeignKey(Sender,null=False)
    receivers = models.TextField(default='[]',null=False)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'mail_template'
        verbose_name = 'mail_template'


class Term(models.Model):
    name = models.CharField(max_length=255,default='',unique=True,null=False)
    type = models.CharField(max_length=255,default='',null=False)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'mail_term'
        verbose_name = 'mail_term'


class Receiver(models.Model):
    name = models.CharField(max_length=255,default='',unique=True,null=False)
    email_addr = models.EmailField(max_length=255,default='',unique=True,null=False)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'mail_receiver'
        verbose_name = 'mail_receiver'


class History(models.Model):
    sender = models.CharField(max_length=255,default='',unique=False,null=False)
    title = models.TextField(max_length=255,default='',unique=False,null=False)
    body = models.TextField(max_length=255,default='',unique=False,null=False)
    receivers = models.TextField(max_length=255,default='',unique=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'mail_history'
        verbose_name = 'mail_history'
