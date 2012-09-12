#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import ESTATUS
from comun.funciones import cargarProfesiones, cargarCondicionesProf, cargarProfesores, cargarCarrerasSede, cargarDias, cargarHoras, cargarTurnos
from planta.academica.models import Profesion

class FormProfesion(forms.Form):
    cod_profesion = forms.CharField(label=_(u"Código profesión:"), widget=forms.TextInput(attrs={'size':'3', 'maxlength':'3', 'title':_(u'Indique el código de la profesión'), 'tabindex':'1'}))
    profesion = forms.CharField(label=_(u"Profesión:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique el nombre de la profesión'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppro = "<div id='ayudapro' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_profesion(self):
        if Profesion.objects.filter(profesion=self.cleaned_data['profesion']):
            raise forms.ValidationError(_(u"La profesión ya se encuentra registrada"))
        return self.cleaned_data['profesion']
    
class FormCondicionProfesor(forms.Form):
    cod_condicion = forms.CharField(label=_(u"Código de condición:"), widget=forms.TextInput(attrs={'size':'2','maxlength':'2', 'title':_(u'Indique el código de la condición'), 'tabindex':'1'}))
    des_condicion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'60', 'title':_(u'Indique la descripción de la condición'), 'tabindex':'2'}))
    carga_horaria = forms.IntegerField(label=_(u"Carga Horaria:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la carga horaria'), 'tabindex':'3'}))
    observacion = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'80', 'title':_(u'Indique alguna observación'), 'tabindex':'5'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpchr = "<div id='ayudachr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
class FormProfesor(forms.Form):
    cod_profesor = forms.CharField(label=_(u"Código:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique el código del profesor'), 'tabindex':'1'}))
    cedula = forms.CharField(label=_(u"Cédula:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la cédula del profesor'), 'tabindex':'2'}))
    primerapellido = forms.CharField(label=_(u"Primer apellido:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u'Indique el primer apellido'), 'tabindex':'3'}))
    segundoapellido = forms.CharField(label=_(u"Segundo apellido:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u'Indique el segundo apellido'), 'tabindex':'4'}), required=False)
    primernombre = forms.CharField(label=_(u"Primer nombre:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u'Indique el primer nombre'), 'tabindex':'5'}))
    segundonombre = forms.CharField(label=_(u"Segundo nombre:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u'Indique el segundo nombre'), 'tabindex':'6'}), required=False)
    carga_horaria = forms.IntegerField(label=_(u"Carga Horaria:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique la carga horaria del profesor'), 'tabindex':'7'}))
    foto = forms.ImageField(label=_(u"Foto:"), widget=forms.FileInput(attrs={'title':_(u'Escoja la foto que se anexará al expediente del profesor'), 'tabindex':'11'}), required=False)
    correo = forms.EmailField(label=_(u"Correo:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'100', 'title':_(u'Indique la dirección de correo electrónico'), 'tabindex':'8'}), required=False)
    telefono = forms.CharField(label=_(u"Teléfono:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique el número de teléfono'), 'tabindex':'12'}), required=False)
    movil = forms.CharField(label=_(u"Celular:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique el número de celular'), 'tabindex':'9'}), required=False)
    profesion = forms.ChoiceField(label=_(u'Profesión:'), choices=cargarProfesiones(), widget=forms.Select(attrs={'title':_(u'Seleccione la profesión del profesor'), 'tabindex':'13'}))
    condicion = forms.ChoiceField(label=_(u'Condición:'), choices=cargarCondicionesProf(), widget=forms.Select(attrs={'title':_(u'Seleccione la condición del profesor'), 'tabindex':'10'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpci  = "<div id='ayudaci'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppap = "<div id='ayudapap' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpsap = "<div id='ayudasap' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppno = "<div id='ayudapno' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpsno = "<div id='ayudasno' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpchr = "<div id='ayudachr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfot = "<div id='ayudafot' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpmai = "<div id='ayudamai' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptlf = "<div id='ayudatlf' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcel = "<div id='ayudacel' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppro = "<div id='ayudapro' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcon = "<div id='ayudacon' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormProfesor, self).__init__(*args, **kwargs)
        self.fields['profesion'].choices = cargarProfesiones()
        self.fields['condicion'].choices = cargarCondicionesProf()
        
    def clean_profesion(self):
        profesion = self.cleaned_data['profesion']
        if profesion =="0":
            raise forms.ValidationError(_(u"Debe seleccionar la profesión"))
        return self.cleaned_data['profesion']
    
    def clean_condicion(self):
        condicion = self.cleaned_data['condicion']
        if condicion == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la condición"))
        return self.cleaned_data['condicion']
        
class FormProfesorCarrera(forms.Form):
    fasignacion = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de asignación:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha en que fue asignado a la carrera'), 'readonly':'readonly', 'tabindex':'2'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'4'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'5'}))
    profesor = forms.ChoiceField(label=_(u'Profesor:'), choices=cargarProfesores(), widget=forms.Select(attrs={'title':_(u'Seleccione el profesor al cual asignar'), 'tabindex':'3'}))
    carrsed = forms.ChoiceField(label=_(u'Carreras por sede:'), choices=cargarCarrerasSede(), widget=forms.Select(attrs={'title':_(u'Seleccione una carrera'), 'tabindex':'1'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpfas = "<div id='ayudafas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppro = "<div id='ayudapro' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcas = "<div id='ayudacas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormProfesorCarrera, self).__init__(*args, **kwargs)
        self.fields['profesor'].choices = cargarProfesores()
        self.fields['carrsed'].choices = cargarCarrerasSede()
        
    def clean_profesor(self):
        profesor = self.cleaned_data['profesor']
        if profesor == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el profesor"))
        return self.cleaned_data['profesor']
    
    def clean_carrsed(self):
        carrsed = self.cleaned_data['carrsed']
        if carrsed == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la carrera"))
        return self.cleaned_data['carrsed']
        
class FormProfesorDisponibilidad(forms.Form):
    nro_horas = forms.IntegerField(label=_(u"Nro. de horas:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique el número de horas disponibles del profesor'), 'tabindex':'3'}))
    fasignacion = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de asignación:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de asignación'), 'readonly':'readonly', 'tabindex':'2'}))
    observacion = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'7'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'4'}))
    profesor = forms.ChoiceField(label=_(u'Profesor:'), choices=cargarProfesores(), widget=forms.Select(attrs={'title':_(u'Seleccione el profesor'), 'tabindex':'1'}))
    dia = forms.ChoiceField(label=_(u'Día:'), choices=cargarDias(), widget=forms.Select(attrs={'title':_(u'Seleccione el día disponible del profesor'), 'tabindex':'5'}))
    turno = forms.ChoiceField(label=_(u'Turno:'), choices=cargarHoras(), widget=forms.Select(attrs={'title':_(u'Seleccione el turno disponible del profesor'), 'tabindex':'6'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpnhr = "<div id='ayudanhr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfas = "<div id='ayudafas' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppro = "<div id='ayudapro' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdia = "<div id='ayudadia' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helptur = "<div id='ayudatur' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormProfesorDisponibilidad, self).__init__(*args, **kwargs)
        self.fields['profesor'].choices = cargarProfesores()
        self.fields['dia'].choices = cargarDias()
        self.fields['turno'].choices = cargarTurnos()
        
    def clean_profesor(self):
        profesor = self.cleaned_data['profesor']
        if profesor == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el profesor"))
        return self.cleaned_data['profesor']
    
    def clean_dia(self):
        dia = self.cleaned_data['dia']
        if dia == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el día"))
        return self.cleaned_data['dia']
    
    def clean_hora(self):
        hora = self.cleaned_data['hora']
        if hora == "0":
            raise forms.ValidationError(_(u"Debe seleccionar la hora"))
        return self.cleaned_data['hora']