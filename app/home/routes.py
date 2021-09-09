# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from flask import render_template, redirect, request, url_for
from app.home import blueprint
from app.home.lib import vups
from app.home.lib import graphs
import json
from plotly import utils
from jinja2 import TemplateNotFound



##############################################################################
# ROTEAMENTO DAS PÁGINAS
##############################################################################

@blueprint.route('/')
@blueprint.route('/index')
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/dashboard')
@blueprint.route('/dashboard.html')
def dashboard():
    progress_actual_planned = get_plot_line_progress_actual_planned()
    return render_template('dashboard.html', segment='dashboard', progress_actual_planned = progress_actual_planned)


@blueprint.route('/<template>')
def route_template(template):
    print('/<template>')
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
