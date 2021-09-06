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
        )

def getJSON(UF='ES'):
    fig0 = vups.plot_year_taxs(UF=UF)
    fig1 = vups.plot_comp_tributos_cidades_norm()
    fig2 = vups.plot_calendar_heatmap()
    fig3 = vups.plot_map_folium()
    fig4 = graphs.plot_kpi_percentage_progress()
    fig5 = graphs.plot_kpi_spend_hours()
    fig6 = graphs.plot_kpi_tcpi()
    fig7 = graphs.plot_line_progress_actual_planned()

    graphsJSON = []
    graphsJSON.append(json.dumps(fig0, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig1, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig2, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig3, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig4, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig5, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig6, cls=utils.PlotlyJSONEncoder))
    graphsJSON.append(json.dumps(fig7, cls=utils.PlotlyJSONEncoder))

    return graphsJSON