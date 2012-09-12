#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from institucion.models import Carrera_Sede
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from comun.disparadores import dispararEvento

class Pensum(models.Model):
    """
    @note: Clase que contiene el modelo para los pensum de estudio por sede y carrera
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_pensum = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=50)
    finicio = models.DateField()
    ffinal = models.DateField()
    cal_min = models.IntegerField()
    cal_max = models.IntegerField()
    cal_apro = models.IntegerField()
    observaciones = models.CharField(max_length=200, null=True)
    estatus = models.BooleanField(default=True)
    carrerasede = models.ForeignKey(Carrera_Sede, db_column='id_carrerasede')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s %s" % (self.descripcion, self.observaciones)
    
    class Meta:
        verbose_name = _(u"Pensum de Estudio")
        verbose_name_plural = _(u"Pensums de Estudio")
        
    def datos(self):
        cadena = "cod_pensum=%s, descripcion=%s, finicio=%s, ffinal=%s, cal_min=%s, " % (self.pk, self.descripcion, self.finicio, self.ffinal, self.cal_min)
        cadena+= "cal_max=%s, cal_apro=%s, observaciones=%s, estatus=%s, carrerasede=%s" % (self.cal_max, self.cal_apro, self.observaciones, self.estatus,
                                                                                            self.carrerasede.id)
        return [cadena, self.usuarioreg.username, "Pensum"]
        
class Eje_Curricular(models.Model):
    """
    @note: Clase que contiene el modelo de los ejes curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_eje = models.CharField(max_length=3, primary_key=True)
    descripcion = models.CharField(max_length=150)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Eje Curricular")
        verbose_name_plural = _(u"Ejes Curriculares")
        ordering = ["descripcion"]
        
    def datos(self):
        cadena = "cod_eje=%s, descripcion=%s" % (self.pk, self.descripcion)
        return [cadena, self.usuarioreg.username, "Eje_Curricular"]
        
class Condicion_Unidad(models.Model):
    """
    @note: Clase que contiene el modelo para las condiciones de las unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cond_unidad = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=100)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Condición de la Unidad Curricular")
        verbose_name_plural = _(u"Condiciones de las Unidades Curriculares")
        ordering = ["descripcion"]
        
    def datos(self):
        cadena = "cond_unidad=%s, descripcion=%s" % (self.pk, self.descripcion)
        return [cadena, self.usuarioreg.username, "Condicion_Unidad"]
        
class Tipo_Unidad(models.Model):
    """
    @note: Clase que contiene el modelo para los tipos de unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    descripcion = models.CharField(max_length=100)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Tipo de Unidad Curricular")
        verbose_name_plural = _(u"Tipos de Unidades Curriculares")
        ordering = ["descripcion"]
        
    def datos(self):
        cadena = "id=%s, descripcion=%s" % (self.pk, self.descripcion)
        return [cadena, self.usuarioreg.username, "Tipo_Unidad"]
        
class Unidad_Curricular(models.Model):
    """
    @note: Clase que contiene el modelo de las Unidades Curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    id_unidad = models.IntegerField(primary_key=True)
    cod_unidad = models.CharField(max_length=15)
    nombre = models.CharField(max_length=80)
    ucr = models.IntegerField(max_length=3)
    pre_ucr = models.IntegerField(max_length=3)
    obligatoria = models.BooleanField(default=True)
    trayecto = models.CharField(max_length=3)
    trimestre = models.CharField(max_length=3, null=True)
    cant_mod = models.IntegerField()
    estatus = models.BooleanField(default=True)
    hilo = models.BooleanField(default=True)
    pensum = models.ForeignKey(Pensum, db_column='id_pensum')
    condicionunidad = models.ForeignKey(Condicion_Unidad, db_column='cond_unidad')
    ejecurricular = models.ForeignKey(Eje_Curricular, db_column='cod_eje')
    tipounidad = models.ForeignKey(Tipo_Unidad, db_column='id_tipounidad')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.nombre)
    
    class Meta:
        verbose_name = _(u"Unidad Curricular")
        verbose_name_plural = _(u"Unidades Curriculares")
        ordering = ["nombre"]
        
    def datos(self):
        cadena = "id_unidad=%s, cod_unidad=%s, nombre=%s, ucr=%s, pre_ucr=%s, " % (self.pk, self.cod_unidad, self.nombre, self.ucr, self.pre_ucr)
        cadena+= "obligatoria=%s, trayecto=%s, trimestre=%s, cant_mod=%s, estatus=%s, " % (self.obligatoria,self.trayecto,self.trimestre,self.cant_mod,self.estatus)
        cadena+= "hilo=%s, pensum=%s, condicionunidad=%s, ejecurricular=%s, tipounidad=%s" % (self.hilo, self.pensum.cod_pensum, self.condicionunidad.cond_unidad,
                                                                                              self.ejecurricular.cod_eje, self.tipounidad.id)
        return [cadena, self.usuarioreg.username, "Unidad_Curricular"]
    
class Prelacion(models.Model):
    """
    @note: Clase que contiene el modelo para las prelaciones de las unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_prela = models.IntegerField(primary_key=True)
    estatus = models.BooleanField(default=True)
    unidadcurricular = models.ForeignKey(Unidad_Curricular, db_column='id_unidad')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Prelación")
        verbose_name_plural = _(u"Prelaciones")
        
    def datos(self):
        cadena = "cod_prela=%s, estatus=%s, unidadcurricular=%s" % (self.pk, self.estatus, self.unidadcurricular.id_unidad)
        return [cadena, self.usuarioreg.username, "Prelacion"]
        
class Modulo_Curricular(models.Model):
    """
    @note: Clase que contiene el modelo para los módulos de las unidades curriculares
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg@gmail.com
    """
    cod_modulo = models.CharField(max_length=15, primary_key=True)
    nombre = models.CharField(max_length=250)
    ucr = models.IntegerField()
    trayecto = models.CharField(max_length=3)
    trimestre = models.CharField(max_length=3)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2)
    estatus = models.BooleanField(default=True)
    unidadcurricular = models.ForeignKey(Unidad_Curricular, db_column='cod_unidad')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.nombre)
    
    class Meta:
        verbose_name = _(u"Módulo Curricular")
        verbose_name_plural = _(u"Módulos Curriculares")
        ordering = ["nombre"]
        
    def datos(self):
        cadena = "cod_modulo=%s, nombre=%s, ucr=%s, trayecto=%s, trimestre=%s, " % (self.pk, self.nombre, self.ucr, self.trayecto, self.trimestre)
        cadena+= "porcentaje=%s, estatus=%s, unidadcurricular=%s" % (self.porcentaje, self.estatus, self.unidadcurricular.id_unidad)
        return [cadena, self.usuarioreg.username, "Modulo_Curricular"]
    
#Dispara el registro de eventos para el modelo de Pensum
post_save.connect(dispararEvento,Pensum,post_save)
post_delete.connect(dispararEvento, Pensum, post_delete)
#Dispara el registro de eventos para el modelo de Eje_Curricular
post_save.connect(dispararEvento,Eje_Curricular,post_save)
post_delete.connect(dispararEvento, Eje_Curricular, post_delete)
#Dispara el registro de eventos para el modelo de Condicion_Unidad
post_save.connect(dispararEvento,Condicion_Unidad,post_save)
post_delete.connect(dispararEvento, Condicion_Unidad, post_delete)
#Dispara el registro de eventos para el modelo de Tipo_Unidad
post_save.connect(dispararEvento,Tipo_Unidad,post_save)
post_delete.connect(dispararEvento, Tipo_Unidad, post_delete)
#Dispara el registro de eventos para el modelo de Unidad_Curricular
post_save.connect(dispararEvento,Unidad_Curricular,post_save)
post_delete.connect(dispararEvento, Unidad_Curricular, post_delete)
#Dispara el registro de eventos para el modelo de Prelacion
post_save.connect(dispararEvento,Prelacion,post_save)
post_delete.connect(dispararEvento, Prelacion, post_delete)
#Dispara el registro de eventos para el modelo de Modulo_Curricular
post_save.connect(dispararEvento,Modulo_Curricular,post_save)
post_delete.connect(dispararEvento, Modulo_Curricular, post_delete)