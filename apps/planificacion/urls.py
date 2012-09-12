# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación planificacion
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'planificacion.views.inicio', name=_(u'inicio')),
    url(r'^planificar/?$', 'planificacion.views.registrarPlanificacion', name=_(u'registro de la planificación')),
    url(r'^planificar/unidad/?$', 'planificacion.views.registrarPlanificacionUnidad', name=_(u'registro de la planificación de Unidades Curriculares')),
)