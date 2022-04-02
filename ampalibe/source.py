env = """# PAGE ACCESS TOKEN 
export AMP_ACCESS_TOKEN=

# PAGE VERIF TOKEN
export AMP_VERIF_TOKEN= 


# DATABASE AUTHENTIFICATION
export ADAPTER=SQLITE
#export ADAPTER=MYSQL

####### CASE MYSQL ADAPTER
export DB_HOST=
export DB_USER=
export DB_PASSWORD=
export DB_NAME=
export DB_PORT=3306

####### CASE SQLITE ADAPTER
export DB_FILE=ampalibe.db

# APPLICATION CONFIGURATION
export AMP_HOST=0.0.0.0
export AMP_PORT=4555

# URL APPLICATION
export AMP_URL=
"""

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

:: URL APPLICATION
set AMP_URL=
"""
core = """import ampalibe
from conf import Configuration

bot = ampalibe.init(Configuration())

# create a get started option to get permission of user.
# bot.chat.get_started()

@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    '''
    main function where messages received on
    the facebook page come in.

    @param sender_id String: 
        sender facebook id
    @param cmd String: 
        message content
    @param extends Dict: 
        contain list of others
            data sent by facebook (sending time, ...)
            data sent by your payload if not set in parameter
    '''
    
    bot.chat.send_message(sender_id, "Hello, Ampalibe")
    """


conf = """from os import environ as env


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
    APP_URL = env.get('AMP_URL')
"""



