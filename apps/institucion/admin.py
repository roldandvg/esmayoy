#!/usr/bin/env python
# -*- coding: utf-8 -*-
from institucion.models import Sede, Departamento, Carrera, Carrera_Sede

from django.contrib import admin

admin.site.register(Sede)
admin.site.register(Departamento)
admin.site.register(Carrera)
admin.site.register(Carrera_Sede)