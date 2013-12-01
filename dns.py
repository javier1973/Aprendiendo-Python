#!/usr/bin/python
# -*- coding: utf-8 -*-

import os 
import sys 

#esta implementado para una red /24 que es la que usamos en la pracitca.

def add_dir():
	#guardamos direccion en zona directa con registro A
	print " funcion add_dir"
	fichero_directa=open("directa","a")
	fichero_directa.write(sys.argv[3]+"\t A \t"+sys.argv[4]+"\n")
	#print "Se guarda: {0} A {1} \n".format(sys.argv[3] , sys.argv[4])
	fichero_directa.close
	#guardamoes en zona inversa
	fichero_inversa=open("inversa","a")
	IP=sys.argv[4].split(".")
	fichero_inversa.write(IP[3]+"\t PTR \t"+sys.argv[3]+".directa.org"+"\n")
	fichero_inversa.close

def add_alias():
	#guardamos alias en zona directa con registro CNAME
	print "alias"
	fichero_directa=open("directa","a")
	fichero_directa.write(sys.argv[3]+"\t CNAME \t"+sys.argv[4]+"\n")
	#print "Se guarda: {0} CNAME {1} \n".format(sys.argv[3] , sys.argv[4])
	fichero_directa.close

# comprobamos tiene tosdos los argumentos y llamamos funcion
def alias():
	if len(sys.argv) == 5:
		add_alias()
		#reiniciamos servicio
		os.system("service bind9 restart") 
	else:
		ayuda()

# comprobamos tiene tosdos los argumentos y llamamos funcion
def direccion(): 
	if len(sys.argv) == 5:
		add_dir() #pdriamos incluir todo el proceso de añadir pero asi es más facil de entender¿?
		#reiniciamos servicio
		os.system("service bind9 restart") 
	else:
		ayuda()

def add():#evaluamos si ingresan el segundo argumento correcto 
    if sys.argv[2] in ("--dir","--alias"):
		case_add[sys.argv[2]]()
    else:
		print 'El segundo argumento de -a no es valido ha de ser --dir ó --alias'

def borra():
	#abrimos los archivo de zona directa e inversa en modo de solo lectura
	fdirecta=open("directa","r")
	finversa=open("inversa","r")
	#metemos en listas los ficheros
	ldirecta=fdirecta.readlines() 
	linversa=finversa.readlines() 
	#cerramos el fichero
	fdirecta.close 
	finversa.close
	inv=-1
	fdirecta=open("directa","w")
	finversa=open("inversa","w")
	
	for i in ldirecta:
		if i.find(sys.argv[2])==0:
			inv=0
			ldirecta.remove(i) 
	if inv == 0:
		for j in linversa:
			linversa.remove(j)
		for k in ldirecta:
			fdirecta.write(k)
		for l in linversa:
			finversa.write(l)
	else:
		print "No se han encontado registros para borrar con {0}".format(sys.argv[2])
		#reiniciamos servicio
		os.system("service bind9 restart") 
	fdirecta.close
	finversa.close
	
def ayuda():
    print "Ayuda del comando dns.py \n"
    print "-a para insertar registros A seguido de --dir nombre e IP \n"
    print "-a para insertar registros CNAME seguido de --alias nombre1 nombre2\n"
    print "-b para borrar seguido de nombre del registro\n"
    print "? para desplegar la ayuda\n"

case = {"-a" : add,
        "-b" : borra,
        "?" : ayuda,
        }

case_add = {"--dir" : direccion,
			"--alias" : alias,
			}
# checkeamos el primer argumento si ok llamamos a case
if sys.argv[1] in ("-a","-b","?"):
	case[sys.argv[1]]()
else:
	print 'El primer argumento no es valido ha de ser -a -b ó ?'
			
