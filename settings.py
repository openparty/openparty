# Django settings for openparty project.
import os.path
PROJECT_PATH = os.path.dirname(__file__)

# Add all third party vendor dependencies to project's path:
# so we can load it without install them
import sys
if not 'vendor' in sys.path:
    sys.path.append('vendor')
if not '.' in sys.path:
    sys.path.append('.')

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'   # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'openparty' # Or path to database file if using sqlite3.
DATABASE_USER = 'root'      # Not used with sqlite3.
DATABASE_PASSWORD = ''      # Not used with sqlite3.
DATABASE_HOST = 'localhost' # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''          # Set to empty string for default. Not used with sqlite3.

EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
# EMAIL_USE_TLS = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')x_^bgbj$v_r-5=rn&01pm-5*%szlnc+8^3kh4$^$#z-gn5yo#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    # "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
)

LOGIN_URL = '/login'

ROOT_URLCONF = 'openparty.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.comments',
    'django.contrib.markup',
    #TODO: take the unittest framework back
    # 'openparty.dependencies.ameba.django.unittest',
    'south',
    'apps.core',
    'apps.member',
    'apps.twitter',
)

# One-week activation window; you may, of course, use a different value.
ACCOUNT_ACTIVATION_DAYS = 7
SITE_URL = 'http://app.beijing-open-party.org'

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
INTERNAL_IPS = ('127.0.0.1')

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
