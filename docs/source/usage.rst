Usage
=====

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

.. code-block:: console

   $ ampalibe create myfirstbot

There will be a created directory named **myfirstbot/** and all the files contained in it.

.. note::

   You can directly create projet without a new directory with **init** command

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

.. raw:: html
   <iframe width="1280" height="720" src="https://www.youtube.com/embed/KoD_-Ho__04?list=PLN1d8qaIQgmKmCwy3SMfndiivbgwXJZvi" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


Run the app
-----------------

In the project folder, type

.. code-block:: console

   $ ampalibe run 




