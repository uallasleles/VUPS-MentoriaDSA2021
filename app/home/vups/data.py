# -*- encoding: utf-8 -*-

# from typing import Text
from numpy import genfromtxt
from . import const, utils
import os, json, pandas as pd
# from tqdm import tqdm
# from pandas.io.formats.format import CategoricalFormatter

# ############################################################################

def getData_fromTXT(file_name):
    data = genfromtxt(
        file_name, delimiter=",", skip_header=1, converters={0: lambda s: str(s)}
    )
    return data.tolist()

def to_dict(d):
    l = d.columns.to_list()
    z = zip(l, l)
    d = dict(z)
    return d

def to_json(d):
    j = json.loads(d)
    return json.dumps(d, indent=4)    

def write_json(j):
    with open(os.path.join(const.DATADIR, "file.json"), "w") as f:
        json.dump(to_json(j), f, indent=4)

def create_dtype_map(df, name):
    PATH = const.METADIR
    FILENAME = "DTYPEMAP_{}.json".format(name)
    FILEPATH = os.path.join(PATH, FILENAME)

    MAP = {}
    MAP["DTypeMap"] = {}

    # NOMES DOS CAMPOS
    FIELD_NAME = df.columns.to_list()

    # TIPO DE DADO PARA CADA CAMPO
    FIELD_DTYPE = []
    for i in iter(df.dtypes.iat):
        FIELD_DTYPE.append(i.name)
    
    # CRIA UM DICT KEY-VALUE COM NOME E TIPO
    z = dict(zip(FIELD_NAME, FIELD_DTYPE))
    MAP["DTypeMap"] = z
    MAP = json.dumps(MAP, indent=4)
    j = json.loads(MAP)

    # GRAVA O DICIONÁRIO EM UM ARQUIVO
    with open(FILEPATH, "w") as f:
        json.dump(j, f, indent=4)

def load_json(name):
    data = {}
    filename = "DTYPEMAP_{}.json".format(name)
    filepath = os.path.join(const.METADIR, filename)
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(f)
    return data

def from_json(f):
    return json.loads(f)

def which_file_exists(name):
    """
    TESTE PARA DETERNINAR QUAL FORMATO DE DATASET ESTÁ DISPONÍVEL PARA CARREGAMENTO
    """
    
    extensions = [".parquet", ".csv"] # EXTENSÕES PARA VERIFICAÇÃO, EM ORDEM DE PRECEDÊNCIA
    
    for ext in extensions:
        
        # CRIA UM PATH DO ARQUIVO PARA CADA EXTENSÃO
        path = os.path.join(const.DATADIR, "{}{}".format(name, ext))
        filepath = {"filepath": {"ext": path}}
        filepath = list(filepath.get("filepath").items())

        # TESTA SE O ARQUIVO EXISTE (POR ORDEM DE PRECEDÊNCIA CONSIDERA O 1º ARQUIVO CORRESPONDIDO)
        if os.path.exists(filepath[0][1]):
            return filepath

    # RECORRE AS URL'S REGISTRADAS, CASO AINDA NÃO EXISTA O ARQUIVO PARA ALGUMA DAS EXTENSÕES VERIFICADAS
    filepath = list(getattr(const, name).get("URLS").items())

    # RETORNA O PATH DO DATASOURCE PARA SER IMPORTADO/CARREGADO
    return filepath

def dtype_transform(df, mapa):
    """
    PRINCIPAL FUNÇÃO PARA TRANSFORMAÇÃO DE DADOS
    """
    
    # TENTA IDENTIFICAR AS COLUNAS DE DATA
    if mapa is not None:
        date_cols = mapa.get('date_cols')
    else:
        date_cols = fn_date_cols(df)

    # TENTA IDENTIFICAR AS COLUNAS NUMÉRICAS
    numeric_cols = fn_number_cols(df)

    # SELECIONA AS COLUNAS TIPO OBJECT PARA CONVERTÊ-LAS EM CATEGÓRICAS
    cat_cols = list(df[df.columns[~df.columns.isin(date_cols + numeric_cols)]].select_dtypes(include="object").columns)
    print(cat_cols)

    # TRATAMENTO DE DADOS
    # ========================================================================
    df = utils.remove_espaco(df, date_cols + numeric_cols)

    # INICIA AS TRANFORMAÇÕES
    # ========================================================================
    
    # TRANSFORMA AS COLUNAS DATETIME
    for c in date_cols:
        try:
            df[c] = pd.to_datetime(df[c], infer_datetime_format=True, errors='coerce')
        except:
            print("ERRO DE CONVERSÃO - COLUNA:{}".format(df[c].column.name))
            pass

    # TRANSFORMA AS COLUNAS CATEGÓRICAS
    for c in cat_cols:
        try:
            df[c] = df[c].astype("category")
        except:
            print("ERRO DE CONVERSÃO - COLUNA:{}".format(df[c]))
            pass

    # TRANSFORMA AS COLUNAS NUMÉRICAS (PARA float64 ou int64)
    for c in numeric_cols:
        i = df.columns.get_loc(c)   # ÍNDICE DA COLUNA
        v = df.iloc[:0, i]          # VALOR NA LINHA ZERO

        # A INFERÊNCIA DO TIPO DE DADO É FEITA ANALISANDO APENAS O 1º VALOR 'v' DE CADA VARIÁVEL DA LISTA

        try:
            # TESTA SE É UM NÚMERO REAL PARA CONVERTER PARA float64
            # isdecimal() APENAS RETORNA True SE TODOS OS CARACTERES FOREM NÚMEROS, NÃO PERMITE (.,-), ETC
            if float(v) and not v.isdecimal():
                try:
                    df[c] = df[c].astype("float64")
                except:
                    pass
            else:  # isdecimal() - SE "NÃO PASSAR" (=True), É UM NÚMERO INTEIRO
                try:
                    # SE FOR NÚMERO INTEIRO, CONVERTE PARA int64
                    df[c] = df[c].astype("int64")
                except:
                    pass
        except:
            print("ERRO DE CONVERSÃO - COLUNA:{}".format(df[c]))
            pass

    return(df)

def convert_to_parquet(lst_dfs: list, filename=None):
    """
    CONCATENA E CONVERTE LISTA DE DATASETS PARA O FORMATO PARQUET DO GOOGLE
    """

    # VERIFICA SE EXISTE MAIS DE UM DATASET PARA CONVERSÃO 
    if len(lst_dfs) > 1:
        # SE POSITIVO, FAZ A CONCATENAÇÃO
        df = pd.concat(lst_dfs, ignore_index=True) 
    else:
        # SENÃO, PEGA O ÚNICO DATASET DA LISTA
        df = lst_dfs[0] 

    # MONTA O CAMINHO ONDE SERÁ GRAVADO O ARQUIVO PARQUET
    filepath_pqt = os.path.join(const.DATADIR, "{}.parquet".format(filename))
    
    # CRIA O ARQUIVO PARQUET
    print("Salvando em disco o arquivo convertido para PARQUET.")
    try:
        df.to_parquet(filepath_pqt)
    except:
        print("ERROR: Dataset {} - Gravação de arquivo PARQUET não realizada! \nCaminho utilizado:{}".format(filename, filepath_pqt))
    
     # VERIFICA QUAL ARQUIVO ESTÁ DISPONÍVEL (DEVERÁ RECONHECER O ARQUIVO PARQUET QUE ACABOU DE SER CRIADO)
    filepath_or_buffer = which_file_exists(filename)

    return filepath_or_buffer

def fn_date_cols(df):
    """
    RECURSO SECUNDÁRIO PARA DETERNINAR O DTYPE POR ANÁLISE DO CONTEÚDO DA COLUNA
    """
    
    import re

    date_patern1 = re.compile(
        r"(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
    )
    date_patern2 = re.compile(
        r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"
    )

    lst_cols = []

    for n in list(df.columns):
        i = df.columns.get_loc(n)   # ÍNDICE DA COLUNA
        v = df.iloc[:, i]           # VALOR NA LINHA ZERO
        try:
            if (re.search(date_patern1, v) is not None) or (
                re.search(date_patern2, v) is not None):
                lst_cols.append(n)
        except:
            pass

    return lst_cols

def fn_number_cols(df):
    """
    RECURSO SECUNDÁRIO PARA DETERNINAR O DTYPE POR ANÁLISE DO CONTEÚDO DA COLUNA
    """

    lst_cols = []

    for n in list(df.columns):
        i = df.columns.get_loc(n)  # ÍNDICE DA COLUNA
        v = df.iloc[:, i]  # VALOR NA LINHA ZERO
        try:
            if float(n):  # SE PASSAR, É UM NÚMERO (Tenta converter para float)
                lst_cols.append(n)
        except:
            pass

    return lst_cols