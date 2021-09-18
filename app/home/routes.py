# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from sqlalchemy.util.langhelpers import methods_equivalent
from traitlets.traitlets import default
from app.base.models import Microdados
from app.home import blueprint
from flask import render_template, redirect, url_for, request, Response, jsonify, flash
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from app.home import vups
from app.home.vups import graphs
from app.home.vups import data
from sqlalchemy import select
from app import db
import json
from plotly import utils
import unicodedata
import time

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

##############################################################################
# ROTEAMENTO DAS PÁGINAS
##############################################################################

# Index
# ============================================================================
@blueprint.route('/')
@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html', segment='index')

# Dashboard
# ============================================================================
@blueprint.route('/dashboard')
@blueprint.route('/dashboard.html')
@login_required
def dashboard():
    return render_template('dashboard.html', segment='dashboard'
        # , calendar_heatmap                = get_plot_calendar_heatmap()
        # , year_taxs                       = get_plot_year_taxs()
        # , percentage_progress             = get_plot_kpi_percentage_progress()
        # , spend_hours                     = get_plot_kpi_spend_hours()
        # , tcpi                            = get_plot_kpi_tcpi()
        # , small_bar_percentage_progress   = get_plot_small_bar_percentage_progress()
        # , small_bar_spend_hours           = get_plot_small_bar_spend_hours()
        # , progress_actual_planned         = get_plot_line_progress_actual_planned()
        # , cost_variance                   = get_plot_widget_cost_variance()
        # , schedule_variance               = get_plot_widget_schedule_variance()
        # , gantt                           = get_plot_gantt()
        # , tributos_cidades                = get_plot_comp_tributos_cidades()
        # , tributos_cidades_norm           = get_plot_comp_tributos_cidades_norm()
        # , tributos_ipca                   = get_plot_tributos_ipca()
        )

# GRAPH UPDATE: Heatmap
# ============================================================================
@blueprint.route('/heatmap')
def query():
    municipio = request.args.get('city', default=None, type=None)

    # municipio = "%{}%".format(json_data['city'])
    result = Microdados.query.filter(Microdados.Municipio.like(municipio)).first()
    if result:
        calendar_heatmap = get_plot_calendar_heatmap(municipio=result.Municipio)
    
    return calendar_heatmap

# GRAPH UPDATE: Tributos
# ============================================================================
@blueprint.route('/tributos')
def tributos():
    multiselect = request.args.getlist('cidades[]') # OBTEM REQUISIÇÃO
    string_list = [each_string.upper() for each_string in multiselect] # TRATAMENTO - CAIXA ALTA
    string_list = [strip_accents(each_string) for each_string in string_list] # TRATAMENTO - REMOVE ACENTOS
    tributos = get_plot_comp_tributos_cidades(lista=string_list) # PROCESSAMENTO - GERA GRÁFICO (JSON)
    return tributos

# GRAPH UPDATE: Tributos Normalizados
# ============================================================================
@blueprint.route('/tributos_norm')
def tributos_norm():
    multiselect = request.args.getlist('cidades[]')
    string_list = [each_string.upper() for each_string in multiselect]
    string_list = [strip_accents(each_string) for each_string in string_list]
    tributos_norm = get_plot_comp_tributos_cidades_norm(lista=string_list)
    return tributos_norm

# GRAPH UPDATE: Tributos Normalizados
# ============================================================================
@blueprint.route('/tributos_ipca')
def tributos_ipca():
    multiselect = request.args.getlist('cidades[]')
    string_list = [each_string.upper() for each_string in multiselect]
    string_list = [strip_accents(each_string) for each_string in string_list]
    tributos_ipca = get_plot_tributos_ipca(lista=string_list)
    return tributos_ipca


# Templates
# ============================================================================
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


# Atualiza Gráficos
# ============================================================================
@blueprint.route('/refresh_progress_actual_planned', methods=['POST', 'GET'])
def refresh_progress_actual_planned():
    return get_plot_line_progress_actual_planned()


# Botão para atualizar 1 gráfico
# ============================================================================
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
def get_plot_comp_tributos_cidades(lista):
    return json.dumps(
        obj = vups.plot_comp_tributos_cidades(list_cidades=lista), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_comp_tributos_cidades_norm(lista):
    return json.dumps(
        obj = vups.plot_comp_tributos_cidades_norm(list_cidades=lista), 
        cls = utils.PlotlyJSONEncoder)

def get_plot_calendar_heatmap(municipio):
    graphJSON = json.dumps(
        obj = vups.plot_calendar_heatmap(cidade=municipio),
        cls = utils.PlotlyJSONEncoder)
    return graphJSON

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

def progress():
	def generate():
		x = 0
		while x <= 100:
			yield "data:" + str(x) + "\n\n"
			x = x + 1
			time.sleep(0.5)
	return Response(generate(), mimetype= 'text/event-stream')

@blueprint.route('/importar')
def importer(data=vups.datasets.microdados(nrows=100)): 
    def generate():
        try:
            print("Importando Dataset")
            total=data.shape[0]

            print("Iterando registros")
            for col in data.itertuples():
                yield "data:" + format(col.Index+1) + "\n\n"
                record = Microdados(**{
                    'DataNotificacao' : col[1],
                    'DataCadastro' : col[2],
                    'DataDiagnostico' : col[3],
                    'DataColeta_RT_PCR' : col[4],
                    'DataColetaTesteRapido' : col[5],
                    'DataColetaSorologia' : col[6],
                    'DataColetaSorologiaIGG' : col[7],
                    'DataEncerramento' : col[8],
                    'DataObito' : col[9],
                    'Classificacao' : col[10],
                    'Evolucao' : col[11],
                    'CriterioConfirmacao' : col[12],
                    'StatusNotificacao' : col[13],
                    'Municipio' : col[14],
                    'Bairro' : col[15],
                    'FaixaEtaria' : col[16],
                    'IdadeNaDataNotificacao' : col[17],
                    'Sexo' : col[18],
                    'RacaCor' : col[19],
                    'Escolaridade' : col[20],
                    'Gestante' : col[21],
                    'Febre' : col[22],
                    'DificuldadeRespiratoria' : col[23],
                    'Tosse' : col[24],
                    'Coriza' : col[25],
                    'DorGarganta' : col[26],
                    'Diarreia' : col[27],
                    'Cefaleia' : col[28],
                    'ComorbidadePulmao' : col[29],
                    'ComorbidadeCardio' : col[30],
                    'ComorbidadeRenal' : col[31],
                    'ComorbidadeDiabetes' : col[32],
                    'ComorbidadeTabagismo' : col[33],
                    'ComorbidadeObesidade' : col[34],
                    'FicouInternado' : col[35],
                    'ViagemBrasil' : col[36],
                    'ViagemInternacional' : col[37],
                    'ProfissionalSaude' : col[38],
                    'PossuiDeficiencia' : col[39],
                    'MoradorDeRua' : col[40],
                    'ResultadoRT_PCR' : col[41],
                    'ResultadoTesteRapido' : col[42],
                    'ResultadoSorologia' : col[43],
                    'ResultadoSorologia_IGG' : col[44],
                    'TipoTesteRapido' : col[45]
                })
                print("Adicionando registro para sessão! Nº {}".format(col.Index+1))
                with db.session as s:
                    s.add(record)
                    s.flush()
                    s.commit()
                time.sleep(0.5)
        except:
            print("Houve uma exceção! Revertendo as alterações!")
            db.session.rollback() # Rollback the changes on error
        
        finally:
            print("Fechando a conexão")
            db.session.close() # Close the connection

    return Response(generate(), mimetype= 'text/event-stream')