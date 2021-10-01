# Módulo de valores constantes

# Imports
import os
import json

# Constantes
APP_LOGO = "imagens/logo.png"
MAPPING_FILE = "config/mapeamento_campos_dataset.json"

# ABSPATH = os.path.abspath('.')
# BASENAME = os.path.basename('.')
# #COMMONPATH = os.path.commonpath('.')
# COMMONPREFIX = os.path.commonprefix('.')
# DIRNAME = os.path.dirname(__file__)
# REALPATH = os.path.realpath('.')

BASEDIR = os.path.dirname(os.path.dirname(__file__))
DATADIR = os.path.join(BASEDIR + "\\data\\")

# DATAFILE = {
#     'FILENAME': 'MICRODADOS.csv',
#     'SEP': ';',
#     'ENCODING': 'latin1',
#     'DATADIC': 'dictionary.md'}

DATAFILE = {
    "FILENAME": "MICRODADOS_BAIRROS.csv",
    "SEP": ";",
    "ENCODING": "latin1",
    "DATADIC": "dictionary.md",
}

# DATAFILE = {
#     'FILENAME': 'Arrecadacao_01-01-1998_a_31-12-2001.csv',
#     'SEP': ',',
#     'ENCODING': 'utf-8',
#     'DATADIC': 'dictionary.md'}

# Inicializa os nomes das colunas do dataset
ID = "ID"
STATUS = "Status"
CRIADO_POR = "Criado Por"
ATRIBUIDO_A = "Atribuido A"
ATENDIDO_POR = "Atendido Por"
SEVERIDADE = "Severidade"
PRIORIDADE = "Prioridade"
CLIENTE = "Cliente"
DATA_CRIACAO = "Data Criação"

# Nomes no arquivo csv
CSV_ID = "ID"
CSV_STATUS = "Status"
CSV_CRIADO_POR = "Criado Por"
CSV_ATRIBUIDO_A = "Atribuido A"
CSV_ATENDIDO_POR = "Atendido Por"
CSV_SEVERIDADE = "Severidade"
CSV_PRIORIDADE = "Prioridade"
CSV_CLIENTE = "Cliente"
CSV_DATA_CRIACAO = "Data Criação"

# Dicionário de mapeamento dos campos
FIELD_MAP = {
    "ID": "ID",
    "Status": "Status",
    "Criado Por": "Criado Por",
    "Atribuido A": "Atribuido A",
    "Atendido Por": "Atendido Por",
    "Severidade": "Severidade",
    "Prioridade": "Prioridade",
    "Cliente": "Cliente",
    "Data Criação": "Data Criação",
}

# Formato de data
DATE_FORMAT = "%d-%m-%Y %H:%M"

# Variáveis customizadas
CREATED_TIME = "CreatedTime"
CREATED_DT = "CreatedDT"
STATUS_TYPE = "StatusType"
CLOSED_ISSUE_STATUS = [
    "Fechado",
    "Resolvido",
    "Solução Proposta",
    "Pesquisa Realizada",
    "Solução Aplicada",
    "Solução Documentada",
]

# Função para leitura das configurações
def read_config():

    # Variáveis
    global ID
    global STATUS
    global CRIADO_POR
    global ATRIBUIDO_A
    global ATENDIDO_POR
    global SEVERIDADE
    global PRIORIDADE
    global CLIENTE
    global DATA_CRIACAO
    global DATA_FECHAMENTO

    global CSV_ID
    global CSV_STATUS
    global CSV_CRIADO_POR
    global CSV_ATRIBUIDO_A
    global CSV_ATENDIDO_POR
    global CSV_SEVERIDADE
    global CSV_PRIORIDADE
    global CSV_CUSTOMER
    global CSV_DATA_CRIACAO
    global CSV_DATA_FECHAMENTO
    global CSV_TIPO_CHAMADO

    global FIELD_MAP
    global DATE_FORMAT

    # Carrega o arquivo json
    with open(MAPPING_FILE) as f:
        CONFIG_OBJECT = json.load(f)

    # Mapeamento de campos
    FIELD_MAP = CONFIG_OBJECT["KeyMapping"]["FieldMapping"]
    ID = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["id"]
    STATUS = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["status"]
    CRIADO_POR = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["criado_por"]
    ATRIBUIDO_A = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["atribuido_a"]
    ATENDIDO_POR = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["atendido_por"]
    SEVERIDADE = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["severidade"]
    PRIORIDADE = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["prioridade"]
    CLIENTE = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["cliente"]
    DATA_CRIACAO = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["data_criacao"]
    DATA_FECHAMENTO = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["data_fechamento"]
    TIPO_CHAMADO = CONFIG_OBJECT["KeyMapping"]["VarMapping"]["tipo_chamado"]
    DATE_FORMAT = CONFIG_OBJECT["DateFormat"]

    key_list = list(FIELD_MAP.keys())
    val_list = list(FIELD_MAP.values())

    CSV_ID = key_list[val_list.index(ID)]
    CSV_STATUS = key_list[val_list.index(STATUS)]
    CSV_CRIADO_POR = key_list[val_list.index(CRIADO_POR)]
    CSV_ATRIBUIDO_A = key_list[val_list.index(ATRIBUIDO_A)]
    CSV_ATENDIDO_POR = key_list[val_list.index(ATENDIDO_POR)]
    CSV_SEVERIDADE = key_list[val_list.index(SEVERIDADE)]
    CSV_PRIORIDADE = key_list[val_list.index(PRIORIDADE)]
    CSV_CLIENTE = key_list[val_list.index(CLIENTE)]
    CSV_DATA_CRIACAO = key_list[val_list.index(DATA_CRIACAO)]
    CSV_DATA_FECHAMENTO = key_list[val_list.index(DATA_FECHAMENTO)]
    CSV_TIPO_CHAMADO = key_list[val_list.index(TIPO_CHAMADO)]


microdados_date_cols = [
    'DataNotificacao',
    'DataCadastro',
    'DataDiagnostico',
    'DataColeta_RT_PCR',
    'DataColetaTesteRapido',
    'DataColetaSorologia',
    'DataColetaSorologiaIGG',
    'DataEncerramento',
    'DataObito']
    
microdados_cat_cols = []

mapa_microdados = {
    'date_cols': microdados_date_cols,
    'cat_cols': microdados_cat_cols
}

ARRECADACAO = {
    "NAME": "ARRECADACAO",
    "URLS": {
        "Arrecadacao_01-01-1998_a_31-12-2001": "https://drive.economia.gov.br/owncloud/index.php/s/TD34YJTxalj4X3G/download",
        "Arrecadacao_01-01-2002_a_31-12-2005": "https://drive.economia.gov.br/owncloud/index.php/s/ktiBaOnGIF4K2fw/download",
        "Arrecadacao_01-01-2006_a_31-12-2009": "https://drive.economia.gov.br/owncloud/index.php/s/Jr6vLnMBHLH2dYJ/download",
        "Arrecadacao_01-01-2010_a_31-12-2013": "https://drive.economia.gov.br/owncloud/index.php/s/BaUyR54HEzTHajy/download",
        "Arrecadacao_01-01-2014_a_31-12-2017": "https://drive.economia.gov.br/owncloud/index.php/s/FNJFQQtoRpPZJd1/download",
    }
}

MICRODADOS = {
    "NAME": "MICRODADOS",
    "URLS": {
        "MICRODADOS": "https://bi.s3.es.gov.br/covid19/MICRODADOS.csv",
    }
}

MICRODADOS_BAIRROS = {
    "NAME": "MICRODADOS_BAIRROS",
    "URLS": {
        "MICRODADOS_BAIRROS": "https://bi.s3.es.gov.br/covid19/MICRODADOS_BAIRROS.csv",
    }
}

TIPO_ARRECADACAO = {
    "NAME": "TIPO_ARRECADACAO",
    "URLS": {
        "MICRODADOS_BAIRROS": "https://bi.s3.es.gov.br/covid19/MICRODADOS_BAIRROS.csv",
    }
}

TRANSFERENCIAS = {
    "NAME": "TRANSFERENCIAS",
    "URLS": {
        "TRANSF_UF-MUN-2018": os.path.join(DATADIR + "transfestadomunicipios-2018.csv"),
        "TRANSF_UF-MUN-2019": os.path.join(DATADIR + "transfestadomunicipios-2019.csv"),
        "TRANSF_UF-MUN-2020": os.path.join(DATADIR + "transfestadomunicipios-2020.csv"),
        "TRANSF_UF-MUN-2021": os.path.join(DATADIR + "transfestadomunicipios-2021.csv"),
    }
}

POPULACAO = {
    "NAME": "POPULACAO",
    "URLS": {
        "POPULACAO_2018": os.path.join(DATADIR + "populacao_2018.csv"),
        "POPULACAO_2019": os.path.join(DATADIR + "populacao_2018.csv"),
        "POPULACAO_2020": os.path.join(DATADIR + "populacao_2018.csv"),
        "POPULACAO_2021": os.path.join(DATADIR + "populacao_2018.csv"),
    }
}