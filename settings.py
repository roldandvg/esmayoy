#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Configuración Django para el proyecto esmayoy
from django import VERSION as djversion
import os, sys
from gnupg import *

gpg = GPG(gnupghome="/home/"+os.environ['USER']+"/")
PATH = os.path.dirname(__file__)
reload(sys)
sys.setdefaultencoding("utf-8")

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('T.S.U. Roldan D. Vargas G.', 'roldandvg@gmail.com'),
    ('T.S.U. Oscar Lobo', 'oscarescalando@gmail.com'),
    ('T.S.U. Susana Sánchez', 'misuchajeemichu@gmail.com'),
    ('T.S.U. Jannet Peréz', 'tennajjan@gmail.com'),
    ('T.S.U. Tatiana Rondón', 'taticarolirondon@gmail.com'),
)

MANAGERS = ADMINS

basedatos = open("apps/configuracion/databasesign.txt","rb")
descifrar = gpg.decrypt(basedatos.read()) #en caso de haber configurado una contraseña se requiere agregar la variable passphrase=contraseña-clave-privada
firma = gpg.verify(descifrar.data)

if firma.valid:
    NAMEDB = descifrar.data.splitlines()[5] #asigna el nombre de la base de datos
    USERDB = descifrar.data.splitlines()[6] #asigna el nombre del usuario que conecta a la base de datos
    PASSDB = descifrar.data.splitlines()[7] #asigna la contraseña de conexión a la base de datos
    HOSTDB = descifrar.data.splitlines()[3] #asigna el nombre del servidor de base de datos
    PORTDB = int(descifrar.data.splitlines()[4]) #asigna el puerto de conexión del servidor de base de datos
else:
    NAMEDB = ''
    USERDB = ''
    PASSDB = ''
    HOSTDB = ''
    PORTDB = ''

if djversion[0]==1 and djversion[1]==2:
    DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    DATABASE_NAME     = NAMEDB
    DATABASE_USER     = USERDB
    DATABASE_PASSWORD = PASSDB
    DATABASE_HOST     = HOSTDB
    DATABASE_PORT     = PORTDB
else:
    DATABASES = {
        'default': {
             'ENGINE': 'django.db.backends.postgresql_psycopg2', # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
             'NAME': NAMEDB,
             'USER': USERDB,
             'PASSWORD': PASSDB,
             'HOST': HOSTDB,
             'PORT': PORTDB,
        },
        'slave': {
            'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': PATH + '/esmayoy.db',                      # Or path to database file if using sqlite3.
            'USER': '',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',
        },
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Caracas'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'es-ve'

LANGUAGES = (
    ('es', 'Español'),
    ('en', 'Inglés'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = os.path.join(PATH, "media")

FONTH_PATH = os.path.join(PATH, "media/fonts")
IMAGES_PATH = os.path.join(PATH, "media/images")

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')zo=b4)fmuui2b2-c_z+gpyz0!&k1j9xh01@cg3p*9ltq5*n0$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'esmayoy.urls'

TEMPLATE_DIRS = (
    os.path.join(PATH, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'comun',
    'institucion',
    'academico',
    'unidadcurricular',
    'usuario',
    'horario',
    'planta.academica',
    'planta.fisica',
    'planificacion',
    'inscripcion',
    'configuracion',
    'dajax',
)

DAJAX_MEDIA_PREFIX = "dajax"
DAJAX_JS_FRAMEWORK = "jQuery"
DAJAX_FUNCTIONS = (
    'academico.ajax.buscarAlumno',
    'academico.ajax.mostrarDatosAlumno',
    'comun.ajax.cargarEstados',
    'comun.ajax.cargarMunicipios',
    'comun.ajax.cargarParroquias',
    'comun.ajax.eliminarRegistro',
    'usuario.ajax.habilitarFechas',
    'usuario.ajax.habilitarCant',
    'usuario.ajax.reloadCaptcha',
    'usuario.ajax.mostrarDatosUsuario',
    'institucion.ajax.mostrarDatosSede',
    'institucion.ajax.mostrarDatosDpto',
    'institucion.ajax.mostrarDatosCarrera',
    'institucion.ajax.mostrarDatosCarreraSede',
    'unidadcurricular.ajax.mostrarDatosPensum',
    'unidadcurricular.ajax.mostrarDatosEje',
    'unidadcurricular.ajax.mostrarDatosCondicion',
    'unidadcurricular.ajax.mostrarDatosTipoUnidad',
    'unidadcurricular.ajax.mostrarDatosUnidad',
    'unidadcurricular.ajax.mostrarDatosPrelacion',
    'unidadcurricular.ajax.mostrarDatosModulocurr',
)

LOGIN_URL = "/login/"
LOGOUT_URL = "/"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
