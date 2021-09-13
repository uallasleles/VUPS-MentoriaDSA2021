# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from sqlalchemy.util.langhelpers import methods_equivalent
from app.base.models import Microdados
from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from app.home import vups
from app.home.vups import graphs
from app.home.vups import data
from sqlalchemy import select
from app import db
import json
from plotly import utils

##############################################################################
# ROTEAMENTO DAS PÁGINAS
##############################################################################

@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():  
    return render_template('index.html', segment='index')



@blueprint.route('/query', methods=["GET", "POST"])
def query():
    if request.method=='POST':
        
        municipio = request.form['city']
        
        result = db.session.query(Microdados).whereclause(Microdados.Municipio==municipio)
        print(result)

        for i in result:
            print(f"{i.Municipio} {i.Classificacao}")    

    return render_template('settings.html')

@blueprint.route('/dashboard')
@blueprint.route('/dashboard.html')
@login_required
def dashboard():
    return render_template('dashboard.html', segment='dashboard'
        #, calendar_heatmap                = get_plot_calendar_heatmap()
        , year_taxs                       = get_plot_year_taxs()
        , percentage_progress             = get_plot_kpi_percentage_progress()
        , spend_hours                     = get_plot_kpi_spend_hours()
        , tcpi                            = get_plot_kpi_tcpi()
        , small_bar_percentage_progress   = get_plot_small_bar_percentage_progress()
        , small_bar_spend_hours           = get_plot_small_bar_spend_hours()
        , progress_actual_planned         = get_plot_line_progress_actual_planned()
        , cost_variance                   = get_plot_widget_cost_variance()
        , schedule_variance               = get_plot_widget_schedule_variance()
        , gantt                           = get_plot_gantt()
        , tributos_cidades                = get_plot_comp_tributos_cidades()
        , tributos_cidades_norm           = get_plot_comp_tributos_cidades_norm()
        , tributos_ipca                   = get_plot_tributos_ipca()
        )

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:
        if not template.endswith( '.html' ):
            template += '.html'
        # Detect the current page
        segment = get_segment( request )
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment    
    except:
        return None


@blueprint.route('/refresh_progress_actual_planned', methods=['POST', 'GET'])
def refresh_progress_actual_planned():
    return get_plot_line_progress_actual_planned()


@blueprint.route('/refresh_kpi')
def refresh_kpi():
    percentage_progress = get_plot_kpi_percentage_progress()
    spend_hours = get_plot_kpi_spend_hours()
    tcpi = get_plot_kpi_tcpi()
    return percentage_progress, spend_hours, tcpi

##############################################################################
# FUNÇÕES PARA DUMPS DE PLOTS EM JSON
##############################################################################

# KPI's
def get_plot_kpi_percentage_progress():
    return json.dumps(
        obj = graphs.plot_kpi_percentage_progress(), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_kpi_spend_hours():
    return json.dumps(
        obj = graphs.plot_kpi_spend_hours(), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_kpi_tcpi():
    return json.dumps(
        obj = graphs.plot_kpi_tcpi(), 
        cls = utils.PlotlyJSONEncoder)

# Pimpão
def get_plot_comp_tributos_cidades():
    return json.dumps(
        obj = vups.plot_comp_tributos_cidades(), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_comp_tributos_cidades_norm():
    return json.dumps(
        obj = vups.plot_comp_tributos_cidades_norm(), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_calendar_heatmap():
    return json.dumps(
        obj = vups.plot_calendar_heatmap(), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_tributos_ipca():
    return json.dumps(
        obj = vups.plot_tributos_ipca(), 
        cls = utils.PlotlyJSONEncoder)

# Uallas
def get_plot_year_taxs(UF='ES'):
    return json.dumps(
        obj = vups.plot_year_taxs(UF=UF), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_map_folium():
    return json.dumps(
        obj = vups.plot_map_folium(),
        cls = utils.PlotlyJSONEncoder)

# Small Bars
def get_plot_small_bar_percentage_progress():
    return json.dumps(
        obj = graphs.plot_small_bar_percentage_progress(),
        cls = utils.PlotlyJSONEncoder)

def get_plot_small_bar_spend_hours():
    return json.dumps(
        obj = graphs.plot_small_bar_spend_hours(),
        cls = utils.PlotlyJSONEncoder)

# Line Plot - Progresso Atual vs Planejado
def get_plot_line_progress_actual_planned():
    graphJSON = json.dumps(
        obj = graphs.plot_line_progress_actual_planned(),
        cls = utils.PlotlyJSONEncoder)
    return graphJSON

# Widgets
def get_plot_widget_cost_variance():
    return json.dumps(
        obj = graphs.plot_widget_cost_variance(),
        cls = utils.PlotlyJSONEncoder)

def get_plot_widget_schedule_variance():
    return json.dumps(
        obj = graphs.plot_widget_schedule_variance(),
        cls = utils.PlotlyJSONEncoder)

# Gantt
def get_plot_gantt():
    return json.dumps(
        obj = graphs.plot_gantt(),
        cls = utils.PlotlyJSONEncoder)

# não usar FORM
# alterar para javaScript
@blueprint.route('/settings', methods=["GET", "POST"])
def button():
    if request.method == "POST":
        return data.importer()