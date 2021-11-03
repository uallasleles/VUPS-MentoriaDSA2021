# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from numpy import DataSource
from app.base.models import Microdados
from app.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound
from app.home.vups import graphs, database, datasets, utils as vups_utils, const
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
        color_palette=get_plot_bar_color_palette(),
        pessoas_sintomas=get_plot_n_pessoas_por_sintomas(),
        small_bar_percentage_progress=get_plot_small_bar_percentage_progress(),
        small_bar_spend_hours=get_plot_small_bar_spend_hours(),
        progress_actual_planned=get_plot_line_progress_actual_planned()
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


@blueprint.route("/api/data")
def data():
    dsname = request.args.get('sourceName', type=str)
    draw = request.args.get('draw', type=int) #request.form['draw']
    row = request.args.get('start', type=int)
    rowperpage = request.args.get('length')
    
    dados = dataExample
    columnDefs = []
    
    if dsname is not None:
        try:
            df = getattr(datasets.Datasets, dsname)()
            dados = [row for row in df.to_dict(orient='records')]
            dados = dados[0:100]
            # columnDefs = [
            #     {
            #         'targets': [dados.columns.get_loc(v)],
            #         'name': v
            #     } for v in dados.columns
            # ]
            # print(dados.info())
        except:
            pass
    
    response = {
        "data": dados,
        "recordsTotal": len(dados),
        "recordsFiltered": len(dados),
        "draw": draw, 
        # "columnDefs": columnDefs,
    }

    return response

dataExample = [
        {
            "id": "1",
            "name": "Tiger Nixon",
            "position": "System Architect",
            "salary": "$320,800",
            "start_date": "2011/04/25",
            "office": "Edinburgh",
            "extn": "5421"
        },
        {
            "id": "2",
            "name": "Garrett Winters",
            "position": "Accountant",
            "salary": "$170,750",
            "start_date": "2011/07/25",
            "office": "Tokyo",
            "extn": "8422"
        },
        {
            "id": "3",
            "name": "Ashton Cox",
            "position": "Junior Technical Author",
            "salary": "$86,000",
            "start_date": "2009/01/12",
            "office": "San Francisco",
            "extn": "1562"
        },
        {
            "id": "4",
            "name": "Cedric Kelly",
            "position": "Senior Javascript Developer",
            "salary": "$433,060",
            "start_date": "2012/03/29",
            "office": "Edinburgh",
            "extn": "6224"
        },
        {
            "id": "5",
            "name": "Airi Satou",
            "position": "Accountant",
            "salary": "$162,700",
            "start_date": "2008/11/28",
            "office": "Tokyo",
            "extn": "5407"
        },
        {
            "id": "6",
            "name": "Brielle Williamson",
            "position": "Integration Specialist",
            "salary": "$372,000",
            "start_date": "2012/12/02",
            "office": "New York",
            "extn": "4804"
        },
        {
            "id": "7",
            "name": "Herrod Chandler",
            "position": "Sales Assistant",
            "salary": "$137,500",
            "start_date": "2012/08/06",
            "office": "San Francisco",
            "extn": "9608"
        },
        {
            "id": "8",
            "name": "Rhona Davidson",
            "position": "Integration Specialist",
            "salary": "$327,900",
            "start_date": "2010/10/14",
            "office": "Tokyo",
            "extn": "6200"
        },
        {
            "id": "9",
            "name": "Colleen Hurst",
            "position": "Javascript Developer",
            "salary": "$205,500",
            "start_date": "2009/09/15",
            "office": "San Francisco",
            "extn": "2360"
        },
        {
            "id": "10",
            "name": "Sonya Frost",
            "position": "Software Engineer",
            "salary": "$103,600",
            "start_date": "2008/12/13",
            "office": "Edinburgh",
            "extn": "1667"
        },
        {
            "id": "11",
            "name": "Jena Gaines",
            "position": "Office Manager",
            "salary": "$90,560",
            "start_date": "2008/12/19",
            "office": "London",
            "extn": "3814"
        },
        {
            "id": "12",
            "name": "Quinn Flynn",
            "position": "Support Lead",
            "salary": "$342,000",
            "start_date": "2013/03/03",
            "office": "Edinburgh",
            "extn": "9497"
        },
        {
            "id": "13",
            "name": "Charde Marshall",
            "position": "Regional Director",
            "salary": "$470,600",
            "start_date": "2008/10/16",
            "office": "San Francisco",
            "extn": "6741"
        },
        {
            "id": "14",
            "name": "Haley Kennedy",
            "position": "Senior Marketing Designer",
            "salary": "$313,500",
            "start_date": "2012/12/18",
            "office": "London",
            "extn": "3597"
        },
        {
            "id": "15",
            "name": "Tatyana Fitzpatrick",
            "position": "Regional Director",
            "salary": "$385,750",
            "start_date": "2010/03/17",
            "office": "London",
            "extn": "1965"
        },
        {
            "id": "16",
            "name": "Michael Silva",
            "position": "Marketing Designer",
            "salary": "$198,500",
            "start_date": "2012/11/27",
            "office": "London",
            "extn": "1581"
        },
        {
            "id": "17",
            "name": "Paul Byrd",
            "position": "Chief Financial Officer (CFO)",
            "salary": "$725,000",
            "start_date": "2010/06/09",
            "office": "New York",
            "extn": "3059"
        },
        {
            "id": "18",
            "name": "Gloria Little",
            "position": "Systems Administrator",
            "salary": "$237,500",
            "start_date": "2009/04/10",
            "office": "New York",
            "extn": "1721"
        },
        {
            "id": "19",
            "name": "Bradley Greer",
            "position": "Software Engineer",
            "salary": "$132,000",
            "start_date": "2012/10/13",
            "office": "London",
            "extn": "2558"
        },
        {
            "id": "20",
            "name": "Dai Rios",
            "position": "Personnel Lead",
            "salary": "$217,500",
            "start_date": "2012/09/26",
            "office": "Edinburgh",
            "extn": "2290"
        },
        {
            "id": "21",
            "name": "Jenette Caldwell",
            "position": "Development Lead",
            "salary": "$345,000",
            "start_date": "2011/09/03",
            "office": "New York",
            "extn": "1937"
        },
        {
            "id": "22",
            "name": "Yuri Berry",
            "position": "Chief Marketing Officer (CMO)",
            "salary": "$675,000",
            "start_date": "2009/06/25",
            "office": "New York",
            "extn": "6154"
        },
        {
            "id": "23",
            "name": "Caesar Vance",
            "position": "Pre-Sales Support",
            "salary": "$106,450",
            "start_date": "2011/12/12",
            "office": "New York",
            "extn": "8330"
        },
        {
            "id": "24",
            "name": "Doris Wilder",
            "position": "Sales Assistant",
            "salary": "$85,600",
            "start_date": "2010/09/20",
            "office": "Sydney",
            "extn": "3023"
        },
        {
            "id": "25",
            "name": "Angelica Ramos",
            "position": "Chief Executive Officer (CEO)",
            "salary": "$1,200,000",
            "start_date": "2009/10/09",
            "office": "London",
            "extn": "5797"
        },
        {
            "id": "26",
            "name": "Gavin Joyce",
            "position": "Developer",
            "salary": "$92,575",
            "start_date": "2010/12/22",
            "office": "Edinburgh",
            "extn": "8822"
        },
        {
            "id": "27",
            "name": "Jennifer Chang",
            "position": "Regional Director",
            "salary": "$357,650",
            "start_date": "2010/11/14",
            "office": "Singapore",
            "extn": "9239"
        },
        {
            "id": "28",
            "name": "Brenden Wagner",
            "position": "Software Engineer",
            "salary": "$206,850",
            "start_date": "2011/06/07",
            "office": "San Francisco",
            "extn": "1314"
        },
        {
            "id": "29",
            "name": "Fiona Green",
            "position": "Chief Operating Officer (COO)",
            "salary": "$850,000",
            "start_date": "2010/03/11",
            "office": "San Francisco",
            "extn": "2947"
        },
        {
            "id": "30",
            "name": "Shou Itou",
            "position": "Regional Marketing",
            "salary": "$163,000",
            "start_date": "2011/08/14",
            "office": "Tokyo",
            "extn": "8899"
        },
        {
            "id": "31",
            "name": "Michelle House",
            "position": "Integration Specialist",
            "salary": "$95,400",
            "start_date": "2011/06/02",
            "office": "Sydney",
            "extn": "2769"
        },
        {
            "id": "32",
            "name": "Suki Burks",
            "position": "Developer",
            "salary": "$114,500",
            "start_date": "2009/10/22",
            "office": "London",
            "extn": "6832"
        },
        {
            "id": "33",
            "name": "Prescott Bartlett",
            "position": "Technical Author",
            "salary": "$145,000",
            "start_date": "2011/05/07",
            "office": "London",
            "extn": "3606"
        },
        {
            "id": "34",
            "name": "Gavin Cortez",
            "position": "Team Leader",
            "salary": "$235,500",
            "start_date": "2008/10/26",
            "office": "San Francisco",
            "extn": "2860"
        },
        {
            "id": "35",
            "name": "Martena Mccray",
            "position": "Post-Sales support",
            "salary": "$324,050",
            "start_date": "2011/03/09",
            "office": "Edinburgh",
            "extn": "8240"
        },
        {
            "id": "36",
            "name": "Unity Butler",
            "position": "Marketing Designer",
            "salary": "$85,675",
            "start_date": "2009/12/09",
            "office": "San Francisco",
            "extn": "5384"
        },
        {
            "id": "37",
            "name": "Howard Hatfield",
            "position": "Office Manager",
            "salary": "$164,500",
            "start_date": "2008/12/16",
            "office": "San Francisco",
            "extn": "7031"
        },
        {
            "id": "38",
            "name": "Hope Fuentes",
            "position": "Secretary",
            "salary": "$109,850",
            "start_date": "2010/02/12",
            "office": "San Francisco",
            "extn": "6318"
        },
        {
            "id": "39",
            "name": "Vivian Harrell",
            "position": "Financial Controller",
            "salary": "$452,500",
            "start_date": "2009/02/14",
            "office": "San Francisco",
            "extn": "9422"
        },
        {
            "id": "40",
            "name": "Timothy Mooney",
            "position": "Office Manager",
            "salary": "$136,200",
            "start_date": "2008/12/11",
            "office": "London",
            "extn": "7580"
        },
        {
            "id": "41",
            "name": "Jackson Bradshaw",
            "position": "Director",
            "salary": "$645,750",
            "start_date": "2008/09/26",
            "office": "New York",
            "extn": "1042"
        },
        {
            "id": "42",
            "name": "Olivia Liang",
            "position": "Support Engineer",
            "salary": "$234,500",
            "start_date": "2011/02/03",
            "office": "Singapore",
            "extn": "2120"
        },
        {
            "id": "43",
            "name": "Bruno Nash",
            "position": "Software Engineer",
            "salary": "$163,500",
            "start_date": "2011/05/03",
            "office": "London",
            "extn": "6222"
        },
        {
            "id": "44",
            "name": "Sakura Yamamoto",
            "position": "Support Engineer",
            "salary": "$139,575",
            "start_date": "2009/08/19",
            "office": "Tokyo",
            "extn": "9383"
        },
        {
            "id": "45",
            "name": "Thor Walton",
            "position": "Developer",
            "salary": "$98,540",
            "start_date": "2013/08/11",
            "office": "New York",
            "extn": "8327"
        },
        {
            "id": "46",
            "name": "Finn Camacho",
            "position": "Support Engineer",
            "salary": "$87,500",
            "start_date": "2009/07/07",
            "office": "San Francisco",
            "extn": "2927"
        },
        {
            "id": "47",
            "name": "Serge Baldwin",
            "position": "Data Coordinator",
            "salary": "$138,575",
            "start_date": "2012/04/09",
            "office": "Singapore",
            "extn": "8352"
        },
        {
            "id": "48",
            "name": "Zenaida Frank",
            "position": "Software Engineer",
            "salary": "$125,250",
            "start_date": "2010/01/04",
            "office": "New York",
            "extn": "7439"
        },
        {
            "id": "49",
            "name": "Zorita Serrano",
            "position": "Software Engineer",
            "salary": "$115,000",
            "start_date": "2012/06/01",
            "office": "San Francisco",
            "extn": "4389"
        },
        {
            "id": "50",
            "name": "Jennifer Acosta",
            "position": "Junior Javascript Developer",
            "salary": "$75,650",
            "start_date": "2013/02/01",
            "office": "Edinburgh",
            "extn": "3431"
        },
        {
            "id": "51",
            "name": "Cara Stevens",
            "position": "Sales Assistant",
            "salary": "$145,600",
            "start_date": "2011/12/06",
            "office": "New York",
            "extn": "3990"
        },
        {
            "id": "52",
            "name": "Hermione Butler",
            "position": "Regional Director",
            "salary": "$356,250",
            "start_date": "2011/03/21",
            "office": "London",
            "extn": "1016"
        },
        {
            "id": "53",
            "name": "Lael Greer",
            "position": "Systems Administrator",
            "salary": "$103,500",
            "start_date": "2009/02/27",
            "office": "London",
            "extn": "6733"
        },
        {
            "id": "54",
            "name": "Jonas Alexander",
            "position": "Developer",
            "salary": "$86,500",
            "start_date": "2010/07/14",
            "office": "San Francisco",
            "extn": "8196"
        },
        {
            "id": "55",
            "name": "Shad Decker",
            "position": "Regional Director",
            "salary": "$183,000",
            "start_date": "2008/11/13",
            "office": "Edinburgh",
            "extn": "6373"
        },
        {
            "id": "56",
            "name": "Michael Bruce",
            "position": "Javascript Developer",
            "salary": "$183,000",
            "start_date": "2011/06/27",
            "office": "Singapore",
            "extn": "5384"
        },
        {
            "id": "57",
            "name": "Donna Snider",
            "position": "Customer Support",
            "salary": "$112,000",
            "start_date": "2011/01/25",
            "office": "New York",
            "extn": "4226"
        }
    ]
