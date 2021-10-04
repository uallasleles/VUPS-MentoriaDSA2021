# Clã VUPS - Mentoria DSA 2021
Projeto elaborado durante o Programa de Mentoria entre Alunos da **Data Science Academy**.

![Alt text](app\base\static\assets\img\icons\banner-dsa.jpg "Data Science Academy")

# Sobre a análise de dados.

## Tópicos
- Problema de Negócio
- Contexto
- Datasets
- Variáveis
- Ranking
   - PCA
      - Sinais Variáveis
      - Teste Estatístico
      - Escolha dos Fatores
      - Calculo da Puntuação
- Visualizações
   - Comparação de Repasses
   - Poder de Compra do Município
   - Calendário de Casos
   - Resumo COVID
   - Mapa com Ranking

## Problema de Negócio
---
Quais Municípios estão se saindo melhor em relação ao combate ao COVID-19?

## Contexto
---
Foi definido que iríamos focar nossa análise em um único estado brasileiro, dado o tamnho continetal
do nosso país. Como sugestão do nosso Mentor, original do estado do Espírito Santo, resolvemos delimitar
escomo do nosso trabalho aos municípios do ES.

Uma vez decidido os limites geográficos, definimos o escopo temporal do projeto. Por conta do tempo para conclusão
do trabalho, decidimos que uma avaliação mensal do desempenho do municípios seria a melhor estratêgia.

## Datasets
---
Datasets utilizados:
* Dados hitóricos COVID (fonte: )
* Dados históricos Vacinação COVID (fonte: )
* Dados Populacionais (fonte: )
* Repasses Estaduais (fonte: )

## Ranking
---
Para avaliar o desempenho no combate à pendemia, decidimos criar um ranking dos municípios. O desafio era criar
um sistema de avaliação que eliminasse a ponderação arbitrária. Para isso, usamos a soma do produto entre os fatores
oriundos de uma PCA e suas variancias compartilhadas.

#### Variáveis
As variáveis analisadas foram:
* Quantidade de casos (per capita) por mês;
* Quantidade de óbitos (per capita) por mês;
* Quantidade de casos recuperados (per capita) por mês;
* Quantidade de doses de vacina (per capita) por mês;
* Quantidade em dinheiro repassada pelo estado (per capita) por mês;

#### Teste Estatístico
Foi rodado o teste de esfericidade de Bartlett que apontou adequação estatística global do dataset para o modelo.

#### Escolha dos Fatores
Como o dataset era pequeno e não requeria muito poder computacional, decidimos por incluir todos os fatores no modelo,
de maneira que as comunalidades de cada variável tiveram valor final igual a 1.

#### Calculo da Puntuação
O calculo da pontuação se deu pela soma do produto entre os fatores e a variancia compartilhada

## Visualizações
---

### Comparação de Repasses
Criamos uma visualização que fizesse com que o usuário podesse comparar os repasses dos municípios de maneira simples
e objetiva. Duas formas de comparação foram criadas:
* Comparação Nominal: valor bruto recebido pelos municípios
* Comparação de variabilidade: quanto cada repasse variou de mês a més

### Poder de Compra do Município
Visualização que compara o valor recebido com a variação do indice IPCA. De maneira que o primeiro mês de análise
serviu como base de calculo para os mêses subsequentes. Com essa informação, o usuário pode ter uma noção melhor do
poder economico do município em relação ao combate da pandemia.

### Calendário de Casos
Visualização em forma de heatmap com formato de calendário. Tem com objetivo entender padrões de contagio do vírus.
É interessante observar, por exemplo, a quantidade de casos novos 1 semana após feriados municipais (como em AFONSO
CALUDIO no dia 20 de JANEIRO -> valores default da função).
### Resumo COVID
Visualização em linha com o numero de casos totais, obitos, recuperados e ativos, no tempo.

### Mapa com Ranking
Mapa com as divisões domunicípios e coloração referente ao posicionamento das cidades no ranking.


# Sobre a ignição do projeto

Para acelerar o processo de desenvolvimento da aplicação utilizamos um tema bootstrap desenvolvido por Themesberg.
> Bootstrap é o framework CSS mais popular do mundo. É um conjunto de componentes da web que ajudam a construir interfaces de usuário rápidas e modernas sem ter que configurar o código clichê para elementos básicos.

Desta forma podemos nos concentrar em personalizar o site usando as variáveis ​​Sass para alterar cores, fontes, tamanhos, e adicionar novos recursos.

Vantagens de usar um modelo

> 1. *Qualidade*. Base de código sólida e que funciona na maioria dos dispositivos e navegadores.
> 2. *Responsividade*. Site responsivo e acessívei em vários dispositivos.

<br>

Principais recursos frontend utilizados:
- Framework Bootstrap
- Ferramenta de fluxo de trabalho GULP
- Pré-processador CSS SASS

<br />

Com relação a estrutura base para o backend utilizamos o seguinte:

- Design modular com **Blueprints**
- Autenticação baseada em sessão (via **flask_login**) e formulários de validação.
- DBMS: SQLite
- DB Tools: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- Amazon Web Service para deploy da aplicação

<br />

## Como usá-lo

```bash
# Obter o código
$ git clone https://github.com/uallasleles/VUPS-MentoriaDSA2021.git
```

```bash
# Instalar o Virtualenv

# Sistemas baseados em Unix
$ virtualenv env
$ source env/bin/activate

# Sistemas baseados em Windows
> virtualenv env
> .\env\Scripts\activate
```

```bash
# Instalar os pacotes Python necessários para o App
$ pip3 install -r requirements.txt
```

Para inicializar a aplicação é necessário definir as variáveis de ambiente FLASK_APP e FLASK_ENV.  
A variável FLASK_APP é usada para especificar como carregar o aplicativo.  
A variável FLASK_ENV define o ambiente em que o aplicativo Flask é executado (production ou development).  
Porém, utilizamos o dotenv do Flask para definir variáveis ​​de ambiente automaticamente, em vez de configurarmos cada vez que inicializamos a aplicação.

As declarações manuais referente as instruções que foram automatizadas são as seguintes:
```bash
# Configurar a variável de ambiente FLASK_APP

# (Unix/Mac) 
$ export FLASK_APP=run.py

# Windows (CMD) 
> set FLASK_APP=run.py

# Windows (Powershell) 
$ env:FLASK_APP = ".\run.py"
```

```bash
# Configurar o ambiente para DEBUG (opcional)

# (Unix/Mac) 
$ export FLASK_ENV=production

# Windows (CMD) 
> set FLASK_ENV=production

# Windows (Powershell) 
> env:FLASK_ENV = "production"
```

Após estas configurações você pode inicializar a aplicação.
```bash
# Iniciar o Dashboard App 

# Opções: 

# Modo de Desenvolvimento
# --host=0.0.0.0 - expõe o aplicativo em todas as interfaces de rede (padrão 127.0.0.1)
# --port=5000    - Especifique a porta do aplicativo (padrão 5000)

$ flask run --host=0.0.0.0 --port=5000

# Acesse o Dashboard App em seu browser: http://127.0.0.1:5000/
```

> Nota: Para usar o aplicativo, acesse a página de registro e crie um novo usuário. Após a autenticação, o aplicativo irá desbloquear as páginas privadas.

<br />

## Estrutura do código base

O projeto é codificado usando blueprints, app factory pattern, perfil de configuração dual (desenvolvimento e produção) e uma estrutura intuitiva apresentada a seguir:

> Versão Simplificada

```bash
< PROJECT ROOT >
   |
   |-- app/                      # Implements app logic
   |    |-- base/                # Base Blueprint - handles the authentication
   |    |-- home/                # Home Blueprint - serve UI Kit pages
   |    |
   |   __init__.py               # Initialize the app
   |
   |-- requirements.txt          # Development modules - SQLite storage
   |
   |-- .env                      # Inject Configuration via Environment
   |-- config.py                 # Set up the app
   |-- run.py                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

> O fluxo bootstrap

- `run.py` carrega o arquivo `.env`.
- Inicializa o aplicativo usando o perfil especificado: *Debug* ou *Production*
  - Se env.DEBUG está configurado para *True* o armazenamento SQLite é usado
  - Se env.DEBUG está configurado para *False* o driver de banco de dados especificado é usado (MySql, PostgreSQL)
- Chama o método de criação de aplicativos `create_app` definido em app/__init__.py
- Redireciona os usuários convidados para a página de Login
- Desbloqueia as páginas servidas pelo blueprint *home* para usuários autenticados.

<br />

> App / Base Blueprint

O blueprint *Base* trata da autenticação (rotas e formulários) e do gerenciamento de ativos. A estrutura é apresentada a seguir:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- home/                                # Home Blueprint - serve páginas do app (área privada)
   |    |-- base/                                # Base Blueprint - lida com a autenticação
   |         |-- vups/
   |         |    |-- __init__, JS, images>          # CSS files, Javascripts files
   |         |-- static/
   |         |    |-- <css, JS, images>          # CSS files, Javascripts files
   |         |
   |         |-- templates/                      # Modelos usados ​​para renderizar páginas
   |              |
   |              |-- includes/                  #
   |              |    |-- navigation.html       # Componente do menu superior
   |              |    |-- sidebar.html          # Componente da barra lateral
   |              |    |-- footer.html           # Rodapé do aplicativo
   |              |    |-- scripts.html          # Scripts comuns a todas as páginas
   |              |
   |              |-- layouts/                   # Páginas mestre
   |              |    |-- base-fullscreen.html  # Usado por páginas de autenticação
   |              |    |-- base.html             # Usado por páginas comuns
   |              |
   |              |-- accounts/                  # Páginas de autenticação
   |                   |-- login.html            # Página de login
   |                   |-- register.html         # Página de registro
   |
   |-- requirements.txt                          # Development modules - SQLite storage
   |-- requirements-mysql.txt                    # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt                    # Production modules  - PostgreSql DMBS
   |
   |-- .env                                      # Configuração de injeção via ambiente
   |-- config.py                                 # Set up the app
   |-- run.py                                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

> App / Home Blueprint

O blueprint *Home* lida com as páginas do UI Kit para usuários autenticados. Esta é a zona privada do aplicativo - a estrutura é apresentada a seguir:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- base/                     # Base Blueprint - handles the authentication
   |    |-- home/                     # Home Blueprint - serve app pages (private area)
   |         |
   |         |-- templates/           # UI Kit Pages
   |              |
   |              |-- index.html      # Default page
   |              |-- page-404.html   # Error 404 - mandatory page
   |              |-- page-500.html   # Error 500 - mandatory page
   |              |-- page-403.html   # Error 403 - mandatory page
   |              |-- *.html          # All other HTML pages
   |
   |-- requirements.txt               # Development modules - SQLite storage
   |-- requirements-mysql.txt         # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt         # Production modules  - PostgreSql DMBS
   |
   |-- .env                           # Inject Configuration via Environment
   |-- config.py                      # Set up the app
   |-- run.py                         # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

## Deployment

O aplicativo é fornecido com uma configuração básica para ser executado em [Docker](https://www.docker.com/), [Heroku](https://www.heroku.com/), [Gunicorn](https://gunicorn.org/), e [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

<br />

### [Docker](https://www.docker.com/) execution
---

O aplicativo pode ser executado facilmente em um contêiner docker. Os passos:

> Get the code

```bash
$ git clone https://github.com/app-generator/flask-dashboard-volt.git
$ cd flask-dashboard-volt
```

> Start the app in Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visit `http://localhost:5005` in your browser. The app should be up & running.

<br />

### [Heroku](https://www.heroku.com/)
---

Steps to deploy on **Heroku**

- [Create a FREE account](https://signup.heroku.com/) on Heroku platform
- [Install the Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) that match your OS: Mac, Unix or Windows
- Open a terminal window and authenticate via `heroku login` command
- Clone the sources and push the project for LIVE deployment

```bash
$ # Clone the source code:
$ git clone https://github.com/app-generator/flask-dashboard-volt.git
$ cd flask-dashboard-volt
$
$ # Check Heroku CLI is installed
$ heroku -v
heroku/7.25.0 win32-x64 node-v12.13.0 # <-- All good
$
$ # Check Heroku CLI is installed
$ heroku login
$ # this commaond will open a browser window - click the login button (in browser)
$
$ # Create the Heroku project
$ heroku create
$
$ # Trigger the LIVE deploy
$ git push heroku master
$
$ # Open the LIVE app in browser
$ heroku open
```

<br />

### [Gunicorn](https://gunicorn.org/)
---

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX.

> Install using pip

```bash
$ pip install gunicorn
```
> Start the app using gunicorn binary

```bash
$ gunicorn --bind 0.0.0.0:8001 run:app
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

<br />

### [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/)
---

Waitress (Gunicorn equivalent for Windows) is meant to be a production-quality pure-Python WSGI server with very acceptable performance. It has no dependencies except ones that live in the Python standard library.

> Install using pip

```bash
$ pip install waitress
```
> Start the app using [waitress-serve](https://docs.pylonsproject.org/projects/waitress/en/stable/runner.html)

```bash
$ waitress-serve --port=8001 run:app
Serving on http://localhost:8001
```

Visit `http://localhost:8001` in your browser. The app should be up & running.

<br />

---

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- base/                               # Base Blueprint
   |    |    |-- static/assets/
   |    |    |           |-- css/               # UI Kit css
   |    |    |           |-- JS/                # Javascript files
   |    |    |           |-- images/            # images used by the app
   |    |    |           |-- scss/              # SCSS files (if any)
   |    |    |
   |    |    |-- templates/                      # Templates used to render pages
   |    |         |
   |    |         |-- includes/                  #
   |    |         |    |-- navigation.html       # Top menu component
   |    |         |    |-- sidebar.html          # Sidebar component
   |    |         |    |-- footer.html           # App Footer
   |    |         |    |-- scripts.html          # Scripts common to all pages
   |    |         |
   |    |         |-- layouts/                   # Master pages
   |    |         |    |-- base-fullscreen.html  # Used by Authentication pages
   |    |         |    |-- base.html             # Used by common pages
   |    |         |
   |    |         |-- accounts/                  # Authentication pages
   |    |              |-- login.html            # Login page
   |    |              |-- register.html         # Registration page
   |    |
   |    |-- home/                                # Home Blueprint - serve app pages (private area)
   |         |-- templates/                      # UI Kit Pages
   |              |
   |              |-- index.html                 # Default page
   |              |-- page-404.html              # Error 404 - mandatory page
   |              |-- page-500.html              # Error 500 - mandatory page
   |              |-- page-403.html              # Error 403 - mandatory page
   |              |-- *.html                     # All other HTML pages
   |
   |-- ************************************************************************
```


