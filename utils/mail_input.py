#!/usr/bin/env python
# -*- coding:utf-8 -*-
from views import render_json
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from db.mail_mod import Sender, Receiver, Template, Term
import json
from rest_framework.views import APIView
from api.serializers import TermSerializer, ReceiverSerializer, SenderSerializer

class input_template(APIView):
    def get(self, request, format=None):
        data = {}
        senders = Sender.objects.all()
        receivers = Receiver.objects.all()
        data['senders'] = SenderSerializer(instance=senders, many=True).data
        data['receivers'] = ReceiverSerializer(instance=receivers, many=True).data
        return render_json(data)


class do_input_sender(APIView):
    def post(self, request, format=None):
        data = {"status": False}
        name = request.data.get("name")
        passwd = request.data.get("passwd")
        addr = request.data.get("addr")
        if name and passwd and addr:
            if Sender.objects.filter(name=name).first():
                data["msg"] = "发件人名称已存在"
                return render_json(data)
            else:
                Sender.objects.create(name=name, password=passwd, email_addr=addr)
                data['status'] = True
                data['msg'] = "发件人添加成功"
                return render_json(data)
        else:
            data["msg"] = "发件人名称，密码，邮件地址填写不完整"
            return render_json(data)


class do_input_receiver(APIView):
    def post(self, request, format=None):
        data = {"status": False}
        name = request.data.get("name")
        addr = request.data.get("addr")
        if name and addr:
            if Receiver.objects.filter(name=name).first():
                data["msg"] = "收件人名称已存在"
                return render_json(data)
            else:
                Receiver.objects.create(name=name, email_addr=addr)
                data['status'] = True
                data['msg'] = "收件人添加成功"
                return render_json(data)
        else:
            data["msg"] = "收件人名称，邮件地址填写不完整"
            return render_json(data)


class do_input_template(APIView):
    def post(self, request, format=None):
        data = {"status": False}
        terms = []
        name = request.data.get("name")
        title = request.data.get("title")
        body = request.data.get("body")
        terms_name = request.data.get("terms_name")
        terms_type = request.data.get("terms_type")
        sender = request.data.get("sender")
        receiver = request.data.get("receiver")
        # print name, title, body, sender, receiver
        for num in range(len(terms_name)):
            a = 0
            b = 0
            if terms_name[num]:
                a = 1
            if terms_type[num]:
                b = 1
            if a ^ b:
                data["msg"] = "变量填写错误"
            elif terms_name.count(terms_name[num]) != 1:
                print terms_name.count(terms_name[num])
                data["msg"] = "变量名称重复"
            else:
                if Term.objects.filter(name=terms_name[num]).first():
                    terms.append(Term.objects.get(name=terms_name[num]).id)
                else:
                    new_term = Term.objects.create(name=terms_name[num], type=terms_type[num])
                    terms.append(new_term.id)
                continue
            return render_json(data)

        if name and title and body and sender:
            if Template.objects.filter(name=name).first():
                data["msg"] = "模板名已存在"
                return render_json(data)
            else:
                if receiver:
                    receiver = json.dumps([int(x) for x in receiver.split(',')])
                else:
                    receiver = json.dumps([])

                sender = Sender.objects.get(id=sender)
                terms = json.dumps(terms)
                Template.objects.create(name=name, terms=terms, title=title, body=body, sender=sender, receivers=receiver)
                data["status"] = True
                data["msg"] = "模板添加成功"
                return render_json(data)
        else:
            data["msg"] = "名称，标题，内容，填写不完整"
            return render_json(data)


class modify_template(APIView):
    def get(self, request, pk, format=None):
        data = {"terms": [], "select_receivers": []}
        pk = request.GET.get("id", "")
        template = Template.objects.get(id=pk)
        data["id"] = pk
        data["name"] = template.name
        data["title"] = template.title
        data["body"] = template.body
        s = Sender.objects.filter(id=template.sender.id)
        data["select_senders"] = SenderSerializer(instance=s, many=True).data
        for term_id in json.loads(template.terms):
            term = Term.objects.get(id=term_id)
            data["terms"].append({"name": term.name, "type": term.type})
        for receiver in json.loads(template.receivers):
            r = Receiver.objects.get(id=receiver)
            data["select_receivers"].append({"email_addr": r.email_addr, "id": r.id, "name": r.name})
        senders = Sender.objects.all()
        receivers = Receiver.objects.all()
        data['senders'] = SenderSerializer(instance=senders, many=True).data
        data['receivers'] = ReceiverSerializer(instance=receivers, many=True).data
        return render_json(data)


class do_modify_template(APIView):
    def post(self, request, format=None):
        data = {"status": False}
        terms = []
        id = request.data.get("id")
        name = request.data.get("name")
        title = request.data.get("title")
        body = request.data.get("body")
        terms_name = request.data.get("terms_name", [])
        terms_type = request.data.get("terms_type", [])
        sender = request.data.get("sender")
        receiver = request.data.get("receiver")

        for num in range(len(terms_name)):
            a = 0
            b = 0
            if terms_name[num]:
                a = 1
            if terms_type[num]:
                b = 1
            if a ^ b:
                data["msg"] = "变量填写错误"
                return render_json(data)
            elif terms_name.count(terms_name[num]) != 1:
                data["msg"] = "变量名称重复"
                return render_json(data)
            else:
                if Term.objects.filter(name=terms_name[num]).first():
                    terms.append(Term.objects.get(name=terms_name[num]).id)
                else:
                    new_term = Term.objects.create(name=terms_name[num], type=terms_type[num])
                    terms.append(new_term.id)

        if name and title and body and sender:
            template = Template.objects.get(id=id)
            if receiver:
                receiver = json.dumps([int(x) for x in receiver.split(',')])
            else:
                receiver = json.dumps([])
            sender = Sender.objects.get(id=sender)
            terms = json.dumps(terms)
            template.name = name
            template.title = title
            template.terms = terms
            template.body = body
            template.sender = sender
            template.receivers = receiver
            template.save()
            data["status"] = True
            data["msg"] = "模板修改成功"
        else:
            data["msg"] = "名称，标题，内容，填写不完整"
        return render_json(data)



class do_delete_template(APIView):
    def post(self, request, format=None):
        data = {}
        id = request.data.get("id")
        if Template.objects.filter(id=id).first():
            Template.objects.get(id=id).delete()
            data["msg"] = "模板删除成功"
        else:
            data["msg"] = "模板已删除"
        return render_json(data)


class do_delete_sender(APIView):
    def post(self, request, format=None):
        data = {}
        senders = request.data.get("senders",[])
        for id in senders:
            sender = Sender.objects.get(id=id)
            for template in Template.objects.all():
                if sender.id == template.sender.id:
                    data["msg"] = "%s被模板%s使用，无法被删除，若删除，请先配置模板"%(sender.name, template.name)
                    return render_json(data)
            sender.delete()
        data["msg"] = "发件人删除成功"
        return render_json(data)


class do_delete_receiver(APIView):
    def post(self, request, format=None):
        data = {}
        receivers = request.data.get("receivers",[])
        for id in receivers:
            receiver = Receiver.objects.get(id=id)
            for template in Template.objects.all():
                if receiver.id in json.loads(template.receivers):
                    data["msg"] = "%s被模板%s使用，无法被删除，若删除，请先配置模板"%(receiver.name, template.name)
                    return render_json(data)
            receiver.delete()
        data["msg"] = "收件人删除成功"
        return render_json(data)
