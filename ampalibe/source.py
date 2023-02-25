ENV = """# PAGE ACCESS TOKEN 
export AMP_ACCESS_TOKEN=

# PAGE VERIF TOKEN
export AMP_VERIF_TOKEN= 


# DATABASE AUTHENTIFICATION
export ADAPTER=SQLITE
#export ADAPTER=MYSQL
#export ADAPTER=POSTGRESQL
#export ADAPTER=MONGODB

####### CASE MYSQL, POSTGRESQL OR MONGODB ADAPTER
export DB_HOST=
export DB_USER=
export DB_PASSWORD=
export DB_NAME=
#export DB_PORT=
#export SRV_PROTOCOL=1

####### CASE SQLITE ADAPTER
export DB_FILE=ampalibe.db


# APPLICATION CONFIGURATION
export AMP_HOST=0.0.0.0
export AMP_PORT=4555

# URL APPLICATION
export AMP_URL=

# ENABLE ADMIN
#export ADMIN_ENABLE=1
"""

ENV_CMD = """:: PAGE ACCESS TOKEN 
set AMP_ACCESS_TOKEN=

:: PAGE VERIF TOKEN
set AMP_VERIF_TOKEN= 

:: DATABASE AUTHENTIFICATION
set ADAPTER=SQLITE
:: set ADAPTER=MYSQL
:: set ADAPTER=POSTGRESQL
:: set ADAPTER=MONGODB

::::: CASE MYSQL, POSTGRESQL OR MONGODB ADAPTER
set DB_HOST=
set DB_USER=
set DB_PASSWORD=
set DB_NAME=
:: set DB_PORT=
:: set SRV_PROTOCOL=1

:: CASE SQLITE ADAPTER
set DB_FILE=ampalibe.db


:: APPLICATION CONFIGURATION
set AMP_HOST=0.0.0.0
set AMP_PORT=4555

:: URL APPLICATION
set AMP_URL=

:: ENABLE ADMIN 
:: set ADMIN_ENABLE=1

"""

CORE = """import ampalibe
from ampalibe import Messenger

chat = Messenger()

# create a get started option to get permission of user.
# chat.get_started()

@ampalibe.command('/')
def main(sender_id, cmd, **ext):
    '''
    main function where messages received on
    the facebook page come in.

    @param sender_id String: 
        sender facebook id
    @param cmd String: 
        message content
    @param ext Dict: 
        contain list of others
            data sent by facebook (sending time, ...)
            data sent by your payload if not set in parameter
    '''
    
    chat.send_text(sender_id, "Hello, Ampalibe")
    """

CONF = """from os import environ as env


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
    DB_PORT = env.get('DB_PORT')
    DB_NAME = env.get('DB_NAME')
    SRV_PROTOCOL = env.get('SRV_PROTOCOL')

    ACCESS_TOKEN = env.get('AMP_ACCESS_TOKEN')
    VERIF_TOKEN = env.get('AMP_VERIF_TOKEN')

    APP_HOST = env.get('AMP_HOST', '0.0.0.0')
    APP_PORT = int(env.get('AMP_PORT', 4555))
    APP_URL = env.get('AMP_URL')
    ADMIN_ENABLE = env.get('ADMIN_ENABLE')
    
"""

LANGS = """{
    "hello_world": {
        "en": "Hello World",
        "fr": "Bonjour le monde"
    },

    "ampalibe": {
        "en": "Jackfruit", 
        "fr": "Jacquier",
        "mg": "Ampalibe"
    }
}
"""

MODELS = """from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class AmpalibeUser(SQLModel, table=True):
    __tablename__: str = "amp_user"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=50, unique=True, nullable=False)
    action: Optional[str] = None
    last_use: datetime = Field(default=datetime.now(), nullable=False, index=True)
    lang: Optional[str] = Field(min_length=2, max_length=3)
"""

RESOURCES = """from sqladmin import ModelView
from models import AmpalibeUser
from ampalibe import __version__, __author__
from sqladmin import BaseView, expose

#  Declare here all class ofModelView or BaseView to put in Admin dahsboard


'''
Example CRUD for a table
'''
class UserAmpalibe(ModelView, model=AmpalibeUser):
    name = "Ampalibe User"
    icon = "fa-solid fa-user"
    column_list = [
        AmpalibeUser.user_id,
        AmpalibeUser.action,
        AmpalibeUser.last_use,
        AmpalibeUser.lang,
    ]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True


'''
This is example of custom page you can make in your admin page
'''
class OtherView(BaseView):
    name = "Other Page"
    icon = "fa-solid fa-list-alt"

    @expose("/other", methods=["GET"])
    def other_page(self, request):
        return self.templates.TemplateResponse(
            "other.html",
            context={"request": request, "version": __version__, "author": __author__},
        )
"""

OTHER_HTML = """
{% extends "layout.html" %}
{% block content %}
    <div>
        <h1 style="text-align: center ;">
            Custom Admin Page for Ampalibe {{ version }} authored by {{ author }}
        </h1>
    </div>
{% endblock %}
"""
