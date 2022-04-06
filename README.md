# Ampalibe
<p align="center"> <img height="300" src="https://github.com/iTeam-S/Ampalibe/raw/main/docs/source/_static/ampalibe_logo.png"/></p>

<p align="center">
Ampalibe is a light Python framework for quickly creating bots Facebook Messenger. </br>
It provides a new concept for creating bots, it manages webhook sides, processes data sent by facebook and provides api messengers with advanced functions ( payload management. items length, ...) .
</p>


[![PyPI - Version](https://img.shields.io/pypi/v/ampalibe?style=for-the-badge)](https://pypi.org/project/ampalibe/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/ampalibe?label=DOWNLOADS&style=for-the-badge)](https://pypi.org/project/ampalibe/)


## Installation

```s
pip install ampalibe
```

OR you can install dev version


```s
pip install https://github.com/iTeam-S/Ampalibe/archive/refs/heads/main.zip
```

### Dependencies:
- [Python 3.7+](https://www.python.org/)


## Usage

> command-line __ampalibe__ is __ampalibe.bat__ for _Windows_

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

- [Ampalibe Readthedocs](https://ampalibe.readthedocs.io/)


## About 

Ampalibe is a word of Malagasy 🇲🇬 origin designating the fruit jackfruit.

We have made a promise to
 
- keep it **light**
- make it **easy to use**
- do it **quickly to develop**

## Why use Ampalibe ? 

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
def get_name(sender_id, cmd, **extends):
    query.set_action(sender_id, None)  #  clear current action
    chat.send_message(sender_id, f'Hello {cmd}')
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
def get_mail(sender_id, cmd, **extends):
    # save the mail in temporary data
    query.set_temp(sender_id, 'mail', cmd)

    chat.send_message(sender_id, f'Enter your password')
    query.set_action(sender_id, '/get_password')


@ampalibe.action('/get_password')
def get_password(sender_id, cmd, **extends):
    query.set_action(sender_id, None)  # clear current action
    mail = query.get_temp(sender_id, 'mail')  # get mail in temporary data

    chat.send_message(sender_id, f'your mail and your password are {mail} {cmd}')
    query.del_temp(sender_id, 'mail')  # delete temporary data
```

----------------------------------------------------------------------------

- **Manage Payload:** `send data with Payload object and get it in destination function's parameter`
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
    chat.send_message(sender_id, "Hello " + name)

    # if the arg is not defined in the list of parameters,
    # it is put in the extends variable
    if extends.get('ref'):
        chat.send_message(sender_id, 'your ref is ' + extends.get('ref'))

```
--------------------------------------------------------------------------
- **No need to manage the length of the items to send:** `A next page button will be displayed directly`
```python
import ampalibe
from ampalibe import Payload
from conf import Configuration

bot = ampalibe.init(Configuration())
chat = bot.chat

@ampalibe.command('/')
def main(sender_id, cmd, **extends):
    list_items = [
        {
            "title": f"item n°{i+1}",
            "image_url": "https://i.imgflip.com/6b45bi.jpg",
            "buttons": [
                {
                    "type": "postback",
                    "title": "Get item",
                    "payload": Payload("/item", id_item=i+1)
                }
            ]
        }
        for i in range(30)
    ]
    # next=True for displaying directly next page button.
    chat.send_template(sender_id, list_items, next=True)

@ampalibe.command('/item')
def get_item(sender_id, id_item):
    chat.send_message(sender_id, f"item n°{id_item} selected")

```

