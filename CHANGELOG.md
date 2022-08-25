## Ampalibe 1.0.1

> Pypi: https://pypi.org/project/ampalibe/1.0.1/

### FEATURES

- Command & Action 
- Payload Managament
- Messenger API functions
- File Management 


## Ampalibe 1.0.2

> Pypi: https://pypi.org/project/ampalibe/1.0.2/

### NEW

- Works on Windows
- Docs for custom endpoints
- Imporve docs


## Ampalibe 1.0.4

> Pypi: https://pypi.org/project/ampalibe/1.0.4/

### FIX 

- Improve docs
- Update readme
- Remove deprecated methods
- Add warning for action not found
- Fix Api  messenger Payload in second Page Template

### NEW  FEATURES

- Hot reload Support: `ampalibe run --dev`
- Add  python version 3.6 support 
- Add `download_file` options to direct download a link
- Add `ampalibe env` command to generate only env


## Ampalibe 1.0.5

### FIX 

- Fix Ampalibe ASCII broken
- Fix send_file Messenger API
- Remove mysql-connector dependancy


### NEW FEATURES

- Quick Reply Auto Next for item length more than 13
- Help Messsage for Linux
- Add QuickReply Object
- Add Button Object
- Add Element Object
- Customize text of next quick_reply
- Customize text of next generic template
- Number of processes workers in production mode
- Persistent Menu to Object ( List Buttons )



## Ampalibe 1.0.6

- ADD port argument in command-line for linux
- Docker deployement in your own server
- Docker Deployement with heroku 


## Ampalibe 1.0.7

- ADD `testmode` arg in the server to run without threads 
- ADD `langage Management`
    - lang managed directly by ampalibe
    - add 'ampalibe lang' command to generate langs.json file
    - add translate function to translate word or sentence
    - add `set_lang` method to set lang of an user 

- ADD simulate function to simulate a message.



## Ampalibe 1.1.0

- Support for Postgres DATABASE
- New Structure: All conf importation is optionnal now
- New method for messenger api: `send_custom`
- Make `NULL` Default for lang insted `fr`
- FIX error in `get_temp` methode when data not exist
- `simulate` function is ready for ampalibe 
- Introduction of ampalibe `crontab` 
- Add listenner for events: `messages_reads`, `messages_reactions`, `messages_delivery`
- Continious integration for new Pull Request 
- Continious Delivery for Github package and Pypi 
- Rewrite `scripts` for Linux & Windows to same base code 
- Typewriting introduction for output command
- Documentation updated
- Remove workers


## Ampalibe 1.1.1 patch

- fix port argument doesn't work on 
- fix error when python is python3 and not python

## Ampalibe 1.1.2 patch

- [IMP] Add indication in dockerfile
- [FIX] Payload object instead of dict in quick_replies when build Element
- [FIX] Fix Typo in Ampalibe definition
- [FIX] Missing gitignore file on create & init
- [IMP] Adapt ASGI server to be supported by Heroku/python image
- [IMP] Command decorators priority before action decorators in ampalibe core


## Ampalibe 1.1.3 Stable

- [FIX] Cmd object & Payload in persistant menu 
- [FIX] route not recognized in Payload Object (#42) 
- [FIX][REF] Fix persistent menu Button not Jsonserialized (#45) 
- [ADD] Functionnal test in CI (#46) 
