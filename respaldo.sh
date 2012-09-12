#!/bin/bash

###############################################
#Desarrollado por TSU Oscar Lobo
#Email oscarescalando@gmail.com
#Desarrollado julio 2011
#Proyecto ESMAYOY
##############################################
#Sistema de respaldo para base de datos postgre

clear
echo ""
echo ""
echo "##############################################"
echo "#       PROYECTO ESMAYOY - PNFI IUTE         #"
echo "#  PROGRAMA PARA RESPALDO DE BASE DE DATOS   #"
echo "##############################################"
echo "# Selecione la opcion                        #"
echo "# 1 - Respaldo de base de datos              #"
echo "# 2 - Restaurar base de datos                #"
echo "# 3 - Crear tarea de respaldo automatica     #"
echo "# s - Salir                                  #"
echo "##############################################"
echo -e "Seleccione su opcion: \c"
read op

#Variables

#usuario de la base de datos
uid=admin
#password
psw=123456
#puerto del postgre
puerto=5432

case $op in

1)
	
	#Crea copia de seguridad de la base de datos
	echo ""
	echo -e "Ingrese la base de datos a respaldar: \c"
	read db
	echo -e "Ingrese la ruta de respaldo y el nombre del archivo para respaldo: \c"
	read ruta
	cmd=$(date +"%F_%H%M%S")
	pg_dump -i -h localhost -p $puerto -U $uid -F c -b -v -f "$ruta$cmd.backup" $db
	clear
	echo ""
	echo "Respaldo realizado en $ruta$cmd.backup"
	

;;

2)
	
	#Restaurar copia de seguridad de la base de datos
	echo ""
	echo "####################################################################"
	echo "EL PROCESO DE RESTAURACION DE BASE DE DATOS BORRARA TODOS LOS DATOS "
	echo "EXISTENTES EN LA BASE DE DATO SELECCIONADA"
	echo "####################################################################"
	echo ""
	echo -n "Para realizar el proceso seleccione [y/n]:"
	read salir
	if [ $salir = y ] || [ $salir = Y ]
		then
		echo -e "Ingrese la base de datos a restaurar: \c"
		read db
		echo -e "Ingrese la ruta de respaldo y el nombre del archivo a restaurar: \c"
		read ruta
		pg_restore -i -h localhost -p $puerto -U $uid -d $db -v "$ruta"
		echo "Restauracion realizada"
	
	elif [ $salir = n ] || [ $salir = N ]
		then
		clear
		./respaldo.sh
	else
		echo Invalid Option	
	fi
	
;;


3)
	#Crear tarea de respaldo automatico en el crom
	#Solicitamos los datos
	echo ""
	echo -e "Ingrese la base de datos a respaldar: \c"
	read db
	echo -e "Ingrese la ruta de respaldo y el nombre del archivo para respaldo: \c"
	read ruta



	echo -e "Define minuto de jecucion la tarea de 0 a 59:  \c"
	read minuto
	echo -e "Define hora de ejecucion de la tarea, de 0 a 23:  \c"
	read hora
	
	echo -e "Ingrese Ruta donde se genero el script= script_res.sh para respaldo :  \c"
	read ruta_s
	
	#creamos el archivo del script
	touch script_res.sh
	#esparamos un tiempo
	sleep 1
	echo "creando script_res.sh"
	l1=$(echo "#!/bin/bash ")
	l0=$(echo " ")
	l2=$(echo "############################################### ")
	l3=$(echo "#Desarrollado por TSU Oscar Lobo ")
	l4=$(echo "#Email oscarescalando@gmail.com ")
	l5=$(echo "#Desarrollado julio 2011 ")
	l6=$(echo "############################################## ")
	l7=$(echo "#Sistema de respaldo para base de datos postgre ")

	l9='cmd=$(date +"%F_%H%M%S")'
	l10=$(echo $l9)
	

	l11='pg_dump -i -h localhost -p $puerto -U $uid -F c -b -v -f "'$ruta'$cmd.backup" '$db
	
	l12=$(echo $l11)

	

	echo $l1 >> script_res.sh
	echo $l0 >> script_res.sh
	echo $l2 >> script_res.sh
	echo $l3 >> script_res.sh
	echo $l4 >> script_res.sh
	echo $l5 >> script_res.sh
	echo $l6 >> script_res.sh
	echo $l7 >> script_res.sh
	echo $l0 >> script_res.sh
	echo $l10 >> script_res.sh
	echo $l0 >> script_res.sh
	echo $l12 >> script_res.sh
	echo $l0 >> script_res.sh

	#crear tarea en el crom
	echo "creando tarea en el crontab"
	#00 00 * * * sh /ruta/script_respaldos.sh
	
	tarea=$minuto $hora' * * * sh '$ruta_s'script_res.sh'

	#echo $tarea
	echo $tarea >> /etc/crontab
	echo "registro agregado al cron de tareas con exito"

;;

s)
	echo -n "Para salir de la aplicacion presione [y/n]:"
	read salir
	if [ $salir = y ] || [ $salir = Y ]
		then
		echo 
	elif [ $salir = n ] || [ $salir = N ]
		then
		clear
		./respaldo.sh
	else
		echo Invalid Option	
	fi
	;;
	
*)
	echo Opcion invalida
	clear
	./respaldo.sh
esac
