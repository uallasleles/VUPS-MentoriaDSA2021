# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from app.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from app.home.vups import graphs, database, utils as vups_utils
import json
from plotly import utils

##############################################################################
# ROTEAMENTO DAS PÁGINAS
##############################################################################

# Index
# ============================================================================
@blueprint.route("/")
@blueprint.route("/index")
@login_required
def index():
    return render_template("index.html", segment="index")

# Dashboard
# ============================================================================
@blueprint.route("/dashboard")
@blueprint.route("/dashboard.html")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        segment="dashboard",
        bubbles=get_plot_slider_bubbles(),
        gantt=get_plot_gantt(),
        kpi_confirmados=get_kpi_confirmados(),
        kpi_descartados=get_kpi_descartados(),
        kpi_suspeitos=get_kpi_suspeitos(),
        kpi_obitos=get_kpi_obitos(),
        # taxs=get_plot_year_taxs(),
        # tributos_cidades=get_plot_comp_tributos_cidades(),
        # tributos_cidades_norm=get_plot_comp_tributos_cidades_norm(),
        color_palette = get_plot_bar_color_palette(),
        pessoas_sintomas = get_plot_n_pessoas_por_sintomas(),
        small_bar_percentage_progress=get_plot_small_bar_percentage_progress(),
        small_bar_spend_hours=get_plot_small_bar_spend_hours(),
        progress_actual_planned = get_plot_line_progress_actual_planned()
    )

@blueprint.route("/tables")
def tables():
    return render_template('tables.html')

# GRAPH UPDATE: Heatmap
# ============================================================================
@blueprint.route("/heatmap")
def query():
    municipio = request.args.get("cidade", default='SERRA', type=None)
    municipio = vups_utils.remove_acento(
        municipio.upper()
    )  # TRATAMENTO - CAIXA ALTA E REMOVE ACENTOS

    calendar_heatmap = get_plot_calendar_heatmap(municipio=municipio)

    return calendar_heatmap


# GRAPH UPDATE: Tributos
# ============================================================================
# @blueprint.route("/tributos")
# def tributos():
#     multiselect = request.args.getlist("cidades[]")  # OBTEM REQUISIÇÃO
#     string_list = [
#         each_string.upper() for each_string in multiselect
#     ]  # TRATAMENTO - CAIXA ALTA
#     string_list = [
#         vups_utils.remove_acento(each_string) for each_string in string_list
#     ]  # TRATAMENTO - REMOVE ACENTOS
#     tributos = get_plot_comp_tributos_cidades(
#         lista=string_list
#     )  # PROCESSAMENTO - GERA GRÁFICO (JSON)
#     return tributos


# # GRAPH UPDATE: Tributos Normalizados
# # ============================================================================
# @blueprint.route("/tributos_norm")
# def tributos_norm():
#     multiselect = request.args.getlist("cidades[]")
#     string_list = [each_string.upper() for each_string in multiselect]
#     string_list = [vups_utils.remove_acento(each_string) for each_string in string_list]
#     tributos_norm = get_plot_comp_tributos_cidades_norm(lista=string_list)
#     return tributos_norm


# GRAPH UPDATE: Tributos Normalizados
# ============================================================================
# @blueprint.route("/tributos_ipca")
# def tributos_ipca():
#     municipio = request.args.get("cidade", default=None, type=None)
#     municipio = vups_utils.remove_acento(
#         municipio.upper()
#     )  # TRATAMENTO - CAIXA ALTA E REMOVE ACENTOS
#     tributos_ipca = get_plot_tributos_ipca(municipio=municipio)
#     return tributos_ipca


# Templates
# ============================================================================
@blueprint.route("/<template>")
@login_required
def route_template(template):

    try:
        if not template.endswith(".html"):
            template += ".html"
        # Detect the current page
        segment = get_segment(request)
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(template, segment=segment)
    except TemplateNotFound:
        return render_template("page-404.html"), 404
    except:
        return render_template("page-500.html"), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split("/")[-1]
        if segment == "":
            segment = "index"
        return segment
    except:
        return None


# Atualiza Gráficos
# ============================================================================
@blueprint.route("/refresh_progress_actual_planned", methods=["POST", "GET"])
def refresh_progress_actual_planned():
    return get_plot_line_progress_actual_planned()


##############################################################################
# FUNÇÕES PARA DUMPS DE PLOTS EM JSON
##############################################################################

# KPI's
def get_kpi_confirmados():
    return json.dumps(obj=graphs.kpi_confirmados(), cls=utils.PlotlyJSONEncoder)

def get_kpi_descartados():
    return json.dumps(obj=graphs.kpi_descartados(), cls=utils.PlotlyJSONEncoder)

def get_kpi_suspeitos():
    return json.dumps(obj=graphs.kpi_suspeitos(), cls=utils.PlotlyJSONEncoder)

def get_kpi_obitos():
    return json.dumps(obj=graphs.kpi_obitos(), cls=utils.PlotlyJSONEncoder)

# Pimpão ##############################################################
def get_plot_comp_tributos_cidades(lista=[]):
    return json.dumps(
        obj=graphs.plot_comp_tributos_cidades(list_cidades=lista),
        cls=utils.PlotlyJSONEncoder,
    )


def get_plot_comp_tributos_cidades_norm(lista=[]):
    return json.dumps(
        obj=graphs.plot_comp_tributos_cidades_norm(list_cidades=lista),
        cls=utils.PlotlyJSONEncoder,
    )


def get_plot_calendar_heatmap(municipio):
    graphJSON = json.dumps(
        obj=graphs.plot_calendar_heatmap(cidade=municipio), cls=utils.PlotlyJSONEncoder
    )
    return graphJSON


# def get_plot_tributos_ipca(municipio):
#     return json.dumps(obj=graphs.plot_tributos_ipca(cidade=municipio), cls=utils.PlotlyJSONEncoder)


# ####################################################################

# Uallas
def get_plot_year_taxs(UF="ES"):
    graphJSON = json.dumps(
        obj=graphs.plot_year_taxs(UF=UF), 
        cls=utils.PlotlyJSONEncoder)
    return graphJSON

def get_plot_map_folium():
    return json.dumps(obj=graphs.plot_map_folium(), cls=utils.PlotlyJSONEncoder)


# Small Bars
def get_plot_small_bar_percentage_progress():
    return json.dumps(
        obj=graphs.plot_small_bar_percentage_progress(), cls=utils.PlotlyJSONEncoder
    )


def get_plot_small_bar_spend_hours():
    return json.dumps(
        obj=graphs.plot_small_bar_spend_hours(), cls=utils.PlotlyJSONEncoder
    )


# Line Plot - Progresso Atual vs Planejado
def get_plot_line_progress_actual_planned():
    graphJSON = json.dumps(
        obj=graphs.plot_line_progress_actual_planned(), cls=utils.PlotlyJSONEncoder
    )
    return graphJSON


# Widgets
def get_plot_widget_cost_variance():
    return json.dumps(
        obj=graphs.plot_widget_cost_variance(), cls=utils.PlotlyJSONEncoder
    )


def get_plot_widget_schedule_variance():
    return json.dumps(
        obj=graphs.plot_widget_schedule_variance(), cls=utils.PlotlyJSONEncoder
    )


# Gantt
def get_plot_gantt():
    return json.dumps(obj=graphs.plot_gantt(), cls=utils.PlotlyJSONEncoder)


# Slider Bubbles
def get_plot_slider_bubbles():
    graphJSON = json.dumps(
        obj=graphs.plot_slider_bubbles(), cls=utils.PlotlyJSONEncoder
    )
    return graphJSON

# Bar with Line
def get_plot_bar_with_line():
    graphJSON = json.dumps(
        obj=graphs.plot_bar_with_line(), 
        cls=utils.PlotlyJSONEncoder
    )
    return graphJSON

def get_plot_bar_color_palette():
    graphJSON = json.dumps(
        obj=graphs.plot_bar_color_palette(), 
        cls=utils.PlotlyJSONEncoder
    )
    return graphJSON

def get_plot_n_pessoas_por_sintomas():
    graphJSON = json.dumps(
        obj=graphs.plot_n_pessoas_por_sintomas(), 
        cls=utils.PlotlyJSONEncoder
    )
    return graphJSON

def get_resumo():
    resumo = graphs.fn_resumo_microdados()
    return resumo

@blueprint.route("/importar")
def importar():
    database.importar()