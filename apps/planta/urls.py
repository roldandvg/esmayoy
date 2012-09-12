# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación planta
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'planta.views.inicio', name=_(u'inicio')),
    url(r'^academica/profesion/?$', 'planta.academica.views.registrarProfesion', name=_(u'registro de profesiones')),
    url(r'^academica/condprof/?$', 'planta.academica.views.registrarCondProfesor', name=_(u'registro de condiciones de los profesores')),
    url(r'^academica/profesor/?$', 'planta.academica.views.registrarProfesor', name=_(u'registro de profesores')),
    url(r'^academica/profesorcarr/?$', 'planta.academica.views.registrarProfCarrera', name=_(u'registro de profesores por carrera')),
    url(r'^academica/profesordisp/?$', 'planta.academica.views.registrarProfDisponibilidad', name=_(u'registro de disponibilidad de profesores')),
    url(r'^fisica/tipoaula/?$', 'planta.fisica.views.registrarTipoAula', name=_(u'registro de tipo de aulas')),
    url(r'^fisica/tipoedificio/?$', 'planta.fisica.views.registrarTipoEdificio', name=_(u'registro de tipo de edificios')),
    url(r'^fisica/edificio/?$', 'planta.fisica.views.registrarEdificio', name=_(u'registro de edificios')),
    url(r'^fisica/aula/?$', 'planta.fisica.views.registrarAula', name=_(u'registro de aulas')),
    url(r'^fisica/aulacarrera/?$', 'planta.fisica.views.registrarAulaCarrera', name=_(u'registro de aulas por carreras')),
)