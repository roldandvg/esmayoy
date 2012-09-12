#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from planta.fisica.models import Tipo_Aula, Tipo_Edificio, Edificio, Aula, Aula_Carrera

class Tipo_AulaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('descripcion',)
    
class Tipo_EdificioAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('descripcion',)
    
class EdificioAdmin(admin.ModelAdmin):
    list_display = ('cod_edif', 'tipo_edificio', 'descripcion', 'nro_aulas', 'estatus', 'observaciones')
    list_filter = ('estatus', 'tipo_edificio')
    search_fields = ('descripcion',)
    
class AulaAdmin(admin.ModelAdmin):
    list_display = ('edificio', 'tipo_aula', 'cod_aula', 'descripcion', 'capacidad', 'estatus', 'observaciones')
    list_filter = ('edificio', 'tipo_aula', 'capacidad', 'estatus')
    search_fields = ('descripcion',)
    
class Aula_CarreraAdmin(admin.ModelAdmin):
    list_display = ('carrera_sede', 'aula', 'fecha_asignacion', 'estatus', 'lu', 'ma', 'mi', 'ju', 'vi', 'sa', 'do')
    list_filter = ('carrera_sede', 'aula', 'fecha_asignacion', 'estatus', 'lu', 'ma', 'mi', 'ju', 'vi', 'sa', 'do')
    search_fields = ('carrera_sede', 'aula',)

admin.site.register(Tipo_Aula, Tipo_AulaAdmin)
admin.site.register(Tipo_Edificio, Tipo_EdificioAdmin)
admin.site.register(Edificio, EdificioAdmin)
admin.site.register(Aula, AulaAdmin)
admin.site.register(Aula_Carrera, Aula_CarreraAdmin)