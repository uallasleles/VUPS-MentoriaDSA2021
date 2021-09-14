# VUPS Mentoria DSA 2021

Dashboard gerado pela plataforma AppSeed com módulos básicos, banco de dados, autenticação e scripts de implantação.

<br />

> Features

- DBMS: SQLite, PostgreSQL (production) 
- DB Tools: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- Modular design with **Blueprints**, simple codebase
- Session-Based authentication (via **flask_login**), Forms validation
- Deployment scripts: Docker, Gunicorn / Nginx, Heroku

<br />

## Como usá-lo

```bash
$ # Get the code
$ git clone https://github.com/app-generator/flask-dashboard-volt.git
$ cd flask-dashboard-volt
$
$ # Virtualenv modules installation (Unix based systems)
$ # virtualenv env
$ # source env/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ virtualenv env
$ .\env\Scripts\activate
$
$ # Install modules - SQLite Database
$ pip3 install -r requirements.txt
$
$ # OR with PostgreSQL connector
$ pip install -r requirements-pgsql.txt
$
$ # Set the FLASK_APP environment variable
$ # (Unix/Mac) export FLASK_APP=run.py
$ (Windows) set FLASK_APP=run.py
$ # (Powershell) $env:FLASK_APP = ".\run.py"
$
$ # Set up the DEBUG environment
$ # (Unix/Mac) export FLASK_ENV=development
$ (Windows) set FLASK_ENV=development
$ # (Powershell) $env:FLASK_ENV = "development"
$
$ # Start the application (development mode)
$ # --host=0.0.0.0 - expose the app on all network interfaces (default 127.0.0.1)
$ # --port=5000    - specify the app port (default 5000)  
$ flask run --host=0.0.0.0 --port=5000
$
$ # Access the dashboard in browser: http://127.0.0.1:5000/
```

> Nota: Para usar o aplicativo, acesse a página de registro e crie um novo usuário. Após a autenticação, o aplicativo irá desbloquear as páginas privadas.

<br />

## Code-base structure

O projeto é codificado usando blueprints, app factory pattern, perfil de configuração dual (desenvolvimento e produção) e uma estrutura intuitiva apresentada a seguir::

> Simplified version

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
   |-- requirements-mysql.txt    # Production modules  - Mysql DMBS
   |-- requirements-pqsql.txt    # Production modules  - PostgreSql DMBS
   |
   |-- .env                      # Inject Configuration via Environment
   |-- config.py                 # Set up the app
   |-- run.py                    # Start the app - WSGI gateway
   |
   |-- ************************************************************************
```

<br />

> The bootstrap flow

- `run.py` loads the `.env` file
- Inicialize o aplicativo usando o perfil especificado: *Debug* ou *Production*
  - Se env.DEBUG está configurado para *True* o armazenamento SQLite é usado
  - Se env.DEBUG está configurado para *False* o driver de banco de dados especificado é usado (MySql, PostgreSQL)
- Chame o método de criação de aplicativos `create_app` definido em app/__init__.py
- Redirecione os usuários convidados para a página de Login
- Desbloqueie as páginas servidas pelo blueprint *home* para usuários autenticados

<br />

> App / Base Blueprint

O blueprint *Base* trata da autenticação (rotas e formulários) e do gerenciamento de ativos. A estrutura é apresentada a seguir:

```bash
< PROJECT ROOT >
   |
   |-- app/
   |    |-- home/                                # Home Blueprint - serve páginas do app (área privada)
   |    |-- base/                                # Base Blueprint - lida com a autenticação
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

## Recompile CSS

Para recompilar arquivos SCSS, siga esta configuração:

<br />

**Passo #1** - Ferramentas de instalação

- [NodeJS](https://nodejs.org/en/) 12.x or higher
- [Gulp](https://gulpjs.com/) - globally 
    - `npm install -g gulp-cli`
- [Yarn](https://yarnpkg.com/) (optional) 

<br />

**Passo #2** - Mude o diretório de trabalho para a pasta `assets`

```bash
$ cd app/base/static/assets
```

<br />

**Passo #3** - Instale os módulos (isso criará um diretório `node_modules` clássico)

```bash
$ npm install
// OR
$ yarn
```

<br />

**Passo #4** - Editar e recompilar arquivos SCSS

```bash
$ gulp scss
```

O arquivo gerado é salvo no diretório `static/assets/css`.

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

## Credits & Links

- [Flask Framework](https://www.palletsprojects.com/p/flask/) - The offcial website
- [Boilerplate Code](https://appseed.us/boilerplate-code) - Index provided by **AppSeed**
- [Boilerplate Code](https://github.com/app-generator/boilerplate-code) - Index published on Github

<br />

---
[Flask Bootstrap 5](https://appseed.us/admin-dashboards/flask-dashboard-volt) Volt - Provided by **AppSeed [App Generator](https://appseed.us/app-generator)**.

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