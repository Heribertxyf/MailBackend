# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
import json
# Create your views here.
def render_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="text/json", status=status)