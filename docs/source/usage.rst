Get Started
============

.. _installation:

Installation
------------

To use Ampalibe, first install it using pip:

.. code-block:: console

   $ pip install ampalibe

Creation of a new project
-------------------------

After installation, an ``ampalibe`` executable is available in your system path, 
and we will create our project with this command.

.. important::

   command-line ``ampalibe`` is ``ampalibe.bat`` for **Windows**


.. code-block:: console

   $ ampalibe create myfirstbot

There will be a created directory named **myfirstbot/** and all the files contained in it.

.. note::

   You can directly create project without a new directory with **init** command

.. code-block:: console

   $ cd myExistingDirectory
   $ ampalibe init


Understanding of files
-------------------------

.. image:: https://github.com/iTeam-S/Ampalibe/raw/main/docs/source/_static/structure.png

.. hlist::
   :columns: 1

   * ``assets/`` statics file folder
      * ``public/`` reachable via url
      * ``private/`` not accessible via url
   
   * ``.env`` environment variable file

   * ``conf.py`` configuration file that retrieves environment variables 

   * ``core.py`` file containing the starting point of the code

.. important::

   .env file is env.bat in Windows


Before starting
-----------------

How to complete the environment variable file

.. hlist::
   :columns: 1

   * **AMP_ACCESS_TOKEN** Facebook Page access token
   * **AMP_VERIF_TOKEN** Token that Facebook use as part of the recall URL check.
   * **ADAPTER** type of database used by ampalibe (SQLITE OR MYSQL) 
      * **FOR MYSQL ADAPTER**
         * *DB_HOST**
         * *DB_USER*
         * *DB_PASSWORD*
         * *DB_NAME*
         * *DB_PORT*
      * **FOR SQLITE ADAPTER**
         * *DB_FILE*
   * **AMP_HOST** server listening address
   * **AMP_PORT** server listening port
   * **AMP_URL** URL of the server given to Facebook



Run the app
-----------------

In the project folder, type

.. code-block:: console

   $ ampalibe run


for dev mode with **Hot Reload**

.. code-block:: console

   $ ampalibe run --dev

::

   INFO:     Started server process [26753]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:4555 (Press CTRL+C to quit)

.. note::

   Ampalibe use uvicorn to run server, so it is an output of uvicorn

