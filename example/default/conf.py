from os import environ as env


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

    APP_HOST = env.get('AMP_HOST', '0.0.0.0')
    APP_PORT = int(env.get('AMP_PORT', 4555))
    APP_URL = env.get('AMP_URL')

    WORKERS = env.get('WORKERS', 1)

