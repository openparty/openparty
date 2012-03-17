============================
OpenParty (Unconference Community website)
============================

This repository stores the OpenParty website.


Installation
============

To get setup with OpenParty code you must have the follow installed:

 * Python 2.5+
 * virtualenv 1.4.7+

Setting up environment
----------------------

Create a virtual environment where dependencies will live::

    $ virtualenv --no-site-packages openparty
    $ source openparty/bin/activate
    (openparty)$

Install openparty project dependencies::

    (openparty)$ pip install -r requirements


Setting up the database
-----------------------

This will vary for production and development. By default the project is set
up to run on a SQLite database. If you are setting up a production database
see the Configuration section below for where to place settings and get the
database running. Now you can run::

    (openparty)$ python openparty_project/manage.py syncdb
    (openparty)$ python openparty_project/manage.py loaddata fixtures/initial_{wakawaka,boxes}.json

The wakawaka fixtures will require a user to exist before being ran. During
syncdb it is worth it to make a superuser account which can then be used for
making other users staff/superusers after they sign up.

Running a web server
--------------------

In development you should run::

    (openparty)$ python manage.py openparty_project/runserver
