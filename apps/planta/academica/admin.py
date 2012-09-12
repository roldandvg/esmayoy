#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from planta.academica.models import Profesion, Condicion_Profesor, Profesor, Profesor_Carrera, Profesor_Disponibilidad

class ProfesionAdmin(admin.ModelAdmin):
    list_display = ('cod_profesion', 'profesion')
    list_filter = ('cod_profesion', 'profesion')
    search_fields = ('profesion',)
    
class Condicion_ProfesorAdmin(admin.ModelAdmin):
    list_display = ('cod_condicion', 'des_condicion', 'carga_horaria', 'observacion', 'estatus')
    list_filter = ('cod_condicion', 'estatus')
    search_fields = ('des_condicion',)
    
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('cod_profesor', 'cedula', 'primerapellido', 'segundoapellido', 'primernombre', 'segundonombre', 'carga_horaria', 'correo', 'telefono', 'movil', 'profesion', 'condicion')
    list_filter = ('cedula', 'primerapellido', 'segundoapellido', 'primernombre', 'segundonombre', 'profesion')
    search_fields = ('cedula',)
    
class Profesor_CarreraAdmin(admin.ModelAdmin):
    list_display = ('profesor', 'fasignacion', 'carrera_sede', 'estatus', 'observaciones')
    list_filter = ('fasignacion', 'estatus', 'profesor')
    search_fields = ('profesor', 'fasignacion',)
    
class Profesor_DisponibilidadAdmin(admin.ModelAdmin):
    list_display = ('fasignacion', 'profesor', 'dia', 'turno', 'nro_horas', 'estatus', 'observacion')
    list_filter = ('fasignacion', 'estatus', 'profesor', 'dia', 'turno')
    search_fields = ('profesor', 'fasignacion', 'dia', 'turno',)

admin.site.register(Profesion, ProfesionAdmin)
admin.site.register(Condicion_Profesor, Condicion_ProfesorAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Profesor_Carrera, Profesor_CarreraAdmin)
admin.site.register(Profesor_Disponibilidad, Profesor_DisponibilidadAdmin)