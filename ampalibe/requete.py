import mysql.connector

class Request:
    def __init__(self, conf):
        '''
            Initialisation: Connexion à la base de données
        '''
        self.DB_CONF = {
            'host': conf.DB_HOST,
            'user': conf.DB_USER,
            'password': conf.DB_PASSWORD,
            'database': conf.DB_NAME,
            'port': conf.DB_PORT
        }
        self.__connect()
        self.__init_db()

    def __connect(self):
        self.db = mysql.connector.connect(**self.DB_CONF)
        self.cursor = self.db.cursor()

    def __init_db(self):
        '''
            Creation des tables necessaires à l'applicatifs
        '''
        req = '''
            CREATE TABLE IF NOT EXISTS `amp_user` (
                `id` INT NOT NULL AUTO_INCREMENT,
                `user_id` varchar(50) NOT NULL UNIQUE,
                `action` varchar(50) DEFAULT NULL,
                `last_use` datetime NOT NULL DEFAULT current_timestamp(),
                `lang` varchar(5) DEFAULT NULL,
                `tmp` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        '''
        self.cursor.execute(req)
        self.db.commit()
    
    def verif_db(fonction):
        '''
            Un decorateur de verification de la
            connexion au serveur avant traitement.
        '''
        def trt_verif(*arg, **kwarg):
            if not arg[0].db.is_connected():
                # reconnexion de la base
                try:
                    arg[0].db.reconnect()
                except Exception:
                    arg[0].__connect()
            return fonction(*arg, **kwarg)
        return trt_verif

    @verif_db
    def verif_user(self, user_id):
        '''
            Fonction d'insertion du nouveau utilisateur
            et/ou mise à jour de la date de dernière utilisation.
        '''
        # Insertion dans la base si non present
        # Mise à jour du last_use si déja présent
        req = '''
            INSERT INTO amp_user(user_id) VALUES (%s)
            ON DUPLICATE KEY UPDATE last_use = NOW()
        '''
        self.cursor.execute(req, (user_id,))
        self.db.commit()
    
    @verif_db
    def get_action(self, user_id):
        '''
            Recuperer l'action de l'utilisateur
        '''
        req = 'SELECT action FROM amp_user WHERE user_id = %s'
        self.cursor.execute(req, (user_id,))
        # retourne le resultat
        return self.cursor.fetchone()[0]
    
    @verif_db
    def set_action(self, user_id, action):
        '''
            Definir l'action de l'utilisateur
        '''
        req = 'UPDATE amp_user set action = %s WHERE user_id = %s'
        self.cursor.execute(req, (action, user_id))
        self.db.commit()
