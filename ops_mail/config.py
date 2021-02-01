#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


class Config:
    MAIL_HOST = "mail.yun-idc.com"
    SENDER = 'cloud.alarm@capitalonline.net'
    INTERVAL = 15
    HOUR_INTERVAL = 1440

    def __init__(self):
        pass


class DevConfig(Config):
    DATABASE = {
        'name':     'cds_mail',
        'user':     'root',
        'password': '123456',
        'host':     '127.0.0.1',
        'port':     '3306',
    }
    SITE_DOMAIN = 'http://10.128.100.183:8003'
    TSDB_DOMAIN = 'http://10.128.100.161:4242'
    GIC_CLIENT_DOMAIN = 'http://10.13.102.182:8000'


class ProConfig(Config):
    DATABASE = {
        'name':     'cds_mail',
        'user':     'prada',
        'password': 'lovecapitalpradaqwerfdsa',
        'host':     '10.128.100.45',
        'port':     '6666',
    }
    SITE_DOMAIN = 'http://10.128.100.188:8003'
    TSDB_DOMAIN = 'http://10.128.100.161:4242'
    GIC_CLIENT_DOMAIN = 'http://10.13.102.182:8000'


class TestingConfig(Config):
    DATABASE = {
        'name':     'cds_mail',
        'user':     'root',
        'password': 'cds-cloud@2018',
        'host':     '10.128.100.190',
        'port':     '3306',
    }
    SITE_DOMAIN = 'http://10.128.100.195:8003'
    TSDB_DOMAIN = 'http://10.128.100.161:4242'
    GIC_CLIENT_DOMAIN = 'http://10.13.102.182:8000'


ENV_CONFIG = {
    'test': TestingConfig,
    'pro': ProConfig,
    'default': DevConfig,
    'dev': DevConfig,
}


CONFIG = ENV_CONFIG.get(os.environ.get('ENV_CONFIG','default'))
