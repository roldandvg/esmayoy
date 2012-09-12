#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _

urlpatterns = patterns('',
    url(r'^login/?$', 'usuario.views.acceso', name=_(u'acceso al sistema')),
    url(r'^logout/?$', 'usuario.views.salir', name=_(u'salida del sistema')),
    url(r'^seguridad/?$', 'usuario.views.registrarSeguridadIngAlumnos', name=_(u'registro de seguridad de inscripción de alumnos')),
    url(r'^seguridad/inicio/?$', 'usuario.views.inicio', name=_(u'página de inicio del módulo de seguridad')),
    url(r'^permisos/?$', 'usuario.views.registrarPermisosUsuario', name=_(u'registros de permisos otorgados a los usuarios')),
    url(r'^usuario/?$', 'usuario.views.registrarUsuario', name=_(u'registros de usuarios')),
    url(r'^password/?$', 'usuario.views.registrarModContrasenha', name=_(u'registros de modificación de contraseña')),
)