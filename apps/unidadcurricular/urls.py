# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación unidadcurricular
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'unidadcurricular.views.inicio', name=_(u'inicio')),
    url(r'^pensum/?$', 'unidadcurricular.views.registrarPensum', name=_(u'registro de pensum')),
    url(r'^ejecurr/?$', 'unidadcurricular.views.registrarEjeCurr', name=_(u'registro del eje curricular')),
    url(r'^conduni/?$', 'unidadcurricular.views.registrarCondUnidad', name=_(u'registro de la condición de la unidad curricular')),
    url(r'^tipounicurr/?$', 'unidadcurricular.views.registrarTipoUnidCurr', name=_(u'registro de los tipos de unidad curricular')),
    url(r'^unidadcurr/?$', 'unidadcurricular.views.registrarUnidadCurr', name=_(u'registro de la unidad curricular')),
    url(r'^prelacion/?$', 'unidadcurricular.views.registrarPrelacion', name=_(u'registro de prelaciones')),
    url(r'^modcurr/?$', 'unidadcurricular.views.registrarModuloCurricular', name=_(u'registro de módulo curricular')),
)