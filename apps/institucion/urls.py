# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación institucion
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'institucion.views.inicio', name=_(u'inicio')),
    url(r'^sede/?$', 'institucion.views.registrarSede', name=_(u'registros sedes')),
    url(r'^dpto/?$', 'institucion.views.registrarDpto', name=_(u'registros departamentos')),
    url(r'^carrera/?$', 'institucion.views.registrarCarrera', name=_(u'registros de carreras')),
    url(r'^carrsede/?$', 'institucion.views.registrarCarrSed', name=_(u'registros de carreras por sede')),
)