import sys 
from .source import *

__version__ = '1.0.8-alpha-dev'
__author__ = 'iTeam-$'


def create_files(path):
    print(core, file=open(f'{path}/core.py', 'w'))
    print(conf, file=open(f'{path}/conf.py', 'w'))
    if sys.platform == 'win32':
        print(env_cmd, file=open(f'{path}/.env.bat', 'w'))
    else:
        print(env, file=open(f'{path}/.env', 'w'))


if sys.argv[0] == '-m' and len(sys.argv) > 1:
    if sys.argv[1] == 'version':
        print(__version__)
    elif sys.argv[1] == 'init':
        create_files('.')
    elif sys.argv[1] == 'create':
        create_files(sys.argv[2])
    sys.exit(0)
       

from .model import Model
from aiocron import crontab
from .messenger import Messenger
from .core import webserver, Extra as init
from .utils import action, command, Payload
from .utils import translate, download_file, simulate

