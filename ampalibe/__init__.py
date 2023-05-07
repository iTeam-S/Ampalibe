import os
import sys
import time
import inspect
import colorama
import tempfile
from . import source

__version__ = "1.1.9"
__author__ = "iTeam-$"


colorama.init()


def typing_print(text):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.02)
    print()


def create_env(path):
    if sys.platform == "win32":
        print(source.ENV_CMD, file=open(f"{path}/.env.bat", "w"))
    else:
        print(source.ENV, file=open(f"{path}/.env", "w"))
    typing_print("~\033[32m 👌 \033[0m | Env file created")


def create_lang(path):
    print(source.LANGS, file=open(f"{path}/langs.json", "w"))
    typing_print("~\033[32m 👌 \033[0m | Langs file created")


def init_proj(path):
    create_env(path)
    create_lang(path)
    print(source.CORE, file=open(f"{path}/core.py", "w"))
    typing_print("~\033[32m 👌 \033[0m | Core file created")

    print(source.CONF, file=open(f"{path}/conf.py", "w"))
    typing_print("~\033[32m 👌 \033[0m | Config file created")

    for folder in {"public", "private"}:
        os.makedirs(os.path.join(path, "assets", folder), exist_ok=True)

    print(
        ".env\n.env.bat\n__pycache__/\nngrok\nngrok.exe\n_db.json",
        file=open(f"{path}/.gitignore", "a"),
    )

    print(
        "ampalibe",
        file=open(f"{path}/requirements.txt", "a"),
    )


if sys.argv[0] == "-m" and len(sys.argv) > 1:
    if sys.argv[1] == "version":
        typing_print("\033[32m" + __version__ + " ⭐ \033[0m")

    elif sys.argv[1] == "init":
        typing_print("~\033[32m 👌 \033[0m | Initiating  ...")
        init_proj(".")
        typing_print(
            inspect.cleandoc(
                """
                ~\033[32m 👌 \033[0m | Project Ampalibe initiated. \033[32mYoupii !!! 😎 \033[0m
                ~\033[36m TIPS\033[0m |\033[0m Fill in .env file.
                ~\033[36m TIPS\033[0m |\033[36m ampalibe run\033[0m for lauching project.
            """
            )
        )

    elif sys.argv[1] == "create":
        proj_name = sys.argv[2]
        typing_print(f"~\033[32m 👌 \033[0m | Creating {proj_name} ...")
        os.makedirs(proj_name)
        init_proj(proj_name)
        typing_print(
            inspect.cleandoc(
                f"""
                ~\033[32m 👌 \033[0m | Project Ampalibe created. \033[32mYoupii !!! 😎 \033[0m
                ~\033[36m TIPS\033[0m |\033[0m Fill in .env file.
                ~\033[36m TIPS\033[0m |\033[36m cd {proj_name} && ampalibe run\033[0m for lauching project.
            """
            )
        )

    elif sys.argv[1] == "env":
        create_env(".")

    elif sys.argv[1] == "lang":
        create_lang(".")

    elif sys.argv[1] == "run":
        print(
            inspect.cleandoc(
                "\033[36m"
                + r"""
                                                                0o
                                                                Oo
                                                                coooool
                                                               looooooool
                                                              loooooooooool
            _    __  __ ____   _    _     ___ ____  _____     looooooooooool
           / \  |  \/  |  _ \ / \  | |   |_ _| __ )| ____|    looooooooooool
          / _ \ | |\/| | |_) / _ \ | |    | ||  _ \|  _|       loooooooooool
         / ___ \| |  | |  __/ ___ \| |___ | || |_) | |___        looooooool
        /_/   \_\_|  |_|_| /_/   \_\_____|___|____/|_____|         oooooo
        """
                + "\033[0m"
            )
        )
        typing_print(
            "~\033[32m 👌\033[0m | Env Loaded\n~\033[32m 👌\033[0m | Ampalibe"
            " running..."
        )

    elif sys.argv[1] == "usage":
        typing_print(
            inspect.cleandoc(
                """
                    Usage: ampalibe \033[32m { create, init, env, run, version, help } \033[0m
                    ------
                    👉 \033[32m create ... : \033[0m create a new project in a new directory specified
                    👉 \033[32m init: \033[0m create a new project in current dir
                    👉 \033[32m version: \033[0m show the current version
                    👉 \033[32m env: \033[0m generate only a .env file
                    👉 \033[32m lang: \033[0m generate only a langs.json file
                    👉 \033[32m run [--dev]: \033[0m run the server, autoreload if --dev is specified
                    👉 \033[32m help: \033[0m show this current help
                """
            )
        )

    sys.exit(0)

try:
    from conf import Configuration  # type: ignore
except ImportError:
    dir_tmp = os.path.join(tempfile.gettempdir(), "ampalibe_temp")
    os.makedirs(dir_tmp, exist_ok=True)
    with open(os.path.join(dir_tmp, "conf.py"), "w") as f:
        f.write(source.CONF)
    sys.path.insert(0, dir_tmp)
finally:
    from .constant import *
    from .model import Model
    from .logger import Logger
    from aiocron import crontab
    from .payload import Payload
    from .messenger import Messenger
    from .core import webserver, Init as init
    from .utils import translate, download_file, simulate
    from .decorators import (
        event,
        action,
        command,
        before_receive,
        after_receive,
    )
