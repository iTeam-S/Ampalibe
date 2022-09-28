# Ampalibe
<p align="center"> <img height="300" src="https://github.com/iTeam-S/Ampalibe/raw/main/docs/source/_static/ampalibe_logo.png"/></p>
<div align="center">
 <h4>
    <a href="https://github.com/iTeam-S/Ampalibe#other-resource">Video Tutorials</a>
  <span> · </span>
    <a href="https://ampalibe.readthedocs.io">Documentation</a>
  <span> · </span>
    <a href="https://github.com/iTeam-S/Ampalibe/issues/">Report Bug</a>
 </h4>

<p>
 <b>Ampalibe</b> is a lightweight Python framework for building Facebook Messenger bots faster.
It provides a new concept, it manages webhooks, processes data sent by Facebook and provides <a href="https://developers.facebook.com/docs/messenger-platform/">API Messenger</a> with advanced functions such as payload management, item length, and more.
</p>

<a href='https://github.com/iTeam-S/Ampalibe/#'><img src='https://img.shields.io/badge/version-1.1.5.dev-%23008080'/></a>
<a href='https://ampalibe.readthedocs.io/en/latest/'><img src='https://readthedocs.org/projects/ampalibe/badge/?version=latest&style=flat'/></a>
<a href='https://github.com/iTeam-S/Ampalibe/actions/workflows/ci.yml'><img src='https://github.com/iTeam-S/Ampalibe/actions/workflows/ci.yml/badge.svg'/></a>
<a href='https://github.com/iTeam-S/Ampalibe/actions/workflows/cd-pg.yml'><img src='https://github.com/iTeam-S/Ampalibe/actions/workflows/cd-pg.yml/badge.svg'/></a>
<a href='https://github.com/iTeam-S/Ampalibe/actions/workflows/cd-pypi.yml'><img src='https://github.com/iTeam-S/Ampalibe/actions/workflows/cd-pypi.yml/badge.svg'/></a>



<p>
 <a href='https://pypi.org/project/ampalibe/'> <img src='https://img.shields.io/pypi/v/ampalibe?style=for-the-badge'/></a>
 <a href='https://pypi.org/project/ampalibe/'> <img src='https://img.shields.io/pypi/dm/ampalibe?label=DOWNLOADS&style=for-the-badge'/></a>
 <a href='https://github.com/iTeam-S/'> <img src='https://img.shields.io/badge/Team-iTeam--$-teal?style=for-the-badge'/></a>
 <a href='#'> <img src='https://img.shields.io/badge/Maintained-Yes-darkgreen?style=for-the-badge'/></a>
 <a href='https://pypi.org/project/ampalibe/'> <img src='https://img.shields.io/pypi/pyversions/ampalibe?style=for-the-badge'/></a>
 <a href='https://discord.gg/yE4YEfkp/'> <img src='https://img.shields.io/discord/995937004405661807?style=for-the-badge'/></a>
</p>

<p>
   <strong> Show your support</strong>  <em> by giving a star 🌟 if this project helped you! </em>
 </p>
</div>


## Installation

```s
pip install ampalibe
```

OR you can install dev version


```s
pip install https://github.com/iTeam-S/Ampalibe/archive/refs/heads/main.zip
```

------------------

if you use mysql as database, you have to install `mysql-connector` or `mysql-connector-python` with ampalibe

```s
pip install ampalibe[mysql-connector]
```

----------------------

if you use postgresql as database, you have to install `psycopg2` with ampalibe

```s
pip install ampalibe[psycopg2]
```

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

for dev mode with __Hot Reload__
```s
ampalibe run --dev
```

### Register for an Access Token

You will need to configure a Facebook application, a Facebook page, get the access to the page, link the application to the page, configure a webhook for your app before you can really start using __Ampalibe__.

[This app setup guide](https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup) should help

OR 

See [this video](https://www.youtube.com/watch?v=Sg2P9uFJEF4&list=PL0zWFyU4-Sk5FcKJpBTp0-_nDm0kIQ5sY&index=1) on Youtube


## Documentation

- [Ampalibe Readthedocs](https://ampalibe.readthedocs.io/)

#### Other resource

- [ [Youtube] Create a Facebook Bot Messenger with AMPALIBE Framework (EN) ](https://www.youtube.com/playlist?list=PL0zWFyU4-Sk5FcKJpBTp0-_nDm0kIQ5sY)
- [ [Youtube] Tutoriel Framework Ampalibe (FR)](https://www.youtube.com/playlist?list=PLz95IHSyn29U4PA1bAUw3VT0VFFbq1LuP)
- [ [Youtube] Ampalibe Framework Episode (Teny Vary Masaka) ](https://www.youtube.com/playlist?list=PLN1d8qaIQgmKmCwy3SMfndiivbgwXJZvi)


## Deployment 

**Using container**

> Go to our dir project and run 

```s
$ docker run -d -v "${PWD}:/usr/src/app" -p 4555:4555 ghcr.io/iteam-s/ampalibe
```

**Using heroku container**

- Go to heroku docs for [docker deploys](https://devcenter.heroku.com/articles/container-registry-and-runtime) 

- Change your Dockerfile like this

```dockerfile
FROM ghcr.io/iteam-s/ampalibe

ADD . /usr/src/app/

# RUN pip install --no-cache-dir -r requirements.txt

CMD ampalibe -p $PORT run
```
- Customize your Dockerfile if necessary


**Using heroku python**

 - Go to heroku docs for [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true)


 - Define your Procfile like this `web: ampalibe -p $PORT run` 

## About 

Ampalibe is a word of Malagasy  <img src="https://github.com/RajaRakoto/github-docs/blob/master/dago.gif?raw=true" width=15>  origin designating the fruit jackfruit.

We have made a promise to
 
- keep it **light**
- make it **easy to use**
- do it **quickly to develop**


## Contributors

![Image des contributeurs GitHub](https://contrib.rocks/image?repo=iTeam-S/Ampalibe)

## Community 

### 📌 Extension

- [Ampalibe extension](https://marketplace.visualstudio.com/items?itemName=iTeam-S.ampalibe)  by [Raja Rakotonirina](https://github.com/RajaRakoto)

       A VScode extension that allows the user to write a snippet of code using easy to remember prefixes



