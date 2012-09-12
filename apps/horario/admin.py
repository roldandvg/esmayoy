#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from horario.models import Turno, Hora, Dia, Modalidad_Horario, Horario

admin.site.register(Turno)
admin.site.register(Hora)
admin.site.register(Dia)
admin.site.register(Modalidad_Horario)
admin.site.register(Horario)