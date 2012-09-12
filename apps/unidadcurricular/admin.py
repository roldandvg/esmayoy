#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unidadcurricular.models import Pensum, Eje_Curricular, Condicion_Unidad, Tipo_Unidad, Unidad_Curricular, Prelacion, Modulo_Curricular

from django.contrib import admin

admin.site.register(Pensum)
admin.site.register(Eje_Curricular)
admin.site.register(Condicion_Unidad)
admin.site.register(Tipo_Unidad)
admin.site.register(Unidad_Curricular)
admin.site.register(Prelacion)
admin.site.register(Modulo_Curricular)