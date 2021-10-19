# -*- encoding: utf-8 -*-
"""
* MÓDULO: const
"""


# Imports
import os
import json

# Constantes
BASEDIR = os.path.dirname(os.path.dirname(__file__))
DATADIR = os.path.join(BASEDIR, "data")
DATATMP = os.path.join(DATADIR, "tmp")
METADIR = os.path.join(DATADIR, "metadata")

# ABSPATH = os.path.abspath('.')
# BASENAME = os.path.basename('.')
# COMMONPATH = os.path.commonpath('.')
# COMMONPREFIX = os.path.commonprefix('.')
# DIRNAME = os.path.dirname(__file__)
# REALPATH = os.path.realpath('.')

# ############################################################################
# TRIAGEM DOS TIPOS DE DADOS
# ############################################################################

def read_dtype_map(DS_NAME):
    DTYPE_DICT = {
        "date_cols": [],
        "cat_cols": [],
        "float_cols": [],
        "int_cols": [],
        }

    try:
        with open(os.path.join(METADIR, DS_NAME)) as f:
            DTYPE_MAP = json.load(f)

        for key, value in DTYPE_MAP["DTypeMap"].items():
            if value == 'datetime64[ns]':   DTYPE_DICT["date_cols"].append(key)
            if value == 'float64':          DTYPE_DICT["float_cols"].append(key)
            if value == 'int64':            DTYPE_DICT["int_cols"].append(key)
            if value == 'category':         DTYPE_DICT["cat_cols"].append(key)
            
    except:
        pass

    return(DTYPE_DICT)


# ############################################################################
# REGISTROS DAS FONTES DE DADOS UTILIZADAS
# ############################################################################

MICRODADOS = {
    "NAME": "MICRODADOS",
    "TITLE": "",
    "DESCRIPTION": "",
    "URLS": {
        "MICRODADOS": "https://bi.s3.es.gov.br/covid19/MICRODADOS.csv",
    },
    "FORMAT": ".csv",
    "DELIMITER": ";",
    "ENCODING": "ISO-8859-1",
    "MAP": read_dtype_map("DTYPEMAP_MICRODADOS.json")
}

MICRODADOS_BAIRROS = {
    "NAME": "MICRODADOS_BAIRROS",
    "TITLE": "",
    "DESCRIPTION": "",
    "URLS": {
        "MICRODADOS_BAIRROS": "https://bi.s3.es.gov.br/covid19/MICRODADOS_BAIRROS.csv",
    },
    "FORMAT": ".csv",
    "DELIMITER": ",",
    "ENCODING": "ISO-8859-1",
    "MAP": read_dtype_map("DTYPEMAP_MICRODADOS_BAIRROS.json")
}

TIPO_ARRECADACAO = {
    "NAME": "TIPO_ARRECADACAO",
    "TITLE": "",
    "DESCRIPTION": "Dados referentes ao tipo de arrecadação dos tributos estaduais",
    "URLS": {
        "TipoArrecadacao": "https://drive.economia.gov.br/owncloud/index.php/s/OEehiiL427jBp7C/download",
    },
    "FORMAT": ".csv",
    "DELIMITER": ",",
    "ENCODING": "UTF-8",
    "MAP": read_dtype_map("DTYPEMAP_TIPO_ARRECADACAO.json")
}

ARRECADACAO = {
    "NAME": "ARRECADACAO",
    "TITLE": "",
    "DESCRIPTION": "Dados referentes aos boletins de arrecadação dos tributos estaduais",
    "URLS": {
        "Arrecadacao_01-01-1998_a_31-12-2001": "https://drive.economia.gov.br/owncloud/index.php/s/TD34YJTxalj4X3G/download",
        "Arrecadacao_01-01-2002_a_31-12-2005": "https://drive.economia.gov.br/owncloud/index.php/s/ktiBaOnGIF4K2fw/download",
        "Arrecadacao_01-01-2006_a_31-12-2009": "https://drive.economia.gov.br/owncloud/index.php/s/Jr6vLnMBHLH2dYJ/download",
        "Arrecadacao_01-01-2010_a_31-12-2013": "https://drive.economia.gov.br/owncloud/index.php/s/BaUyR54HEzTHajy/download",
        "Arrecadacao_01-01-2014_a_31-12-2017": "https://drive.economia.gov.br/owncloud/index.php/s/FNJFQQtoRpPZJd1/download",
    },
    "FORMAT": ".csv",
    "DELIMITER": ",",
    "ENCODING": "UTF-8",
    "MAP": read_dtype_map("DTYPEMAP_ARRECADACAO.json")
}

TRANSFERENCIAS = {
    "NAME": "TRANSFERENCIAS",
    "TITLE": "Transferências constitucionais do Estado aos Municípios",
    "DESCRIPTION": "As transferências constitucionais consistem na distribuição de recursos provenientes da arrecadação de tributos estaduais aos municípios, com base em dispositivos constitucionais.",
    "URLS": {
        "TRANSFESTADOMUNICIPIOS-2009": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/cf45af79-99fa-4b24-a150-4c2139282ec3/download/transfestadomunicipios-2009.csv",
        "TRANSFESTADOMUNICIPIOS-2010": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/7d75b44b-73b5-4c05-806a-0aa24a1d7141/download/transfestadomunicipios-2010.csv",
        "TRANSFESTADOMUNICIPIOS-2011": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/e7f8c51a-1f6c-47e6-98a3-1022b78f2058/download/transfestadomunicipios-2011.csv",
        "TRANSFESTADOMUNICIPIOS-2012": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/79d03705-9254-471e-9e1c-02b2aeaed790/download/transfestadomunicipios-2012.csv",
        "TRANSFESTADOMUNICIPIOS-2013": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/953122a9-a877-439b-8c6c-cf84ee6c10c6/download/transfestadomunicipios-2013.csv",
        "TRANSFESTADOMUNICIPIOS-2015": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/4a623059-e635-497b-81e9-1bc912299dd7/download/transfestadomunicipios-2015.csv",
        "TRANSFESTADOMUNICIPIOS-2016": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/238eb2e4-e3e7-48ed-a617-6c0027acb3ed/download/transfestadomunicipios-2016.csv",
        "TRANSFESTADOMUNICIPIOS-2017": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/ca76f901-6b8c-4bea-8fd7-d62b690035ab/download/transfestadomunicipios-2017.csv",
        "TRANSFESTADOMUNICIPIOS-2018": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/6fb7b95f-23f8-471f-a9a2-a1112b930ab9/download/transfestadomunicipios-2018.csv",
        "TRANSFESTADOMUNICIPIOS-2019": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/a91e3528-6e7e-499f-9cc2-e281433b1329/download/transfestadomunicipios-2019.csv",
        "TRANSFESTADOMUNICIPIOS-2020": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/511c02b1-93b7-421c-8727-d786f80fd8e5/download/transfestadomunicipios-2020.csv",
        "TRANSFESTADOMUNICIPIOS-2021": "https://dados.es.gov.br/dataset/d85497f8-3dc4-4104-8e18-f242ae82b6ee/resource/672f4fcc-c1aa-4c3d-b0a0-e4cd4e2695da/download/transfestadomunicipios-2021.csv",
    },
    "FORMAT": ".csv",
    "DELIMITER": ";",
    "ENCODING": "UTF-8",
    "MAP": read_dtype_map("DTYPEMAP_TRANSFERENCIAS.json")
}

POPULACAO = {
    "NAME": "POPULACAO",
    "TITLE": "",
    "DESCRIPTION": "",
    "URLS": {
        "POPULACAO_2018": os.path.join(DATADIR, "populacao_2018.csv"),
        "POPULACAO_2019": os.path.join(DATADIR, "populacao_2019.csv"),
        "POPULACAO_2020": os.path.join(DATADIR, "populacao_2020.csv"),
        "POPULACAO_2021": os.path.join(DATADIR, "populacao_2021.csv"),
    },
    "FORMAT": ".csv",
    "DELIMITER": ",",
    "ENCODING": "UTF-8",
    "MAP": read_dtype_map("DTYPEMAP_POPULACAO.json")
}