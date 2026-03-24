#!/usr/bin/python3
# coding: utf-8


__author__ = 'Frederick NEY'

import os

from fastapi_framework_mvc.utils import make_controller, make_middleware, make_project, install_routes


def parser():
    import argparse
    parser = argparse.ArgumentParser(description='FastAPI Framework MVC CLI', formatter_class=argparse.RawTextHelpFormatter)
    action = parser.add_subparsers(dest='action')
    project_parser = action.add_parser('project', help='Usage:\npython -m fastapi_framework_mvc.cli project -h', formatter_class=argparse.RawTextHelpFormatter)
    project_parser.add_argument(
        '-c', '--create', 
        help='name of the project\nExample:\npython -m fastapi_framework_mvc.cli project --create webapp', 
        required=True,
        metavar='NAME'
    )
    controller_parser = action.add_parser('controller', help='Usage:\npython -m fastapi_framework_mvc.cli controller -h', formatter_class=argparse.RawTextHelpFormatter)
    controller_parser.add_argument(
        '-c', '--create', 
        help='Create controller\nexample:\npython -m fastapi_framework_mvc.cli controller --create controllers/web/login', 
        required=True, 
        metavar='NAME'
    )
    controller_parser.add_argument(
        '-router', '--router-mode', 
        help='Create a router base controller', 
        default=False, 
        action='store_true', 
        required=False
    )
    middleware_parser = action.add_parser('middleware', help='Usage:\npython -m fastapi_framework_mvc.cli middleware -h', formatter_class=argparse.RawTextHelpFormatter)
    middleware_parser.add_argument(
        '-c', '--create', 
        help='Create middleware\nexample:\npython -m fastapi_framework_mvc.cli middleware --create my_middleware', 
        required=True, 
        metavar='NAME'
    )
    manager_parser = action.add_parser('manager', help='Usage:\npython -m fastapi_framework_mvc.cli manager -h', formatter_class=argparse.RawTextHelpFormatter)
    manager_parser.add_argument(
        '-l', '--link-controller', 
        help='manage app routes\nexample:\npython -m fastapi_framework_mvc.cli manager --link-controller controllers/web/login', 
        required=True
    )
    manager_parser.add_argument(
        '-p', '--prefix', 
        help='api prefix (only for api endpoints)', 
        required=False,
        default=None
    )
    args = parser.parse_args()
    if args.action == 'project':
        make_project(os.getcwd(), args.create, os.path.dirname(os.path.realpath(__file__)))
        exit(0)
    elif args.action == 'controller':
        make_controller(os.getcwd(), args.create, router=args.router_mode)
        exit(0)
    elif args.action == "middleware":
        make_middleware(os.getcwd(), args.create)
        exit(0)
    elif args.action == "manager":
        install_routes(
            os.getcwd(), 
            args.link_controller, 
            type=
            'ws' if 'controllers/ws/' in args.link_controller else 
            'socket' if 'socket/' in args.link_controller else
            'errorhandler' if 'errors' in args.link_controller else 'web',
            prefix=args.prefix
        )


if __name__ == '__main__':
    parser()
