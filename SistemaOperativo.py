# -*- coding: cp1252 -*-

import simpy
import random
import math

# Marcos Gutierrez 			17909
# Raul Monzon				17014
# Descripcion: Simulacion de tiempo de corrida de un sistema operativo
# Fecha: 23 de febrero 2018

#Semilla
random.seed(10)
#Cantidad del RAM del sistema Operativo
cantidadRAM = 100
#Intrucciones a realizar por unidad de tiempo
cantidad_instrucciones = 3
#Tiempo de operaci? I/O
tiempoOperacion = 0
#Lista con los tiempos almacenados
tiemposProcesos = []
#Numero de proceso que se ejecutaran a la vez
capacidad_Proceso = 2
#Intervalo entre creaci? de procesos
intervalo = 3
#Cantidad de procesos a realizar
cantidad_procesos = 200

class SistemaOperativo:
	def __init__ (self, env):
		#Creamos el espacio donde se guardara
		self.RAM = simpy.Container(env, init=cantidadRAM, capacity=cantidadRAM)
		self.CPU = simpy.Resource(env, capacity=capacidad_Proceso)

class Proceso:
    def __init__(self, nombre, numero,env, sistema_operativo):
        #Atributos de la clase
        self.env = env
        self.finalizado = False#Indica si el proceso no tiene instrucciones por realizar, en la hoja de trabajo la nombran como terminated
        self.nombre = nombre#Nombre del proceso
        self.cantidadInstrucciones = random.randint(1,10)#Cantidad de instrucciones por realizar
        self.memRequerida = random.randint(1,10) #= random.randint(1, 10)#Cantidad de memoria RAM que necesita para realizar este proceso
        self.tiempo_creacion = 0 #Tiempo en el que se creo
        self.tiempo_terminado = 0 # Tiempo en el termino
        self.tiempo_total = 0 #Tiempo total que le tomo de crearse a terminarse
        self.numero = numero #Indice/n?mero del proceso
        self.sistema_operativo = sistema_operativo
        self.proceso = env.process(self.realizar(env, sistema_operativo))

    def realizar(self,env,sistema_operativo):
    	principio = env.now
    	self.tiempo_creacion = principio
    	print ('%s: ha sido creado en %d.'%(self.nombre,principio))#Imprime el momento en el que se creo el objeto (proceso)
    	with sistema_operativo.RAM.get(self.memRequerida) as getRam:  # Obtener RAM dependiendo de la requerida
    		yield getRam
    		# Inicio us de RAM
    		print('%s: obtiene Ram en %d. Estado: Esperando.' % (self.nombre, env.now)) #Imprime el momento en el que el proceso entra al estado waiting
    		siguiente = 0 #Esta variable nos indica que hacer luego de pasar el estado running
    		
    		while not self.finalizado: #Realiza estas instrucciones hasta que el estado del proceso terminated sea truex|x
    			with sistema_operativo.CPU.request() as req:
    				print('%s: ha solicitado al CPU en %d. Estado: Esperando.' % (self.nombre, env.now))
    				yield req
    				#Cuando finalmente entra a la CPU realiza estas instrucciones
    				print('%s: obtiene CPU en %d. Estado: Corriendo.' % (self.nombre, env.now))

    				for i in range (cantidad_instrucciones):  #Si el proceso aun tiene instrucciones por realizar, reduce uno el n?mero de instrucciones faltantes.
    					if self.cantidadInstrucciones > 0:
    						self.cantidadInstrucciones = self.cantidadInstrucciones - 1
    						siguiente_paso = random.randint(1,2)  # Para definir su siguiente paso
    				yield env.timeout(1)  #Como se modelo segun la hoja de trabajo, debe esperar una unidad de tiempo entre cada instruccion  # Realizar operaciones por ciclo
    				
    				 #Proceso I/O	
    				if siguiente_paso == 1:
    					print('%s: entra a operacion I/O en %d estado I/0' % (self.nombre, env.now))
    					yield env.timeout(tiempoOperacion)

    				#Si termina todas las instrucciones entra su finalizado se vuelve true
    				if self.cantidadInstrucciones ==0:
    					self.finalizado = True

    		print('%s: Terminado en %d (Status: Terminated)' % (self.nombre, env.now))
    		sistema_operativo.RAM.put(self.memRequerida)
    	fin = env.now # Liberar RAM
    	self.tiempo_terminado = fin #Guarda el tiempo final
    	self.tiempo_total = int(self.tiempo_terminado - self.tiempo_creacion) #Tiempo total que tomo el proceso llevarse a cabo
    	tiemposProcesos.insert(self.numero, self.tiempo_total) #Agregar el indice con su tiempo total respectivo a la lista

#Metodo de Generado de Procesos
def generador_procesos(env, sistema_operativo,i):
	#for i in range (cantidad_procesos):
		#Hace una cantidad de procesos que esta definido por cantidad_procesos
 	tiempo_creacion = random.expovariate(1.0/intervalo)#Distribuci? exponencial que sigue la creaci? de procesos
 	Proceso('Proceso %d' % i, i, env, sistema_operativo)
    	yield env.timeout(tiempo_creacion)  #Tiempo en el que se tarda en aparacer cada proceso

 #Metodo para generar 
def logFile(filePath, string):
    file = open(filePath, "a")
    file.write(string+ "\n")
    file.close()
    
class Main(object):     
    def __init__(self):#Se inicializa
        env = simpy.Environment()  # Crea un ambiente y lo llama env
        sistema_operativo = SistemaOperativo(env)  # crea la clase sistema operativo (recursos)
        for i in range (cantidad_procesos):
        	env.process(generador_procesos(env, sistema_operativo,i))  # Crear procesos
        	#logFile("log.csv",)
        env.run()       

        #calculando datos estadisticos promedio
        def estadisticaPromedio(s):
        	promedio = 0
        	promedio = sum(s) * 1.0/len(s)
        	return promedio

        #Pone los valores de cada uno en los atributos
        tiempoTotalPromedio = estadisticaPromedio(tiemposProcesos)
        varianza = map(lambda x: (x - tiempoTotalPromedio) ** 2, tiemposProcesos)
        tiempoDesviacionEstanda = math.sqrt(estadisticaPromedio(varianza))

        print "El tiempo Promedio es de: ", tiempoTotalPromedio
        print "La desviacion estandar es: ", tiempoDesviacionEstanda




Main()



