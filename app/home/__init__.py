# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from flask import Blueprint

blueprint = Blueprint(
    "home_blueprint",
    __name__,
    url_prefix="",
    template_folder="templates",
    static_folder="static",
)
