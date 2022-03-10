# Ampalibe
<p align="center"> <img height="300" src="https://github.com/iTeam-S/Ampalibe/raw/main/docs/source/_static/ampalibe_logo.png"/></p>

<p align="center">
Ampalibe is a light Python framework for quickly creating bots Facebook Messenger. </br>
It provides a new concept for creating bots, it manages webhook sides, processes data sent by facebook and provides api messengers with advanced functions.
</p>


[![Documentation status](https://readthedocs.org/projects/ampalibe/badge/?version=latest)](https://ampalibe.readthedocs.io)
[![Repository size](https://img.shields.io/github/repo-size/iTeam-S/ampalibe.svg)](https://github.com/iTeam-S/ampalibe)


## Installation

```s
pip install https://github.com/iTeam-S/Ampalibe/archive/refs/heads/main.zip
```

### Dependencies:
- [Python 3.7+](https://www.python.org/)


## Usage
```s
ampalibe create myproject
```

OR 


```shell
$ cd myproject
$ ampalibe init
```

to run project, just use
```s
ampalibe run
```

## Documentation

- [Ampalibe Readthedocs](https://ampalibe.readthedocs.io/) (Not yet ready)


## About 

Ampalibe is a word of Malagasy 🇲🇬 origin designating the fruit jackfruit.

We have made a promise to
 
- keep it **light**
- make it **easy to use**
- do it **quickly to develop**

### Advantages

- **No need to manage weebhooks and data:** `messages are received directly in a main function`
```python
import ampalibe
from conf import Configuration

bot = ampalibe.init(Configuration())
chat = bot.chat

@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    chat.send_message(sender_id, 'Hello world')
    chat.send_message(senser_id, f'This is your message: {cmd}')
    chat.send_message(senser_id, f'and this is your facebook id: {sender_id}')
```
----------------------------------------------------

- **Manages the actions expected by the users:** `define the function of the next treatment`
```python
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
def get_mail(sender_id, name, **extends):
    query.set_action(sender_id, None)  #  clear current action
    chat.send_message(sender_id, f'Bonjour {name}')
```
----------------------------------------------------

- **Manage temporary data:** `set, get, and delete`
```python
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
def get_mail(sender_id, mail, **extends):
    # save the mail in temporary data
    query.set_temp(sender_id, 'mail', mail)
    chat.send_message(sender_id, f'This is your mail: {mail}')

    chat.send_message(sender_id, f'Enter your password')
    query.set_action(sender_id, '/get_password')


@ampalibe.action('/get_password')
def get_password(sender_id, password, **extends):
    query.set_action(sender_id, None)  # clear current action
    mail = query.get_temp(sender_id, 'mail')  # get mail in temporary data

    chat.send_message(sender_id, f'your mail and your password are {mail} {password}')
    query.del_temp(sender_id, 'mail')  # delete temporary data
```

- **Manage Payload of quick_reply or result:** `send data with Payload object and get it in destination function's parameter`
```python
import ampalibe
from ampalibe import Payload
from conf import Configuration

bot = ampalibe.init(Configuration())
chat = bot.chat


@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    quick_rep = [
        {
            "content_type": "text",
            "title": 'Angela',
            "payload": Payload('/membre', name='Angela', ref='2016-sac')
        },
        {
            "content_type": "text",
            "title": 'Rivo',
            "payload": Payload('/membre', name='Rivo')
        }
    ]
    chat.send_quick_reply(sender_id, quick_rep, 'Who?')
    

@ampalibe.command('/membre')
def get_membre(sender_id, cmd, name, **extends):
    if extends.get('ref'):
        chat.send_message(sender_id, 'your ref is ' + extends.get('ref'))
    else:
        chat.send_message(sender_id, "Hello " + nom)
```

