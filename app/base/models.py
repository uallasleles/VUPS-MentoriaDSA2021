# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Date
from app import db, login_manager
from app.base.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # we need bytes here (not plain str)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Microdados(db.Model):
    
    __tablename__ = 'Microdados'
    #__table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True, nullable=False)

    DataNotificacao = Column(String)
    DataCadastro = Column(String)
    DataDiagnostico = Column(String)
    DataColeta_RT_PCR = Column(String)
    DataColetaTesteRapido = Column(String)
    DataColetaSorologia = Column(String)
    DataColetaSorologiaIGG = Column(String)
    DataEncerramento = Column(String)
    DataObito = Column(String)

    Classificacao = Column(String)
    Evolucao = Column(String)
    CriterioConfirmacao = Column(String)
    StatusNotificacao = Column(String)
    Municipio = Column(String)
    Bairro = Column(String)
    FaixaEtaria = Column(String)
    IdadeNaDataNotificacao = Column(String)
    Sexo = Column(String)
    RacaCor = Column(String)
    Escolaridade = Column(String)
    Gestante = Column(String)
    Febre = Column(String)
    DificuldadeRespiratoria = Column(String)
    Tosse = Column(String)
    Coriza = Column(String)
    DorGarganta = Column(String)
    Diarreia = Column(String)
    Cefaleia = Column(String)

    ComorbidadePulmao = Column(String)
    ComorbidadeCardio = Column(String)
    ComorbidadeRenal = Column(String)
    ComorbidadeDiabetes = Column(String)
    ComorbidadeTabagismo = Column(String)
    ComorbidadeObesidade = Column(String)

    FicouInternado = Column(String)
    ViagemBrasil = Column(String)
    ViagemInternacional = Column(String)
    ProfissionalSaude = Column(String)
    PossuiDeficiencia = Column(String)
    MoradorDeRua = Column(String)
    ResultadoRT_PCR = Column(String)
    ResultadoTesteRapido = Column(String)
    ResultadoSorologia = Column(String)
    ResultadoSorologia_IGG = Column(String)
    TipoTesteRapido = Column(String)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
    
            setattr(self, property, value)
        
    def __repr__(self):
        return str(self.Municipio)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None
