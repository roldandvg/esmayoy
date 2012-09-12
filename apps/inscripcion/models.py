#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from academico.models import Alumno, Anualidad, Trimestre
from unidadcurricular.models import Unidad_Curricular, Modulo_Curricular
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from django.utils.translation import ugettext as _
from comun.disparadores import dispararEvento

class Estatus_Inscanual(models.Model):
    estatus = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=45)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Estatus de Inscripción Anual")
        verbose_name_plural = _(u"Estatus de Inscripciones Anuales")
        
    def datos(self):
        cadena = "estatus=%s, descripcion=%s" % (self.pk, self.descripcion)
        return [cadena, self.usuarioreg.username, "Estatus_Inscanual"]
    
class Estatus_Insctrimestral(models.Model):
    estatus = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=45)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        return u"%s" % (self.descripcion)
    
    class Meta:
        verbose_name = _(u"Estatus de Inscripción Trimestral")
        verbose_name_plural = _(u"Estatus de Inscripciones Trimestrales")
        
    def datos(self):
        cadena = "estatus=%s, descripcion=%s" % (self.pk, self.descripcion)
        return [cadena, self.usuarioreg.username, "Estatus_Insctrimestral"]

class Inscripcion_Anual(models.Model):
    seccion = models.CharField(max_length=2)
    nota = models.IntegerField()
    asistencia = models.IntegerField()
    estatus = models.ForeignKey(Estatus_Inscanual, db_column="estatus")
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    anualidad = models.ForeignKey(Anualidad, db_column="idanualidad")
    unidad = models.ForeignKey(Unidad_Curricular, db_column="id_unidad")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Inscripción Anual")
        verbose_name_plural = _(u"Inscripciones Anuales")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, nota=%s, asistencia=%s, estatus=%s, " % (self.pk, self.seccion, self.nota, self.asistencia, self.estatus.estatus)
        cadena+= "alumno=%s, anualidad=%s, unidad=%s" % (self.alumno.cod_alumno, self.anualidad.idanualidad, self.unidad.id_unidad)
        return [cadena, self.usuarioreg.username, "Inscripcion_Anual"]
        
class Historico_Inscanual(models.Model):
    seccion = models.CharField(max_length=2)
    nota = models.IntegerField()
    asistencia = models.IntegerField()
    estatus = models.ForeignKey(Estatus_Inscanual, db_column="estatus")
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    anualidad = models.ForeignKey(Anualidad, db_column="idanualidad")
    unidad = models.ForeignKey(Unidad_Curricular, db_column="id_unidad")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Histórico de Inscripción Anual")
        verbose_name_plural = _(u"Histórico de Inscripciones Anuales")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, nota=%s, asistencia=%s, estatus=%s, " % (self.pk, self.seccion, self.nota, self.asistencia, self.estatus.estatus)
        cadena+= "alumno=%s, anualidad=%s, unidad=%s" % (self.alumno.cod_alumno, self.anualidad.idanualidad, self.unidad.id_unidad)
        return [cadena, self.usuarioreg.username, "Historico_Inscanual"]
        
class Hito(models.Model):
    seccion = models.CharField(max_length=2)
    nota = models.IntegerField()
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    inscripcion_anual = models.ForeignKey(Inscripcion_Anual, db_column="idinscranual")
    modulo_curricular = models.ForeignKey(Modulo_Curricular, db_column="id_modulo")
    estatus = models.ForeignKey(Estatus_Inscanual, db_column="estatus")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Hito")
        verbose_name_plural = _(u"Hitos")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, nota=%s, alumno=%s, " % (self.pk, self.seccion, self.nota, self.alumno.cod_alumno)
        cadena+= "inscripcion_anual=%s, modulo_curricular=%s, estatus=%s, " % (self.inscripcion_anual.id, self.modulo_curricular.cod_modulo, self.estatus.estatus)
        cadena+= "trimestre=%s" % self.trimestre
        return [cadena, self.usuarioreg.username, "Hito"]
        
class Historico_Hito(models.Model):
    seccion = models.CharField(max_length=2)
    nota = models.IntegerField()
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    historico_inscanual = models.ForeignKey(Historico_Inscanual, db_column="hist_inscranual")
    modulo_curricular = models.ForeignKey(Modulo_Curricular, db_column="id_modulo")
    estatus = models.ForeignKey(Estatus_Inscanual, db_column="estatus")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Histórico de Hito")
        verbose_name_plural = _(u"Histórico de Hitos")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, nota=%s, alumno=%s, " % (self.pk, self.seccion, self.nota, self.alumno.cod_alumno)
        cadena+= "historico_inscanual=%s, modulo_curricular=%s, " % (self.historico_inscanual.id, self.modulo_curricular.cod_modulo)
        cadena+= "estatus=%s, trimestre=%s" % (self.estatus.estatus, self.trimestre)
        return [cadena, self.usuarioreg.username, "Historico_Hito"]
        
class Inscripcion_Trimestral(models.Model):
    seccion = models.CharField(max_length=2)
    nota = models.IntegerField()
    asistencia = models.IntegerField()
    estatus = models.ForeignKey(Estatus_Insctrimestral, db_column="estatus")
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    inscripcion_anual = models.ForeignKey(Inscripcion_Anual, db_column="idinscranual")
    modulo_curricular = models.ForeignKey(Modulo_Curricular, db_column="id_modulo")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Inscripción Anual")
        verbose_name_plural = _(u"Inscripciones Anuales")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, nota=%s, asistencia=%s, estatus=%s, " % (self.pk, self.seccion, self.nota, self.asistencia, self.estatus.estatus)
        cadena+= "alumno=%s, inscripcion_anual=%s, modulo_curricular=%s, " % (self.alumno.cod_alumno, self.inscripcion_anual.id, self.modulo_curricular.cod_modulo)
        cadena+= "trimestre=%s" % self.trimestre.idtrimestre
        return [cadena, self.usuarioreg.username, "Inscripcion_Trimestral"]
        
class Historico_Insctrimestral(models.Model):
    seccion = models.CharField(max_length=2)
    nota = models.IntegerField()
    asistencia = models.IntegerField()
    estatus = models.ForeignKey(Estatus_Insctrimestral, db_column="estatus")
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    historico_inscanual = models.ForeignKey(Historico_Inscanual, db_column="idinscranual")
    unidad_curricular = models.ForeignKey(Unidad_Curricular, db_column="id_unidad")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        verbose_name = _(u"Histórico de Inscripción Trimestral")
        verbose_name_plural = _(u"Histórico de Inscripciones Trimestrales")
        
    def datos(self):
        cadena = "id=%s, seccion=%s, nota=%s, asistencia=%s, estatus=%s, " % (self.pk, self.seccion, self.nota, self.asistencia, self.estatus.estatus)
        cadena+= "alumno=%s, historico_inscanual=%s, " % (self.alumno.cod_alumno, self.historico_inscanual.id)
        cadena+= "unidad_curricular=%s, trimestre=%s" % (self.unidad_curricular.id_unidad, self.trimestre.idtrimestre)
        return [cadena, self.usuarioreg.username, "Historico_Insctrimestral"]
    
#Dispara el registro de eventos para el modelo de Estatus_Inscanual
post_save.connect(dispararEvento,Estatus_Inscanual,post_save)
post_delete.connect(dispararEvento, Estatus_Inscanual, post_delete)
#Dispara el registro de eventos para el modelo de Estatus_Insctrimestral
post_save.connect(dispararEvento,Estatus_Insctrimestral,post_save)
post_delete.connect(dispararEvento, Estatus_Insctrimestral, post_delete)
#Dispara el registro de eventos para el modelo de Inscripcion_Anual
post_save.connect(dispararEvento,Inscripcion_Anual,post_save)
post_delete.connect(dispararEvento, Inscripcion_Anual, post_delete)
#Dispara el registro de eventos para el modelo de Historico_Inscanual
post_save.connect(dispararEvento,Historico_Inscanual,post_save)
post_delete.connect(dispararEvento, Historico_Inscanual, post_delete)
#Dispara el registro de eventos para el modelo de Hito
post_save.connect(dispararEvento,Hito,post_save)
post_delete.connect(dispararEvento, Hito, post_delete)
#Dispara el registro de eventos para el modelo de Historico_Hito
post_save.connect(dispararEvento,Historico_Hito,post_save)
post_delete.connect(dispararEvento, Historico_Hito, post_delete)
#Dispara el registro de eventos para el modelo de Inscripcion_Trimestral
post_save.connect(dispararEvento,Inscripcion_Trimestral,post_save)
post_delete.connect(dispararEvento, Inscripcion_Trimestral, post_delete)
#Dispara el registro de eventos para el modelo de Historico_Insctrimestral
post_save.connect(dispararEvento,Historico_Insctrimestral,post_save)
post_delete.connect(dispararEvento, Historico_Insctrimestral, post_delete)