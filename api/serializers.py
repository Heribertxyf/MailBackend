# -*- coding: utf-8 -*-
from rest_framework import serializers
from db.mail_mod import Log
import json


class LogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = Log
        fields = ('id', 'cname','cemail','cphone','ccompany', 'cmessage','created_at')

