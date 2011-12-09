==========================
 Alte Kamereren's website
==========================

Running on your own computer
============================

Requirements
------------

You need Python 2.7 with pip, and git.
Then run::

    git clone git@github.com:tapetersen/aksite.git
    cd aksite
    pip install pil epio yaml
    pip install -r requirements.txt

Windows
~~~~~~~

For Windows I recommend the x86 python 2.7 from activestate: 
http://www.activestate.com/activepython/downloads

You also need git for windows: http://git-scm.com/ . You need to select OpenSSH when installing.

Open git bash from the start menu and run::

    pypm-script.py install pil
    
cd to some good develop-directory and run the commands above.

Setting up the db
-----------------
Run (ignore the error about auth_permission after the first command)::

    python manage.py syncdb
    python manage.py migrate
    python manage.py syncdb
    
    
Uploading to ep.io
==================

You need to get local_settings.py (it contains keys 
that should not be uploaded to a public git-repo).

Then you need an account at ep.io and to be added to the
altekamereren app.

Ask Sam how.

You need to get the static files from feincms too, 
copy and put in static manually for now, until collectstatic works better.

Then run (only once per computer)::

    epio upload_ssh_key
    
Then you can run::
    
    epio upload
    
to upload a new version of the app.

To get the database run::

    epio django "dumpdata app page medialibrary auth.group auth.user sites guardian --natural --format=yaml --indent=2" > data.yaml
    manage.py loaddata data.yaml
    
To get uploaded files run::

    rsync -rv vcs@ssh.ep.io:altekamereren/ media/
    
On windows, get MSYS rsync and run::
    
    rsync -rv --iconv=cp1252,UTF-8 vcs@ssh.ep.io:altekamereren/ media/
