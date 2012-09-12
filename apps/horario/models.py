#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from planta.fisica.models import Aula
from planificacion.models import Planificacion_Unidad
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from django.utils.translation import ugettext as _
from comun.disparadores import dispararEvento

class Turno(models.Model):
    id_turno = models.CharField(max_length=2, primary_key=True)
    des_turno = models.CharField(max_length=45)
    observaciones = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField()
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.des_turno, self.observaciones)
    
    class Meta:
        verbose_name = _(u"Turno")
        verbose_name_plural = _(u"Turnos")
        ordering = ["des_turno"]
        
    def datos(self):
        cadena = "id_turno=%s, des_turno=%s, observaciones=%s, estatus=%s" % (self.pk, self.des_turno, self.observaciones, self.estatus)
        return [cadena, self.usuarioreg.username, "Turno"]
        
class Hora(models.Model):
    id_hora = models.CharField(max_length=8, primary_key=True)
    des_hora = models.CharField(max_length=45)
    observacion = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField()
    horaini = models.TimeField()
    horafin = models.TimeField()
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.des_hora, self.observacion)
    
    class Meta:
        verbose_name = _(u"Hora")
        verbose_name_plural = _(u"Horas")
        ordering = ["des_hora"]
        
    def datos(self):
        cadena = "id_hora=%s, des_hora=%s, observacion=%s, estatus=%s, horaini=%s, horafin=%s" % (self.pk, self.des_hora, self.observacion, self.estatus,
                                                                                                  self.horaini, self.horafin)
        return [cadena, self.usuarioreg.username, "Hora"]
        
class Dia(models.Model):
    id_dia = models.CharField(max_length=2, primary_key=True)
    des_dia = models.CharField(max_length=20)
    observacion = models.CharField(max_length=250, null=True)
    estatus = models.BooleanField()
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.des_dia, self.observacion)
    
    class Meta:
        verbose_name = _(u"Día")
        verbose_name_plural = _(u"Días")
        ordering = ["des_dia"]
        
    def datos(self):
        cadena = "id_dia=%s, des_dia=%s, observacion=%s, estatus=%s" % (self.pk, self.des_dia, self.observacion, self.estatus)
        return [cadena, self.usuarioreg.username, "Dia"]
        
class Modalidad_Horario(models.Model):
    idmodalidad_horario = models.CharField(max_length=2, primary_key=True)
    des_modalidad = models.CharField(max_length=45)
    observacion = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField()
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.des_modalidad, self.observacion)
    
    class Meta:
        verbose_name = _(u"Modalidad de Horario")
        verbose_name_plural = _(u"Modalidades de Horarios")
        ordering = ["des_modalidad"]
        
    def datos(self):
        cadena = "idmodalidad_horario=%s, des_modalidad=%s, observacion=%s, estatus=%s" % (self.pk, self.des_modalidad, self.observacion, self.estatus)
        return [cadena, self.usuarioreg.username, "Modalidad_Horario"]
        
class Horario(models.Model):
    idhorario = models.CharField(max_length=4, primary_key=True)
    observacion = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField()
    dia = models.ForeignKey(Dia, db_column="id_dia")
    hora = models.ForeignKey(Hora, db_column="id_hora")
    modalidad_horario = models.ForeignKey(Modalidad_Horario, db_column="idmodalidad_horario")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.observacion)
    
    class Meta:
        verbose_name = _(u"Horario")
        verbose_name_plural = _(u"Horarios")
        
    def datos(self):
        cadena = "idhorario=%s, observacion=%s, estatus=%s, dia=%s, hora=%s, modalidad_horario=%s" % (self.pk, self.observacion, self.estatus, self.dia.id_dia,
                                                                                                      self.hora.id_hora, self.modalidad_horario.idmodalidad_horario)
        return [cadena, self.usuarioreg.username, "Horario"]
        
class Horario_Trimestral(models.Model):
    fregistro = models.DateField()
    estatus = models.BooleanField(default=False)
    planificacion_unidad = models.ForeignKey(Planificacion_Unidad, db_column="idplanificacionunidad")
    aula = models.ForeignKey(Aula, db_column="idaula")
    horario = models.ForeignKey(Horario, db_column="idhorario")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
        
    class Meta:
        verbose_name = _(u"Horario Trimestral")
        verbose_name_plural = _(u"Horarios Trimestrales")
        
    def datos(self):
        cadena = "id=%s, fregistro=%s, estatus=%s, planificacion_unidad=%s, aula=%s, horario=%s" % (self.pk, self.fregistro, self.estatus, 
                                                                                                    self.planificacion_unidad.id, self.aula.cod_aula, 
                                                                                                    self.horario.idhorario)
        return [cadena, self.usuarioreg.username, "Horario_Trimestral"]
    
#Dispara el registro de eventos para el modelo de Turno
post_save.connect(dispararEvento,Turno,post_save)
post_delete.connect(dispararEvento, Turno, post_delete)
#Dispara el registro de eventos para el modelo de Hora
post_save.connect(dispararEvento,Hora,post_save)
post_delete.connect(dispararEvento, Hora, post_delete)
#Dispara el registro de eventos para el modelo de Dia
post_save.connect(dispararEvento,Dia,post_save)
post_delete.connect(dispararEvento, Dia, post_delete)
#Dispara el registro de eventos para el modelo de Modalidad_Horario
post_save.connect(dispararEvento,Modalidad_Horario,post_save)
post_delete.connect(dispararEvento, Modalidad_Horario, post_delete)
#Dispara el registro de eventos para el modelo de Horario
post_save.connect(dispararEvento,Horario,post_save)
post_delete.connect(dispararEvento, Horario, post_delete)
#Dispara el registro de eventos para el modelo de Horario_Trimestral
post_save.connect(dispararEvento,Horario_Trimestral,post_save)
post_delete.connect(dispararEvento, Horario_Trimestral, post_delete)