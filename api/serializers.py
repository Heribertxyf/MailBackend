# -*- coding: utf-8 -*-
from rest_framework import serializers
from db.mail_mod import History, Template, Term, Receiver, Sender
import json


class TemplateSerializer(serializers.ModelSerializer):
    terms = serializers.SerializerMethodField()
    sender = serializers.SerializerMethodField()
    receivers = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = ('id', 'name', 'terms', 'title', 'body', 'sender', 'receivers')

    def get_terms(self, obj):
        terms = {}
        for id in json.loads(obj.terms):
            data = Term.objects.get(id=id)
            terms[data.name] = data.type
        return terms

    def get_sender(self, obj):
        return obj.sender.name

    def get_receivers(self, obj):
        receivers = []
        for id in json.loads(obj.receivers):
            receivers.append(Receiver.objects.get(id=id).name)
        return receivers


class HistorySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    class Meta:
        model = History
        fields = ('sender','title','body','receivers','created_at')


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender
        fields = ('id','name','password','email_addr')


class ReceiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receiver
        fields = ('id','name','email_addr')


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('id','name','type')
