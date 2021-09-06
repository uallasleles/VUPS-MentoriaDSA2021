# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from flask import render_template, redirect, request, url_for
from app.base import blueprint

@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))

## Errors

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404