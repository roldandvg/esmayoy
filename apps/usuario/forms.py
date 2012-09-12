#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from comun.constantes import DESICION, DESICIONINVERSA, INTENTOS_ACCESO, DIAS_CADUCIDADPASS
from comun.funciones import cargarUsuarios, cargarCarrerasSede, cargarPermisos
from datetime import *
import hashlib

now = datetime.now()

class FormAcceso(forms.Form):
    usuario = forms.CharField(label=_(u"Usuario:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'30', 'title':_(u'Indique el nombre de usuario con acceso al sistema'), 'tabindex':'1'}))
    contrasenha = forms.CharField(label=_(u"Contraseña:"), widget=forms.PasswordInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique la contraseña de acceso'), 'tabindex':'2'}))
    captcha = forms.CharField(label=_(u"Captcha:"), widget=forms.TextInput(attrs={'title':_(u'Introduzca los dígitos del la imagen. El sistema distingue entre mayúsculas y minúsculas'), 'tabindex':'3', 'onclick':"this.value=''"}))
    
    helpusr = "<div id='ayudausr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcon = "<div id='ayudacon' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcap = "<div id='ayudacap' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(FormAcceso, self).__init__(*args, **kwargs)
    
    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if not User.objects.filter(username=usuario):
            raise forms.ValidationError(_(u"El usuario no existe"))
        else:
            usr = User.objects.get(username=usuario)
            if not usr.is_active:
                raise forms.ValidationError(_(u"El usuario esta inactivo"))
        return self.cleaned_data['usuario']
    
    def clean_contrasenha(self):
        usuario = self.data['usuario']
        contrasenha = self.cleaned_data['contrasenha']
        if User.objects.filter(username=usuario):
            usr = User.objects.get(username=usuario)
            if not usr.check_password(contrasenha):
                if int(self.request.session['contador_acceso'])>(INTENTOS_ACCESO-1):
                    usr.is_active = False
                    usr.save()
                    raise forms.ValidationError(_(u"Su usuario fue bloqueado. Contacte con el administrador"))
                else:
                    raise forms.ValidationError(_(u"La contraseña es incorrecta"))
            else:
                if usr.fecha_modpass is None or usr.fecha_modpass=="":
                    usr.fecha_modpass = now
                    usr.save()
                fecha_caducidad = usr.fecha_modpass + timedelta(days=DIAS_CADUCIDADPASS)
                if fecha_caducidad < datetime.now():
                    raise forms.ValidationError(_(u"La contraseña expiró. Debe solicitar una nueva contraseña"))
                
        return self.cleaned_data['contrasenha']
    
    def clean_captcha(self):
        if str(self.data['imghash']) != hashlib.sha1(settings.SECRET_KEY[:20]+str(self.data['captcha'])).hexdigest():
            if int(self.request.session['contador_acceso'])>(INTENTOS_ACCESO-1):
                if self.data['usuario']!="" and User.objects.filter(username=self.data['usuario']):
                    usr = User.objects.get(username=self.data['usuario'])
                    usr.is_active = False
                    usr.save()
                    raise forms.ValidationError(_(u"Su usuario fue bloqueado. Contacte con el administrador"))
            else:
                raise forms.ValidationError(_(u"La validación de la imagen es incorrecta"))
        return self.cleaned_data['captcha']
        
    
class FormSegIngAlumn(forms.Form):
    validar_seg = forms.ChoiceField(label=_(u"Validar por seguridad:"), choices=DESICIONINVERSA, widget=forms.Select(attrs={'title':_(u'Seleccione si va a validar la seguridad para la inscripción de alumnos'), 'tabindex':'1'}))
    validar_fecha = forms.ChoiceField(label=_(u"Validar por Período:"), choices=DESICIONINVERSA, widget=forms.Select(attrs={'title':_(u'Seleccione si va a validar la seguridad para la inscripción de acuerdo a un rango de fechas'), 'onchange':'Dajax.usuario_habilitarFechas({"opcion":this.value})', 'tabindex':'2'}))
    finicio = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de inicio:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de inicio del período de inscripción'), 'readonly':'readonly', 'disabled':'disabled', 'tabindex':'3'}), required=False)
    ffinal = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de cierre:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de cierre del período de inscripción'), 'readonly':'readonly', 'disabled':'disabled', 'tabindex':'4'}), required=False)
    validar_cantalumn = forms.ChoiceField(label=_(u"Validar por cantidad:"), choices=DESICIONINVERSA, widget=forms.Select(attrs={'title':_(u'Seleccione si va a validar la seguridad para la inscripción de alumnos de acuerdo a una cantidad'), 'onchange':'Dajax.usuario_habilitarCant({"opcion":this.value})', 'tabindex':'5'}))
    cant_alumnos = forms.IntegerField(label=_(u"Cantidad de alumnos:"), widget=forms.TextInput(attrs={'size':'8', 'maxlength':'8', 'title':_(u'Indique la cantidad de alumnos que puede inscribir'), 'disabled':'disabled', 'tabindex':'6'}), required=False)
    usuario = forms.ChoiceField(label=_(u'Usuario:'), choices=cargarUsuarios(), widget=forms.Select(attrs={'title':_(u'Seleccione el usuario al cual asignar la seguridad'), 'tabindex':'7'}))
    carrsed = forms.ChoiceField(label=_(u'Carreras por sede:'), choices=cargarCarrerasSede(), widget=forms.Select(attrs={'title':_(u'Seleccione una carrera'), 'tabindex':'8'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpvse = "<div id='ayudavse' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpvfe = "<div id='ayudavfe' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfin = "<div id='ayudafin' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpffi = "<div id='ayudaffi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpval = "<div id='ayudaval' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcal = "<div id='ayudacal' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpusr = "<div id='ayudausr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcas = "<div id='ayudacas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormSegIngAlumn, self).__init__(*args, **kwargs)
        self.fields['usuario'].choices = cargarUsuarios()
        self.fields['carrsed'].choices = cargarCarrerasSede()
        
    def clean_usuario(self):
        usr = self.cleaned_data['usuario']
        if usr=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el usuario"))
        return self.cleaned_data['usuario']
    
    def clean_carrsed(self):
        carrsed = self.cleaned_data['carrsed']
        if carrsed == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la carrera"))
        return self.cleaned_data['carrsed']
    
class FormUsuario(forms.Form):
    usuario = forms.CharField(label=_(u"Usuario:"), widget=forms.TextInput(attrs={'title':_(u'Indique el nombre del usuario a registrar'), 'size':'28', 'maxlength':'30', 'tabindex':'1'}))
    contrasenha = forms.CharField(label=_(u"Contraseña:"), widget=forms.PasswordInput(attrs={'autocomplete':'off', 'onkeyup':'chkPass(this.value)','size':'20', 'maxlength':'20', 'title':_(u'Indique la contraseña para este usuario'), 'tabindex':'2'}))
    confirmcontrasenha = forms.CharField(label=_(u"Confirmar contraseña:"), widget=forms.PasswordInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique nuevamente la contraseña para este usuario'), 'tabindex':'3'}))
    nombre = forms.CharField(label=_(u"Nombre:"), widget=forms.TextInput(attrs={'title':_(u'Indique el Nombre de la persona'), 'size':'28', 'maxlength':'30', 'tabindex':'4'}))
    apellido = forms.CharField(label=_(u"Apellido:"), widget=forms.TextInput(attrs={'title':_(u'Indique el Apellido de la persona'), 'size':'28', 'maxlength':'30', 'tabindex':'5'}))
    correo = forms.EmailField(label=_(u"Correo:"), widget=forms.TextInput(attrs={'title':_(u'Indique la dirección de correo del usuario'), 'size':'28', 'maxlength':'75', 'tabindex':'6'}))
    activo = forms.ChoiceField(label=_(u"Activo:"), choices=(('True','Si'),('False','No')), widget=forms.Select(attrs={'title':_(u'Seleccione si el usuario a registrar esta activo'), 'tabindex':'7'}))
    fortaleza = forms.CharField(widget=forms.HiddenInput(attrs={'readonly':'readonly', 'size':'1'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpusr = "<div id='ayudausr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcon = "<div id='ayudacon' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcco = "<div id='ayudacco' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnom = "<div id='ayudanom' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpape = "<div id='ayudaape' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpmai = "<div id='ayudamai' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpact = "<div id='ayudaact' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfor = "<div id='ayudafor' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_usuario(self):
        usr = self.cleaned_data['usuario']
        modificar = self.data['modificar']
        if modificar=="" and usr!="" and User.objects.filter(username=usr):
            raise forms.ValidationError(_(u"El usuario indicado ya existe"))
        return self.cleaned_data['usuario']
    
    def clean_contrasenha(self):
        fortaleza = self.data['fortaleza']
        if fortaleza!="" and fortaleza.isdigit() and int(fortaleza)<3:
            raise forms.ValidationError(_(u"La contraseña indicada es muy débil"))
        return self.cleaned_data['contrasenha']
    
    def clean_confirmcontrasenha(self):
        contrasenha = self.data['contrasenha']
        confirmcontrasenha = self.cleaned_data['confirmcontrasenha']
        if contrasenha!=confirmcontrasenha:
            raise forms.ValidationError(_(u"La contraseña no coincide"))
        return self.cleaned_data['confirmcontrasenha']
    
    def clean_correo(self):
        usr = self.data['usuario']
        correo = self.cleaned_data['correo']
        modificar = self.data['modificar']
        if modificar=="" and correo!="" and User.objects.filter(email=correo):
            raise forms.ValidationError(_(u"El correo indicado esta siendo utilizado por otro usuario"))
        return self.cleaned_data['correo']
        
class FormPermisoUsuario(forms.Form):
    usuario = forms.ChoiceField(label=_(u"Usuario:"), choices=cargarUsuarios(), widget=forms.Select(attrs={'title':_(u'Seleccione el usuario al cual conceder permisos'), 'tabindex':'1'}))
    permiso = forms.MultipleChoiceField(label=_(u"Permisos:"), choices=cargarPermisos(), widget=forms.CheckboxSelectMultiple(attrs={'title': _(u'Seleccione los permisos a conceder'), 'size':cargarPermisos().__len__(), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpusr = "<div id='ayudausr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpper = "<div id='ayudaper' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormPermisoUsuario, self).__init__(*args, **kwargs)
        self.fields['usuario'].choices = cargarUsuarios()
        self.fields['permiso'].choices = cargarPermisos()
        
    def clean_usuario(self):
        usr = self.cleaned_data['usuario']
        if usr=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el usuario"))
        return self.cleaned_data['usuario']
        
class FormModContrasenha(forms.Form):
    usuario = forms.CharField(label=_(u"Usuario:"), widget=forms.TextInput(attrs={'size':'28', 'maxlength':'30', 'title':_(u'Nombre de usuario logueado'), 'readonly':'readonly', 'tabindex':'1'}))
    contrasenha = forms.CharField(label=_(u"Contraseña:"), widget=forms.PasswordInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique la contraseña actual'), 'tabindex':'2'}))
    contrasenhanva = forms.CharField(label=_(u"Contraseña nueva:"), widget=forms.PasswordInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique la contraseña nueva'), 'tabindex':'3'}))
    contrasenhaconfirm = forms.CharField(label=_(u"Confirme Contraseña:"), widget=forms.PasswordInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Confirme la nueva contraseña'), 'tabindex':'4'}))
    
    helpusr = "<div id='ayudausr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcon = "<div id='ayudacon' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnco = "<div id='ayudanco' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcnc = "<div id='ayudacnc' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_contrasenha(self):
        usuario = self.data['usuario']
        contrasenha = self.cleaned_data['contrasenha']
        if User.objects.filter(username=usuario):
            usr = User.objects.get(username=usuario)
            if not usr.check_password(contrasenha):
                raise forms.ValidationError(_(u"La contraseña es incorrecta"))
        return self.cleaned_data['contrasenha']
    
    def clean_contrasenhanva(self):
        contrasenhanva = self.cleaned_data['contrasenhanva']
        contrasenha = self.data['contrasenha']
        if contrasenha!="" and contrasenhanva!="" and contrasenha == contrasenhanva:
            raise forms.ValidationError(_(u"La nueva contraseña debe ser diferente a la actual"))
        return self.cleaned_data['contrasenhanva']
    
    def clean_contrasenhaconfirm(self):
        contrasenhanva = self.data['contrasenhanva']
        contrasenhaconfirm = self.cleaned_data['contrasenhaconfirm']
        if contrasenhanva!="" and contrasenhaconfirm!="" and contrasenhanva!=contrasenhaconfirm:
            raise forms.ValidationError(_(u"La contraseña no coincide"))
        return self.cleaned_data['contrasenhaconfirm']