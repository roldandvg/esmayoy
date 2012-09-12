#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

"""
@note: Variable que contiene las URL de la aplicación academico
@author: T.S.U. Roldan D. Vargas G.
@contact: roldandvg at gmail.com
"""
urlpatterns = patterns('academico.views',
    (r'^inicio/?$', 'inicio'),
    (r'^alumno/?$', 'registrarAlumno'),
    (r'^datsoceco/?$', 'registrarDatosocioecon'),
    (r'^documento/?$', 'registrarDocumento'),
    (r'^recdocs/?$', 'registrarRecdoc'),
    (r'^tipotri/?$', 'registrarTipotrime'),
    (r'^trimestre/?$', 'registrarTrimestre'),
    (r'^datosaca/?$', 'registrarDatosaca'),
    (r'^anualidad/?$', 'registrarAnualidad'),
    (r'^anualidad/carrera/?$', 'registrarAnualidadCarrera'),
    (r'^anualidad/trimestre/?$', 'registrarAnualidadTriCarrera'),
)