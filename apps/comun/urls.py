#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación común
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'comun.views.auditoriaLogs', name=_(u'logs')),
    url(r'^academico/?$', 'comun.views.auditoriaLogsAcademico', name=_(u'logs del módulo académico')),
    url(r'^configuracion/?$', 'comun.views.auditoriaLogsConfiguracion', name=_(u'logs del módulo configuración')),
    url(r'^horario/?$', 'comun.views.auditoriaLogsHorario', name=_(u'logs del módulo horario')),
    url(r'^inscripcion/?$', 'comun.views.auditoriaLogsInscripcion', name=_(u'logs del módulo inscripción')),
    url(r'^institucion/?$', 'comun.views.auditoriaLogsInstitucion', name=_(u'logs del módulo institución')),
    url(r'^planificacion/?$', 'comun.views.auditoriaLogsPlanificacion', name=_(u'logs del módulo planificación')),
    url(r'^planta/academica/?$', 'comun.views.auditoriaLogsPlantaAca', name=_(u'logs del módulo planta académica')),
    url(r'^planta/fisica/?$', 'comun.views.auditoriaLogsPlantaFis', name=_(u'logs del módulo planta física')),
    url(r'^seguridad/?$', 'comun.views.auditoriaLogsSeguridad', name=_(u'logs del módulo seguridad')),
    url(r'^unidadcurr/?$', 'comun.views.auditoriaLogsUnidadCurr', name=_(u'logs del módulo unidad curricular')),
    url(r'^general/?$', 'comun.views.auditoriaLogsGeneral', name=_(u'logs generales del sistema')),
    url(r'^set_imagen/?$', 'comun.views.setImagen', name=_(u'subir imágenes al servidor')),
)