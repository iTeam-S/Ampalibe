env = """# PAGE ACCESS TOKEN 
AMP_ACCESS_TOKEN=

# PAGE VERIF TOKEN
AMP_VERIF_TOKEN= 


# DATABASE AUTHENTIFICATION
ADAPTER=SQLITE
# ADAPTER=MYSQL

####### CASE MYSQL ADAPTER
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=3306

####### CASE SQLITE ADAPTER
DB_FILE=ampalibe.db

# APPLICATION CONFIGURATION
AMP_HOST=0.0.0.0
AMP_PORT=4555"""

env_cmd = """:: PAGE ACCESS TOKEN 
set AMP_ACCESS_TOKEN=

:: PAGE VERIF TOKEN
set AMP_VERIF_TOKEN= 

:: DATABASE AUTHENTIFICATION
set ADAPTER=SQLITE
:: ADAPTER=MYSQL

::::: CASE MYSQL ADAPTER
set DB_HOST=
set DB_USER=
set DB_PASSWORD=
set DB_NAME=
set DB_PORT=3306

:: CASE SQLITE ADAPTER
set DB_FILE=ampalibe.db


:: APPLICATION CONFIGURATION
set AMP_HOST=0.0.0.0
set AMP_PORT=4555
"""
core = """import ampalibe
from conf import Configuration

'''
    Main function, where messages received on
    the facebook page come in.

    @param user_id: 
        sender facebook id
    @param cmd: 
        message content
    @param extends: 
        contain list of others
        data sent by facebook (sending time, ...)
'''
req = ampalibe.Req(Configuration())
bot = ampalibe.Messenger(Configuration.ACCESS_TOKEN)


@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    print("Hello World")"""


conf = """from os import environ as env
# Charge tous les variables dans le fichier .env


class Configuration:
    '''
        Retrieves the value from the environment.
        Takes the default value if not defined.
    '''
    ADAPTER = env.get('ADAPTER')

    DB_FILE = env.get('DB_FILE')
    
    DB_HOST = env.get('DB_HOST', 'localhost')
    DB_USER = env.get('DB_USER', 'root')
    DB_PASSWORD = env.get('DB_PASSWORD', '')
    DB_PORT = env.get('DB_PORT', 3306)
    DB_NAME = env.get('DB_NAME')

    ACCESS_TOKEN = env.get('AMP_ACCESS_TOKEN')
    VERIF_TOKEN = env.get('AMP_VERIF_TOKEN')

    APP_HOST = env.get('AMP_HOST')
    APP_PORT = int(env.get('AMP_PORT'))
"""