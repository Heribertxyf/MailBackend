#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os


class Config:
    MAIL_HOST = "smtp.office365.com"
    MAIL_PORT = 587

    def __init__(self):
        pass


class DevConfig(Config):
    DATABASE = {
        'name':     'cds_mail',
        'user':     'api',
        'password': 'apicdscloud',
        'host':     '127.0.0.1',
        'port':     '3306',
    }


class ProConfig(Config):
    DATABASE = {
        'name':     'cds_mail',
        'user':     'api',
        'password': 'apicdscloud',
        'host':     '127.0.0.1',
        'port':     '3306',
    }

class TestingConfig(Config):
    DATABASE = {
        'name':     'cds_mail',
        'user':     'api',
        'password': 'apicdscloud',
        'host':     '127.0.0.1',
        'port':     '3306',
    }

ENV_CONFIG = {
    'test': TestingConfig,
    'pro': ProConfig,
    'default': DevConfig,
    'dev': DevConfig,
}


CONFIG = ENV_CONFIG.get(os.environ.get('ENV_CONFIG','default'))
