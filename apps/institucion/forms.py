#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import ESTATUS, DESICION
from institucion.models import Sede, Departamento, Carrera, Carrera_Sede
from comun.funciones import cargarCarreras, cargarSedes, cargarDepartamentos

class FormSede(forms.Form):
    cod_sede = forms.CharField(label=_(u"Código sede:"),widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el código de la sede a registrar'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique una descripción'), 'tabindex':'2'}))
    direccion = forms.CharField(label=_(u"Dirección:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique la dirección de la sede'), 'tabindex':'3'}),
                                required=False)
    telefonos = forms.CharField(label=_(u"Teléfonos:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'80', 'title':_(u'Indique los teléfonos de la sede'), 'tabindex':'4'}),
                                required=False)
    fcreacion = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de creación:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de creación'), 'readonly':'readonly', 'tabindex':'5'}),
                                required=False)
    contacto = forms.CharField(label=_(u"Contacto:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique la persona de contacto'), 'tabindex':'7'}),
                               required=False)
    email = forms.EmailField(label=_(u"Correo:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique la dirección de correo electrónico'), 'tabindex':'8'}),
                             required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la sede'), 'tabindex':'6'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el código de la sede. Este campo permite una longitud máxima de 2 carácteres. Este campo es obligatorio.")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el nombre bajo el cual se describe la sede a registrar. La longitud máxima de este campo es de 50 carácteres. Este campo es obligatorio.")
    helpdir = "<div id='ayudadir' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la dirección en la que se encuentra ubicada la sede. La longitud máxima es de 100 carácteres. Este campo es opcional.")
    helptlf = "<div id='ayudatlf' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique un número teléfonico para la sede. La longitud máxima es de 80 carácteres numéricos y el signo '-'. Este campo es opcional.")
    helpfcr = "<div id='ayudafcr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la fecha de creación de la sede a registrar. Este campo no es editable y solo se puede ingresar la fecha a través del calendario dispuesto para ello. Este campo es opcional.")
    helpcto = "<div id='ayudacto' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el nombre de la persona de contacto de la sede. La longitud máxima es de 50 carácteres. Este campo es opcional.")
    helpmai = "<div id='ayudamai' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una dirección de correo electrónico para la sede o perosona de contacto. La longitud máxima es de 50 carácteres. Este campo es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_cod_sede(self):
        cod_sede = self.cleaned_data['cod_sede']
        modificar = self.data['modificar']
        if Sede.objects.filter(pk=cod_sede) and modificar=="":
            raise forms.ValidationError(_(u"El código de sede ya existe"))
        return self.cleaned_data['cod_sede']

class FormDpto(forms.Form):
    cod_dep = forms.CharField(label=_(u"Código departamento:"),widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el código del departamento'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique una descripción'), 'tabindex':'2'}))
    contacto = forms.CharField(label=_(u"Contacto:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique la persona de contacto'), 'tabindex':'3'}),
                               required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus del departamento'), 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcto = "<div id='ayudacto' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def clean_cod_dep(self):
        cod_dep = self.cleaned_data['cod_dep']
        modificar = self.data['modificar']
        if Departamento.objects.filter(pk=cod_dep) and modificar=="":
            raise forms.ValidationError(_(u"El código de departamento ya existe"))
        return self.cleaned_data['cod_dep']
    
class FormCarrera(forms.Form):
    cod_carrera = forms.CharField(label=_(u"Código de carrera"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el código de la carrera'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique una descripción'), 'tabindex':'2'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la carrera'), 'tabindex':'3'}))
    departamento = forms.ChoiceField(label=_(u'Departamento:'), choices=cargarDepartamentos(), widget=forms.Select(attrs={'title':_(u'Seleccione el departamento al cual esta adscrito la carrera'), 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpdto = "<div id='ayudadto' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormCarrera, self).__init__(*args, **kwargs)
        self.fields['departamento'].choices = cargarDepartamentos()
        
    def clear_cod_carrera(self):
        cod_carrera = self.cleaned_data['cod_carrera']
        modificar = self.data['modificar']
        if Carrera.objects.filter(pk=cod_carrera) and modificar=="":
            raise forms.ValidationError(_(u"El código de la carrera ya existe"))
        return self.cleaned_data['cod_carrera']
    
    def clear_departamento(self):
        departamento = self.cleaned_data['departamento']
        if departamento=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el departamento"))
        return self.cleaned_data['departamento']

class FormCarrSede(forms.Form):
    sede = forms.ChoiceField(label=_(u'Sede:'), choices=cargarSedes(), widget=forms.Select(attrs={'title':_(u'Seleccione una sede'), 'tabindex':'1'}))
    carrera = forms.ChoiceField(label=_(u'Carrera:'), choices=cargarCarreras(), widget=forms.Select(attrs={'title':_(u'Seleccione una carrera'), 'tabindex':'2'}))
    nro_carnet = forms.IntegerField(label=_(u'Nro de carnet:'), widget=forms.TextInput(attrs={'size':'20','maxlength':'20','title':_(u'Indique el número de carnet'), 'tabindex':'5'}))
    cant_carnet = forms.IntegerField(label=_(u'Cantidad de carnet:'), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique la cantidad de carnets permitido'), 'value':'0', 'tabindex':'6'}))
    format_carnet = forms.IntegerField(label=_(u'Formato de carnet:'), widget=forms.TextInput(attrs={'size':'2','maxlength':'2', 'title':_(u'Indique el formato del carnet'), 'tabindex':'7'}))
    prefijo_sede = forms.ChoiceField(label=_(u"Prefijo Sede:"), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si el carnet va a contener el prefijo de la sede'), 'tabindex':'3'}))
    prefijo_carrera = forms.ChoiceField(label=_(u"Prefijo Carrera:"), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si el carnet va a contener el prefijo de la carrera'), 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpsed = "<div id='ayudased' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcar = "<div id='ayudacar' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpnca = "<div id='ayudanca' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpcca = "<div id='ayudacca' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helpfca = "<div id='ayudafca' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppse = "<div id='ayudapse' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    helppca = "<div id='ayudapca' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"")
    
    def __init__(self, *args, **kwargs):
        super(FormCarrSede, self).__init__(*args, **kwargs)
        self.fields['sede'].choices = cargarSedes()
        self.fields['carrera'].choices = cargarCarreras()
        
    def clean_sede(self):
        sede = self.cleaned_data['sede']
        if sede=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la sede"))
        return self.cleaned_data['sede']
        
    def clean_carrera(self):
        sede = self.data['sede']
        carrera = self.cleaned_data['carrera']
        modificar = self.data['modificar']
        if Carrera_Sede.objects.filter(carrera=carrera, sede=sede) and modificar=="":
            raise forms.ValidationError(_(u'La carrera ya posee un registro'))
        elif carrera=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la carrera"))
        return self.cleaned_data['carrera']
    
    def clean_nro_carnet(self):
        nro_carnet = self.cleaned_data['nro_carnet']
        format_carnet = self.data['format_carnet']
        if format_carnet!="" and nro_carnet!="" and int(format_carnet) < str(nro_carnet).__len__():
            raise forms.ValidationError(_(u"La cantidad de dígitos es superior al formato"))
        return self.cleaned_data['nro_carnet']
    
    def clean_format_carnet(self):
        sede = self.data["sede"]
        carrera = self.data["carrera"]
        prefijo_sede = self.data["prefijo_sede"]
        prefijo_carrera = self.cleaned_data.get("prefijo_carrera")
        nro_carnet = self.data["nro_carnet"]
        format_carnet = self.cleaned_data['format_carnet']
        digitos = str(nro_carnet).__len__()
        if prefijo_sede=="True" and sede!="0":
            digitos += str(sede).__len__()
        if prefijo_carrera=="True" and carrera!="0":
            digitos += str(carrera).__len__()
        if nro_carnet!="" and format_carnet!="" and int(digitos) > int(format_carnet):
            raise forms.ValidationError(_(u"El formato del carnet es inválido"))
        return self.cleaned_data['format_carnet']