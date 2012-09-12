#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from django.utils.translation import ugettext as _

class Pais(models.Model):
    nombre = models.CharField(max_length=100)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = _(u"Paises")
        
    def datos(self):
        cadena = "id=%s, nombre=%s" % (self.pk, self.nombre)
        return [cadena, self.usuarioreg.username, "Pais"]

class Estado(models.Model):
    id = models.CharField(max_length=2, primary_key=True)
    nombre = models.CharField(max_length=50)
    pais = models.ForeignKey(Pais,db_column='pais_id')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')

    def __unicode__(self):
        return self.nombre

    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = _(u"Estados")
        
    def datos(self):
        cadena = "id=%s, nombre=%s, pais=%s" % (self.pk, self.nombre, self.pais.id)
        return [cadena, self.usuarioreg.username, "Estado"]

class Municipio(models.Model):
    id = models.CharField(max_length=4, primary_key=True)
    nombre = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado,db_column='estado_id')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = _(u"Municipios")
        
    def datos(self):
        cadena = "id=%s, nombre=%s, estado=%s" % (self.pk, self.nombre, self.estado.id)
        return [cadena, self.usuarioreg.username, "Municipio"]

class Parroquia(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    nombre = models.CharField(max_length=80)
    municipio = models.ForeignKey(Municipio, db_column='municipio_id')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')

    def __unicode__(self):
        return self.nombre
    
    class Meta:
        ordering = ["nombre"]
        verbose_name_plural = _(u"Parroquias")
        
    def datos(self):
        cadena = "id=%s, nombre=%s, municipio=%s" % (self.pk, self.nombre, self.municipio.id)
        return [cadena, self.usuarioreg.username, "Parroquia"]


class Imagen(models.Model):
    def custom_upload_to(self, filename):
        """
        @note: Función que permite crear dinámicamente la ruta en donde será almacenada la imagen
        @license: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg@gmail.com
        @date: 2010-07-14
        @return: Retorna la ruta en donde será almacenada la imagen de acuerdo al nombre especificado
        """
        return '/media/uploads/%s/%s' % ('academico', filename)
    imagen = models.ImageField(upload_to="/media/uploads/")

class HistoricoRegistros(models.Model):
    modelo = models.CharField(max_length=40)
    fecha = models.DateField(auto_now_add=True)
    operacion = models.CharField(max_length=10)
    datos = models.TextField()
    usuario = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return "%s %s %s" % (self.modelo, self.operacion, self.datos)
    
    class Meta:
        ordering = ["modelo"]
        verbose_name = _(u"Histórico de Registro")
        verbose_name_plural = _(u"Histórico de Registros")

from comun.disparadores import dispararEvento
#Dispara el registro de eventos para el modelo de Pais
post_save.connect(dispararEvento,Pais,post_save)
post_delete.connect(dispararEvento, Pais, post_delete)
#Dispara el registro de eventos para el modelo de Estado
post_save.connect(dispararEvento,Estado,post_save)
post_delete.connect(dispararEvento, Estado, post_delete)
#Dispara el registro de eventos para el modelo de Municipio
post_save.connect(dispararEvento,Municipio,post_save)
post_delete.connect(dispararEvento, Municipio, post_delete)
#Dispara el registro de eventos para el modelo de Parroquia
post_save.connect(dispararEvento,Parroquia,post_save)
post_delete.connect(dispararEvento, Parroquia, post_delete)