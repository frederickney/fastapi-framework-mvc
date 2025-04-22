# Introduction

## Configuration

The base configuration file is located on the config dir.
### SSL Encryption

For enabling ssl encryption within the application, you will need to add in the __"SERVER"__ key entry in the config file

```yaml
  SSL:
    Certificate: "path to the cer file (public key)"
    PrivateKey: "path to the pki file (private key)"
```

You can add default database using only the configuration file.

### Default database with builtin driver in sqlalchemy 

```yaml
...
DATABASE: 
  default: mysql
  mysql: 
    driver: mysql+pymysql
    user: "replace this with your database user"
    password: "replace this with your database user's password"
    database: "replace this with your database name"
    address: "replace this with your hostname"
    models: "mysql (python module that require to be put under Models.Persistent module)"
    readonly: false
...
```

### Default database with non builtin driver in sqlalchemy 

```yaml
...
DATABASE:
  informix:
    driver: informix
    user: "replace this with your database user"
    password: "replace this with your database user's password"
    database: "replace this with your database name"
    address: "replace this with your hostname"
    models: "informix (python module that require to be put under Models.Persistent module)"
    params:
      SERVER: "replace with your server name"
      CLIENT_LOCALE: "replace with your client locale"
      DB_LOCALE: "replace with your server locale"
    dialects:
      informix: 
        module: IfxAlchemy.IfxPy
        class: IfxDialect_IfxPy
      informix.IfxPy: 
        module: IfxAlchemy.IfxPy
        class: IfxDialect_IfxPy
      informix.pyodbc: 
        module: IfxAlchemy.pyodbc
        class: IfxDialect_pyodbc
    readonly: false
...
```

__"params"__ are parameters that need to be send within the connection to the database.
In that example using informix database __"SERVER"__, __"CLIENT_LOCALE"__ and __"DB_LOCALE"__ are required parameters for the connection to the database.

__"dialects"__ are the python modules configuration to translate models into sql statements to query the database

By default escape char between url and first param is __?__ and escape char between parameters is __&__ but they can be changed by adding within your database params section:

```yaml
...
      url_param_separator: '?' #Change it with yours
      params_separator: '&' #Change it with yours
...
```

### Multiple databases

```yaml
...
DATABASE:
  db01:
    ...
  db02:
    ...
...
```

## Creating server routes

There are 3 files where you could register your flask server routes, You could find these file under the src/Server folder:

* Errors:

All the server http error code must be registered inside the __init__ method of the ErrorHandler.py file.

Example:
```python
srv.add_exception_handler(500, Controllers.Web.HTTP50XController.error500)
```

* Web based http file routes:

All the web based http routes must be registered inside the __init__ method of the Web.py file.

Example:
```python
server.add_route('/', Controllers.Web.HomeController.index, methods=['GET'], 'home')
```

* Rest api routes:

All the Rest API based routes must be registered inside the __init__ method of the WS.py file.


Example:
```python
server.add_api_route('/api/content/', Controllers.WS.ApiController.index, methods=['GET'], 'api.content')
```

## Creating controllers:

In case of database used within controllers, you will need to use __@safe__ from __fastapi_framework_mvc.Database.decorators__ over your function. Example bellow:

```python

from fastapi_framework_mvc.Database.decorators import safe


class Content(object):

    @safe
    @staticmethod
    def index(api_param):
        return api_param


class Controller(Content):

    @classmethod
    def index(cls, api_param:str):
        return super(Controller, cls).index(api_param)

```

* Web based http file controllers:

All web based http file controllers must be placed under the ```Controllers.Web``` module.

The class based controllers that you register into the app must be imported into the ```__init__.py``` file of the ```Controller.Web``` module.

The file based that contain your view functions must  must also be inmported into the ```__init__.py``` file of the ```Controller.Web``` module.


* Rest api controllers:

All Rest API based controllers must be placed under the src/Controllers/WS folder.

The class based controllers that you register into the app must be imported into the ```__init__.py``` file of the ```Controller.Web``` module.

The file based that contain your view functions must  must also be inmported into the ```__init__.py``` file of the ```Controller.Web``` module.

## Creating models:


you can create SQLAlchemy models by creating a new module under the ```Models.Persistent``` module and place each models inside your module that you previously created. 

The models that you register into the app must be an ```Database.Model ``` or ```Database.get_models_by_name('replace that with your database connection name')``` object, you could import this object using the following line into your database model:


```python
from Database import Database
```

All models must be imported inside the ```__init__.py``` of your base module and you must import this module in the ```__init__.py``` of the ```Models.Persistent``` module


## Static folder:

The src/static folder contains all static file for your web based application.

## Template folder:

The src/template folder contains layouts and templates file for your web based application.
Those files are content configurable, you can also import layout inside the your template file, it allow you to have only content editable part into your template file.

---

# Using docker-compose file:

* First start of the flask server:

```bash
docker-compose up 
```

* To start the flask server:

```bash
docker-compose start 
```

* To restart the flask server

```bash
docker-compose restart 
```

* To shutdown the flask server:

```bash
docker-compose stop 
```

---

# Running on Azure Function App:

```python title="function_app.py"
# coding: utf-8
import azure.functions as functions
import fastapi_framework_mvc.azure 
import logging
import os


os.environ.setdefault('CONFIG_FILE', './config/config.yml')
app = functions.AsgiFunctionApp(fastapi_framework_mvc.azure.AzureFunctionsApp(), http_auth_level=functions.AuthLevel.ANONYMOUS)
```

# Running on local desktop:

We assume that your system already had python v3+ and pip v3+ installed.

* installation:

```bash 
git clone https://github.com/frederickney/fastapi-framework-mvc.git
cd fastapi-framework-mvc
pip3 install .
```

or 
```pip 
pip install fastapi-framework-mvc
```

* CLI interface

```bash
python -m fastapi_framework_mvc.cli -h
```


* Create a new project

```bash
python -m fastapi_framework_mvc.cli -cp <your project>
```

or

```bash
python -m fastapi_framework_mvc.cli --create-project <your project>
```

When the project is created, more command can be used when the env __"CONFIG_FILE"__ is set and can be run through

```bash
python -m fastapi_framework_mvc.app
```

see -h for usages

* On every startup

```bash 
export CONFIG_FILE=config/config.yml
```

* Starting the flask server in standalone

```bash 
python -m fastapi_framework_mvc.server
```

* Starting the flask server with gunicorn and workers process

```bash 
python -m fastapi_framework_mvc.wsgi
```

---

# LICENSE

#### See [License file](LICENSE)
