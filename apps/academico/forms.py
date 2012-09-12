#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from comun.constantes import NACIONALIDAD, SEXO, NROHIJOS, DESICION, ESTATUS, DEFAULT, ESTATUSCONDICION
from comun.funciones import str2bool, cargarSedes, cargarCarreras, cargarDocumentos, cargarTipostrimestres, cargarPaises, cargarEstados, cargarMunicipios, cargarParroquias, cargarTrimestres, cargarCondicionesingreso, cargarSistemasestudio, cargarTitulosbachiller, cargarAnualidades, cargarAnualidadesCarreras, cargarCarrerasSede
from academico.models import Alumno, Condicion_Estudiante
from django.utils.translation import ugettext as _

class FormAlumno(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de alumnos
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    nacionalidad = forms.ChoiceField(label=_(u"Nacionalidad:"), choices=NACIONALIDAD, widget=forms.Select(attrs={'title':_(u"Seleccione la nacionalidad"), 'tabindex':'8'}))
    cedula = forms.CharField(label=_(u"Cédula:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title': _(u"Indique la cédula de identidad del alumno"), 'tabindex':'2'}))
    primerapellido = forms.CharField(label=_(u"Primer Apellido:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u"Indique el primer apellido del alumno"), 'tabindex':'3'}))
    segundoapellido = forms.CharField(label=_(u"Segundo Apellido:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u"Indique el segundo apellido del alumno"), 'tabindex':'4'}), required=False)
    primernombre = forms.CharField(label=_(u"Primer Nombre:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u"Indique el primer nombre del alumno"), 'tabindex':'5'}))
    segundonombre = forms.CharField(label=_(u"Segundo Nombre:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u"Indique el segundo nombre del alumno"), 'tabindex':'6'}), required=False)
    sexo = forms.ChoiceField(label=_(u"Sexo:"), choices=SEXO, widget=forms.Select(attrs={'title':_(u"Seleccione el sexo del alumno"), 'tabindex':'7'}))
    fnacimiento = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de Nacimiento:"), widget=forms.TextInput(attrs={'size':'10','maxlength':'10', 'title':_(u"Indique la fecha de nacimiento"), 'readonly':'readonly', 'tabindex':'9'}))
    direccion = forms.CharField(label=_(u"Dirección:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'250', 'title':_(u"Indique la dirección de vivienda"), 'tabindex':'13'}))
    telefono = forms.CharField(label=_(u"Teléfonos:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'45', 'title':_(u"Indique los número telefónicos"), 'tabindex':'14'}), required=False)
    movil = forms.CharField(label=_(u"Celular:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'45', 'title':_(u"Indique los números telefónicos de celulares"), 'tabindex':'15'}), required=False)
    email = forms.EmailField(label=_(u"Correo electrónico:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'100', 'title':_(u"Indique la dirección de correo electrónico"), 'tabindex':'12'}), required=False)
    foto = forms.ImageField(label=_(u"Foto:"), widget=forms.FileInput(attrs={'title':_(u"seleccione la foto"), 'tabindex':'1'}), required=False)
    ref_personal = forms.CharField(label=_(u"Ref. Personal:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u"Indique los datos de referencia personal"), 'tabindex':'16'}), required=False)
    tel_ref_personal = forms.CharField(label=_(u"Tlf. de Ref. Personal:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'45', 'title':_(u"Indique los números telefónicos de referencia personal"), 'tabindex':'17'}), required=False)
    lugar_nacimiento = forms.CharField(label=_(u"Lugar de nacimiento:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'100', 'title': _(u"Indique la ciudad de nacimiento"), 'tabindex':'10'}), required=False)
    carrsed = forms.ChoiceField(label=_(u'Carreras por sede:'), choices=cargarCarrerasSede(), widget=forms.Select(attrs={'title':_(u'Seleccione una carrera'), 'tabindex':'11'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpnac  = "<div id='ayudanac'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la nacionalidad que posee el alumno a registrar. Este dato es de caracter obligatorio.")
    helpci   = "<div id='ayudaci'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la Cédula de Identidad del alumno. Solo se permiten números con una longitud máxima de 10 carácteres. Este dato es de caracter obligatorio.")
    helppap  = "<div id='ayudapap'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el primer apellido del alumno a registrar, no se permiten números ni espacios en blanco y la longitud máxima es de 30 carácteres. Este dato es de caracter obligatorio.")
    helpsap  = "<div id='ayudasap'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de que el alumno a registrar posea un segundo apellido debe indicarlo en este campo, no se permiten números ni espacios en blanco y la longitud máxima es de 30 carácteres. Este dato es opcional.")
    helppno  = "<div id='ayudapno'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el primer nombre del alumno a registrar, no se permiten números ni espacios en blanco y la longitud máxima es de 30 carácteres. Este dato es de caracter obligatorio.")
    helpsno  = "<div id='ayudasno'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de que el alumno a registrar posea un segundo nombre debe indicarlo en este campo, no se permiten números ni espacios en blanco y la longitud máxima es de 30 carácteres. Este dato es opcional.")
    helpsex  = "<div id='ayudasex'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el sexo que le corresponda al alumno que esta registrando. Este dato es de caracter obligatorio.")
    helpfna  = "<div id='ayudafna'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario la fecha de nacimiento del alumno. Los campos de fecha no son editables y solo se puede ingresar datos mediante el calendario. Este dato es de caracter obligatorio.")
    helpdir  = "<div id='ayudadir'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la dirección detallada del alumno. Este campo tiene una longitud máxima de 250 caracteres. Este dato es de caracter obligatorio.")
    helptlf  = "<div id='ayudatlf'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el(los) número(s) telefónico(s) del alumno. Solo se permiten números, espacios en blanco y el signo '-'. Este campo tiene una longitud máxima de 45 carácteres. Este dato es opcional.")
    helpcel  = "<div id='ayudacel'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el(los) número(s) de celular(es) del alumno. Solo se permiten números, espacios en blanco y el signo '-'. Este campo tiene una longitud máxima de 45 carácteres. Este dato es opcional.")
    helpmail = "<div id='ayudamail' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la dirección de correo del alumno. Este campo tiene una longitud máxima de 100 carácteres. Este dato es opcional.")
    helpfoto = "<div id='ayudafoto' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione el archivo en el que se encuentra la foto del alumno. Este dato es opcional.")
    helprefp = "<div id='ayudarefp' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el detalle de alguna referencia personal suministrada por el alumno. Solo se permiten carácteres alfanuméricos con una longitud máxima de 100 carácteres. Este dato es opcional.")
    helptlfr = "<div id='ayudatlfr' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el(los) número(s) telefónico(s) de la persona suministrada como referencia personal. Este campo solo permite ingresar números, espacios en blanco y el signo '-'. Este dato es opcional.")
    helplnac = "<div id='ayudalnac' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la ciudad en la que nació el alumno. Este campo tiene una longitud máxima de 100 caracteres. Este dato es opcional.")
    helpcase = "<div id='ayudacase' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegables la carrera a la cual pertenece el alumno a registrar. Este dato es de caracter obligatorio.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que inicializa los campos del formulario de alumno
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormAlumno, self).__init__(*args, **kwargs)
        self.fields['carrsed'].choices = cargarCarrerasSede()
        
    def clean_carrsed(self):
        """
        @note: Función que verifica si la carrera fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado una carrera
        """
        carrsed = self.cleaned_data['carrsed']
        if carrsed=="0":
            raise forms.ValidationError(_(u"Debe seleccionar una carrera"))
        return self.cleaned_data['carrsed']
        
class FormDatoSocioEcon(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de los datos socio-económicos del alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    nhijos = forms.ChoiceField(label=_(u"Nro. de Hijos:"), choices=NROHIJOS, widget=forms.Select(attrs={'title':_(u'Seleccione el número de hijos'), 'tabindex':'2'}), required=False)
    mtraslado = forms.CharField(label=_(u"Medio de traslado:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el medio de traslado'), 'tabindex':'3'}), required=False)
    costeo_est = forms.CharField(label=_(u"Costeo de estudio:"), widget=forms.TextInput(attrs={'size':'30', 'maxlength':'30', 'title':_(u'Indique la forma de costeo de estudio'), 'tabindex':'4'}), required=False)
    tipovivienda = forms.CharField(label=_(u"Tipo de Vivienda:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el tipo de vivienda'), 'tabindex':'5'}), required=False)
    cond_alojamiento = forms.CharField(label=_(u"Cond. de Alojamiento:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique la condición de alojamiento'), 'tabindex':'6'}), required=False)
    nivel_m = forms.CharField(label=_(u"Nivel est. Madre:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el nivel de estudio de la madre'), 'tabindex':'8'}), required=False)
    nivel_p = forms.CharField(label=_(u"Nivel est. Padre:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el nivel de estudio del padre'), 'tabindex':'9'}), required=False)
    monto_ingreso = forms.DecimalField(label=_(u"Monto de ingreso:"), widget=forms.TextInput(attrs={'size':'15', 'maxlength':'15', 'title':_(u'Indique el monto de ingreso familiar'), 'tabindex':'7'}), required=False)
    trabaja = forms.ChoiceField(label=_(u"Trabaja:"), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si el alumno trabaja'), 'tabindex':'10'}))
    tipo_empresa = forms.CharField(label=_(u"Tipo de empresa:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el tipo de empresa'), 'tabindex':'11'}), required=False)
    empresa = forms.CharField(label=_(u"Empresa:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'80', 'title':_(u'Indique el nombre de la empresa'), 'tabindex':'12'}), required=False)
    direc_empresa = forms.CharField(label=_(u"Dirección empresa:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'200', 'title':_(u'Indique la dirección de la empresa'), 'tabindex':'13'}), required=False)
    telefonoe = forms.CharField(label=_(u"Teléfono empresa:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'45', 'title':_(u'Indique los teléfonos de la empresa'), 'tabindex':'14'}), required=False)
    discapacidad = forms.ChoiceField(label=_(u"Discapacidad:"), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si el alumno posee alguna discapasidad'), 'tabindex':'16'}))
    des_discapacidad = forms.CharField(label=_(u"Desc. de discapacidad:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'80', 'title':_(u'Indique que discapacidad posee el alumno'), 'tabindex':'17'}), required=False)
    indigena = forms.ChoiceField(label=_(u"Indigena:"), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si el alumno es indigena'), 'tabindex':'18'}))
    obs_datse = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'15'}), required=False)
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpnhi  = "<div id='ayudanhi'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el número de hijos que posee el alumno a registrar. Este dato es opcional.")
    helpmtr  = "<div id='ayudamtr'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el medio de traslado del alumno a registrar. Este campo solo permite carácteres alfanuméricos con una longitud máxima de 20 carácteres. Este dato es opcional.")
    helpces  = "<div id='ayudaces'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la forma en que el alumno costea sus estudios. Este campo solo permite carácteres alfanuméricos con una longitud máxima de 30 carácteres. Este dato es opcional.")
    helptvi  = "<div id='ayudatvi'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el tipo de vivienda en la que vive actualmente el alumno. Este campo solo permite carácteres alfanuméricos con una longitud máxima de 20 carácteres. Este dato es opcional.")
    helpcal  = "<div id='ayudacal'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique en que condiciones se encuentra viviendo el alumno. Este campo solo acepta carácteres alfanuméricos con una longitud máxima de 20 carácteres. Este dato es opcional.")
    helpnim  = "<div id='ayudanim'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el nivel de estudio de la madre del alumno. Solo se permiten carácteres alfanuméricos con una longitud máxima de 20 carácteres. Este dato es opcional.")
    helpnip  = "<div id='ayudanip'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el nivel de estudio del padre del alumno. Solo se permiten carácteres alfanuméricos con una longitud máxima de 20 carácteres. Este dato es opcional.")
    helpmin  = "<div id='ayudamin'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique en este campo el monto de ingreso mensual del grupo familiar. Solo se permiten carácteres numéricos y el signo '.' con una longitud máxima de 15 carácteres. Este dato es opcional.")
    helptra  = "<div id='ayudatra'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable si el alumno se encuentra trabajando actualmente. Este dato es opcional.")
    helptpem = "<div id='ayudatpem' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de haber seleccionado si el alumno trabaja, debe especificar el tipo de empresa para la cual labora. Este campo permite carácteres alfanuméricos con una longitud máxima de 20 carácteres. Este dato es obligatorio en caso de que el alumno trabaje, de lo contrario es un dato opcional.")
    helpemp  = "<div id='ayudaemp'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de haber seleccionado si el alumno trabaja, debe indicar el nombre de la empresa para la cual trabaja. Este campo permite carácteres alfanuméricos con una longitud máxima de 80 carácteres. Este dato es obligatorio en caso de que el alumno trabaje, de lo contrario es un dato opcional.")
    helpdiem = "<div id='ayudadiem' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de haber seleccionado si el alumno trabaja, debe indicar la dirección exacta de la empresa para la cual trabaja. Este campo permite carácteres alfanuméricos con una longitud máxima de 200 carácteres. Este dato es obligatorio en caso de que el alumno trabaje, de lo contrario es un dato opcional.")
    helptlfe = "<div id='ayudatlfe' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de haber seleccionado si el alumno trabaja, debe indicar el(los) número(s) telefónico(s) de la empresa. Solo se permiten carácteres numéricos, espacios en blanco y el signo '-'. Este dato es obligatorio en caso de que el alumno trabaje, de lo contrario es un dato opcional.")
    helpdisc = "<div id='ayudadisc' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable si el alumno posee alguna discapacidad. Este dato es obligatorio.")
    helpdesd = "<div id='ayudadesd' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de haber seleccionado la opción de poseer discapacidad, debe indicar una descripción detallada acerca de la discapacidad que posee el alumno. Solo se permiten carácteres alfanuméricos con una longitud máxima de 80 carácteres. Este dato es obligatorio en caso de haber seleccionado si el alumno posee alguna discapacidad, en caso contrario es opcional.")
    helpindi = "<div id='ayudaindi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable si el alumno es indígena. Este dato es obligatorio.")
    helpobsd = "<div id='ayudaobsd' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"En caso de haber indicado si el alumno es indígena, debe indicar a que grupo indígena pertenece. Este dato es obligatorio en caso de haber seleccionado si el alumno es indígena, en caso contrario es un dato opcional.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que inicializa los campos del formulario de datos socio-económicos del alumno
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormDatoSocioEcon, self).__init__(*args, **kwargs)
        
        if self.data:
            if str2bool(self.data['trabaja']):
                self.fields['tipo_empresa'].required = True
                self.fields['empresa'].required = True
                self.fields['direc_empresa'].required = True
                self.fields['telefonoe'].required = True
            if str2bool(self.data['discapacidad']):
                self.fields['des_discapacidad'].required = True
    
    def clean_tipo_empresa(self):
        """
        @note: Función que verifica si el alumno trabaja y no se especifica el tipo de empresa
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber especificado un tipo de empresa (en caso de que el alumno trabaje)
        """
        trabaja = str2bool(self.data['trabaja'])
        tipo_empresa = self.cleaned_data['tipo_empresa']
        if trabaja and tipo_empresa=="":
            raise forms.ValidationError(_(u"Debe indicar el tipo de empresa"))
        return self.cleaned_data['tipo_empresa']
    
    def clean_empresa(self):
        """
        @note: Función que verifica si el alumno trabaja y no se especifica el nombre de la empresa
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber especificado un nombre de empresa (en caso de que el alumno trabaje)
        """
        trabaja = str2bool(self.data['trabaja'])
        empresa = self.cleaned_data['empresa']
        if trabaja and empresa=="":
            raise forms.ValidationError(_(u"Debe indicar el nombre de la empresa"))
        return self.cleaned_data['empresa']
    
    def clean_des_discapacidad(self):
        """
        @note: Función que verifica si el alumno posee alguna discapacidad y no se especifica la descripción de la misma
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber especificado la descripción de la discapacidad (en caso de que el alumno posea alguna discapacidad)
        """
        discapacidad = str2bool(self.data['discapacidad'])
        des_discapacidad = self.cleaned_data['des_discapacidad']
        if discapacidad and des_discapacidad=="":
            raise forms.ValidationError(_(u"debe indicar la discapacidad que presenta el alumno"))
        return self.cleaned_data['des_discapacidad']
            
    
class FormDocumento(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de documentos exigidos para trámites administrativos
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique una descripción del documento solicitado'), 'tabindex':'1'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique alguna observación'), 'tabindex':'2'}), required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus del documento'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpdes = "<div id='ayudades' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique una descripción detallada acerca del documento que se va a solicitar, este campo permite carácteres alfanuméricos con una longitud máxima de 100 carácteres. Este dato es obligatorio.")
    helpobs = "<div id='ayudaobs' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique alguna observación acerca del documento solicitado, este campo permite carácteres alfanuméricos con una longitud máxima de 100 carácteres. Este dato es opcional.")
    helpest = "<div id='ayudaest' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable si el documento a registrar se encuentra activo o inactivo. Este dato es obligatorio.")

class FormRecDoc(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de documentos consignados por el alumno
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    documento = forms.MultipleChoiceField(label=_(u"Docs entregados:"), choices=cargarDocumentos(), widget=forms.CheckboxSelectMultiple(attrs={'title': _(u'Seleccione si el alumno entrego el documento'), 'size':cargarDocumentos().__len__(), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpdo = "<div id='ayudado'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Marque todos aquellos documentos entregados por el alumno, debe seleccionar al menos 1 documento. Este dato es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que inicializa los campos del formulario de Recepción de Documentos
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormRecDoc, self).__init__(*args, **kwargs)
        self.fields['documento'].choices = cargarDocumentos()
        
class FormTipoTrimestre(forms.Form):
    """
    @note: Clase que contiene el formulario de registro para los tipos de trimestre
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    cod_tipotri = forms.CharField(label=_(u"Código"), widget=forms.TextInput(attrs={'size':'2', 'maxlength':'2', 'title':_(u'Indique el código del tipo de trimestre'), 'tabindex':'1'}))
    tipotrimestre = forms.CharField(label=_(u"tipo de trimestre"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'150', 'title':_(u'Indique el tipo de trimestre a registrar'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpcod = "<div id='ayudacod' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el código del tipo de trimestre a registrar, el cual identificará a este registro. La longitud máxima de este campo es de 2 carácteres. Este dato es obligatorio.")
    helptip = "<div id='ayudatip' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el tipo de trimestre a registrar. Este campo tiene una longitud máxima de 150 carácteres y solo se permiten carácteres alfanuméricos. Este dato es obligatorio.")

class FormTrimestre(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de trimestres
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idtrimestre = forms.CharField(label=_(u"Código de trimestre:"), widget=forms.TextInput(attrs={'size':'6', 'maxlength':'6', 'title':_(u'Indique el código para el trimestre'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'100', 'title':_(u'Indique la descripción del trimestre'), 'tabindex':'6'}))
    finicio = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de inicio:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de inicio del trimestre'), 'readonly':'readonly', 'tabindex':'3'}))
    fculmina = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de culminación:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de culminación del trimestre'), 'readonly':'readonly', 'tabindex':'4'}), required=False)
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'5'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUS, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus del trimestre'), 'tabindex':'7'}))
    tipotrimestre = forms.ChoiceField(label=_(u'Tipo de trimestre:'), choices=cargarTipostrimestres(), widget=forms.Select(attrs={'title':_(u'Seleccione un tipo de trimestre'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid = "<div id='ayudaid' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador para el trimestre a registrar. Este campo permite una longitud máxima de 6 carácteres. Este dato es obligatorio.")
    helpde = "<div id='ayudade' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la descripción del trimestre a registrar, solo se permiten carácteres alfanuméricos con una longitud máxima de 100 carácteres. Este dato es obligatorio.")
    helpfi = "<div id='ayudafi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado, la fecha de inicio del trimestre, este campo no es editable y sólo se pueden ingresar datos mediante el calendario. Este dato es obligatorio.")
    helpfc = "<div id='ayudafc' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado, la fecha programada de culminación del trimestre, este campo no es editable y sólo se pueden ingresar datos mediante el calendario. Este dato es opcional.")
    helpob = "<div id='ayudaob' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones pertinentes al trimestre que desea registrar. Sólo se permiten carácteres alfanuméricos con una longitud máxima de 255 carácteres. Este dato es obligatorio.")
    helpes = "<div id='ayudaes' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus del trimestre. Este dato es obligatorio.")
    helptp = "<div id='ayudatp' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el tipo de trimestre al cual pertenece el trimestre a registrar. Este dato es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que inicializa los campos del formulario de Trimestre
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormTrimestre, self).__init__(*args, **kwargs)
        self.fields['tipotrimestre'].choices = cargarTipostrimestres()
        
    def clean_tipotrimestre(self):
        """
        @note: Función que verifica si el tipo de trimestre fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el tipo de trimestre
        """
        tipotrimestre = self.cleaned_data['tipotrimestre']
        if tipotrimestre == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el tipo de trimestre"))
        return self.cleaned_data['tipotrimestre']
        
class FormDatoAcademico(forms.Form):
    """
    @note: Clase que contiene el formulario de registro para los datos académicos
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    fingreso = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de ingreso:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique la fecha de ingreso a la institución'), 'readonly':'readonly', 'tabindex':'3'}))
    obs_dataca = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'5'}), required=False)
    nliceo = forms.CharField(label=_(u"Nombre del Liceo:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'200', 'title':_(u'Indique el nombre del Liceo en el que estudio'), 'tabindex':'6'}), required=False)
    tliceo = forms.CharField(label=_(u"Título obtenido:"), widget=forms.TextInput(attrs={'size':'25', 'maxlength':'25', 'title':_(u'Indique el título obtenido en el liceo'), 'tabindex':'7'}), required=False)
    serialtitulo = forms.CharField(label=_(u"Serial del título:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'50', 'title':_(u'Indique el serial del título'), 'tabindex':'8'}), required=False)
    profesional = forms.ChoiceField(label=_(u"Profesional:"), choices=DESICION, widget=forms.Select(attrs={'title':_(u'Seleccione si el alumno es profesional'), 'tabindex':'4'}))
    pais = forms.ChoiceField(label=_(u"Pais:"), choices=cargarPaises(), widget=forms.Select(attrs={'title':_(u'Seleccione el pais de origen'), 'onchange':'Dajax.comun_cargarEstados({\'pais\':this.value})', 'tabindex':'9'}))
    estado = forms.ChoiceField(label=_(u"Estado:"), choices=DEFAULT, widget=forms.Select(attrs={'title':_(u'Seleccione el estado del pais de origen'), 'onchange':'Dajax.comun_cargarMunicipios({\'estado\':this.value})', 'tabindex':'10'}))
    municipio = forms.ChoiceField(label=_(u"Municipio:"), choices=DEFAULT, widget=forms.Select(attrs={'title':_(u'Seleccione el municipio de origen'), 'onchange':'Dajax.comun_cargarParroquias({\'municipio\':this.value})', 'tabindex':'11'}))
    parroquia = forms.ChoiceField(label=_(u"Parroquía:"), choices=DEFAULT, widget=forms.Select(attrs={'title':_(u'Seleccione la parroquía de origen'), 'tabindex':'12'}))
    trimestre = forms.ChoiceField(label=_(u"Trimestre:"), choices=cargarTrimestres(), widget=forms.Select(attrs={'title':_(u'Seleccione el trimestre'), 'tabindex':'13'}))
    condicion_ingreso = forms.ChoiceField(label=_(u"Condición de ingreso:"), choices=cargarCondicionesingreso(), widget=forms.Select(attrs={'title':_(u'Seleccione la condición de ingreso'), 'tabindex':'14'}))
    sistema_estudio = forms.ChoiceField(label=_(u"Sistema de estudio:"), choices=cargarSistemasestudio(), widget=forms.Select(attrs={'title':_(u'Seleccione el sistema de estudio'), 'tabindex':'15'}))
    titulo_bachiller = forms.ChoiceField(label=_(u"Título de Bachiller:"), choices=cargarTitulosbachiller(), widget=forms.Select(attrs={'title':_(u'Seleccione el título de bachiller obtenido'), 'tabindex':'16'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpfing  = "<div id='ayudafing'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado, la fecha de ingreso a la institución. Este campo no es editable y solo se pueden ingresar datos mediante el calendario. Este dato es obligatorio.")
    helpobsda = "<div id='ayudaobsda' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones correspondientes al ingreso del alumno a la institución. Sólo se permiten carácteres alfanuméricos con una longitud máxima de 255 carácteres. Este dato es opcional.")
    helpnlic  = "<div id='ayudanlic'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el nombre del Liceo en el cual se graduó el alumno. Este campo permite una longitud máxima de 200 carácteres. Este dato es opcional.")
    helptlic  = "<div id='ayudatlic'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el título obtenido en el Liceo o Institución de la cual egresó. Este campo permite una longitud máxima de 25 carácteres alfanuméricos. Este dato es opcional.")
    helpsrti  = "<div id='ayudasrti'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el número de serial del título obtenido, este campo permite una longitud máxima de 50 carácteres. Este dato es opcional.")
    helpprof  = "<div id='ayudaprof'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable si el alumno es profesional o no. Este dato es obligatorio.")
    helppais  = "<div id='ayudapais'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el Pais de procedencia del alumno. Este dato es obligatorio.")
    helpedo   = "<div id='ayudaedo'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el Estado de procedencia del alumno. Este dato es obligatorio.")
    helpmun   = "<div id='ayudamun'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el Municipio de procedencia del alumno. Este dato es obligatorio.")
    helpparr  = "<div id='ayudaparr'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la Parroquía de procedencia del alumno. Este dato es obligatorio.")
    helptri   = "<div id='ayudatri'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el trimestre en el cual esta ingresando el alumno. Este dato es obligatorio.")
    helpcondi = "<div id='ayudacondi' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la condición de ingreso del alumno a la institución. Este dato es obligatorio.")
    helpsises = "<div id='ayudasises' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el sistema de estudio seleccionado por el alumno a registrar. Este dato es obligatorio.")
    helptibac = "<div id='ayudatibac' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el título de bachiller. Este dato es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que vinicializa los campos del formulario de Datos Académicos del Alumno
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormDatoAcademico, self).__init__(*args, **kwargs)
        self.fields['pais'].choices = cargarPaises()
        if 'pais' in self.data:
            self.fields['estado'].choices = cargarEstados(self.data['pais'])
        if 'estado' in self.data:
            self.fields['municipio'].choices = cargarMunicipios(self.data['estado'])
        if 'municipio' in self.data:
            self.fields['parroquia'].choices = cargarParroquias(self.data['municipio'])
        self.fields['trimestre'].choices = cargarTrimestres()
        self.fields['condicion_ingreso'].choices = cargarCondicionesingreso()
        self.fields['sistema_estudio'].choices = cargarSistemasestudio()
        self.fields['titulo_bachiller'].choices = cargarTitulosbachiller()
        
    def clean_pais(self):
        """
        @note: Función que verifica si el pais fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el pais
        """
        pais = self.cleaned_data['pais']
        if pais=="0":
            raise forms.ValidationError(_(u"Debe seleccionar un pais"))
        return self.cleaned_data['pais']
    
    def clean_estado(self):
        """
        @note: Función que verifica si el estado de un pais fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el estado de un pais
        """
        edo = self.cleaned_data['estado']
        if edo=="0":
            raise forms.ValidationError(_(u"Debe seleccionar un estado"))
        return self.cleaned_data['estado']
    
    def clean_municipio(self):
        """
        @note: Función que verifica si el municipio fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el municipio
        """
        mun = self.cleaned_data['municipio']
        if mun=="0":
            raise forms.ValidationError(_(u"Debe seleccionar un municipio"))
        return self.cleaned_data['municipio']
    
    def clean_parroquia(self):
        """
        @note: Función que verifica si la parroquía de un municipio fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado la parroquía
        """
        parr = self.cleaned_data['parroquia']
        if parr=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la parroquía"))
        return self.cleaned_data['parroquia']
        
    def clean_trimestre(self):
        """
        @note: Función que verifica si el trimestre fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el trimestre
        """
        trimestre = self.cleaned_data['trimestre']
        if trimestre == "0":
            raise forms.ValidationError(_(u"Debe seleccionar un trimestre"))
        return self.cleaned_data['trimestre']
    
    def clean_condicion_ingreso(self):
        """
        @note: Función que verifica si la condición de ingreso fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado la condición de ingreso
        """
        condicion_ingreso = self.cleaned_data['condicion_ingreso']
        if condicion_ingreso=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la condición de ingreso"))
        return self.cleaned_data['condicion_ingreso']
    
    def clean_sistema_estudio(self):
        """
        @note: Función que verifica si el sistema de estudio fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el sistema de estudio
        """
        sistema_estudio = self.cleaned_data['sistema_estudio']
        if sistema_estudio=="0":
            raise forms.ValidationError(_(u"Debe seleccionar el sistema de estudio"))
        return self.cleaned_data['sistema_estudio']
    
    def clean_titulo_bachiller(self):
        """
        @note: Función que verifica si el título de bachiller fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado el título de bachiller
        """
        titulo = self.cleaned_data['titulo_bachiller']
        if titulo =="0":
            raise forms.ValidationError(_(u"Debe seleccionar el título"))
        return self.cleaned_data['titulo_bachiller']
        
class FormAnualidad(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de anualidades
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idanualidad = forms.CharField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'20', 'maxlength':'20', 'title':_(u'Indique el id de la anualidad'), 'tabindex':'1'}))
    descripcion = forms.CharField(label=_(u"Descripción:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'200', 'title':_(u'Indique la descripción de la anualidad'), 'tabindex':'5'}))
    finicio = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de inicio:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'readonly':'readonly', 'title':_(u'Indique la fecha de inicio'), 'tabindex':'3'}), required=False)
    fculmina = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de culminación:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'readonly':'readonly', 'title':_(u'Indique la fecha de culminación'), 'tabindex':'4'}), required=False)
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.TextInput(attrs={'size':'40', 'maxlength':'45', 'title':_(u'Indique alguna observación'), 'tabindex':'6'}), required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUSCONDICION, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'2'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid   = "<div id='ayudaid'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador para la anualidad a registrar, este campo sólo permite una longitud máxima de 20 carácteres. Este dato es obligatorio.")
    helpdes  = "<div id='ayudades'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique la descripción acerca de la anualidad a registrar, sólo se permiten carácteres alfanuméricos con una longitud máxima de 200 carácteres. Este dato es obligatorio.")
    helpfini = "<div id='ayudafini' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la fecha de inicio de la anualidad. Este campo no es editable y solo se pueden ingresar datos mediante el calendario. Este dato es opcional.")
    helpfcul = "<div id='ayudafcul' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la fecha de culminación de la anualidad. Este campo no es editable y solo se pueden ingresar datos mediante el calendario. Este dato es opcional.")
    helpobs  = "<div id='ayudaobs'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones asociadas a la anualidad a registrar. Solo se permiten carácteres alfanuméricos con una longitud máxima de 45 carácteres. Este dato es opcional.")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus de la anualidad a registrar. Este dato es obligatorio.")
    
class FormAnualidadCarrera(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de anualidades por carrera
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idanualidad_carrera = forms.IntegerField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique el id de la anualidad por esta carrera'), 'tabindex':'4'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'5'}))
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUSCONDICION, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'2'}))
    carrsed = forms.ChoiceField(label=_(u'Carreras por sede:'), choices=cargarCarrerasSede(), widget=forms.Select(attrs={'title':_(u'Seleccione una carrera'), 'tabindex':'1'}))
    anualidad = forms.ChoiceField(label=_(u'Anualidad:'), choices=cargarAnualidades(), widget=forms.Select(attrs={'title':_(u'Seleccione una Anualidad'), 'tabindex':'3'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid   = "<div id='ayudaid'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador de la anualidad, este campo tiene una longitud máxima de 10 carácteres. Este dato es obligatorio.")
    helpobs  = "<div id='ayudaobs'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones de la anualidad a registrar, sólo se permiten carácteres alfanuméricos con una longitud máxima de 255 carácteres. Este dato es obligatorio.")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus de la anualidad a registrar. Este dato es obligatorio.")
    helpcase = "<div id='ayudacase' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la carrera de la sede a la cual se va a asociar la anualidad a registrar. Este dato es obligatorio.")
    helpanua = "<div id='ayudaanua' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la anualidad correspondiente. Este dato es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que inicializa los campos del formulario de Anualidades por Carrera
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormAnualidadCarrera, self).__init__(*args, **kwargs)
        self.fields['carrsed'].choices = cargarCarrerasSede()
        self.fields['anualidad'].choices = cargarAnualidades()
        
    def clean_carrsed(self):
        """
        @note: Función que verifica si la carrera fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado una carrera
        """
        carrsed = self.cleaned_data['carrsed']
        if carrsed=="0":
            raise forms.ValidationError(_(u"Debe seleccionar una carrera"))
        return self.cleaned_data['carrsed']
    
    def clean_anualidad(self):
        """
        @note: Función que verifica si la anualidad fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado una anualidad
        """
        anualidad = self.cleaned_data['anualidad']
        if anualidad=="0":
            raise forms.ValidationError(_(u"Debe seleccionar la anualidad"))
        return self.cleaned_data['anualidad']
        
class FormAnualidadTriCarrera(forms.Form):
    """
    @note: Clase que contiene el formulario de registro de anualidades por trimestre y carrera
    @licence: GPLv2
    @author: T.S.U. Roldan D. Vargas G.
    @contact: roldandvg at gmail.com
    """
    idanualidadtrimestre = forms.IntegerField(label=_(u"ID:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'title':_(u'Indique el id'), 'tabindex':'3'}))
    fregistro = forms.DateField(('%d/%m/%Y',),label=_(u"Fecha de registro:"), widget=forms.TextInput(attrs={'size':'10', 'maxlength':'10', 'readonly':'readonly', 'title':_(u'Indique la fecha de registro'), 'tabindex':'2'}))
    observaciones = forms.CharField(label=_(u"Observaciones:"), widget=forms.Textarea(attrs={'cols':'40', 'rows':'2', 'maxlength':'255', 'title':_(u'Indique alguna observación'), 'tabindex':'5'}), required=False)
    estatus = forms.ChoiceField(label=_(u"Estatus:"), choices=ESTATUSCONDICION, widget=forms.Select(attrs={'title':_(u'Seleccione el estatus'), 'tabindex':'4'}))
    trimestre = forms.ChoiceField(label=_(u"Trimestre:"), choices=cargarTrimestres(), widget=forms.Select(attrs={'title':_(u'Seleccione el trimestre'), 'tabindex':'1'}))
    anualidad_carrera = forms.ChoiceField(label=_(u"Anualidad por Carrera:"), choices=cargarAnualidadesCarreras(), widget=forms.Select(attrs={'title':_(u'Seleccione la anualidad por carrera'), 'tabindex':'6'}))
    modificar = forms.CharField(widget=forms.HiddenInput(attrs={'size':'2', 'readonly':'readonly'}), required=False)
    
    helpid   = "<div id='ayudaid'   class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique el identificador de la anualidad a registrar. Este campo permite una longitud máxima de 10 carácteres. Este dato es obligatorio.")
    helpfreg = "<div id='ayudafreg' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione del calendario suministrado la fecha de registro de la anualidad. Este campo no es editable y solo se pueden ingresar datos mediante el calendario. Este dato es obligatorio.")
    helpobs  = "<div id='ayudaobs'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Indique las observaciones acerca de la anualidad a registrar, sólo se permiten carácteres alfanuméricos con una longitud máxima de 255 carácteres. Este dato es opcional.")
    helpest  = "<div id='ayudaest'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el estatus de la anualidad. Este dato es obligatorio.")
    helptri  = "<div id='ayudatri'  class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable el trimestre al cual va a asociar la anualidad a registrar. Este dato es obligatorio.")
    helpanca = "<div id='ayudaanca' class='mostrarDetalles help' style='display:none;'>%s</div>" % _(u"Seleccione de la lista desplegable la anualidad registrada para una carrera específica. Este dato es obligatorio.")
    
    def __init__(self, *args, **kwargs):
        """
        @note: Función que inicializa los campos del formulario de Anualidad por Trimestre y Carrera
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        """
        super(FormAnualidadTriCarrera, self).__init__(*args, **kwargs)
        self.fields['trimestre'].choices = cargarTrimestres()
        self.fields['anualidad_carrera'].choices = cargarAnualidadesCarreras()
        
    def clean_trimestre(self):
        """
        @note: Función que verifica si el trimestre fue seleccionado
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado un trimestre
        """
        trimestre = self.cleaned_data['trimestre']
        if trimestre == "0":
            raise forms.ValidationError(_(u"Debe seleccionar el trimestre"))
        return self.cleaned_data['trimestre']
    
    def clean_anualidad_carrera(self):
        """
        @note: Función que verifica si la carrera por anualidad fue seleccionada
        @licence: GPLv2
        @author: T.S.U. Roldan D. Vargas G.
        @contact: roldandvg at gmail.com
        @return: Retorna un mensaje al usuario en caso de no haber seleccionado una carrera por anualidad
        """
        anualidad_carrera = self.cleaned_data['anualidad_carrera']
        if anualidad_carrera =="0":
            raise forms.ValidationError(_(u"Debe seleccionar la anualidad"))
        return self.cleaned_data['anualidad_carrera']