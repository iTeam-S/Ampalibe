Usage
=========

A Minimal Application
-----------------------

A minimal Ampalibe application looks something like this:

.. code-block:: python

    import ampalibe
    from conf import Configuration

    bot = ampalibe.init(Configuration())

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        bot.chat.send_message(sender_id, "Hello, Ampalibe")


So what did that code do?

.. hlist::
   :columns: 1

   * ``line 1`` we import ampalibe package.
   
   * ``line 2`` we import Configuration class which contains our env variable.

   * ``line 4`` we inite ampalibe with configuration and store the result instance. 

   *  we create a function decorated by ampalibe.command('/') to say Ampalibe that it's the main function.

   * ``line 8`` We respond to the sender by greeting Ampalibe


.. note::

   messages are received directly in a main function


Command
---------

Ampalibe's philosophy says that all received messages, whether it is a simple or payload message, or an image, is considered to be commands

The command decorator of ampalibe is used to specify the function where a specific command must launch. 
If no corresponding command is found, it launches the main function


.. code-block:: python

    import ampalibe
    from conf import Configuration

    bot = ampalibe.init(Configuration())

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        bot.chat.send_message(sender_id, "Hello, Ampalibe")

    '''
        if the message received start with '/eat'
        the code enter here, not in main
        ex: /eat 1 jackfruit

        cmd value contains /eat 1 jackfruit
    '''
    @ampalibe.command('/eat')
    def spec(sender_id, cmd, **extends):
        print(sender_id)  # 1555554455
        print(cmd)  # '1 jackfruit'

    
    '''
       ex: /drink_a_jackfruit_juice
    '''
    @ampalibe.command('/drink_a_jackfruit_juice')
    def spec(sender_id, cmd, **extends):
        print(sender_id)  # 1555554455
        print(cmd)  #  /drink_a_jackfruit_juice

.. note::

   When we create a function decorated by ampalibe.command, ``**extends`` parameter must be present

Action
----------

At some point, we will need to point the user to a specific function, to retrieve user-specific data, for example, ask for his email, ask for the word the person wants to search for.

To do this, you have to define the action expected by the user, to define what should be expected from the user.

in this example, we will use two things, the **action decorator** and the **query.set_action** method

**Example 1**: Ask the name of user, and greet him

.. code-block:: python

    import ampalibe
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat
    query = bot.query

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        chat.send_message(sender_id, 'Enter your name')
        query.set_action(sender_id, '/get_name')
        
    @ampalibe.action('/get_name')
    def get_name(sender_id,  cmd, **extends):
        query.set_action(sender_id, None)  #  clear current action
        chat.send_message(sender_id, f'Hello {cmd}')

**Example 2**: Ask a number and say if it a even number or odd number

.. code-block:: python

    import ampalibe
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat
    query = bot.query

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        chat.send_message(sender_id, 'Enter a number')
        query.set_action(sender_id, '/get_number')
        
    @ampalibe.action('/get_number')
    def get_number(sender_id, cmd, **extends):
        query.set_action(sender_id, None)  #  clear current action
        if cmd.isdigit():
            if int(cmd) % 2 == 0:
                chat.send_message(sender_id, 'even number')
            else:
                chat.send_message(sender_id, 'odd number')
        else:
            chat.send_message(sender_id, f'{cmd} is not a number')


We define the next function in which the user message entered and can obtain all the texts of the message in "cmd"


.. important::

   Remember to erase the current action to prevent the message from entering the same function each time

.. note::

   When we create a function decorated by ampalibe.action, ``**extends`` parameter must be present



Temporary data
-----------------

For each processing of each message, we will need to store information temporarily,
like saving the login while waiting to ask for the password

the methods used are **set_temp**, **get_temp**, **del_temp**

.. code-block:: python

    import ampalibe
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat
    query = bot.query

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        chat.send_message(sender_id, 'Enter your mail')
        query.set_action(sender_id, '/get_mail')
        
    @ampalibe.action('/get_mail')
    def get_mail(sender_id, cmd, **extends):
        # save the mail in temporary data
        query.set_temp(sender_id, 'mail', cmd)

        chat.send_message(sender_id, f'Enter your password')
        query.set_action(sender_id, '/get_password')


    @ampalibe.action('/get_password')
    def get_password(sender_id, cmd, **extends):
        query.set_action(sender_id, None)  # clear current action
        # get mail in temporary data
        mail = query.get_temp(sender_id, 'mail')  
        chat.send_message(sender_id, f'your mail and your password are {mail} {cmd}')
        # delete mail in temporary data
        query.del_temp(sender_id, 'mail')  


Payload Management
----------------------

Ampalibe facilitates the management of payloads with the possibility of sending arguments.

You can send data with ``Payload`` object and get it in destination function's parameter

.. code-block:: python

    import ampalibe
    # import the Payload class
    from ampalibe import Payload
    from ampalibe.ui import QuickReply
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat


    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        quick_rep = [
            QuickReply(
                title='Angela',
                payload=Payload('/membre', name='Angela', ref='2016-sac')
            ),
            QuickReply(
                title='Rivo',
                payload=Payload('/membre', name='Rivo', ref='2016-sac')
            )
        ]
        chat.send_quick_reply(sender_id, quick_rep, 'Who?')
        

    @ampalibe.command('/member')
    def get_membre(sender_id, cmd, name, **extends):
        '''
            You can receive the arguments payload in extends or 
            specifying the name of the argument in the parameters
        '''
        chat.send_message(sender_id, "Hello " + name)

        # if the arg is not defined in the list of parameters,
        # it is put in the extends variable
        if extends.get('ref'):
            chat.send_message(sender_id, 'your ref is ' + extends.get('ref'))


File management
-------------------

We recommand to make static file in assets folder, 

for files you use as a URL file, you must put assets/public, in assets/private otherwise

.. code-block:: python

    '''
    Suppose that a logo file is in "assets/public/iTeamS.png" and that we must send it via url
    '''

    import ampalibe
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat


    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        '''
            to get a file in assets/public folder, 
            the route is <adresse>/asset/<file>
        '''
        chat.send_file_url(
            sender_id,
            Configuration.APP_URL + '/asset/iTeamS.png', 
            filetype='image'
        )

Langage Management
-------------------------

Since Ampalibe v1.0.7, a file langs.json is generated by default.

if you are using old project, you can run this command to generate manually a lang file. 

.. code-block:: console

   $ ampalibe lang

you can add in this file all your words by respecting key/value format of json.

.. code-block:: javascript

   {
        "<WORD_KEY>" : {
            "<LANG_KEY_1>" : "<VALUE>",
            "<LANG_KEY_2>" : "<VALUE>",
             ...
            "<LANG_KEY_n>" : "<VALUE>",
        },

   }


So you can use it in translate function

**core.py**

.. code-block:: python

    import ampalibe
    from ampalibe import translate
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat
    query = bot.query

    @ampalibe.command('/')
    def main(sender_id, lang, cmd, **extends):
        chat.send_message(
            sender_id, 
            translate('hello_world', lang)

.. note::

    You can use the ``lang`` parameter in your code to get the lang of an user. 
    
    you can take it in **extends** parameter too


.. code-block:: python

    import ampalibe
    from ampalibe import translate

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        print(extends.get('lang'))  # current lang of sender_id

Use the ``set_lang`` method to set the lang of an user. 

.. code-block:: python

    import ampalibe
    from ampalibe import translate
    from conf import Configuration

    bot = ampalibe.init(Configuration())
    chat = bot.chat
    query = bot.query

    @ampalibe.command('/')
    def main(sender_id, cmd, **extends):
        chat.send_message(
            sender_id, 
            "Hello world"
        )
        query.set_lang(sender_id, 'fr')
        query.set_action(sender_id, '/what_my_lang')
    

    @ampalibe.action('/what_my_lang')
    def other_func(sender_id, lang, cmd, **extends):
        query.set_action(sender_id, None)

        chat.send_message(sender_id, 'Your lang is ' + lang + ' now')
        chat.send_message(
            sender_id, 
            translate('hello_world', lang)
        )

.. important::

    if the word key is not exist in the lang file, the word is not translated.

    the ``translate`` function return the word key if the word is not translated.