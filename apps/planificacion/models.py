#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from institucion.models import Carrera
from academico.models import Anualidad_Tri_Carrera
from unidadcurricular.models import Modulo_Curricular
from planta.academica.models import Profesor
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from comun.disparadores import dispararEvento

class Planificacion(models.Model):
    descripcion = models.CharField(max_length=255)
    fregistro = models.DateField()
    observaciones = models.CharField(max_length=255, null=True)
    anualidad_trimestre = models.ForeignKey(Anualidad_Tri_Carrera, db_column="idanualidadtrimestre")
    carrera = models.ForeignKey(Carrera, db_column="cod_carrera")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.descripcion, self.observaciones)
    
    class Meta:
        verbose_name = _(u"Planificación")
        verbose_name_plural = _(u"Planificaciones")
        
    def datos(self):
        cadena = "id=%s, descripcion=%s, fregistro=%s, observaciones=%s, anualidad_trimestre=%s, carrera=%s" % (self.pk, self.descripcion, self.fregistro,
                                                                                                                self.observaciones, 
                                                                                                                self.anualidad_trimestre.idanualidadtrimestre,
                                                                                                                self.carrera.cod_carrera)
        return [cadena, self.usuarioreg.username, "Planificacion"]
        
class Planificacion_Unidad(models.Model):
    seccion = models.CharField(max_length=2)
    cant_alumnos = models.IntegerField()
    cupo = models.IntegerField()
    observaciones = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField(default=False)
    planificacion = models.ForeignKey(Planificacion, db_column="idplanificacion")
    profesor = models.ForeignKey(Profesor, db_column="cod_profesor")
    modulo = models.ForeignKey(Modulo_Curricular, db_column="id_modulo")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.observaciones)
    
    class Meta:
        verbose_name = _(u"Planificación de la Unidad")
        verbose_name_plural = _(u"Planificación de las Unidades")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, cant_alumnos=%s, cupo=%s, observaciones=%s, " % (self.pk, self.seccion, self.cant_alumnos, self.cupo, self.observaciones)
        cadena+= "estatus=%s, planificacion=%s, profesor=%s, modulo=%s" % (self.estatus, self.planificacion.id, self.profesor.cod_profesor, self.modulo.cod_modulo)
        return [cadena, self.usuarioreg.username, "Planificacion_Unidad"]
    
#Dispara el registro de eventos para el modelo de Planificacion
post_save.connect(dispararEvento,Planificacion,post_save)
post_delete.connect(dispararEvento, Planificacion, post_delete)
#Dispara el registro de eventos para el modelo de Planificacion_Unidad
post_save.connect(dispararEvento,Planificacion_Unidad,post_save)
post_delete.connect(dispararEvento, Planificacion_Unidad, post_delete)