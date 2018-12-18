import sys
import os
import re
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1
from codecs import encode

class Solicitud:
    # Campos = []
    # Valor = {}
    def __init__(self, FicheroSolicitud):
        self.FicheroSolicitud = FicheroSolicitud
        self.Campos = []
        self.Datos = {}
		self.CamposDeRegistro = []
    def DefinirCampos(lista):
        self.Campos = lista
    def ObtenerDatos(self):
        """
        Obtener campos
		resultado:
            * Diccionario Valor{[campo,valor],...}
            * Lista de campos Campos[]
        """
        fp = open(self.FicheroSolicitud, 'rb') 
        parser = PDFParser(fp)
        doc = PDFDocument(parser)
        fields = resolve1(doc.catalog['AcroForm'])['Fields']
     
        for i in fields:
            field = resolve1(i)
            name, value = field.get('T'), field.get('V')

            # Dar formato a los campos
            name = name.decode("unicode_escape")
            name = name.upper()

            if isinstance(value, bytes):
                value = value.decode("unicode_escape")

            self.Valor[name] = value

            self.Campos.append(name)

        fp.close

    def ObtenerValoresPpales(self):
        Lista = {}
        for i in self.CamposPpales:
            # print("CampoPpal: {0}".format(i))
    
            if i[0] == "@":
                r = re.compile(i[1:].upper())
                i = i[1:]
            else:
                r = re.compile(".*" + i.upper() + ".*")
            newlist = list(filter(r.match, self.Campos)) # Read Note
    
            # print("newlist: {0}".format(newlist[0]))

            v = self.Valor[newlist[0]]
            if v is None:
                v = '--'
            elif v is "/'On'":
                v = 'X'    
            v = str(v)
            Lista[newlist[0]] = v
        return(Lista)
        

class HojaSolicitudes():
    Campos = []
    LineaCabecera = ''
    ListaSolicitudes = []
    def GeneraCabecera():
        pass
    def GeneraLinea():
        pass
    def GeneraFichero(FicheroSalida):
        pass
	
class LineaSolicitud():
    pass

# --------------------------------------------------------------
# Obtener una lista de ficheros
ListaFicheros = os.listdir(".")
ListaPdf = []
for fichero in ListaFicheros:
    if fichero.endswith(".pdf"): ListaPdf.append(fichero)

# Si existe algún fichero
if ListaPdf:
    # crear la hoja de salida
    fs = open('salida.rtf','w')
    #añadir cabecera
    """
    for i in CamposPpales:
        cabecera += i + '|'
    fs.writelines(cabecera)
    fs.writelines('\n')
    print (cabecera)  
    """
	
    #Para cada fichero de la lista
    for fichero in ListaPdf:
        print("-------------------------\nFichero: {0}".format(fichero))
        
        S = Solicitud(fichero)
        S.CamposPpales = ['apellidos', 'NIF', 'correo', 'empresa', 'expediente', 'lote', 'final contrato', \
                           'VPN', 'calidad', 'desarrollo', 'preproduccion', '@produccion']
        #obtener campos
        S.Parsear()
        Lista = S.ObtenerValoresPpales()
        del S

        #escribir los campos en la hoja de salida
        linea = ''
        for i in Lista:
            linea += Lista[i] + '|'
        fs.writelines(linea + "\n")
        # print(linea)
        # a = input("Pulsa una tecla")
        fs.close
    
