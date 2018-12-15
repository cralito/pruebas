import sys
import os
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from codecs import encode

CamposPpales = ['apellidos', \
                'NIF', \
                #'firma', \
                'correo', \
                'empresa', \
                'expediente', \
                'lote', \
                'final contrato', \
                'VPN', \
                'calidad', \
                'desarrollo', \
                'preproduccion', \
                '@produccion']

cabecera = ''

# Obtener una lista de ficheros
ListaFicheros = os.listdir(".")
ListaPdf = []
for fichero in ListaFicheros:
    if fichero.endswith(".pdf"): ListaPdf.append(fichero)

for fichero in ListaPdf:
    print(fichero)

# Si existe algún fichero
if ListaPdf:
    # crear la hoja de salida
    fs = open('salida.rtf','w')
    #añadir cabecera
    for i in CamposPpales:
        cabecera += i + '|'
    fs.writelines(cabecera)
    fs.writelines('\n')
    print (cabecera)  
	
    #Para cada fichero de la lista
    for fichero in ListaPdf:
        print("-------------------------\nFichero: {0}".format(fichero))
        #obtener campos
        fp = open(fichero, 'rb') 
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        fields = resolve1(doc.catalog['AcroForm'])['Fields']
        valor = {}
        campo = []
        for i in fields:
            field = resolve1(i)
            name, value = field.get('T'), field.get('V')

            name = name.decode("unicode_escape")
            name = name.upper()

            # print(type(value))
            if isinstance(value, bytes):
                value = value.decode("unicode_escape")

            valor[name] = value
            print(name, valor[name])
			
            campo.append(name)
            
            linea = ''
        for i in CamposPpales:
            print("CampoPpal: {0}".format(i))
    
            if i[0] == "@":
                r = re.compile(i[1:].upper())
            else:
                r = re.compile(".*" + i.upper() + ".*")
            newlist = list(filter(r.match, campo)) # Read Note
    
            print("newlist: {0}".format(newlist[0]))

            v = valor[newlist[0]]
            if v is None:
                v = '--'
            elif v is "/'On'":
                v = 'X'    
 
            linea += str(v) + '|'
        #escribir los campos en la hoja de salida
        fs.writelines(linea + "\n")
        print(linea)
        # a = input("Pulsa una tecla")
fs.close
    
