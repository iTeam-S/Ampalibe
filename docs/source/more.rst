Supported Database
=====================

The advantage of using Ampalibe's supported databases is that we can inherit the Model object of ampalibe to make a database request.

We no longer need to make the connection to the database.

we use the instances received from the *Model* object as the variable **db**, **cursor**,

**Example**

``model.py`` file

.. code-block:: python

    from ampalibe import Model

    class Database(Model):
        def __init__(self, conf):
            super().__init__(conf)

        @Model.verif_db
        def get_list_users(self):
            '''
                CREATE CUSTOM method to communicate with database
            '''
            req = "SELECT * from amp_user"
            self.cursor.execute(req)
            data = self.cursor.fetchall()
            self.db.commit()
            return data

``core.py`` file

.. code-block:: python

    import ampalibe
    from conf import Configuration
    from model import Database

    req = Database(Configuration())


    bot = ampalibe.init(Configuration())
    chat = bot.chat


    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
       print(req.get_list_users())


.. important::

    *Model.verif_db* is a decorator who checks that the application is well connected to the database before launching the request.


.. note::
    
    However we can still use other databases than those currently supported




Logging and structure
=====================

Logging
--------

By default, all error in Messenger API methods is showing in output

Messenger API methods response is a request <Response> so we can use it to view the response

.. code-block:: python

    res = chat.send_message(sender_id, "Hello Ampalibe")

    if res.status_code == 200:
        print("OK! NO problem") 
    else:
        print('KO') 
        print(res.text, res.status_code)


Structure
-----------

Each developer is **free to choose the structure he wants**, by just importing the files into the core.py.

We can make our functions everywhere, even as methods

``core.py`` file 

.. code-block:: python

    # importing another file contains ampalibe decorator
    import user
    import ampalibe
    from conf import Configuration
    from ampalibe import Payload

    bot = ampalibe.init(Configuration())
    chat = bot.chat


    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        buttons = [
            {
                "type": "postback",
                "title": "Dashboard",
                "payload": '/login/admin'
            }
        ]
        chat.send_button(sender_id, buttons, 'What do you want to do?')


    class Admin:

        @ampalibe.command('/login/admin')
        def login(sender_id, **extends):
            '''
                function is always calling when payload or message start by /login/admin
            '''
            bot.query.set_action(sender_id, '/get_username')
            bot.chat.send_message(sender_id, 'Enter your username')


``user.py`` file 

.. code-block:: python

    import ampalibe
    from conf import Configuration
    bot = ampalibe.init(Configuration())
    chat = bot.chat


    class User:

        @ampalibe.action('/get_username')
        def username(sender_id, cmd, **extends):
            bot.chat.send_message(sender_id, 'OK ' + cmd)
            bot.query.set_action(sender_id, None)


.. note:: 

    if you want use a MVC Pattern
    
    here is an example of an MVC template that can be used: `Ampalibe MVC Template <https://github.com/gaetan1903/Ampalibe_MVC_Template>`_


Custom endpoint
=================

The web server part and the endpoints are managed directly by Ampalibe

However, a custom end point can be created using the `FastAPI <https://fastapi.tiangolo.com/tutorial/first-steps/>`_ object instance


.. code-block:: python

    import ampalibe
    from ampalibe import webserver
    from conf import Configuration

    bot = ampalibe.init(Configuration())


    @webserver.get('/test')
    def test():
        return 'Hello, test'

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        bot.chat.send_message(sender_id, "Hello, Ampalibe")

    

