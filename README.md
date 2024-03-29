[![Build Status](https://travis-ci.org/openparty/openparty.png)](https://travis-ci.org/openparty/openparty)
[![Build Status](https://drone.io/github.com/qingfeng/openparty/status.png)](https://drone.io/github.com/qingfeng/openparty/latest)
[![Requirements Status](https://requires.io/github/openparty/openparty/requirements.svg?branch=master)](https://requires.io/github/openparty/openparty/requirements/?branch=master)

# OpenParty (Unconference Community website)


This repository stores the OpenParty website.


## Installation

To get setup with OpenParty code you must have the follow installed:

> * Python 3
> * Pipenv
> * MySQL

## Setting up environment

```
pyenv install 3.9
pip install pipenv
pipenv --python 3.9
pipenv shell
pipevn install
```


## Setting up the database

This will vary for production and development. By default the project is set
up to run on a SQLite database. If you are setting up a production database
see the Configuration section below for where to place settings and get the
database running. Now you can run:

```
pipenv shell
(openparty)$ python manage.py migrate --fake-initial
```

## Install pre-commit hook

First time `pre-commit install` which will install a git commit hook.


Manually check file format `pre-commit run --all-files`.

Update pre-commit hook's version `pre-commit autoupdate`.

## Running a web server

In development you should run:

```
(openparty)$ python manage.py runserver
```

## Deploy it

If you are deploying on ubuntu, you may install those build dependencies.

```
sudo aptitude install libmysqlclient-dev libxml2-dev libxslt1-dev
```

Install those python libs through virtual env.

```
sudo easy_install -U pip
sudo pip install virtualenv
sudo mkdir /usr/local/virtualenv
cd /usr/local/virtualenv
sudo virtualenv --distribute --no-site-packages openparty
source /usr/local/virtualenv/openparty/bin/activate
cd PROJECT_FOLDER

```

```
sudo su -
source /usr/local/virtualenv/openparty/bin/activate
pip install -r requirements.txt
```

- [Deploy django applications with nginx, uwsgi, virtualenv, south, git and fabric](http://www.abidibo.net/blog/2012/06/20/deploy-django-applications-nginx-uwsgi-virtualenv-south-git-and-fabric-part-4/)
