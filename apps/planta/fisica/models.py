#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from comun.disparadores import dispararEvento

class Tipo_Aula(models.Model):
    descripcion = models.CharField(max_length=100)
    estatus = models.BooleanField()
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Tipo de aula")
        verbose_name_plural = _(u"Tipos de aulas")
        
    def datos(self):
        cadena = "id=%s, descripcion=%s, estatus=%s" % (self.pk, self.descripcion, self.estatus)
        return [cadena, self.usuarioreg.username, "Tipo_Aula"]
        
class Tipo_Edificio(models.Model):
    descripcion = models.CharField(max_length=80)
    estatus = models.BooleanField()
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Tipo de edificio")
        verbose_name_plural = _(u"Tipos de edificios")
        
    def datos(self):
        cadena = "id=%s, descripcion=%s, estatus=%s" % (self.pk, self.descripcion, self.estatus)
        return [cadena, self.usuarioreg.username, "Tipo_Edificio"]
        
class Edificio(models.Model):
    cod_edif = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=100)
    nro_aulas = models.IntegerField()
    observaciones = models.CharField(max_length=250, null=True)
    estatus = models.BooleanField()
    tipo_edificio = models.ForeignKey(Tipo_Edificio, db_column="tipo_edif")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s %s" % (self.cod_edif, self.descripcion, self.observaciones)
    
    class Meta:
        verbose_name = _(u"Edificio")
        verbose_name_plural = _(u"Edificios")
        
    def datos(self):
        cadena = "cod_edif=%s, descripcion=%s, nro_aulas=%s, observaciones=%s, estatus=%s, tipo_edificio=%s" % (self.pk, self.descripcion, self.nro_aulas,
                                                                                                                self.observaciones, self.estatus,
                                                                                                                self.tipo_edificio.id)
        return [cadena, self.usuarioreg.username, "Edificio"]
        
class Aula(models.Model):
    cod_aula = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=45)
    capacidad = models.IntegerField()
    observaciones = models.CharField(max_length=200)
    estatus = models.BooleanField()
    edificio = models.ForeignKey(Edificio, db_column="idedificios")
    tipo_aula = models.ForeignKey(Tipo_Aula, db_column="idtipo_aulas")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s %s" % (self.cod_aula, self.descripcion, self.observaciones)
    
    class Meta:
        verbose_name = _(u"Aula")
        verbose_name_plural = _(u"Aulas")
        
    def datos(self):
        cadena = "cod_aula=%s, descripcion=%s, capacidad=%s, observaciones=%s, estatus=%s, edificio=%s, tipo_aula=%s" % (self.pk, self.descripcion, self.capacidad,
                                                                                                                         self.observaciones, self.estatus,
                                                                                                                         self.edificio.cod_edif,self.tipo_aula.id)
        return [cadena, self.usuarioreg.username, "Aula"]
        
class Aula_Carrera(models.Model):
    observaciones = models.CharField(max_length=50, null=True)
    fecha_asignacion = models.DateField()
    lu = models.BooleanField(default=False)
    ma = models.BooleanField(default=False)
    mi = models.BooleanField(default=False)
    ju = models.BooleanField(default=False)
    vi = models.BooleanField(default=False)
    sa = models.BooleanField(default=False)
    do = models.BooleanField(default=False)
    estatus = models.BooleanField()
    aula = models.ForeignKey(Aula, db_column="idaulas")
    carrera_sede = models.ForeignKey(Carrera_Sede, db_column="id_carrerasede")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.observaciones)
    
    class Meta:
        verbose_name = _(u"Aula por Carrera")
        verbose_name_plural = _(u"Aulas por Carreras")
        
    def datos(self):
        cadena = "id=%s, observaciones=%s, fecha_asignacion=%s, lu=%s, ma=%s, " % (self.pk, self.observaciones, self.fecha_asignacion, self.lu, self.ma)
        cadena+= "mi=%s, ju=%s, vi=%s, sa=%s, do=%s, estatus=%s, aula=%s, carrera_sede=%s" % (self.mi, self.ju, self.vi, self.sa, self.do, self.estatus, 
                                                                                              self.aula.cod_aula, self.carrera_sede.id)
        return [cadena, self.usuarioreg.username, "Aula_Carrera"]
        
#Dispara el registro de eventos para el modelo de Tipo_Aula
post_save.connect(dispararEvento,Tipo_Aula,post_save)
post_delete.connect(dispararEvento, Tipo_Aula, post_delete)
#Dispara el registro de eventos para el modelo de Tipo_Edificio
post_save.connect(dispararEvento,Tipo_Edificio,post_save)
post_delete.connect(dispararEvento, Tipo_Edificio, post_delete)
#Dispara el registro de eventos para el modelo de Edificio
post_save.connect(dispararEvento,Edificio,post_save)
post_delete.connect(dispararEvento, Edificio, post_delete)
#Dispara el registro de eventos para el modelo de Aula
post_save.connect(dispararEvento,Aula,post_save)
post_delete.connect(dispararEvento, Aula, post_delete)
#Dispara el registro de eventos para el modelo de Aula_Carrera
post_save.connect(dispararEvento,Aula_Carrera,post_save)
post_delete.connect(dispararEvento, Aula_Carrera, post_delete)