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


@blueprint.route('/index')
def index():
    return render_template('index.html', segment='index')


@blueprint.route('/st')
def st():
    return redirect(url_for('streamlit.py'))


@blueprint.route('/<template>')
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


@blueprint.route('/callback', methods=['POST', 'GET'])
def cb():
    return getJSON(request.args.get('data'))[0]

@blueprint.route('/dashboard')
def dashboard():
    graphsJSON=getJSON()
    return render_template('dashboard.html', segment='dashboard', 
        graphJSON0=graphsJSON[0], 
        graphJSON1=graphsJSON[1],
        graphJSON2=graphsJSON[2],
        graphJSON3=graphsJSON[3],
        graphJSON4=graphsJSON[4],
        graphJSON5=graphsJSON[5],
        graphJSON6=graphsJSON[6],
        graphJSON7=graphsJSON[7],
        graphJSON8=graphsJSON[8],
        )

graphsJSON = []
def getJSON():
    fig_lst = [
        vups.plot_year_taxs(UF=UF),
        vups.plot_comp_tributos_cidades_norm(),
        vups.plot_calendar_heatmap(),
        vups.plot_map_folium(),
        graphs.plot_kpi_percentage_progress(),
        graphs.plot_kpi_spend_hours(),
        graphs.plot_kpi_tcpi(),
        graphs.plot_line_progress_actual_planned(),
        vups.plot_tributos_ipca(),
        ]

    graphsJSON.append(json.dumps(fig0, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig1, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig2, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig3, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig4, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig5, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig6, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig7, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig8, cls=utils.PlotlyJSONEncoder))

    return graphsJSON

# KPI's
def get_plot_kpi_percentage_progress():
    return graphs.plot_kpi_percentage_progress()

def get_plot_kpi_spend_hours():
    return graphs.plot_kpi_spend_hours()

def get_plot_kpi_tcpi():
    return graphs.plot_kpi_tcpi()

# Pimpão
def get_plot_comp_tributos_cidades():
    return vups.plot_comp_tributos_cidades()

def get_plot_comp_tributos_cidades_norm():
    return vups.plot_comp_tributos_cidades_norm()

def get_plot_calendar_heatmap():
    return vups.plot_calendar_heatmap()

def get_plot_tributos_ipca():
    return vups.plot_tributos_ipca()

# Uallas
def get_plot_year_taxs(UF='ES'):
    return vups.plot_year_taxs(UF=UF)

def get_plot_map_folium():
    return vups.plot_map_folium()

# Small Bars
def get_plot_small_bar_percentage_progress():
    return graphs.plot_small_bar_percentage_progress()

def get_plot_small_bar_spend_hours():
    return graphs.plot_small_bar_spend_hours()

# Line Plot - Progresso Atual vs Planejado
def get_plot_line_progress_actual_planned():
    return graphs.plot_line_progress_actual_planned()

# Widgets
def get_plot_widget_cost_variance():
    return graphs.plot_widget_cost_variance()

def get_plot_widget_schedule_variance()():
    return graphs.plot_widget_schedule_variance()