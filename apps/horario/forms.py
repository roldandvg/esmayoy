#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from comun.constantes import ESTATUS
from comun.funciones import cargarModalidades, cargarPlanificacionUnidades, cargarAulas, cargarHorario

class FormTurno(forms.Form):
    id_turno = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el identificador del turno'), 'tabindex':'1'}))
    des_turno = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique la descripción del turno'), 'tabindex':'2'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique las observaciones del turno'), 'tabindex':'4'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus del turno'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid  = "<div id='ayudaid'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Debe indicar el identificador del turno, este dato es único y no debe estar registrado. Sólo se aceptan carácteres alfanuméricos con una longitud de 2. Este campo es obligatorio.")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una descripción detallada del turno a registrar, este dato se utilizará para ser mostrado en otros formularios. Este datos tiene una longitud de 45 carácteres alfanuméricos. Este campo es obligatorio.")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una observación, si existe, acerca del turno a registrar. Sólo se permiten carácteres alfanumércos con una longitud máxima de 255 carácteres. Este campo es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus correspondiente del turno a registrar. Este campo es obligatorio.")

class FormHora(forms.Form):
    id_hora = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'8', 'maxlength':'8', 'title':_(u'Indique el identificador de horas'), 'tabindex':'1'}))
    des_hora = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique la descripción de la hora'), 'tabindex':'2'}))
    observacion = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique las observaciones de la hora'), 'tabindex':'6'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus de la hora'), 'tabindex':'5'}))
    horaini = forms.TimeField(('%I:%M %p',),label=_(u"Hora inicial:"), widget=forms.TextInput(attrs={'size':'6', 'maxlength':'8', 'title':_(u'Indique la hora inicial'), 'readonly':'readonly', 'tabindex':'3'}))
    horafin = forms.TimeField(('%I:%M %p',),label=_(u"Hora final:"), widget=forms.TextInput(attrs={'size':'6', 'maxlength':'8', 'title':_(u'Indique la hora final'), 'readonly':'readonly', 'tabindex':'4'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid  = "<div id='ayudaid'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador de la hora a registrar, este valor debe ser único y no estar asociado a otro registro. Este campo es obligatorio.")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una descripción detallada de la hora a registrar. Sólo se aceptan carácteres alfanuméricos con una longitud máxima de 8. Este campo es obligatorio.")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique alguna observación, en caso de existir, acerca de la hora a registrar. Sólo se permite una longitud máxima de 255 carácteres alfanuméricos. Este campo es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus inicial de la hora a registrar. Este campo es obligatorio.")
    helphin = "<div id='ayudahin' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la hora inicial a registrar. Este campo no es editable y solo se pueden ingresar datos a través del calendario. Este campo es obligatorio.")
    helphfi = "<div id='ayudahfi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la hora final a registrar. Este campo no es editable y solo se pueden ingresar datos a través del calendario. Este campo es obligatorio.")
    
class FormDia(forms.Form):
    id_dia = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el identificador del día'), 'tabindex':'1'}))
    des_dia = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique la descripción del día'), 'tabindex':'2'}))
    observacion = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'250', 'title':_(u'Indique las observaciones'), 'tabindex':'4'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid  = "<div id='ayudaid'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador del día a registrar, este dato debe ser único y no asociado a otro registro. Sólo se permite una longitud máxima de 2 carácteres. Este campo es obligatorio.")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una descripción detallada del día a registrar. Sólo se permiten carácteres alfanumericos con una longitud máxima de 20 carácteres. Este campo es obligatorio.")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones que considere necesarias para el registro del día. Este dato permite carácteres alfanuméricos con una longitud máxima de 250 carácteres. Este campo es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus del día a registrar. Este campo es obligatorio.")
    
class FormModalidadHorario(forms.Form):
    idmodalidad_horario = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el identificador de la modalidad de horario'), 'tabindex':'1'}))
    des_modalidad = forms.CharField(label=_(u"Descripción:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique la descripción de la modalidad de horario'), 'tabindex':'2'}))
    observacion = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique las observaciones'), 'tabindex':'4'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid  = "<div id='ayudaid'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador para la modalidad de horario, este valor permite identificar la modalidad del horario en otros formularios. Sólo permite una longitud máxima de 2 carácteres. Este campo es obligatorio.")
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una descripción detallada de la modalidad de horario a registrar. Este dato acepta una longitud máxima de 45 carácteres alfanuméricos. Este campo es obligatorio.")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones que considere necesarias para el registro de la modalidad de horario. Sólo se permite una longitud máxima de 255 carácteres alfanuméricos. Este campo es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus actual de la modalidad de horario a registrar. Este campo es obligatorio.")
    
class FormHorario(forms.Form):
    idhorario = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'4', 'maxlength':'4', 'title':_(u'Indique el identificador del horario'), 'tabindex':'1'}))
    observacion = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique las observaciones'), 'tabindex':'4'}),required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'3'}))
    modalidad_horario = forms.ChoiceField(label=_(u'Modalidad:'), choices=cargarModalidades(), widget=forms.Select(attrs={'title':_(u'Seleccione la modalidad del horario'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    #FALTA COLOCAR LOS DIAS Y HORAS
    
    helpid  = "<div id='ayudaid'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador único para el horario a registrar. La longitud máxima es de 4 carácteres. Este campo es obligatorio.")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones que considere pertinentes para el registro del horario. La longitud máxima es de 255 carácteres alfanuméricos. Este campo es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus del horario a registrar. Este campo es obligatorio.")
    helpmod = "<div id='ayudamod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la modalidad de horario a la cual se va a asociar el registro del horario. Este campo es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        super(FormHorario, self).__init__(*args, **kwargs)
        self.fields['modalidad_horario'].choices = cargarModalidades()
        
    def clean_modalidad_horario(self):
        modalidad = self.cleaned_data['modalidad_horario']
        if modalidad=="0":
            raise forms.ValidationError(_(u'Debe seleccionar la modalidad'))
        return self.cleaned_data['modalidad_horario']
        
class FormHorarioTrimestral(forms.Form):
    fregistro = forms.DateField(label=_(u"Fecha de Registro:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'readonly':'readonly', 'title':_(u'Indique la fecha de registro'), 'tabindex':'1'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'2'}))
    planificacion_unidad = forms.ChoiceField(label=_(u'Planificación de unidad:'), choices=cargarPlanificacionUnidades(), widget=forms.Select(attrs={'title':_(u'Seleccione la planificación de la unidad'), 'tabindex':'3'}))
    aula = forms.ChoiceField(label=_(u'Aula:'), choices=cargarAulas(), widget=forms.Select(attrs={'title':_(u'Seleccione el aula'), 'tabindex':'4'}))
    horario = forms.ChoiceField(label=_(u'Horario:'), choices=cargarHorario(), widget=forms.Select(attrs={'title':_(u'Seleccione el horario'), 'tabindex':'5'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpfreg = "<div id='ayudafreg' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la fecha en que se registra el horario. Este campo no es editable y solo se pueden ingresar datos a través del calendario. Este campo es obligatorio.")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus del horario trimestral a registrar. Este campo es obligatorio.")
    helppla  = "<div id='ayudapla'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la planificación de la unidad curricular. Este campo es obligatorio.")
    helpaula = "<div id='ayudaaula' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el aula a la cual se va a asignar el horario. Este campo es obligatorio.")
    helphor  = "<div id='ayudahor'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el horario al cual asociar este registro. Este campo es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        super(FormHorarioTrimestral, self).__init__(*args, **kwargs)
        self.fields['planificacion_unidad'].choices = cargarPlanificacionUnidades()
        self.fields['aula'].choices = cargarAulas()
        self.fields['horario'].choices = cargarHorario()
        
    def clean_planificacion_unidad(self):
        planificacion = self.cleaned_data['planificacion_unidad']
        if planificacion == "0":
            raise forms.ValidationError(_(u"Debe seleccionar una planificación"))
        return self.cleaned_data['planificacion_unidad']
    
    def clean_aula(self):
        aula = self.cleaned_data['aula']
        if aula == "0":
            raise forms.ValidationError(_(u"Debe seleccionar un aula"))
        return self.cleaned_data['aula']
    
    def clean_horario(self):
        horario = self.cleaned_data['horario']
        if horario=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el horario"))
        return self.cleaned_data['horario']