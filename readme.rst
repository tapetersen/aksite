==========================
 Alte Kamereren's website
==========================

Running on your own computer
============================

Requirements
------------

You need Python 3.3 with pip, and git.
Then run::

    git clone git@github.com:tapetersen/aksite.git
    cd aksite
    pip install virualenv
    virtualenv ~/.virtualenvs/aksite
    ~/.virtualenvs/aksite/scripts/activate
    pip install -r requirements.txt

Setting up the db
-----------------
Run (ignore the error about auth_permission after the first command)::

    python manage.py syncdb
    python manage.py migrate
    python manage.py syncdb
    
Uploading to openshift
==================

You need an account at openshift.org and to be added to the
altekamereren app.

Ask Sam how.

To download secret keys::
    
    rhc env list > env.txt

To download the database::

    rhc port-forward

Then connect to the postgreSQL db, make a backup, and restore it to a local db.

You can also ssh and dump the data if you want to use SQLite locally or something like that::

    rhc ssh
    cd app-root/repo/
    source ../data/virtualenv/bin/activate
    python manage.py dumpdata app page medialibrary auth.group auth.user sites guardian --natural --format=xml > data.xml

Transfer it in some way (please write it here if you do) and run locally::

    python manage.py loaddata data.xml

