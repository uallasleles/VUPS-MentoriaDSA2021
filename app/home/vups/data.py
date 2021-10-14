# -*- encoding: utf-8 -*-

# from typing import Text
from numpy import genfromtxt
from app.home.vups import const, utils
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
    FILENAME = "{}{}".format(name, "_DTYPEMAP.json")

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
    with open(os.path.join(PATH, FILENAME), "w") as f:
        json.dump(j, f, indent=4)

def load_json(name):
    data = {}
    filename = "{}_DTYPEMAP.json".format(name)
    filepath = os.path.join(const.DATADIR, filename)
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
    
    if mapa is not None:
        date_cols = mapa.get('date_cols')
    else:
        date_cols = fn_date_cols(df)

    numeric_cols = fn_number_cols(df)
    
    cat_cols = list(df.select_dtypes(include="object").columns)
    
    df = utils.remove_espaco(df, date_cols + numeric_cols)

    for c in date_cols:
        try:
            df[c] = pd.to_datetime(df[c], infer_datetime_format=True, errors='coerce')
        except:
            pass

    for c in cat_cols:
        try:
            df[c] = df[c].astype("category")
        except:
            pass

    for c in numeric_cols:
        i = df.columns.get_loc(c)  # ÍNDICE DA COLUNA
        v = df.iloc[:0, i]  # VALOR NA LINHA ZERO
        try:
            if float(v) and not v.isdecimal():
                try:
                    df[c] = df[c].astype("float64")
                except:
                    pass
            else:  # isdecimal() - SE NÃO PASSAR, É UM NÚMERO INTEIRO (Verifica se todos os caracteres no Unicode são decimais)
                try:
                    df[c] = df[c].astype("int64")
                except:
                    pass
        except:
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
    try:
        print("Salvando em disco o arquivo convertido para PARQUET.")
        df.to_parquet(filepath_pqt)
    except:
        print("O dataset {} não foi convertido para Parquet. \nCaminho utilizado:{}".format(filename, filepath_pqt))
    
    # RETORNA A EXTENSÃO DO ARQUIVO COMO RESPOSTA PARA get_data()
    resp = '.parquet' if os.path.exists(filepath_pqt) else '.csv'
    
    return resp

def fn_date_cols(df):
    """
    RECURSO SECUNDÁRIO PARA DETERNINAR O DTYPE ANALISANDO COLUNA
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
    RECURSO SECUNDÁRIO PARA DETERNINAR O DTYPE ANALISANDO COLUNA
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