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


## Ampalibe 1.1.4 

* [FIX] Fix send quick reply missing 13th with next argument by @rootkit7628 in https://github.com/iTeam-S/Ampalibe/pull/47
* [IMP] Remove unecessary instructions by @gaetan1903 in https://github.com/iTeam-S/Ampalibe/pull/48
* [IMP] Preserve the built-in type of data sent on Payload Management by @gaetan1903 in https://github.com/iTeam-S/Ampalibe/pull/50
* [ADD] Create requirements on init and create by @rootkit7628 in https://github.com/iTeam-S/Ampalibe/pull/51
* [FEAT] Object Payload sent in action by @gaetan1903 in https://github.com/iTeam-S/Ampalibe/pull/54
* [FIX][IMP] Many fix & improvement by @gaetan1903 in https://github.com/iTeam-S/Ampalibe/pull/55
* [FIX] send_buttons error by @gaetan1903 in ec865f7046af472575185635d9e4a9b8087f4dd4
* [IMP][FIX] Verification db connection in b6b18ecfdadb3c324942d5b478873002d34696e2


## Ampalibe 1.1.5

* [IMP] Data integrity for UI & Messenger (#56) 
* [FIX] quick_rep don't support in Element (f8054555e60a74d220e081bd163a2747778fb72e)
* [IMP] Add specific type for attachments (#62) 
* [IMP] stringify Payload object to output (#62) 
* [ADD][IMP] Full functionnality `send_message` API (#63)
* [ADD] Unit Test for messenger_api 
* [ADD] Unit Test for ampalibe CLI
* [IMP] Documentation improved


## Ampalibe 1.1.6

* [IMP] Add argument reusable in send_file & send_file_url
* [ADD] send_attachment SEND API (sending reusable file)
* [FEAT] Personas management send API (create, list, get, delete) by @rivo2302
* [ADD] new messenger api : send receipt template by @rootkit7628
* [FIX] attachments not received in function reported by @SergioDev22
* [IMP] unit test for receiving attachment
* [ADD] decorator before_receive & after_receive message
* [ADD] get_user_profile SEND API


## Ampalibe 1.1.7

* [ADD] Logger fearure for ampalibe (#71)
* [IMP] Make Sqlite support type datetime (#72)
* [IMP] send return data in after_receive function (#73) 
* [IMP] Avoid quick_rep params erase next quick_rep in (9d7a934c2a292ad3a67f3a514f3994df2b141984)
* [IMP] Readability and maintainability (#74) 


## Ampalibe 1.1.8

* [ADD] Mongodb support (#76)
* [IMP] Code quality (#87) (6a695791ab1b07f18cde89484ec41f72a8ed90c4)
* [IMP] Optimize time for translate function (#77)
* [IMP] Change temporary data management (#78) 
* [FIX] translate encoding in windows (af9e1fba065a726243b8c518157f101cd7c2de4b)
* [ADD] New Messenger API: send_product_template (#79)
* [FIX] --dev doesn't work anymore on windows (af7aba3fb1f860109a3aa417de7bbda880f09ffb)
* [ADD] One time notification Messenger API (#80)
* [IMP] fix & imrpov structure (#81)
* [IMP] Improve core readability (#82) (#83) 
* [FIX] Logger , printing twice (#86)
* [IMP] Model optimisation (#88)
* [IMP] Minor syntax style (#89) 


 






