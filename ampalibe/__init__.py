import os
import sys
import inspect
import colorama

from .source import *


__version__ = '1.0.8-alpha-dev'
__author__ = 'iTeam-$'


colorama.init()


def create_env(path):
    if sys.platform == 'win32':
        print(env_cmd, file=open(f'{path}/.env.bat', 'w'))
    else:
        print(env, file=open(f'{path}/.env', 'w'))
    print("~\033[32m 👌 \033[0m | Env file created")


def create_lang(path):
    print(langs, file=open(f'{path}/langs.json', 'w'))
    print("~\033[32m 👌 \033[0m | Langs file created")


def init_proj(path):
    create_env(path)
    create_lang(path)
    print(core, file=open(f'{path}/core.py', 'w'))
    print("~\033[32m 👌 \033[0m | Core file created")

    print(conf, file=open(f'{path}/conf.py', 'w'))
    print("~\033[32m 👌 \033[0m | Config file created")

    for folder in {'public', 'private'}:
        os.makedirs(os.path.join(path, folder), exist_ok=True)


if sys.argv[0] == '-m' and len(sys.argv) > 1:
    if sys.argv[1] == 'version':
        print(__version__, " ⭐")

    elif sys.argv[1] == 'init':
        print("~\033[32m 👌 \033[0m | Initiating  ...")
        init_proj('.')
        print(
            inspect.cleandoc('''
                ~\033[32m 👌 \033[0m | Project Ampalibe initiated. \033[32mYoupii !!! 😎 \033[0m
                ~\033[36m TIPS\033[0m |\033[0m Fill in .env file.
                ~\033[36m TIPS\033[0m |\033[36m ampalibe run\033[0m for lauching project.
            ''')
        )

    elif sys.argv[1] == 'create':
        proj_name = sys.argv[2]
        print(f"~\033[32m 👌 \033[0m | Creating {proj_name} ...")
        os.makedirs(proj_name)
        init_proj(proj_name)
        print(
            inspect.cleandoc(f'''
                ~\033[32m 👌 \033[0m | Project Ampalibe created. \033[32mYoupii !!! 😎 \033[0m
                ~\033[36m TIPS\033[0m |\033[0m Fill in .env file.
                ~\033[36m TIPS\033[0m |\033[36m cd {proj_name} && ampalibe run\033[0m for lauching project.
            ''')
        )

    elif sys.argv[1] == 'env':
        create_env(".")

    elif sys.argv[1] == 'lang':
        create_lang(".")

    elif sys.argv[1] == "run":
        print(inspect.cleandoc("""\033[36m
                                                                0o
                                                                Oo
                                                                coooool
                                                               looooooool
                                                              loooooooooool
            _    __  __ ____   _    _     ___ ____  _____     looooooooooool
           / \  |  \/  |  _ \ / \  | |   |_ _| __ )| ____|    looooooooooool
          / _ \ | |\/| | |_) / _ \ | |    | ||  _ \|  _|       loooooooooool
         / ___ \| |  | |  __/ ___ \| |___ | || |_) | |___        looooooool
        /_/   \_\_|  |_|_| /_/   \_\_____|___|____/|_____|         oooooo \033[0m

        ~\033[32m 👌\033[0m | Env Loaded
        ~\033[32m 👌\033[0m | Ampalibe running...
        """), "\n")

    elif sys.argv[1] == "usage":
        print(
            inspect.cleandoc(
                '''
                    Usage: \033[32m ampalibe { create, init, env, run, version, help } \033[0m
                    ------
                    👉 create ...: create a new project in a new directory specified
                    👉 init: create a new project in current dir
                    👉 version: show the current version
                    👉 env: generate only a .env file
                    👉 lang: generate only a langs.json file
                    👉 run [--dev]: run the server, autoreload if --dev is specified
                    help: show this current help
                '''
            )
        )

    sys.exit(0)


from .model import Model  # noqa: E402
from aiocron import crontab  # noqa: E402
from .messenger import Messenger  # noqa: E402
from .core import webserver, Extra as init  # noqa: E402
from .utils import action, command, Payload  # noqa: E402
from .utils import translate, download_file, simulate  # noqa: E402
