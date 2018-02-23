# Marcos Gutierrez 			17909
# Raul Monzon				17014
# Descripcion: Simulacion de tiempo de corrida de un sistema operativo
# Fecha: 23 de febrero 2018

import simpy
from random import uniform, Random 

#Cantidad del RAM del sistema Operativo
cantidadRAM = 100  
#Numero de proceso que se realizaran
capacidad_Proceso = 2
#Memoria Requerida para la ejecucion:
memRequerida = random.randint(1,10)
#----Procesos READY----#
cantidadInstrucciones = random.randint(1,10)
#--TRUE = terminado---# #--False = no ha terminado--#	
terminado = true
#Primer Tiempo
time = 0


class SistemOperativo(object):
	def _init_(self,env):
		#Creamos el espacio donde se guardara
		self.RAM = simpy.Container(env, init=cantidadRAM, capacidad=capacidad_Proceso)
		self.CPU = simpy.Resource(env, capacidad=capacidad_Proceso)
