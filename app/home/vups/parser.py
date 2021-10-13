# -*- encoding: utf-8 -*-
import json
from . import const
import os 


def load_json(name):
    data = {}
    filename = "{}_DTYPEMAP.json".format(name)    
    filepath = os.path.join(const.DATADIR, filename)
    if os.path.exists(filepath):
        with open(filepath) as f:
            data = json.load(filepath)

    return data
    