# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from flask import Blueprint

blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix='',
    template_folder='templates',
    static_folder='static'
)