# -*- encoding: utf-8 -*-
import json
import os
from . import const


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


def field_map(df, name):

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

    # FORMATA O NOME DO ARQUIVO PARA GRAVAÇÃO
    filename = "{}{}".format(name, "_DTYPEMAP.json")

    # GRAVA O DICIONÁRIO EM UM ARQUIVO
    with open(os.path.join(const.DATADIR, filename), "w") as f:
        json.dump(j, f, indent=4)