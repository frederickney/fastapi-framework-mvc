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
DATABASES: 
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
DATABASES:
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
DATABASES:
  db01:
    ...
  db02:
    ...
...
```

## Creating server routes

There are 3 files where you could register your flask server routes, You could find these file under the src/server folder:

* Errors:

All the server http error code must be registered inside the __init__ method of the errorhandler.py file.

Example:
```python
server.add_exception_handler(500, controllers.web.errors.http_500)
```

* Web based http file routes:

All the web based http routes must be registered inside the __init__ method of the web.py file.

Example:
```python
server.add_route(path='/', route=controllers.web.home.index, methods=["GET"], name='home')
```


Can also loads router:

```python
#controllers.ws.api.router needs to be a fastapi APIRouter instance
server.include_router(controllers.web.router, prefix='/api/v1')
```

* Rest api routes:

All the Rest API based routes must be registered inside the __init__ method of the ws.py file.


Example:
```python
server.add_api_route('/api/content/', controller.ws.api.index, methods=['GET'], 'api.content')
```

Can also loads router:

```python
#controllers.ws.api.router needs to be a fastapi APIRouter instance
server.include_router(controllers.ws.api.v1.router, prefix='/api/v1/')
```

## Creating controllers:

In case of database used within controllers, you will need to use __@safe__ from __fastapi_framework_mvc.database.decorators__ over your function. Example bellow:

```python

from fastapi_framework_mvc.database.decorators import safe


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

All web based http file controllers must be placed under the ```controllers.web``` module.

The class based controllers that you register into the app must be imported into the ```__init__.py``` file of the ```controller.web``` module.

The file based that contain your view functions must must also be imported into the ```__init__.py``` file of the ```controller.web``` module.


* Rest api controllers:

All Rest API based controllers must be placed under the ```controllers.ws``` folder.

The class based controllers that you register into the app must be imported into the ```__init__.py``` file of the ```controller.ws``` module.

The file based that contain your view functions must must also be imported into the ```__init__.py``` file of the ```controller.ws``` module.

## Creating models:


you can create SQLAlchemy models by creating a new module under the ```models.persistent``` module and place each models inside your module that you previously created. 

The models that you register into the app must be an ```database.Model ``` or ```database.get_models_by_name('replace that with your database connection name')``` object, you could import this object using the following line into your database model:


```python
from fastapi_framework_mvc.database import Database
```

All models must be imported inside the ```__init__.py``` of your base module and you must import this module in the ```__init__.py``` of the ```models.persistent``` module


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

* Make sure to have in your __host.json__:

```json
...
  "extensions": {
    "http": { "routePrefix": ""}
  },
...
```

---
# Running on local desktop:

We assume that your system already had python v3+ and pip v3+ installed.
 
installation:
-------------

```bash 
git clone https://github.com/frederickney/fastapi-framework-mvc.git
cd fastapi-framework-mvc
pip3 install .
```

or 
```pip 
pip install fastapi-framework-mvc
```

CLI interface:
--------------

* Powershell

```powershell
fastapi_framework.cli.exe -h
```
* Bash

```bash
fastapi_framework.cli -h
```

* Python module

```bash
python -m fastapi_framework_mvc.cli -h
```


Create a new project:
------------------------

* Powershell:

```powershell
fastapi_framework.cli.exe -cp <your project>
```

or

```bash
fastapi_framework_mvc.cli.exe --create-project <your project>
```

* Bash:

```bash
fastapi_framework.cli -cp <your project>
```
or

```bash
fastapi_framework_mvc.cli --create-project <your project>
```

* Python module:

```bash
python -m fastapi_framework_mvc.cli -cp <your project>
```

or

```bash
python -m fastapi_framework_mvc.cli --create-project <your project>
```

A project can also be packaged and later used by the framework in order to do so, you need to create a 
__pyproject.toml__ that will build your project into a python package. Best practices ar to put the __pyproject.toml__ 
in the parent directory of your created project.

Then you will still have to create a __server__ pathon module 
(and a __models.persistent__ python module if using database connection(s)).

In the __server__ part you will only have to import from your packages the modules under the package server module
within the \_\_init\_\_.py in __server__. example:

```python
# coding: utf-8
#__init__.py

from your_project.server import web, ws, errorhandler, plugins, middleware, socket
```


or if you want multiples application packaged, you will have to create the same python module  __server__ arborescence
as the one initially on your project but instead of rewriting the routes or loading the routers, you can just for example:

```python
# coding: utf-8
# example with two project on the ws.py file
import your_first_project.server.ws
import your_second_project.server.ws


class Route(object):
    """
    Class that will configure all ws services based routes for the server
    """
    def __init__(self, server):
        """
        Constructor
        :param server: FastAPI instance
        :type server: fastapi.FastAPI
        :return: Route object
        """
        your_first_project.server.ws.Route(server)
        your_second_project.server.ws.Route(server)
        return

```

In the __models.persistent__ part you will only have to import from your packages the modules under the package models.persistent module
within the \_\_init\_\_.py in __models.persistent__. example:

```python
# coding: utf-8
#__init__.py

from your_project.models.persistent import *

```

or if you want multiples application packaged, and have one or many model declaration conflicts.

```python
# coding: utf-8
# example with two project on the __init__.py file
from your_first_project.models import persistent as  your_first_project # or any other identifier
from your_second_project.models import persistent as  your_second_project # or any other identifier
```

When the project is created, more command can be used when the env __"CONFIG_FILE"__ is set and can be run through

* Powershell:
```powershell
fastapi_framework_mvc.app.exe
```

* Bash:
```bash
fastapi_framework_mvc.app
```

* Python module:
```bash
python -m fastapi_framework_mvc.app
```
see -h for usages

---

# Launching

* On every startup

Linux/Mac:
```bash 
export CONFIG_FILE=config/config.yml
```

Windows:
```powershell
$env:CONFIG_FILE = "C:\Users\Z01FNEY\PycharmProjects\fastapi-framework-mvc\test\config\config.yml"
```

* Starting using fastapi

In dev mode:

```bash
# needs app.py in your current working directory.
python -m fastapi dev
```

In standalone mode:

```bash
# needs app.py in your current working directory.
python -m fastapi run
```
app.py example [here](app.py)

* Starting the fastapi server in standalone

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
