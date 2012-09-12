# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación inscripcion
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'inscripcion.views.inicio', name=_(u'inicio')),
    url(r'^estatus/anual/?$', 'inscripcion.views.registrarEstatusInscAnual', name=_(u'registro de estatus de inscripción anual')),
    url(r'^estatus/trimestral/?$', 'inscripcion.views.registrarEstatusInscTrimestral', name=_(u'registro de estatus de inscripción trimestral')),
    url(r'^anual/?$', 'inscripcion.views.registrarInscripcionAnual', name=_(u'registro de inscripciones anuales')),
    url(r'^trimestral/?$', 'inscripcion.views.registrarInscripcionTrimestral', name=_(u'registro de inscripciones trimestrales')),
    url(r'^hito/?$', 'inscripcion.views.registrarHito', name=_(u'registro de hitos')),
)