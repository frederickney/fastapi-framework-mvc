# coding: utf-8


__author__ = "Frederick NEY"

import os
import inspect
import importlib

from fastapi_framework_mvc.exceptions.runtime import web_denied
from . import templates
from .module import generate, create_project, create_server, create_fastapi_entrypoint


@web_denied
def make_auth():
    pass


@web_denied
def make_middleware(basepath, middleware):
    if not os.path.exists(os.path.join(os.path.join(basepath, 'server'), 'middleware.py')):
        fp = open(os.path.join(os.path.join(basepath, 'server'), 'middleware.py'), "w")
        fp.write(templates.PYTHON_FILE_HEAD)
    else:
        fp = open(os.path.join(os.path.join(basepath, 'server'), 'middleware.py'), "a")
    fp.write(templates.BASE_MIDDLEWARE.format(middleware))
    fp.close()
    pass


@web_denied
def make_controller(basepath, controller, router=False):
    generate(basepath, controller)
    fp = open(
        os.path.join(os.path.join(basepath, os.path.dirname(controller)), "{}.py".format(os.path.basename(controller))),
        "w"
    )
    if not router:
        fp.write(templates.BASE_CONTROLLER)
    else: 
        fp.write(templates.BASE_ROUTER_CONTROLLER.format(PREFIX=controller.split('/')[-1]))
    fp.close()
    fp = open(
        os.path.join(os.path.join(basepath, os.path.dirname(controller)), '__init__.py'),
        "a"
    )
    if not router:
        fp.write(templates.IMPORT_CONTROLLER.format(
            os.path.basename(controller), os.path.basename(controller)
        ))
    else:
        fp.write(templates.IMPORT_ROUTER_CONTROLLER.format(
            os.path.basename(controller), os.path.basename(controller)
        ))
    fp.close()


@web_denied
def make_project(basepath, project, inst_dir):
    create_project(basepath, project)
    create_server(project, os.path.join(basepath, project), inst_dir)
    create_fastapi_entrypoint(os.path.join(basepath, project))

def _install_router(basepath, controller, type, prefix=None):
    """
    install controllers containing static and class methods
    :param basepath: str path like
    :type basepath: str
    :param controller: str path like
    :type controller: str
    :param type: type of route (web, ws or socket) 
    :type type: str
    """
    fd = open(f'server/{type}.py', 'r')
    content = fd.read() 
    fd.close()
    if content.endswith('return\n'):
        _content = content[:-15]
        _ends = content[-15:]
    else:
        _content = content[:-1]
        _ends = content[-1:]
    if not prefix:
        new_content = f"{_content}{templates.INSTALL_ROUTER.format('server', controller.replace('/', '.'))}{_ends}"
    else:
        new_content = f"{_content}{ templates.INSTALL_PREFIXED_ROUTER.format('server', prefix, controller.replace('/', '.'))}{_ends}"
    fd = open(f'server/{type}.py', 'w')
    fd.write(new_content)
    fd.close()
    pass


def _install_controller(basepath, controller, methods, type):
    """
    install controllers containing static and class methods
    :param basepath: str path like
    :type basepath: str
    :param controller: str path like
    :type controller: str
    :param methods: methods list
    :type methods: list[str]
    :param type: type of route (web, ws or socket) 
    :type type: str
    """
    fd = open(f'server/{type}.py', 'r')
    content = fd.read() 
    fd.close()
    if content.endswith('return\n'):
        _content = content[:-15]
        _ends = content[-15:]
    else:
        _content = content[:-1]
        _ends = content[-1:]
    new_content = f"{_content}"
    for method in methods:
        if type == 'ws':
            new_content += templates.INSTALL_API_ROUTE.format('server', f"{os.path.basename(controller)}/{method}", f"{controller.replace('/', '.')}.{method}", f"{os.path.basename(controller)}.{method}")
        elif type =='socket':
            new_content += templates.INSTALL_WEBSOCKET_ROUTE.format('server', f"{os.path.basename(controller)}/{method}", f"{controller.replace('/', '.')}.{method}", f"{os.path.basename(controller)}.{method}")
        else: 
            new_content += templates.INSTALL_WEB_ROUTE.format('server', f"{os.path.basename(controller)}/{method}", f"{controller.replace('/', '.')}.{method}", f"{os.path.basename(controller)}.{method}")
    if _ends != '\n':
        new_content += f"{_ends}"
    fd = open(f'server/{type}.py', 'w')
    fd.write(new_content)
    fd.close()
    pass


@web_denied
def install_routes(basepath, controller, type, prefix=None):
    import sys
    sys.path.append(basepath)
    if os.path.exists(os.path.join(basepath, os.path.dirname(controller))):
        module = importlib.import_module(controller.replace('/', '.'))
        if 'router' in dir(module):
            #TODO edit server/{type}.py to install router
            _install_router(basepath, controller, type, prefix=prefix)
        elif 'Controller' in dir(module):
            #TODO edit server/{type}.py to install controller by looping on static or class method
            methods = [
                func for func in dir(module.Controller) 
                if ( inspect.isfunction(getattr(module.Controller, func)) or inspect.ismethod(getattr(module.Controller, func))) and not func.startswith('_')
            ]
            _install_controller(basepath, controller, methods, type)
        else: 
            print('Unable to install {} routes'.format(controller))
    else:
        print('Unable to install {} routes'.format(controller))