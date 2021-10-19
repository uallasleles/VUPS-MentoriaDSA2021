# -*- encoding: utf-8 -*-
"""
******************************************************************************
**                                                                          **
**               Programa de Mentoria Entre Alunos DSA (2021)               **
** ------------------------------------------------------------------------ **
**               REALIZADOR: Data Science Academy                           **
**                   MENTOR: Prof.º Jocelino Antônio Demuner                **
**                    Turma: 2 (Codinome: Clã VUPS)                         **
**                  Período: 07/06/2021 - 30/09/2021                        **
**                                                                          **
******************************************************************************
"""
print(__doc__)

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config

from config import config_dict
from app import create_app, db

DEBUG = config('DEBUG', default=True, cast=bool)

# Configuração
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Carregue a configuração usando os valores padrão
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )

if __name__ == '__main__':
    app.run()