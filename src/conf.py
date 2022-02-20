from os import environ as env
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
