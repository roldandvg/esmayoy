#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from institucion.models import Carrera_Sede
from unidadcurricular.models import Pensum
from comun.models import Parroquia
from django.db.models.signals import post_save, post_delete
from django.dispatch import dispatcher
from comun.disparadores import dispararEvento
from django.utils.translation import ugettext as _

class Alumno(models.Model):
    """
    @note: Clase que contiene el modelo del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_alumno = models.CharField(max_length=10, primary_key=True)
    nacionalidad = models.CharField(max_length=1)
    cedula = models.CharField(max_length=10)
    primerapellido = models.CharField(max_length=30)
    segundoapellido = models.CharField(max_length=30, null=True)
    primernombre = models.CharField(max_length=30)
    segundonombre = models.CharField(max_length=30, null=True)
    sexo = models.CharField(max_length=1)
    fnacimiento = models.DateField()
    direccion = models.CharField(max_length=250)
    telefono = models.CharField(max_length=45, null=True)
    email = models.EmailField(max_length=100, null=True)
    movil = models.CharField(max_length=45, null=True)
    foto = models.ImageField(upload_to="uploads", null=True)
    ref_personal = models.CharField(max_length=100, null=True)
    tel_ref_personal = models.CharField(max_length=45, null=True)
    lugar_nacimiento = models.CharField(max_length=100, null=True)
    carrera_sede = models.ForeignKey(Carrera_Sede, db_column='id_carrerasede')
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s %s %s %s %s %s %s" % (self.primerapellido, self.segundoapellido, self.primernombre, self.segundonombre, self.direccion,
                                          self.ref_personal, self.lugar_nacimiento)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Alumno
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Alumno")
        verbose_name_plural = _(u"Alumnos")
        unique_together = (("cod_alumno","cedula"))
        ordering = ["primerapellido","segundoapellido","primernombre","segundonombre"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "cod_alumno=%s, nacionalidad=%s, cedula=%s, " % (self.cod_alumno, self.nacionalidad, self.cedula)
        cadena+= "primerapellido=%s, segundoapellido=%s, primernombre=%s, segundonombre=%s, " % (self.primerapellido, self.segundoapellido,
                                                                                                 self.primernombre, self.segundonombre)
        cadena+= "sexo=%s, fnacimiento=%s, direccion=%s, telefono=%s, email=%s, movil=%s, " % (self.sexo, self.fnacimiento, self.direccion, self.telefono,
                                                                                               self.email, self.movil)
        cadena+= "foto=%s, ref_personal=%s, tel_ref_personal=%s, lugar_nacimiento=%s, carrera_sede=%s" % (self.foto, self.ref_personal, self.tel_ref_personal,
                                                                                                          self.lugar_nacimiento, self.carrera_sede.id)
        return [cadena,self.usuarioreg, "Alumno"]

class DatoSocioeconomico(models.Model):
    """
    @note: Clase que contiene el modelo de los datos socio-económicos del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    nhijos = models.IntegerField(max_length=2, null=True, default=0)
    mtraslado = models.CharField(max_length=20, null=True)
    costeo_est = models.CharField(max_length=30, null=True)
    tipovivienda = models.CharField(max_length=20, null=True)
    cod_alojamiento = models.CharField(max_length=20, null=True)
    nivel_m = models.CharField(max_length=20, null=True)
    nivel_p = models.CharField(max_length=20, null=True)
    monto_ingreso = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    trabaja = models.BooleanField(default=False)
    tipo_empresa = models.CharField(max_length=20, null=True)
    empresa = models.CharField(max_length=80, null=True)
    direccion = models.CharField(max_length=200, null=True)
    telefonoe = models.CharField(max_length=45, null=True)
    discapacidad = models.BooleanField(default=False)
    des_discapacidad = models.CharField(max_length=80, null=True)
    indigena = models.BooleanField(default=False)
    observaciones = models.CharField(max_length=255, null=True)
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s %s %s %s %s %s %s %s %s %s %s" % (self.mtraslado, self.costeo_est, self.tipovivienda, self.cod_alojamiento,
                                                      self.nivel_m, self.nivel_p, self.tipo_empresa, self.empresa, self.direccion,
                                                      self.des_discapacidad, self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase DatoSocioeconomico
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Dato Socio-económico")
        verbose_name_plural = _(u"Datos Socio-económicos")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "id=%s, nhijos=%s, mtraslado=%s, costeo_est=%s, tipovivienda=%s, " % (self.pk, self.nhijos, self.mtraslado, self.costeo_est, self.tipovivienda)
        cadena+= "cod_alojamiento=%s, nivel_m=%s, nivel_p=%s, monto_ingreso=%s, " % (self.cod_alojamiento, self.nivel_m, self.nivel_p, self.monto_ingreso)
        cadena+= "trabaja=%s, tipo_empresa=%s, empresa=%s, direccion=%s, " % (self.trabaja, self.tipo_empresa, self.empresa, self.direccion)
        cadena+= "telefonoe=%s, discapacidad=%s, des_discapacidad=%s, indigena=%s, " % (self.telefonoe, self.discapacidad, self.des_discapacidad, self.indigena)
        cadena+= "observaciones=%s, alumno=%s" % (self.observaciones, self.alumno.cod_alumno)
        return [cadena, self.usuarioreg.username, "DatoSocioeconomico"]
    
class Documento(models.Model):
    """
    @note: Clase que contiene el modelo para los documentos exigidos por la institución
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    descripcion = models.CharField(max_length=100)
    observaciones = models.CharField(max_length=100, null=True)
    estatus = models.BooleanField(default=True)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s %s" % (self.descripcion, self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Documento
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Documento")
        verbose_name_plural = _(u"Documentos")
        ordering = ["descripcion"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "id=%s, descripcion=%s, observaciones=%s, estatus=%s" % (self.pk, self.descripcion, self.observaciones, self.estatus)
        return [cadena, self.usuarioreg.username, "Documento"]
    
class Dato_Documento(models.Model):
    """
    @note: Clase que contiene el modelo para los documentos consignados por el alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    entregado = models.BooleanField(default=False)
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    documento = models.ForeignKey(Documento, db_column="id_documento")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Dato_Documento
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Dato de Documento")
        verbose_name_plural = _(u"Datos de Documentos")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "id=%s, entregado=%s, alumno=%s, documento=%s" % (self.pk, self.entregado, self.alumno.cod_alumno, self.documento)
        return [cadena, self.usuarioreg.username, "Dato_Documento"]
    
class Titulo_Bachiller(models.Model):
    """
    @note: Clase que contiene el modelo para las especialidades del título de bachiller
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_bachiller = models.CharField(max_length=3, primary_key=True)
    descripcion = models.CharField(max_length=100, null=True)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.descripcion)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Titulo_Bachiller
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Título de Bachiller")
        verbose_name_plural = _(u"Títulos de Bachiller")
        ordering = ["descripcion"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "cod_bachiller=%s, descripcion=%s" % (self.cod_bachiller, self.descripcion)
        return [cadena, self.usuarioreg.username, "Titulo_Bachiller"]
    
class Condicion_Ingreso(models.Model):
    """
    @note: Clase que contiene el modelo para la condición de ingreso
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_ingreso = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=100)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.descripcion)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Condicion_Ingreso
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Condición de Ingreso")
        verbose_name_plural = _(u"Condiciones de Ingreso")
        ordering = ["descripcion"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "cod_ingreso=%s, descripcion=%s" % (self.cod_ingreso, self.descripcion)
        return [cadena, self.usuarioreg.username, "Condicion_Ingreso"]
    
class Sistema_Estudio(models.Model):
    """
    @note: Clase que contiene el modelo para el sistema de estudio
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_sest = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=100)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.descripcion)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Sistema_Estudio
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Sistema de Estudio")
        verbose_name_plural = _(u"Sistemas de Estudio")
        ordering = ["descripcion"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "cod_est=%s, descripcion=%s" % (self.cod_sest, self.descripcion)
        return [cadena, self.usuarioreg.username, "Sistema_Estudio"]
    
class Tipo_Trimestre(models.Model):
    """
    @note: Clase que contiene el modelo para el tipo de trimestre
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_tipotri = models.CharField(max_length=2, primary_key=True)
    tipotrimestre = models.CharField(max_length=150)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.tipotrimestre)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Tipo_Trimestre
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Tipo de Trimestre")
        verbose_name_plural = _(u"Tipos de Trimestre")
        ordering = ["tipotrimestre"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "cod_tipotri=%s, tipotrimestre=%s" % (self.cod_tipotri, self.tipotrimestre)
        return [cadena, self.usuarioreg.username, "Tipo_Trimestre"]
    
class Trimestre(models.Model):
    """
    @note: Clase que contiene el modelo para el trimestre
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idtrimestre = models.CharField(max_length=6, primary_key=True)
    descripcion = models.CharField(max_length=100)
    finicio = models.DateField()
    fculmina = models.DateField(null=True)
    observaciones = models.CharField(max_length=255)
    estatus = models.BooleanField()
    tipotrimestre = models.ForeignKey(Tipo_Trimestre, db_column="cod_tipotri")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s %s" % (self.descripcion, self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Trimestre
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Trimestre")
        verbose_name_plural = _(u"Trimestres")
        ordering = ["descripcion"]
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "idtrimestre=%s, descripcion=%s, finicio=%s, fculmina=%s, " % (self.idtrimestre, self.descripcion, self.finicio, self.fculmina)
        cadena+= "observaciones=%s, estatus=%s, tipotrimestre=%s" % (self.observaciones, self.estatus, self.tipotrimestre.cod_tipotri)
        return [cadena, self.usuarioreg.username, "Trimestre"]
    
class Dato_Academico(models.Model):
    """
    @note: Clase que contiene el modelo para los datos académicos del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    fingreso = models.DateField()
    observaciones = models.CharField(max_length=255, null=True)
    nliceo = models.CharField(max_length=200, null=True)
    tliceo = models.CharField(max_length=25, null=True)
    serialtitulo = models.CharField(max_length=50, null=True)
    profesional = models.BooleanField(default=False)
    parroquia = models.ForeignKey(Parroquia, db_column="cod_parroquia")
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    condicion_ingreso = models.ForeignKey(Condicion_Ingreso, db_column="cod_ingreso")
    sistema_estudio = models.ForeignKey(Sistema_Estudio, db_column="cod_sest")
    titulo_bachiller = models.ForeignKey(Titulo_Bachiller, db_column="cod_bachiller")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s %s %s %s" % (self.observaciones, self.nliceo, self.tliceo, self.serialtitulo)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Dato_Academico
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Dato Académico")
        verbose_name_plural = _(u"Datos Académicos")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "id=%s, fingreso=%s, observaciones=%s, nliceo=%s, tliceo=%s, " % (self.pk, self.fingreso, self.observaciones, self.nliceo, self.tliceo)
        cadena+= "serialtitulo=%s, profesional=%s, parroquia=%s, alumno=%s, " % (self.serialtitulo, self.profesional, self.parroquia.id, self.alumno.cod_alumno)
        cadena+= "trimestre=%s, condicion_ingreso=%s, " % (self.trimestre.idtrimestre, self.condicion_ingreso.cod_ingreso)
        cadena+= "sistema_estudio=%s, titulo_bachiller=%s" % (self.sistema_estudio.cod_sest, self.titulo_bachiller.cod_bachiller)
        return [cadena, self.usuarioreg.username, "Dato_Academico"]
        
class Anualidad(models.Model):
    """
    @note: Clase que contiene el modelo para las anualidades
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idanualidad = models.CharField(max_length=20, primary_key=True)
    descripcion = models.CharField(max_length=200)
    finicio = models.DateField(null=True)
    fculmina = models.DateField(null=True)
    observaciones = models.CharField(max_length=45, null=True)
    estatus = models.CharField(max_length=1) #estatus: (C)errado (A)ctivo (P)endiente
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s %s" % (self.descripcion, self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Anualidad
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Anualidad")
        verbose_name_plural = _(u"Anualidades")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "idanualidad=%s, descripcion=%s, finicio=%s, fculmina=%s, observaciones=%s, estatus=%s" % (self.idanualidad, self.descripcion, self.finicio,
                                                                                                            self.fculmina, self.observaciones, self.estatus)
        return [cadena, self.usuarioreg.username, "Anualidad"]
        
class Anualidad_Carrera(models.Model):
    """
    @note: Clase que contiene el modelo para las anualidades por carrera
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idanualidad_carrera = models.IntegerField(primary_key=True)
    observaciones = models.CharField(max_length=255, null=True)
    estatus = models.CharField(max_length=1) #estatus: (C)errado (A)ctivo (P)endiente
    anualidad = models.ForeignKey(Anualidad, db_column="idanualidad")
    carrerasede = models.ForeignKey(Carrera_Sede, db_column="id_carrerasede")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Anualidad_Carrera
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Anualidad por Carrera")
        verbose_name_plural = _(u"Anualidades por Carrera")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "idanualidad_carrera=%s, observaciones=%s, estatus=%s, anualidad=%s, carrerasede=%s" % (self.idanualidad_carrera, self.observaciones, self.estatus,
                                                                                                         self.anualidad, self.carrerasede.id)
        return [cadena, self.usuarioreg.username, "Anualidad_Carrera"]
        
class Anualidad_Tri_Carrera(models.Model):
    """
    @note: Clase que contiene el modelo para las anualidades trimestrales por carrera
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idanualidadtrimestre = models.IntegerField(primary_key=True)
    fregistro = models.DateField()
    observaciones = models.CharField(max_length=255, null=True)
    estatus = models.CharField(max_length=1)
    anualidad_carrera = models.ForeignKey(Anualidad_Carrera, db_column="idanualidad_carrera")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Anualidad_Tri_Carrera
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Anualidad de Trimestre por Carrera")
        verbose_name_plural = _(u"Anualidad de Trimestres por Carreras")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "idanualidadtrimestre=%s, fregistro=%s, observaciones=%s, " % (self.idanualidadtrimestre, self.fregistro, self.observaciones)
        cadena+= "estatus=%s, anualidad_carrera=%s, trimestre=%s" % (self.estatus, self.anualidad_carrera.idanualidad_carrera, self.trimestre.idtrimestre)
        return [cadena, self.usuarioreg.username, "Anualidad_Tri_Carrera"]

class Condicion_Estudiante(models.Model):
    """
    @note: Clase que contiene el modelo para la condición del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_condest = models.CharField(max_length=2, primary_key=True)
    des_condicion = models.CharField(max_length=60)
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.des_condicion)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Condicion_Estudiante
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Condición del Estudiante")
        verbose_name_plural = _(u"Condiciones de los Estudiantes")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "cod_condest=%s, des_condicion=%s" % (self.cod_condest, self.des_condicion)
        return [cadena, self.usuarioreg.username, "Condicion_Estudiante"]

class Expediente(models.Model):
    """
    @note: Clase que contiene el modelo para el expediente de alumnos por trimestre
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    ira = models.DecimalField(max_digits=10, decimal_places=2)
    ucc = models.DecimalField(max_digits=10, decimal_places=2)
    uca = models.DecimalField(max_digits=10, decimal_places=2)
    puntos = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.CharField(max_length=255, null=True)
    estatus = models.BooleanField(default=False)
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    pensum = models.ForeignKey(Pensum, db_column="id_pensum")
    trimestre = models.ForeignKey(Trimestre, db_column="idtrimestre")
    condicion_estudiante = models.ForeignKey(Condicion_Estudiante, db_column="cod_condest")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Expediente
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Expediente por Trimestre")
        verbose_name_plural = _(u"Expedientes por Trimestres")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "id=%s, ira=%s, ucc=%s, uca=%s, puntos=%s, observaciones=%s, " % (self.pk, self.ira, self.ucc, self.uca, self.puntos, self.observaciones)
        cadena+= "estatus=%s, alumno=%s, pensum=%s, trimestre=%s, condicion_estudiante=%s" % (self.estatus, self.alumno.cod_alumno, self.pensum.cod_pensum,
                                                                                              self.trimestre.idtrimestre, self.condicion_estudiante.cod_condest)
        return [cadena, self.usuarioreg.username, "Expediente"]
        
class Expediente_Anualidad(models.Model):
    """
    @note: Clase que contiene el modelo para el expediente de alumnos por anualidades
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    ira = models.DecimalField(max_digits=10, decimal_places=2)
    ucc = models.DecimalField(max_digits=10, decimal_places=2)
    uca = models.DecimalField(max_digits=10, decimal_places=2)
    puntos = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.CharField(max_length=255, null=True)
    alumno = models.ForeignKey(Alumno, db_column="cod_alumno")
    pensum = models.ForeignKey(Pensum, db_column="id_pensum")
    anualidad_carrera = models.ForeignKey(Anualidad_Carrera, db_column="idanualidad_carrera")
    condicion_estudiante = models.ForeignKey(Condicion_Estudiante, db_column="cod_condest")
    usuarioreg = models.ForeignKey(User, db_column='id_usuario')
    
    def __unicode__(self):
        """
        @note: Función que convierte a unicode los datos de los campos de tipo string
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna las cadenas de texto indicadas a unicode
        """
        return u"%s" % (self.observaciones)
    
    class Meta:
        """
        @note: Superclase que configura los parámetros de la clase Expediente_Anualidad
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        verbose_name = _(u"Expediente por Anualidad")
        verbose_name_plural = _(u"Expedientes por Anualidades")
        
    def datos(self):
        """
        @note: Función que establece los datos a ser almacenados en el modelo de Históricos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna una lista de datos a ser almacenados en el histórico de la aplicación
        """
        cadena = "id=%s, ira=%s, ucc=%s, uca=%s, puntos=%s, observaciones=%s, " % (self.pk, self.ira, self.ucc, self.uca, self.puntos, self.observaciones)
        cadena+= "alumno=%s, pensum=%s, anualidad_carrera=%s, condicion_estudiante=%s" % (self.alumno.cod_alumno, self.pensum.cod_pensum, 
                                                                                          self.anualidad_carrera.idanualidad_carrera, 
                                                                                          self.condicion_estudiante.cod_condest)
        return [cadena, self.usuarioreg.username, "Expediente_Anualidad"]
    
#Dispara el registro de eventos para el modelo de Alumno
post_save.connect(dispararEvento,Alumno,post_save)
post_delete.connect(dispararEvento, Alumno, post_delete)
#Dispara el registro de eventos para el modelo de DatoSocioeconomico
post_save.connect(dispararEvento,DatoSocioeconomico,post_save)
post_delete.connect(dispararEvento, DatoSocioeconomico, post_delete)
#Dispara el registro de eventos para el modelo de Documento
post_save.connect(dispararEvento,Documento,post_save)
post_delete.connect(dispararEvento, Documento, post_delete)
#Dispara el registro de eventos para el modelo de Dato_Documento
post_save.connect(dispararEvento,Dato_Documento,post_save)
post_delete.connect(dispararEvento, Dato_Documento, post_delete)
#Dispara el registro de eventos para el modelo de Titulo_Bachiller
post_save.connect(dispararEvento,Titulo_Bachiller,post_save)
post_delete.connect(dispararEvento, Titulo_Bachiller, post_delete)
#Dispara el registro de eventos para el modelo de Condicion_Ingreso
post_save.connect(dispararEvento,Condicion_Ingreso,post_save)
post_delete.connect(dispararEvento, Condicion_Ingreso, post_delete)
#Dispara el registro de eventos para el modelo de Sistema_Estudio
post_save.connect(dispararEvento,Sistema_Estudio,post_save)
post_delete.connect(dispararEvento, Sistema_Estudio, post_delete)
#Dispara el registro de eventos para el modelo de Tipo_Trimestre
post_save.connect(dispararEvento,Tipo_Trimestre,post_save)
post_delete.connect(dispararEvento, Tipo_Trimestre, post_delete)
#Dispara el registro de eventos para el modelo de Trimestre
post_save.connect(dispararEvento,Trimestre,post_save)
post_delete.connect(dispararEvento, Trimestre, post_delete)
#Dispara el registro de eventos para el modelo de Dato_Academico
post_save.connect(dispararEvento,Dato_Academico,post_save)
post_delete.connect(dispararEvento, Dato_Academico, post_delete)
#Dispara el registro de eventos para el modelo de Anualidad
post_save.connect(dispararEvento,Anualidad,post_save)
post_delete.connect(dispararEvento, Anualidad, post_delete)
#Dispara el registro de eventos para el modelo de Anualidad_Carrera
post_save.connect(dispararEvento,Anualidad_Carrera,post_save)
post_delete.connect(dispararEvento, Anualidad_Carrera, post_delete)
#Dispara el registro de eventos para el modelo de Anualidad_Tri_Carrera
post_save.connect(dispararEvento,Anualidad_Tri_Carrera,post_save)
post_delete.connect(dispararEvento, Anualidad_Tri_Carrera, post_delete)
#Dispara el registro de eventos para el modelo de Condicion_Estudiante
post_save.connect(dispararEvento,Condicion_Estudiante,post_save)
post_delete.connect(dispararEvento, Condicion_Estudiante, post_delete)
#Dispara el registro de eventos para el modelo de Expediente
post_save.connect(dispararEvento,Expediente,post_save)
post_delete.connect(dispararEvento, Expediente, post_delete)
#Dispara el registro de eventos para el modelo de Expediente_Anualidad
post_save.connect(dispararEvento,Expediente_Anualidad,post_save)
post_delete.connect(dispararEvento, Expediente_Anualidad, post_delete)