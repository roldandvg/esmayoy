#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from comun.models import Pais, Estado, Municipio, Parroquia

admin.site.register(Pais)
admin.site.register(Estado)
admin.site.register(Municipio)
admin.site.register(Parroquia)