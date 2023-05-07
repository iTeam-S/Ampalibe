# pyright: reportGeneralTypeIssues=false

import os
from .payload import Payload
from datetime import datetime
from conf import Configuration  # type: ignore
from tinydb import TinyDB, Query
from tinydb.operations import delete


class DataBaseConfig:
    def standart(self, conf=Configuration):
        """
        function to configure the standart database
        """
        db_conf = {
            "host": conf.DB_HOST,
            "user": conf.DB_USER,
            "password": conf.DB_PASSWORD,
            "database": conf.DB_NAME,
        }
        if conf.DB_PORT:
            db_conf["port"] = conf.DB_PORT
        return db_conf

    def mongodb(self, conf=Configuration):
        """
        function to configure the mongodb database
        """

        url = "mongodb"
        if hasattr(conf, "SRV_PROTOCOL"):
            url += "+srv://" if not conf.SRV_PROTOCOL else "://"

        if conf.DB_USER and conf.DB_PASSWORD:
            url += f"{conf.DB_USER}:{conf.DB_PASSWORD}@"

        url += conf.DB_HOST

        if conf.DB_PORT:
            url += f":{str(conf.DB_PORT)}/"

        return url


class Model:
    """
    Object for interact with database with pre-defined function
    """

    def __init__(self, conf=Configuration, init=True):
        """
        object to interact with database

        @params: conf [ Configuration object ]
        @return: Request object
        """
        if not init:
            return
        self.ADAPTER = conf.ADAPTER

        if self.ADAPTER in ("MYSQL", "POSTGRESQL"):
            self.DB_CONF = DataBaseConfig().standart(conf)
        elif self.ADAPTER == "MONGODB":
            self.DB_CONF = DataBaseConfig().mongodb(conf)
        else:  # SQLite is choosen by default
            self.DB_CONF = conf.DB_FILE

        self.__connect()
        self.__init_db()
        os.makedirs("assets/private/", exist_ok=True)
        self.tinydb = TinyDB("assets/private/_db.json")

    def __connect(self):
        """
        The function which connect object to the database.
        """
        if self.ADAPTER == "MYSQL":
            try:
                import mysql.connector
            except ImportError:
                raise ImportError(
                    "You must install mysql-connector to use mysql database: pip install mysql-connector"
                )
            self.db = mysql.connector.connect(**self.DB_CONF)

        elif self.ADAPTER == "POSTGRESQL":
            try:
                import psycopg2
            except ImportError:
                raise ImportError(
                    "You must install psycopg2 to use postgresql database: pip install psycopg2"
                )
            self.db = psycopg2.connect(**self.DB_CONF)

        elif self.ADAPTER == "MONGODB":
            try:
                import pymongo
            except ImportError:
                raise ImportError(
                    "You must install pymongo to use mongodb database: pip install pymongo"
                )
            self.db = pymongo.MongoClient(self.DB_CONF)
            self.db = self.db[Configuration.DB_NAME]
            return  # no cursor for mongodb

        else:
            import sqlite3

            self.db = sqlite3.connect(
                self.DB_CONF,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )

        self.cursor = self.db.cursor()

    def __init_db(self):
        """
        Creation of table if not exist
        Check the necessary table if exists
        """

        if self.ADAPTER == "MYSQL":
            req = """
                CREATE TABLE IF NOT EXISTS `amp_user` (
                    `id` INT NOT NULL AUTO_INCREMENT,
                    `user_id` varchar(50) NOT NULL UNIQUE,
                    `action` TEXT DEFAULT NULL,
                    `last_use` datetime NOT NULL DEFAULT current_timestamp(),
                    `lang` varchar(5) DEFAULT NULL,
                    PRIMARY KEY (`id`),
                    INDEX (last_use)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        elif self.ADAPTER == "POSTGRESQL":
            req = """
                CREATE TABLE IF NOT EXISTS amp_user (
                    id SERIAL PRIMARY KEY,
                    user_id VARCHAR UNIQUE NOT NULL,
                    action TEXT DEFAULT NULL,
                    last_use TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    lang VARCHAR DEFAULT NULL
                );
                CREATE INDEX IF NOT EXISTS last_use_index ON amp_user(last_use);
            """
        elif self.ADAPTER == "MONGODB":
            if "amp_user" not in self.db.list_collection_names():
                self.db.create_collection("amp_user")
                # self.db.amp_user.create_index("user_id", unique=True)
            return
        else:
            req = """
               CREATE TABLE IF NOT EXISTS amp_user (
                   id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   user_id TEXT NOT NULL UNIQUE,
                   action TEXT,
                   last_use TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   lang TEXT
                )
            """
        self.cursor.execute(req)
        self.db.commit()

    def verif_db(fonction):  # type: ignore
        """
        decorator that checks if the database
        is connected or not before doing an operation.
        """

        def trt_verif(*arg, **kwarg):
            arg[0].__connect()
            return fonction(*arg, **kwarg)

        return trt_verif

    @verif_db
    def _verif_user(self, user_id):
        """
        method to insert new user and/or update the date
        of last use if the user already exists.

        @params :  user_id

        """
        SQL_MAP = {
            "MYSQL": "INSERT INTO amp_user(user_id) VALUES (%s) ON DUPLICATE KEY UPDATE last_use = NOW();",
            "POSTGRESQL": "INSERT INTO amp_user(user_id) VALUES (%s) ON CONFLICT (user_id) DO UPDATE SET last_use = NOW();",
            "SQLITE": "INSERT INTO amp_user(user_id) VALUES (?) ON CONFLICT(user_id) DO UPDATE SET last_use = CURRENT_TIMESTAMP;",
        }

        if self.ADAPTER == "MONGODB":
            self.db.amp_user.update_one(
                {"user_id": user_id},
                {"$set": {"last_use": datetime.now()}},
                upsert=True,
            )
        else:
            sql = SQL_MAP.get(self.ADAPTER)
            self.cursor.execute(sql, (user_id,))
            self.db.commit()

    @verif_db
    def get_action(self, sender_id):
        """
        get current action of an user

         @params :  sender_id
         @return : current action [ type of String/None ]
        """
        return self.get(sender_id, "action")[0]

    @verif_db
    def set_action(self, sender_id, action):
        """
        define a current action if an user

        @params :  sender_id, action
        @return:  None
        """
        if isinstance(action, Payload):
            action = Payload.trt_payload_out(action)

        if self.ADAPTER in ("MYSQL", "POSTGRESQL"):
            req = "UPDATE amp_user set action = %s WHERE user_id = %s"
        elif self.ADAPTER == "MONGODB":
            self.db.amp_user.update_one(
                {"user_id": sender_id},
                {"$set": {"action": action}},
            )
            return
        else:
            req = "UPDATE amp_user set action = ? WHERE user_id = ?"
        self.cursor.execute(req, (action, sender_id))
        self.db.commit()

    @verif_db
    def set_temp(self, sender_id, key, value):
        """
        set a temp parameter of an user

         @params:  sender_id
         @return:  None
        """
        if self.ADAPTER == "MONGODB":
            self.db.amp_user.update_one(
                {"user_id": sender_id},
                {"$set": {key: value}},
            )
            return
        if not self.tinydb.update({key: value}, Query().user_id == sender_id):
            self.tinydb.insert({"user_id": sender_id, key: value})

    @verif_db
    def get_temp(self, sender_id, key):
        """
        get one temporary data of an user

        @parmas :  sender_id
                   key
        @return: data
        """
        if self.ADAPTER == "MONGODB":
            return self.db.amp_user.find({"user_id": sender_id})[0].get(key)

        res = self.tinydb.search(Query().user_id == sender_id)
        if res:
            return res[0].get(key)

    @verif_db
    def del_temp(self, sender_id, key):
        """
        delete temporary parameter of an user

        @parameter :  sender_id
                      key
        @return: None
        """
        if self.ADAPTER == "MONGODB":
            self.db.amp_user.update_one(
                {"user_id": sender_id},
                {"$unset": {key: ""}},
            )
            return
        self.tinydb.update(delete(key), Query().user_id == sender_id)

    @verif_db
    def get_lang(self, sender_id):
        """
        get current lang of an user

        @params: sender_id
        @return lang or None
        """
        return self.get(sender_id, "lang")[0]

    @verif_db
    def set_lang(self, sender_id, lang):
        """
        define a current lang for an user

        @params :  sender_id
        @return:  None
        """
        if self.ADAPTER in ("MYSQL", "POSTGRESQL"):
            req = "UPDATE amp_user set lang = %s WHERE user_id = %s"
        elif self.ADAPTER == "MONGODB":
            self.db.amp_user.update_one(
                {"user_id": sender_id},
                {"$set": {"lang": lang}},
            )
            return
        else:
            req = "UPDATE amp_user set lang = ? WHERE user_id = ?"
        self.cursor.execute(req, (lang, sender_id))
        self.db.commit()

    @verif_db
    def get(self, sender_id, *args):
        """
        get specific data of an user

        @params :  sender_id, list of data to get
        @return:  list of data
        """
        if self.ADAPTER in ("MYSQL", "POSTGRESQL"):
            req = f"SELECT {','.join(args)} FROM amp_user WHERE user_id = %s"
        elif self.ADAPTER == "MONGODB":
            data = self.db.amp_user.find({"user_id": sender_id})[0]
            return [data.get(k) for k in args]
        else:
            req = f"SELECT {','.join(args)} FROM amp_user WHERE user_id = ?"
        self.cursor.execute(req, (sender_id,))
        return self.cursor.fetchone() or (None, None)
