#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from comun.disparadores import dispararEvento

class Profesion(models.Model):
    cod_profesion = models.CharField(max_length=3, primary_key=True)
    profesion = models.CharField(max_length=100)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.profesion)
    
    class Meta:
        verbose_name = _(u"Profesión")
        verbose_name_plural = _(u"Profesiones")
        ordering = ["profesion"]
        
    def datos(self):
        cadena = "cod_profesion=%s, profesion=%s" % (self.pk, self.profesion)
        return [cadena, self.usuarioreg.username, "Profesion"]
        
class Condicion_Profesor(models.Model):
    cod_condicion = models.CharField(max_length=2, primary_key=True)
    des_condicion = models.CharField(max_length=60)
    carga_horaria = models.IntegerField()
    observacion = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField(default=False)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.des_condicion, self.observacion)
    
    class Meta:
        verbose_name = _(u"Condición del Profesor")
        verbose_name_plural = _(u"Condiciones de los Profesores")
        ordering = ["des_condicion"]
        
    def datos(self):
        cadena = "cod_condicion=%s, des_condicion=%s, carga_horaria=%s, observacion=%s, estatus=%s" % (self.pk, self.des_condicion, self.carga_horaria,
                                                                                                       self.observacion, self.estatus)
        return [cadena, self.usuarioreg.username, "Condicion_Profesor"]
        
class Profesor(models.Model):
    cod_profesor = models.CharField(max_length=10, primary_key=True)
    cedula = models.CharField(max_length=10)
    primerapellido = models.CharField(max_length=30)
    segundoapellido = models.CharField(max_length=30, null=True)
    primernombre = models.CharField(max_length=30)
    segundonombre = models.CharField(max_length=30, null=True)
    carga_horaria = models.IntegerField(null=True)
    foto = models.ImageField(upload_to="uploads", null=True)
    correo = models.EmailField(max_length=100, null=True)
    telefono = models.CharField(max_length=45, null=True)
    movil = models.CharField(max_length=45, null=True)
    profesion = models.ForeignKey(Profesion, db_column="cod_profesion")
    condicion = models.ForeignKey(Condicion_Profesor, db_column="cod_condicion")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s %s %s" % (self.primerapellido, self.segundoapellido, self.primernombre, self.segundonombre)
    
    class Meta:
        verbose_name = _(u"Profesor")
        verbose_name_plural = _(u"Profesores")
        ordering = ["primerapellido", "segundoapellido", "primernombre", "segundonombre"]
        
    def datos(self):
        cadena = "cod_profesor=%s, cedula=%s, primerapellido=%s, segundoapellido=%s, " % (self.pk, self.cedula, self.primerapellido, self.segundoapellido)
        cadena+= "primernombre=%s, segundonombre=%s, carga_horaria=%s, foto=%s, " % (self.primernombre, self.segundonombre, self.carga_horaria, self.foto)
        cadena+= "correo=%s, telefono=%s, movil=%s, profesion=%s, condicion=%s" % (self.correo, self.telefono, self.movil, self.profesion.cod_profesion, 
                                                                                   self.condicion.cod_condicion)
        return [cadena, self.usuarioreg.username, "Profesor"]
        
class Profesor_Carrera(models.Model):
    fasignacion = models.DateField()
    observaciones = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField()
    profesor = models.ForeignKey(Profesor, db_column="cod_profesor")
    carrera_sede = models.ForeignKey(Carrera_Sede, db_column="id_carrerasede")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.observaciones)
    
    class Meta:
        verbose_name = _(u"Profesor por Carrera")
        verbose_name_plural = _(u"Profesores por Carreras")
        
    def datos(self):
        cadena = "id=%s, fasignacion=%s, observaciones=%s, estatus=%s, profesor=%s, carrera_sede=%s" % (self.pk, self.fasignacion, self.observaciones, self.estatus,
                                                                                                        self.profesor.cod_profesor, self.carrera_sede.id)
        return [cadena, self.usuarioreg.username, "Profesor_Carrera"]

from horario.models import Dia, Turno

class Profesor_Disponibilidad(models.Model):
    nro_horas = models.IntegerField()
    fasignacion = models.DateField()
    observacion = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField()
    profesor = models.ForeignKey(Profesor, db_column="cod_profesor")
    dia = models.ForeignKey(Dia, db_column="id_dia")
    turno = models.ForeignKey(Turno, db_column="id_turno")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.observacion)
    
    class Meta:
        verbose_name = _(u"Disponibilidad de Profesor")
        verbose_name_plural = _(u"Disponibilidad de Profesores")
        ordering = ["fasignacion"]
        
    def datos(self):
        cadena = "id=%s, nro_horas=%s, fasignacion=%s, observacion=%s, estatus=%s, profesor=%s, dia=%s, turno=%s" % (self.pk, self.nro_horas, self.fasignacion,
                                                                                                                     self.observacion, self.estatus,
                                                                                                                     self.profesor.cod_profesor, self.dia.id_dia,
                                                                                                                     self.turno.id_turno)
        return [cadena, self.usuarioreg.username, "Profesor_Disponibilidad"]
    
#Dispara el registro de eventos para el modelo de Profesion
post_save.connect(dispararEvento,Profesion,post_save)
post_delete.connect(dispararEvento, Profesion, post_delete)
#Dispara el registro de eventos para el modelo de Condicion_Profesor
post_save.connect(dispararEvento,Condicion_Profesor,post_save)
post_delete.connect(dispararEvento, Condicion_Profesor, post_delete)
#Dispara el registro de eventos para el modelo de Profesor
post_save.connect(dispararEvento,Profesor,post_save)
post_delete.connect(dispararEvento, Profesor, post_delete)
#Dispara el registro de eventos para el modelo de Profesor_Carrera
post_save.connect(dispararEvento,Profesor_Carrera,post_save)
post_delete.connect(dispararEvento, Profesor_Carrera, post_delete)
#Dispara el registro de eventos para el modelo de Profesor_Disponibilidad
post_save.connect(dispararEvento,Profesor_Disponibilidad,post_save)
post_delete.connect(dispararEvento, Profesor_Disponibilidad, post_delete)