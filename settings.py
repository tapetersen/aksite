# Django settings for aksite project.
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = ['192.168.0.10:8000', '127.0.0.1', 'localhost', '127.0.0.1:8000', 'localhost:8000', '*']

try:
    for line in (l for l in open(PROJECT_ROOT + "env.txt") if l.strip()):
        key, value = line.split("=")
        os.environ[key] = value
except IOError:
    pass

import dj_database_url
if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    os.environ["DATABASE_URL"] = os.environ['OPENSHIFT_POSTGRESQL_DB_URL'] + "/" + os.environ['OPENSHIFT_APP_NAME']

DATABASES = {'default': dj_database_url.config(default='sqlite://localhost/db/site.db')}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60*60*24,
        'OPTIONS': {
            'MAX_ENTRIES': 3000,
        }
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Stockholm'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'sv'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

TIME_FORMAT = "H:i"

LANGUAGES = (("sv", "Swedish"),
             ("en", "English"))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#if not DEBUG:
#    MEDIA_ROOT = '/usr/local/www/aksite/media/'
#else:
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = '/usr/local/www/aksite/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, "static_collected")
if "OPENSHIFT_DATA_DIR" in os.environ:
    STATIC_ROOT = os.path.join(os.environ["OPENSHIFT_DATA_DIR"], "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

FEINCMS_TINYMCE_INIT_TEMPLATE = 'admin/content/richtext/init_tinymce.html'
FEINCMS_TINYMCE_INIT_CONTEXT  = {
    'TINYMCE_JS_URL': os.path.join(STATIC_URL,
                                   'tinymce/jscripts/tiny_mce/tiny_mce.js'),
    'TINYMCE_CONTENT_CSS_URL': None,
    'TINYMCE_LINK_LIST_URL': None,
}

WYMEDITOR_URL = os.path.join(STATIC_URL,"js/wymeditor/jquery.wymeditor.min.js")
JQUERY_URL = os.path.join(STATIC_URL,"js/libs/jquery-1.7.min.js")

FEINCMS_WYMEDITOR_INIT_TEMPLATE = 'admin/content/richtext/init_wymeditor.html'
FEINCMS_WYMEDITOR_INIT_CONTEXT  = {
    'WYMEDITOR_JS_URL': WYMEDITOR_URL,
    #'TINYMCE_CONTENT_CSS_URL': None,
    #'TINYMCE_LINK_LIST_URL': None,
}
FEINCMS_RICHTEXT_INIT_CONTEXT = FEINCMS_WYMEDITOR_INIT_CONTEXT
FEINCMS_RICHTEXT_INIT_TEMPLATE = FEINCMS_WYMEDITOR_INIT_TEMPLATE

"""This is the number of days users will have to activate their
accounts after registering. If a user does not activate within
that period, the account will remain permanently inactive and may
be deleted by maintenance scripts provided in django-registration."""
ACCOUNT_ACTIVATION_DAYS = 10

SITE_ID = 1

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'mbmt085yg^&^d7n7g7f+yeba-_6#wxnsi##=#o!rgzsvmy1ra('

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'jinja2_for_django.Loader',
#    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #django.middleware.locale.LocaleMiddleware',
    #'sentry.client.middleware.Sentry404CatchMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ('127.0.0.1',)

ROOT_URLCONF = 'urls'
LOGIN_URL = "/users/login"
LOGIN_REDIRECT_URL = "/users/profile"

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates/'),
)

LOCALE_PATHS = (os.path.join(PROJECT_ROOT, 'locale/'),)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mptt',
    'feincms',
    'feincms.module.page',
    'feincms.content.richtext',
    'feincms.module.medialibrary',
    'django.contrib.admin',
    'django.contrib.admindocs',
    #'django_ses',
    #'sentry',
    'raven.contrib.django',
    'south',
    'app',
    'guardian',
    'storages',
    #'debug_toolbar',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'formatter': 'verbose'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            # Either replace 'mail_admins' by 'sentry' or use both if you want
            'handlers': ['sentry'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'app.mailinglists': {
            'handlers': ['sentry', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'handlers': ['sentry'],
            'level': 'WARNING',
            'propagate': True,
        }
    },
}

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

SOUTH_MIGRATION_MODULES = {
    'page': 'migrations.page',
    'medialibrary': 'migrations.medialibrary', 
    'auth': 'migrations.auth',
}

ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": "app.should_show_toolbar"
}

#EMAIL_BACKEND = 'django_ses.SESBackend'

try:
    from local_settings import *
except ImportError:
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    ADMINS = [user.split(":") for user in os.environ.get("ADMINS", "").split(";")]

DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_STORAGE_BUCKET_NAME = 'elvegris'
AWS_CALLING_FORMAT = 2

AWS_HEADERS = {
    'Cache-Control': 'max-age=86400',
}
