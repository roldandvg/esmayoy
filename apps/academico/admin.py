#!/usr/bin/env python
# -*- coding: utf-8 -*-
__license__   = "GPL v2"
__copyright__ = "Copyleft (C) 2010, Proyecto ESMAYOY"
__author__    = "T.S.U. Roldan D. Vargas G. - roldandvg@gmail.com"

from django.contrib import admin
from academico.models import Alumno, DatoSocioeconomico, Documento, Dato_Documento, Titulo_Bachiller, Condicion_Ingreso, Sistema_Estudio, Tipo_Trimestre, Trimestre, Dato_Academico, Anualidad, Anualidad_Carrera, Anualidad_Tri_Carrera, Condicion_Estudiante, Expediente, Expediente_Anualidad

class AlumnoAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('cod_alumno', 'nacionalidad', 'cedula', 'primerapellido', 'primernombre', 'segundoapellido', 'segundonombre')
    list_filter = ('sexo', 'lugar_nacimiento', 'carrera_sede')
    search_fields = ('cedula', 'primerapellido', 'segundoapellido', 'primernombre', 'segundonombre')
    
class DatoSocioeconomicoAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de datos socio-económicos del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_filter = ('trabaja', 'discapacidad', 'indigena')

class DocumentoAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de documentos para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('descripcion', 'observaciones', 'estatus')
    list_filter = ('estatus',)
    search_fields = ('descripcion',)
    
class Dato_DocumentoAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de recepción de documentos del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('alumno', 'documento', 'entregado')
    list_filter = ('entregado', 'alumno')
    search_fields = ('alumno',)
    
class Titulo_BachillerAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo del título de bachiller para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('cod_bachiller', 'descripcion')
    list_filter = ('cod_bachiller', 'descripcion')
    search_fields = ('descripcion',)
    
class Condicion_IngresoAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de condición de ingreso del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('cod_ingreso', 'descripcion')
    list_filter = ('cod_ingreso', 'descripcion')
    search_fields = ('descripcion',)
    
class Sistema_EstudioAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de sistema de estudio del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('cod_sest', 'descripcion')
    list_filter = ('cod_sest', 'descripcion')
    search_fields = ('descripcion',)
    
class Tipo_TrimestreAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo del tipo de trimestre para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('cod_tipotri', 'tipotrimestre')
    list_filter = ('cod_tipotri', 'tipotrimestre')
    search_fields = ('tipotrimestre',)
    
class TrimestreAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo del trimestre para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('tipotrimestre', 'idtrimestre', 'descripcion', 'finicio', 'fculmina', 'estatus', 'observaciones')
    list_filter = ('tipotrimestre', 'finicio', 'fculmina', 'estatus')
    search_fields = ('descripcion',)
    
class Dato_AcademicoAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de datos académicos del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_filter = ('fingreso', 'alumno', 'parroquia', 'profesional')
    
class Condicion_EstudianteAdmin(admin.ModelAdmin):
    """
    @note: Clase que contiene el modelo de la condición del alumno para el panel administrativo
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    list_display = ('cod_condest', 'des_condicion')
    search_fields = ('des_descripcion')

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(DatoSocioeconomico, DatoSocioeconomicoAdmin)
admin.site.register(Documento, DocumentoAdmin)
admin.site.register(Dato_Documento, Dato_DocumentoAdmin)
admin.site.register(Titulo_Bachiller, Titulo_BachillerAdmin)
admin.site.register(Condicion_Ingreso, Condicion_IngresoAdmin)
admin.site.register(Sistema_Estudio, Sistema_EstudioAdmin)
admin.site.register(Tipo_Trimestre, Tipo_TrimestreAdmin)
admin.site.register(Trimestre, TrimestreAdmin)
admin.site.register(Dato_Academico, Dato_AcademicoAdmin)
admin.site.register(Anualidad)
admin.site.register(Anualidad_Carrera)
admin.site.register(Anualidad_Tri_Carrera)
admin.site.register(Condicion_Estudiante)
admin.site.register(Expediente)
admin.site.register(Expediente_Anualidad)