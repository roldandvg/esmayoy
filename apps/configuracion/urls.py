#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

"""
@note: Variable que contiene las URL de la aplicación configuración
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg@gmail.com
"""
urlpatterns = patterns('',
    url(r'^inicio/?$', 'configuracion.views.inicio', name=_(u'inicio')),
    url(r'^parametro/?$', 'configuracion.views.registrarParametro', name=_(u'registro de parámetros de configuración')),
)