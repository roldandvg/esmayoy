#!/usr/bin/env python
# -*- coding: utf-8 -*-
INTENTOS_ACCESO = 3

TIEMPO_SESSION = 20 * 60 #El primer elemento indica el número de mínutos permitidos para la expiración de la sesión

DIAS_CADUCIDADPASS = 90

DEFAULT = (('0','Seleccione...'),)

ESTATUS = (('True','Activo(a)'),('False','Inactivo(a)'))

ESTATUSCONDICION = (('A', 'Activo'),('C', 'Cerrado'),('P', 'Pendiente'))

ESTATUSINSCRIPCION = (('I', 'Inscrito'),('A', 'Abandono'),('H','En Hito'),('R','Retirado'),('T','Traslado'))

DESICION = (('True','Sí'), ('False','No'))

DESICIONINVERSA = (('False', 'No'), ('True', 'Sí'))

NACIONALIDAD = (('V','Venezolano(a)'), ('E','Extranjero(a)'))

SEXO = (('M','Masculino'),('F','Femenino'))

NROHIJOS = (('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'))

SEMANA = [('lu','Lunes'),('ma','Martes'),('mi','Miércoles'),('ju','Jueves'),('vi','Viernes'),('sa','Sábado'),('do','Domingo')]