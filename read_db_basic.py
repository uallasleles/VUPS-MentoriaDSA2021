""" read from a SQLite database and return data """

from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# the name of the database; add path if necessary
db_name = 'vups.db'
# db_name = 'sockmarket.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class Sock(db.Model):
    __tablename__ = 'socks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    style = db.Column(db.String)
    color = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    updated = db.Column(db.String)


class Microdados(db.Model):
    __tablename__ = 'microdados'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    dataNotificacao = db.Column(db.String)
    dataCadastro = db.Column(db.String)
    dataDiagnostico = db.Column(db.String)
    dataColeta_RT_PCR = db.Column(db.String)
    dataColetaTesteRapido = db.Column(db.String)
    dataColetaSorologia = db.Column(db.String)
    dataColetaSorologiaIGG = db.Column(db.String)
    dataEncerramento = db.Column(db.String)
    dataObito = db.Column(db.String)

    classificacao = db.Column(db.String)
    evolucao = db.Column(db.String)
    criterioConfirmacao = db.Column(db.String)
    statusNotificacao = db.Column(db.String)
    municipio = db.Column(db.String)
    bairro = db.Column(db.String)
    faixaEtaria = db.Column(db.String)
    idadeNaDataNotificacao = db.Column(db.String)
    sexo = db.Column(db.String)
    racaCor = db.Column(db.String)
    escolaridade = db.Column(db.String)
    gestante = db.Column(db.String)
    febre = db.Column(db.String)
    dificuldadeRespiratoria = db.Column(db.String)
    tosse = db.Column(db.String)
    coriza = db.Column(db.String)
    dorGarganta = db.Column(db.String)
    diarreia = db.Column(db.String)
    cefaleia = db.Column(db.String)

    comorbidadePulmao = db.Column(db.String)
    comorbidadeCardio = db.Column(db.String)
    comorbidadeRenal = db.Column(db.String)
    comorbidadeDiabetes = db.Column(db.String)
    comorbidadeTabagismo = db.Column(db.String)
    comorbidadeObesidade = db.Column(db.String)

    ficouInternado = db.Column(db.String)
    viagemBrasil = db.Column(db.String)
    viagemInternacional = db.Column(db.String)
    profissionalSaude = db.Column(db.String)
    possuiDeficiencia = db.Column(db.String)
    moradorDeRua = db.Column(db.String)
    resultadoRT_PCR = db.Column(db.String)
    resultadoTesteRapido = db.Column(db.String)
    resultadoSorologia = db.Column(db.String)
    resultadoSorologia_IGG = db.Column(db.String)
    tipoTesteRapido = db.Column(db.String)

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
        return str(self.municipio)

#routes

def cria_html_ul_li(rs):
    html = '<ul>'
    for r in rs:
        html += '<li>'
        for c in r:
            html += c + ', '
        html = '</li>'
    html += '</ul>'
    return html

@app.route('/')
def index():
    # try:
    txt = 'SANTANA'
    search = "%{}%".format(txt)

    mds = Microdados.query.filter(Microdados.municipio.like(search)).all()
    
    #html = cria_html_ul_li(mds)
    #return html

    return render_template('list.html', mds=mds)

    # except Exception as e:
    #     # e holds description of the error
    #     error_text = "<p>The error:<br>" + str(e) + "</p>"
    #     hed = '<h1>Something is broken.</h1>'
    #     return hed + error_text

if __name__ == '__main__':
    app.run(debug=True)