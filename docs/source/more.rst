Supported Database
=====================

The advantage of using Ampalibe's supported databases is that we can inherit the Model object of ampalibe to make a database request.

We no longer need to make the connection to the database.

we use the instances received from the *Model* object as the variable **db**, **cursor**,

**Example**

``model.py`` file

.. code-block:: python

    from ampalibe import Model

    class CustomModel(Model):
        def __init__(self):
            super().__init__()

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
    from ampalibe import Messenger
    from model import CustomModel

    chat = Messenger()
    query = CustomModel(Configuration())


    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        # query.set_lang(sender_id, 'en') 
        print(query.get_list_users())


.. important::

    *Model.verif_db* is a decorator who checks that the application is well connected to the database before launching the request.


.. note::
    
    However we can still use other databases than those currently supported




Logging and structure
=====================

Logging
--------
.. image:: https://raw.githubusercontent.com/iTeam-S/Ampalibe/main/docs/source/_static/logger.png

By default, Ampalibe uses the logging module to log the application but with custom formatting,to 
make it easier to read and avoid using print.

Messenger API methods response is a request <Response> so we can use it to view the response

.. code-block:: python

    from ampalibe import Logger

    Logger.info("Info message")
    Logger.debug("Debug message")
    Logger.warning("Warning message")
    Logger.error("Error message")
    Logger.critical("Critical message")

    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        Logger.info("Message received from user")
        res = chat.send_text(sender_id, "Hello world")
        if res.status_code == 200:
            Logger.info("Message sent to user")
        else:
            Logger.error("Error sending message to user")
    

Structure
-----------

Each developer is **free to choose the structure he wants**, by just importing the files into the core.py.

We can make our functions everywhere, even as methods

``core.py`` file 

.. code-block:: python

    # importing another file contains ampalibe decorator
    import user
    import ampalibe
    from ampalibe import Messenger, Payload

    chat = Messenger()


    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
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
        def login(sender_id, **ext):
            '''
                function is always calling when payload or message start by /login/admin
            '''
            bot.query.set_action(sender_id, '/get_username')
            bot.chat.send_message(sender_id, 'Enter your username')


``user.py`` file 

.. code-block:: python

    import ampalibe
    from ampalibe import Messenger

    chat = Messenger()


    class User:

        @ampalibe.action('/get_username')
        def username(sender_id, cmd, **ext):
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
    
    chat = ampalibe.Messenger()


    @webserver.get('/test')
    def test():
        return 'Hello, test'

    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        chat.send_message(sender_id, "Hello, Ampalibe")


Crontab
=================

Since Ampalibe v1.1.0, we can use the `Crontab <https://man7.org/linux/man-pages/man5/crontab.5.html>`_ to schedule the execution of a task in the bot.


*"run this task at this time on this date".*

example of using the crontab

.. code-block:: python

    '''
        Send a weather report to everyone in the morning every day at 08:00
    '''

    import ampalibe
    from ampalibe import webserver
    from model import CustomModel
    
    chat = ampalibe.Messenger()
    query = CustomModel()

    @ampalibe.crontab('0 8 * * *')
    async def say_hello():
        for user in query.get_list_users():
            chat.send_message(user[0], 'Good Morning')
    

    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        ...


You can too activate your crontab for later

.. code-block:: python

    '''
        Say hello to everyone in the morning every day at 08:00
    '''

    import ampalibe
    ...

    chat = ampalibe.Messenger()

    def get_weather():
        # Use a webservice to get the weather report
        ...
        return weather
    

    @ampalibe.crontab('0 8 * * *', start=False)
    async def weather_report():
        weather = get_weather()
        for user in query.get_list_users():
            chat.send_message(user[0], weather)
    

    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        print("activate the crontab now")
        weather_report.start()

you can also create directly in the code

.. code-block:: python

    '''
        Send everyone notification every 3 hours
    '''
    
    import ampalibe
    from ampalibe import crontab

    chat = ampalibe.Messenger()

    async def send_notif():
        for user in query.get_list_users():
            chat.send_message(user[0], 'Notification for you')
    
    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        print('Create a crontab schedule')
        ''' 
        Don't forget to add argument loop=ampalibe.core.loop 
        if the crontab is writing inside a function
        ''''
        crontab('0 */3 * * *', func=send_notif, loop=ampalibe.core.loop)


.. code-block:: python

    '''
        Send a notification to a user every 3 hours
    '''
    
    import ampalibe
    from ampalibe import crontab

    chat = ampalibe.Messenger()

    async def send_notif(sender_id):
        chat.send_message(sender_id, 'Notification for you')
    
    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        print('Create a crontabe schedule')
        ''' 
        Don't forget to add argument loop=ampalibe.core.loop 
        if the crontab is running inside decorated function
        like command, action, event
        ''''
        crontab('0 */3 * * *', func=send_notif, args=(sender_id,), loop=ampalibe.core.loop)

.. note::
    
    if you don't know how to create cron syntax you can check `here <https://man7.org/linux/man-pages/man5/crontab.5.html>`_

.. important::

    ampalibe **crontab** use `croniter <https://github.com/kiorky/croniter>`_  for the spec, so you can check all the possibilities of time.
    
    

Event 
=================

Since v1.1+
You can now listening event like `message_reads`, `message_reactions` and `message_delivery`
with ampalibe **event** decorator.


.. code-block:: python
    
    import ampalibe
    
    chat = ampalibe.Messenger()

    @ampalibe.event('read')
    def event_read(**ext):
        print('message is reading')
        print(ext)
        
    @ampalibe.event('delivery')
    def event_read(**ext):
        print('last message is delivery')
        print(ext)
        
    @ampalibe.event('reaction')
    def event_read(**ext):
        print('A message received a reaction')
        print(ext)
        
    @ampalibe.command('/')
    def main(sender_id, cmd, **ext):
        chat.send_message(sender_id, "Hello, Ampalibe") 
       
 
 
.. note:: 
 
    The are 3 arguments for `event` decorator: *read*, *delivery*, *reaction*



Native event 
=================

Since v1.1.6+
You can now add event like `before_receive`  and `after_receive`
in ampalibe as decorator to execute a function before or after a received message


.. code-block:: python
    
    import ampalibe
    from ampalibe.messenger import Action
    
    chat = ampalibe.Messenger()

    @ampalibe.before_receive()
    def before_process(sender_id, **ext):
        chat.send_action(sender_id, Action.mark_seen)
        return True


    @ampalibe.command("/")
    def main(sender_id, **ext):
        chat.send_text(sender_id, "Hello ampalibe")


.. important:: 

    The function decorated with before receive must return the value ``True`` to continue the process.

    So you can stop the process directly by returning the value ``False``.


.. code-block:: python
    
    import ampalibe
    from ampalibe.messenger import Action
    
    chat = ampalibe.Messenger()
    swearing_words = ['f**k you']

    @ampalibe.before_receive()
    def before_process(sender_id, cmd, **ext):
        chat.send_action(sender_id, Action.typing_on)

        if cmd in swearing_words:
            return False
        return True

    @ampalibe.after_receive()
    def after_process(sender_id, **ext):
        chat.send_action(sender_id, Action.typing_off)

    @ampalibe.command("/")
    def main(sender_id, **ext):
        chat.send_text(sender_id, "Hello ampalibe")


.. note:: 
 
    the function decorated by **after_receive** always executes regardless 
    of the value returned by the function decorated by **before_receive** .