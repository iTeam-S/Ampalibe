env = """### PAGE ACCESS TOKEN 
AMP_VERIF_TOKEN=

### PAGE VERIF TOKEN
AMP_VERIF_TOKEN= 

### DATABASE AUTHENTIFICATION
DB_HOST=
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_PORT=3306

### APPLICATION CONFIGURATION
AMP_HOST=0.0.0.0
AMP_PORT=4555"""


server = """import core
core.ampalibe.run(core.Configuration())
"""


core = """import ampalibe
from conf import Configuration

'''
    Principal fonction, où les messages réçu sur
    la page facebook rentrent.

    @param user_id: identifiant facebook de l'exp.
    @param cmd: message de la personne.
    @param extends: contiennent la liste des autres
        données envoyé par facebook (heure d'envoi, ...)
'''
req = ampalibe.Req(Configuration())
bot = ampalibe.Messenger(Configuration.ACCESS_TOKEN)


@ampalibe.commande('/')
def main(sender_id, cmd, **extends):
    print("Hello World")"""


conf = """from os import environ as env
from dotenv import load_dotenv

# Charge tous les variables dans le fichier .env
load_dotenv()


class Configuration:
    '''
        Recupère la valeur dans l'environnement.
        Prend la valeur par defaut si non definit.
    '''
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