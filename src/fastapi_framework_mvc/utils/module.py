# coding: utf-8


__author = "Frederick NEY"

import os
import logging
import shutil

from fastapi_framework_mvc.exceptions.runtime import web_denied
from . import templates


@web_denied
def create_dir(basepath, dir):
    if not os.path.exists(os.path.join(basepath, dir)):
        logging.debug(f'Creating {dir}...')
        os.mkdir(os.path.join(basepath, dir), 0o755)
        while not os.path.exists(os.path.join(basepath, dir)):
            ("Waiting for path creation")


@web_denied
def create_project(basepath, project):
    if not os.path.exists(os.path.join(basepath, project)):
        create_dir(basepath, project)
    create_dir(os.path.join(basepath, project), 'controllers')
    generate(os.path.join(basepath, project), "{}/{}".format('controllers', 'web'))
    generate(os.path.join(basepath, project), "{}/{}".format('controllers', 'ws'))
    create_dir(os.path.join(basepath, project), 'server')
    generate(os.path.join(basepath, project), "{}/{}".format('server', 'web'))
    generate(os.path.join(basepath, project), "{}/{}".format('server', 'ws'))


@web_denied
def generate(basepath, module, sub_module=None, skip_root_level_init=False):
    if not os.path.exists(os.path.join(basepath, os.path.dirname(module))):
        generate(
            basepath, "/".join([module.split('/')[i] for i in range(0, len(module.split('/')) - 1)]), 
            module.split('/')[-1],
            skip_root_level_init=skip_root_level_init
        )
        if sub_module is not None:
            logging.debug(f'Generating {module}...')
            os.mkdir(os.path.join(basepath, module), 0o755)
            while not os.path.exists(os.path.join(basepath, module)):
                "Waiting for path creation"
    if not os.path.exists(os.path.join(basepath, module)):
        if sub_module is not None:
            logging.debug(f'Generating {module}...')
            os.mkdir(os.path.join(basepath, module), 0o755)
            while not os.path.exists(os.path.join(basepath, module)):
                "Waiting for path creation"
    if sub_module is not None:
        if os.path.exists(os.path.join(os.path.join(basepath, os.path.dirname(module)), '__init__.py')):
            logging.debug(f'Updating {os.path.dirname(os.path.dirname(module))}/__init__.py...')
            fp = open(
                os.path.join(os.path.join(basepath, os.path.dirname(module)), '__init__.py'),
                "a"
            )
            fp.write(templates.IMPORTS.format(os.path.basename(module)))
            fp.close()
        else:
            logging.debug(f'Generating { os.path.dirname(module)}/__init__.py...')
            fp = open(
                os.path.join(os.path.join(basepath, os.path.dirname(module)), '__init__.py'),
                "w"
            )
            fp.write(templates.PYTHON_FILE_HEAD)
            fp.write(templates.IMPORTS.format(os.path.basename(module)))
            fp.close()
    elif not skip_root_level_init:
        if not os.path.exists(
                os.path.join(os.path.join(basepath, os.path.dirname(module)), '__init__.py')
        ):
            logging.debug(f'Generating {os.path.dirname(module)}/__init__.py...')
            fp = open(
                os.path.join(os.path.join(basepath, os.path.dirname(module)), '__init__.py'),
                "w"
            )
            fp.write(templates.PYTHON_FILE_HEAD)
            fp.close()


@web_denied
def try_copy(src, dst):
    """

    :param src:
    :param dst:
    :return:
    """
    if not os.path.exists(dst):
        shutil.copytree(src, dst)


@web_denied
def try_create_errors(path):
    pass


@web_denied
def try_create_entry(path, entry):
    if os.path.exists(os.path.join(path, 'server')):
        if not os.path.exists(os.path.join(os.path.join(path, 'server'), '{}.py'.format(entry))):
            fp = open(os.path.join(os.path.join(path, 'server'), '{}.py'.format(entry)), 'w')
            fp.write(templates.HTTP_ENTRY.format(entry))
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '__init__.py'), 'a')
            fp.write(templates.IMPORTS.format(entry))
            fp.close()


@web_denied
def try_create_web_entry(path):
    if os.path.exists(os.path.join(path, 'server')):
        if not os.path.exists(os.path.join(os.path.join(path, 'server'), '{}.py'.format('web'))):
            generate(path, 'controllers/web/home')
            fp = open(os.path.join(path, '{}.py'.format('controllers/web/home')), 'w')
            fp.write(templates.PYTHON_FILE_HEAD)
            fp.write(templates.FASTAPI_RENDERING_IMPORT)
            fp.write(templates.BASE_HOME_CONTROLLER.format('welcome'))
            fp.close()
            fp = open(
                os.path.join(
                    os.path.dirname(os.path.join(path, '{}.py'.format('controllers/web/home'))),
                    "__init__.py"
                ),
                'a'
            )
            fp.write(templates.IMPORT_CONTROLLER.format('home', 'home'))
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '{}.py'.format('web')), 'w')
            fp.write(templates.HTTP_DEFAULT_ENTRY.format('web'))
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '__init__.py'), 'a')
            fp.write(templates.IMPORTS.format('web'))
            fp.close()


@web_denied
def try_create_error_controller(path):
    if os.path.exists(os.path.join(path, 'server')):
        if not os.path.exists(os.path.join(os.path.join(path, 'server'), '{}.py'.format('errorhandler'))):
            content = ''
            for code, error in templates.HTTP_ERRORS.items():
                generate(path, error.replace('.', '/'))
                content += templates.ERROR_ENTRY.format(code, error)
                fp = open(os.path.join(path, '{}.py'.format(error.replace('.', '/'))), 'w')
                fp.write(templates.PYTHON_FILE_HEAD)
                fp.write(templates.FASTAPI_RENDERING_IMPORT)
                fp.write(templates.BASE_ERROR.format(code, code))
                fp.close()
                fp = open(
                    os.path.join(
                        os.path.dirname(os.path.join(path, '{}.py'.format(error.replace('.', '/')))),
                        "__init__.py"
                    ),
                    'a'
                )
                fp.write(templates.IMPORT_ERROR.format(os.path.basename(error.replace('.', '/')), code))
                fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '{}.py'.format('errorhandler')), 'w')
            fp.write(templates.HTTP_ERROR_HANDLER_ENTRY.format(content))
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '__init__.py'), 'a')
            fp.write(templates.IMPORTS.format('errorhandler'))
            fp.close()
    pass


@web_denied
def try_create_ws_entry(path):
    try_create_entry(path, 'ws')


@web_denied
def try_create_default_conf(path, project):
    if not os.path.exists(os.path.join(path, 'config')):
        os.mkdir(os.path.join(path, 'config'), 0o755)
    if not os.path.exists(os.path.join(os.path.join(path, 'config'), 'config.yml')):
        fp = open(os.path.join(os.path.join(path, 'config'), 'config.yml'), 'w')
        fp.write(templates.FASTAPI_FRAMEWORK_BASE_CONF)
        fp.close()

def try_create_fastapi_entrypoint(path):
    if not os.path.exists(os.path.join(path, 'app.py')):
        fd = open(os.path.join(path, 'app.py'), 'w')
        fd.write(templates.FASTAPI_APP)
        fd.close()

@web_denied
def try_create_socket_entry(path):
    if os.path.exists(os.path.join(path, 'server')):
        if not os.path.exists(os.path.join(os.path.join(path, 'server'), '{}.py'.format('socket'))):
            fp = open(os.path.join(os.path.join(path, 'server'), '{}.py'.format('socket')), 'w')
            fp.write(templates.WS_ENTRY)
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '__init__.py'), 'a')
            fp.write(templates.IMPORTS.format('socket'))
            fp.close()


@web_denied
def try_create_plugins_entry(path):
    if os.path.exists(os.path.join(path, 'server')):
        if not os.path.exists(os.path.join(os.path.join(path, 'server'), '{}.py'.format('plugins'))):
            fp = open(os.path.join(os.path.join(path, 'server'), '{}.py'.format('plugins')), 'w')
            fp.write(templates.PLUGINS_ENTRY)
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '__init__.py'), 'a')
            fp.write(templates.IMPORTS.format('plugins'))
            fp.close()


@web_denied
def try_create_middleware_entry(path):
    if os.path.exists(os.path.join(path, 'server')):
        if not os.path.exists(os.path.join(os.path.join(path, 'server'), '{}.py'.format('middleware'))):
            fp = open(os.path.join(os.path.join(path, 'server'), '{}.py'.format('middleware')), 'w')
            fp.write(templates.MIDDLEWARE_ENTRY)
            fp.close()
            fp = open(os.path.join(os.path.join(path, 'server'), '__init__.py'), 'a')
            fp.write(templates.IMPORTS.format('middleware'))
            fp.close()


@web_denied
def create_server(project, path, _inst_dir):
    if not os.path.exists(os.path.join(path, 'server')):
        create_dir(path, 'server')
    if not os.path.exists(os.path.join(os.path.join(path, 'server'), '__init__.py')):
        fp = open(
            os.path.join(os.path.join(path, 'server'), '__init__.py'),
            "w"
        )
        fp.write(templates.PYTHON_FILE_HEAD)
        fp.close()
    try_create_errors(path)
    try_create_error_controller(path)
    try_create_web_entry(path)
    try_create_ws_entry(path)
    try_create_socket_entry(path)
    try_create_plugins_entry(path)
    try_create_middleware_entry(path)
    try_create_default_conf(path, project)


@web_denied
def create_fastapi_entrypoint(path):
    try_create_fastapi_entrypoint(path)
