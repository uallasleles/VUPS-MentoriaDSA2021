# -*- encoding: utf-8 -*-
"""
VUPS - Programa de Mentoria DSA 2021
"""

import os

class Config(object):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig(Config):
    DEBUG = False

class DebugConfig(Config):
    DEBUG = True

config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}