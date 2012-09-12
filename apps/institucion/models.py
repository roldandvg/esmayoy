#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from django.utils.translation import ugettext as _
from comun.disparadores import dispararEvento

class Sede(models.Model):
    """
    @note: Clase que contiene el modelo para las sedes de la institución
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_sede = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100, null=True)
    telefonos = models.CharField(max_length=80, null=True)
    fcreacion = models.DateField(null=True)
    contacto = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=50, null=True)
    estatus = models.BooleanField(default=True)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s %s" % (self.descripcion, self.direccion, self.contacto)
    
    class Meta:
        verbose_name = _(u"Sede")
        verbose_name_plural = _(u"Sedes")
        
    def datos(self):
        cadena = "cod_sede=%s, descripcion=%s, direccion=%s, telefonos=%s, " % (self.pk, self.descripcion, self.direccion, self.telefonos)
        cadena+= "fcreacion=%s, contacto=%s, email=%s, estatus=%s" % (self.fcreacion, self.contacto, self.email, self.estatus)
        return [cadena, self.usuarioreg.username, "Sede"]

class Departamento(models.Model):
    """
    @note: Clase que contiene el modelo para los diferentes departamentos de la institución
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_dep = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=100)
    contacto = models.CharField(max_length=45, null=True)
    estatus = models.BooleanField(default=True)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.descripcion, self.contacto)
    
    class Meta:
        verbose_name = _(u"Departamento")
        verbose_name_plural = _(u"Departamentos")
        
    def datos(self):
        cadena = "cod_dep=%s, descripcion=%s, contacto=%s, estatus=%s" % (self.pk, self.descripcion, self.contacto, self.estatus)
        return [cadena, self.usuarioreg.username, "Departamento"]
    
class Carrera(models.Model):
    """
    @note: Clase que contiene el modelo para las diferentes carreras ofertadas por la institución
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_carrera = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=100)
    estatus = models.BooleanField(default=True)
    departamento = models.ForeignKey(Departamento, db_column="cod_dep")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Carrera")
        verbose_name_plural = _(u"Carreras")
        
    def datos(self):
        cadena = "cod_carrera=%s, descripcion=%s, estatus=%s, departamento=%s" % (self.pk, self.descripcion, self.estatus, self.departamento.cod_dep)
        return [cadena, self.usuarioreg.username, "Carrera"]
    
class Carrera_Sede(models.Model):
    """
    @note: Clase que contiene el modelo para las diferentes carreras ofertadas por cada sede
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    nro_carnet = models.IntegerField(max_length=20)
    cant_carnet = models.IntegerField(max_length=20)
    format_carnet = models.IntegerField(max_length=2)
    prefijo_sede = models.BooleanField(default=False)
    prefijo_carrera = models.BooleanField(default=False)
    sede = models.ForeignKey(Sede, db_column="cod_sede")
    carrera = models.ForeignKey(Carrera, db_column="cod_carrera")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Carrera por Sede")
        verbose_name_plural = _(u"Carreras por Sedes")
        
    def datos(self):
        cadena = "id=%s, nro_carnet=%s, cant_carnet=%s, format_carnet=%s, prefijo_sede=%s, " % (self.pk, self.nro_carnet, self.cant_carnet, self.format_carnet, self.prefijo_sede)
        cadena+= "prefijo_carrera=%s, sede=%s, carrera=%s" % (self.prefijo_carrera, self.sede.cod_sede, self.carrera.cod_carrera)
        return [cadena, self.usuarioreg.username, "Carrera_Sede"]
        
#Dispara el registro de eventos para el modelo de Sede
post_save.connect(dispararEvento,Sede, post_save)
post_delete.connect(dispararEvento, Sede, post_delete)
#Dispara el registro de eventos para el modelo de Departamento
post_save.connect(dispararEvento,Departamento, post_save)
post_delete.connect(dispararEvento, Departamento, post_delete)
#Dispara el registro de eventos para el modelo de Carrera
post_save.connect(dispararEvento,Carrera, post_save)
post_delete.connect(dispararEvento, Carrera, post_delete)
#Dispara el registro de eventos para el modelo de Carrera_Sede
post_save.connect(dispararEvento,Carrera_Sede, post_save)
post_delete.connect(dispararEvento, Carrera_Sede, post_delete)