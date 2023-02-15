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

MODELS = """from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class AmpUser(SQLModel, table=True):
    __tablename__: str = "amp_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=50, unique=True, nullable=False)
    action: Optional[str] = None
    last_use: datetime = Field(default=datetime.now(), nullable=False, index=True)
    lang: Optional[str] = Field(min_length=2, max_length=3)
"""

RESOURCES = '''from models import AmpUser
from ampalibe import __version__, __author__

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from ampalibe.admin import ModelView
from ampalibe.admin import CustomView


class AmpUserView(ModelView):
    """
    class extends ModelView is used to have a crud in the admin panel for model specified
    """

    fields = ["user_id", "action", "last_use", "lang"]

    def __init__(self):
        super().__init__(label="Ampalibe Users", icon="fa fa-users", model=AmpUser)


class OtherView(CustomView):
    """
    class extends CustomView is used to have a custom view in the admin panel
    """

    def __init__(self):
        super().__init__(label="Other", icon="fa fa-other", path="/other")

    async def render(self, request: Request, templates: Jinja2Templates):
        data = {"request": request, "version": __version__, "author": __author__}
        return templates.TemplateResponse("other.html", data)
'''


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
