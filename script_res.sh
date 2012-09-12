#!/bin/bash

###############################################
#Desarrollado por TSU Oscar Lobo
#Email oscarescalando@gmail.com
#Desarrollado julio 2011
##############################################
#Sistema de respaldo para base de datos PostgreSQL

cmd=$(date +"%F_%H%M%S")

pg_dump -i -h localhost -p $puerto -U $uid -F c -b -v -f "respaldo$cmd.backup" esmayoy

#!/bin/bash

###############################################
#Desarrollado por TSU Oscar Lobo
#Email oscarescalando@gmail.com
#Desarrollado julio 2011
##############################################
#Sistema de respaldo para base de datos PostgreSQL

cmd=$(date +"%F_%H%M%S")

pg_dump -i -h localhost -p $puerto -U $uid -F c -b -v -f "$cmd.backup" esmayoy

#!/bin/bash

###############################################
#Desarrollado por TSU Oscar Lobo
#Email oscarescalando@gmail.com
#Desarrollado julio 2011
##############################################
#Sistema de respaldo para base de datos PostgreSQL

cmd=$(date +"%F_%H%M%S")

pg_dump -i -h localhost -p $puerto -U $uid -F c -b -v -f "$cmd.backup" esmayoy