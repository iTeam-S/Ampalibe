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

Each developer is free to choose the structure he wants, by just importing the files into the core.py.

We can make our functions everywhere, even as methods


``core.py`` file 

.. code-block:: python

    import user

    ...

    class Admin:
        
        @ampalibe.command('/login/admin')
        def login(sender_id, **extends):
            '''
                function is always calling when payload or message start by /login/admin
            '''
            bot.query.set_action(sender_id, '/get_username')


``user.py`` file 

.. code-block:: python

    class User:
        @ampalibe.action('/get_username')
        def username(sender_id, **extends):
            bot.send_message(sender_id, 'Enter your username')
            ...