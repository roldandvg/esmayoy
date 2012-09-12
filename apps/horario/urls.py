# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación horario
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'horario.views.inicio', name=_(u'inicio')),
    url(r'^turno/?$', 'horario.views.registrarTurno', name=_(u'registro de turnos')),
    url(r'^hora/?$', 'horario.views.registrarHora', name=_(u'registro de horas')),
    url(r'^dia/?$', 'horario.views.registrarDia', name=_(u'registro de días')),
    url(r'^modalidad/?$', 'horario.views.registrarModhorario', name=_(u'registro de modalidades de horario')),
    url(r'^horario/?$', 'horario.views.registrarHorario', name=_(u'registro de horario')),
    url(r'^horario/trimestre?$', 'horario.views.registrarHorarioTrimestral', name=_(u'registro de horario trimestral')),
)
