"""
Django settings for LZK project.

Generated by 'django-admin startproject' using Django 2.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import saml2
import saml2.attributemaps
import saml2.saml
from django.urls import reverse_lazy as reverse
from django.utils.translation import gettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = False

ALLOWED_HOSTS = []

INTERNAL_IPS = []


# Application definition

INSTALLED_APPS = [
    "LZK",
    "LZK.private",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "psqlextra",
    "compressor",
    "crispy_forms",
    "django_extensions",
    "djangosaml2",
    "guardian",
    "polymorphic",
    "reversion",
    "rules.apps.AutodiscoverRulesConfig",
    "taggit",
    "ordered_model",
    "imagekit",
    "django_tables2",
    "haystack",
    "analytical",
    "rest_framework",
    "django_filters",
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "LZK.middleware.LanguageSelectorMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "djangosaml2.middleware.SamlSessionMiddleware",
]

ROOT_URLCONF = "LZK.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.i18n",
                "django.template.context_processors.tz",
                "django.template.context_processors.csrf",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "LZK.context_processors.login_url",
                "LZK.context_processors.copyright",
                "LZK.context_processors.top_downloads",
            ]
        },
    }
]

WSGI_APPLICATION = "LZK.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
ATOMIC_REQUESTS = True

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTH_USER_MODEL = "LZK.User"


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "de"

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_FINDERS = (
    "LZK.finders.SystemFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "node_modules"),
]

SYSTEM_STATIC_PATHS = {
    "bootstrap/": (
        "/usr/share/sass/bootstrap",
        "/usr/share/nodejs/bootstrap",
    ),
    "fonts-fork-awesome/": ("/usr/share/fonts-fork-awesome",),
    "jquery/": ("/usr/share/javascript/jquery",),
    "popper/": ("/usr/share/nodejs/popper.js/dist/umd",),
    "ckeditor/": ("/usr/share/javascript/ckeditor",),
    "flags/": ("/usr/share/iso-flags-svg/country-squared",),
}

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

HAYSTACK_CONNECTIONS = {
    #'default': {
    #    'ENGINE': 'xapian_backend.XapianEngine',
    #    'PATH': os.path.join(os.path.dirname(__file__), 'xapian_index'),
    # },
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        "PATH": os.path.join(BASE_DIR, "index"),
    },
}
HAYSTACK_SIGNAL_PROCESSOR = "LZK.haystack.SignalProcessor"

COMPRESS_PRECOMPILERS = [("text/x-scss", "LZK.compressor.DjangoSassCompiler")]

LOGIN_URL = reverse("login")
LOGIN_REDIRECT_URL = reverse("private:index")
LOGOUT_REDIRECT_URL = reverse("index")

SAML_CREATE_UNKNOWN_USER = True
SAML_ATTRIBUTE_MAPPING = {
    "uid": ("username",),
    "mail": ("email",),
    "givenName": ("first_name",),
    "sn": ("last_name",),
}
SAML_LOGOUT_REQUEST_PREFERRED_BINDING = saml2.BINDING_HTTP_POST
SAML_IGNORE_LOGOUT_ERRORS = True
SAML_CONFIG = {
    # full path to the xmlsec1 binary programm
    "xmlsec_binary": "/usr/bin/xmlsec1",
    # your entity id, usually your subdomain plus the url to the metadata view
    "entityid": "http://localhost:8000/saml2/metadata/",
    # directory with attribute mapping
    "attribute_map_dir": os.path.dirname(saml2.attributemaps.__file__),
    # this block states what services we provide
    "service": {
        # we are just a lonely SP
        "sp": {
            "name": "Federated Django sample SP",
            "name_id_format": saml2.saml.NAMEID_FORMAT_PERSISTENT,
            "endpoints": {
                # url and binding to the assetion consumer service view
                # do not change the binding or service name
                "assertion_consumer_service": [
                    ("http://localhost:8000/saml2/acs/", saml2.BINDING_HTTP_POST)
                ],
                # url and binding to the single logout service view
                # do not change the binding or service name
                "single_logout_service": [
                    ("http://localhost:8000/saml2/ls/", saml2.BINDING_HTTP_REDIRECT),
                    ("http://localhost:8000/saml2/ls/post", saml2.BINDING_HTTP_POST),
                ],
            },
            # attributes that this project need to identify a user
            "required_attributes": ["uid"],
            # attributes that may be useful to have but not required
            "optional_attributes": ["eduPersonAffiliation"],
            # in this section the list of IdPs we talk to are defined
            "idp": {
                # we do not need a WAYF service since there is
                # only an IdP defined here. This IdP should be
                # present in our metadata
                # the keys of this dictionary are entity ids
                "https://localhost/simplesaml/saml2/idp/metadata.php": {
                    "single_sign_on_service": {
                        saml2.BINDING_HTTP_REDIRECT: "https://localhost/simplesaml/saml2/idp/SSOService.php"
                    },
                    "single_logout_service": {
                        saml2.BINDING_HTTP_REDIRECT: "https://localhost/simplesaml/saml2/idp/SingleLogoutService.php"
                    },
                }
            },
        }
    },
    # where the remote metadata is stored
    "metadata": {"local": [os.path.join(BASE_DIR, "remote_metadata.xml")]},
    # set to 1 to output debugging information
    "debug": 1,
    # Signing
    "key_file": os.path.join(BASE_DIR, "mycert.key"),  # private part
    "cert_file": os.path.join(BASE_DIR, "mycert.pem"),  # public part
    # Encryption
    "encryption_keypairs": [
        {
            "key_file": os.path.join(BASE_DIR, "my_encryption_key.key"),  # private part
            "cert_file": os.path.join(
                BASE_DIR, "my_encryption_cert.pem"
            ),  # public part
        }
    ],
    # own metadata settings
    "contact_person": [
        {
            "given_name": "Lorenzo",
            "sur_name": "Gil",
            "company": "Yaco Sistemas",
            "email_address": "lgs@yaco.es",
            "contact_type": "technical",
        },
        {
            "given_name": "Angel",
            "sur_name": "Fernandez",
            "company": "Yaco Sistemas",
            "email_address": "angel@yaco.es",
            "contact_type": "administrative",
        },
    ],
    # you can set multilanguage information here
    "organization": {
        "name": [("Yaco Sistemas", "es"), ("Yaco Systems", "en")],
        "display_name": [("Yaco", "es"), ("Yaco", "en")],
        "url": [("http://www.yaco.es", "es"), ("http://www.yaco.com", "en")],
    },
    "valid_for": 24,  # how long is our metadata valid
}

AUTHENTICATION_BACKENDS = (
    "rules.permissions.ObjectPermissionBackend",
    "guardian.backends.ObjectPermissionBackend",
    "django.contrib.auth.backends.ModelBackend",
    "djangosaml2.backends.Saml2Backend",
)
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CRISPY_TEMPLATE_PACK = "bootstrap4"
DJANGO_TABLES2_TEMPLATE = "LZK/table.html"

RQ_QUEUES = {}

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
}

if "DJANGO_LOCAL_CONFIGURATION" in os.environ:
    filename = os.path.abspath(os.environ.get("DJANGO_LOCAL_CONFIGURATION"))
    if os.access(filename, os.R_OK):
        with open(filename) as config:
            code = compile(config.read(), filename, "exec")
            exec(code, globals(), locals())
