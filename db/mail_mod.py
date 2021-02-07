#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.


class Log(models.Model):
    cname = models.CharField(max_length=255,default='',unique=False,null=False)
    cemail = models.CharField(max_length=255,default='',unique=True,null=False)
    ccompany = models.CharField(max_length=255,default='',unique=False,null=False)
    cphone = models.IntegerField(null=True)
    cmessage = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    class Meta:
        db_table = 'mail_history'
        verbose_name = 'mail_history'
