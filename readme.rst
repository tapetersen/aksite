==========================
Alte Kamereren's website
==========================

Deploying like a boss
======================
put all the commands in the section "Requirements" in a script. 
run it.

Running on your own computer
============================

Requirements
------------

You need Python >= 3.3 (IMPORTANT! previous versions do not support some critical unicode string features)
with pip, and git.
Then run::
    cd
    git clone git@github.com:tapetersen/aksite.git
    cd aksite
    pip install virtualenv
    virtualenv ~/.virtualenvs/aksite
    source ~/.virtualenvs/aksite/bin/activate 
    pip install -r requirements.txt

Uploading to openshift
==================

Download the secret keys::
    rhc env list -a aksite3 > env.txt

You need an account at openshift.org and to be added to the
altekamereren app.

Setting up the db
-----------------
You have several options when it comes to selecting which database for django to use
in your developement environment. In the two sections below are instructions
for setting up a PostgreSQL server and a solution using SQLite3 respectively.

Using postgreSQL on the local machine
=====================================

to enable us to connect to the database, run::

    rhc port-forward -a aksite3

This command starts a service that will enable port forwarding, so that a port on your local machine
will automatically forward all incoming traffic to the corresponding port on the
server

To connect to the db and dump its  contents in the file db/data.sql, run::
    pg_dump aksite3 -h localhost -p PORT -U USER -f db/data.sql
where PORT is the port specified in the table printed by rhc port-forward command above
and USER is the username provided under the posgresql tab on the openshift control panel
(on the openshift website)

Restore to a local db(note that this will depend on YOUR specific setup) by issuing the command::
    psql -U LOCALUSER -d DATABASE -f db/data.sql
where LOCALUSER is a database user that has the necessary permissions and DATABASE is your database's name


for more information on setting up a local database server on ubuntu for development purposes,
see Ubuntu Wiki[1] 

then, to let django know where the database is located, run::
    echo "DATABASE_URL=localhost:5432" >> env.txt
this puts a new environment variable into env.txt. 
the exact url will depend on your setup. it should be pretty close to this though

you will also need to define a local_settings.py file where you set the DATABASES variable
according to your specific setup. 
Skip ahead to the section "Syncing the database with django"
 
Using sqlite3 on the local machine
===============================
NOTE: this approach does not work for me
You can also ssh and dump the data if you want to use SQLite locally or something like that::

    rhc ssh -a aksite3
    cd app-root/repo/
    source ../data/virtualenv/bin/activate
    python manage.py dumpdata app page medialibrary auth.group auth.user sites guardian --natural --format=xml > data.xml

NOTE: putting the above in a script "dump" in db folder
Transfer it in some way (please write how here if you do) and run locally::

    python manage.py loaddata data.xml

Syncing the database with django
================================
To test that the DATABASES variable is set up correctly, running the
following command should connect to the database using that database's command line client::
    python manage.py dbshell

You are now ready to sync your database with the django framework. 
Run (ignore the error about auth_permission after the first command)::

    python manage.py syncdb
    python manage.py migrate
    python manage.py syncdb


Running the server
==================
To run the server and test your brand new developement environment::
    python manage.py runserver
fire up a browser and go to the address that the server is started on(most likely: localhost:8000)

A brief note on virtualenv
--------------------------
if you completed this readme step-by-step you should now have a prompt that looks similar to this:
(aksite)axel@axel-thinkpad:~/aksite$

the parenthesis in the beginning means that you are now inside the virtual environment 'aksite'.
to get out of it and return to your normal shell, simply run the command::
    deactivate
the command is only available when inside a virtual environment

to re-enter the virtual environment (i.e when coding on this website) run::
    source ~/.virtualenvs/aksite/bin/activate 
protip: put this command in a script or alias it


Congratulations! your environment is now properly configured

Happy hacking!

References
==========
[1] see the section "Alternative setup" on https://help.ubuntu.com/community/PostgreSQL 

[2] http://www.thegeekstuff.com/2009/01/how-to-backup-and-restore-postgres-database-using-pg_dump-and-psql/
    information on dumping and restoring a postgres db

[3] http://simononsoftware.com/virtualenv-tutorial/
    short tutorial on virtualenv


