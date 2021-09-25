# from typing import Text
from numpy import genfromtxt
from app.home import vups

# from time import time
# from datetime import datetime

# from app.base.models import Microdados
# from app.home import vups
# from app import db
# from tqdm import tqdm


def getData_fromTXT(file_name):
    data = genfromtxt(
        file_name, delimiter=",", skip_header=1, converters={0: lambda s: str(s)}
    )
    return data.tolist()


def resumo(municipio=None):
    """
    # população
    # nª de casos
    # posição no ranking
    """
    df = vups.datasets.microdados(columns=["Municipio", "DataNotificacao"])
