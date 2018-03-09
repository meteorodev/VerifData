# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Descripción:
from builtins import print

from src.process import unirMchDBFMen as unir, normales as norM
from src.util import openConfig as cfgdb, loadNC as fnc
from src.controller import estacionController as esController, serieController as serieController
import pandas as pd
import numpy as np
import os.path as pth

class FillMController():
    """This class search into de database a estation and fill empty data firts with dbf files, and then fill whit chirps datset """
    estaBol=["M0001", "M0009", "M0021", "M0023", "M0024", "M0105", "M0310", "M0318", "M0321", "M0328", "M0337", "M0343", "M0344",
             "M0345", "M0346", "M0357", "M0358", "M0359", "M0909", "M0910", "M1094", "M1183", "M1240", "M5021", "M5044", "M0010",
             "M0011", "M0022", "M0053", "M0055", "M0098", "M0108", "M0109", "M0110", "M0111", "M0115", "M0210", "M0211", "M0214",
             "M0264", "M0265", "M0267", "M0282", "M0285", "M0299", "M0316", "M0317", "M0319", "M0320", "M0322", "M0323", "M0329",
             "M0330", "M0331", "M0332", "M0333", "M0334", "M0338", "M0341", "M0342", "M0347", "M0356", "M0525", "M0526", "M0561",
             "M0566", "M0572", "M0573", "M0574", "M0604", "M0605", "M0618", "M0628", "M0701", "M0705", "M0714", "M0734", "M0833",
             "M0834", "M0872", "M0873", "M0874", "M0875", "M0880", "M0886", "M0911", "M0912", "M0913", "M0915", "M0939", "M0940",
             "M0941", "M0942", "M0943", "M0944", "M0945", "M0946", "M0947", "M0948", "M0949", "M0950", "M0951", "M0952", "M0953",
             "M0954", "M0955", "M0956", "M0957", "M1002", "M1012", "M1016", "M1017", "M1056", "M1057", "M1061", "M1200", "M1211",
             "M5003", "M5031", "M5035", "M5036", "M5037", "M5042", "M5043", "M5054", "M5055", "M5074", "M5088", "M5104", "M1156",
             "M1002", "M1016"]

    def __init__(self,):
        """Constructor for FillMounthSerie"""
        cfg = cfgdb.configDB()
        cfg.readConfig("/home/drosero/Documentos/.drvmysql.cnf")
        self.cfg = cfg
        self.udb = unir.UnirMchDBFMen(self.cfg)
        self.esConexion = esController.EstacionController(self.cfg)
        self.conecmch = serieController.SerieController(self.cfg)

    def getSerie(self,añoiN,añofN,codEsta = estaBol, rutadbf="/" ,tabla="V0001",rutanc="/", añonc=1981,varnc="precipitation"):
        """Obtiene un serie de datos
                    @parametros
                    añoiN= año de inicio para el calculo de la normal
                    añofN= año de fin para el calculo de la normal
                    estaciones = listado de estaciones para procesar
                    rutadbf = ruta del archivo dbf para completar la consulta de la base mch
                    tabla = tabla para realizar la consulta de la base de datos
                """
        ##getNormal = norM.Normales()

        if pth.exists(rutadbf):
            self.udb.LoadDBF(rutadbf)

        else:
            print("Archivo .DBF no encontrado......")
            print("Necesito el archivo DBF para completar \n",
                  "solo se consultara la base de datos MCH")

        for es in codEsta:
            estaConsul = self.esConexion.getEstationbycod(es)
            serie = self.conecmch.getSerie(estaConsul.iat[0, 0], añoiN, añofN, tabla)
            #print(serie)
            print("estacion",estaConsul.iat[0, 0],"latitud",estaConsul.iat[0, 3],"  longitud ",estaConsul.iat[0, 4])
            ncfill=self.fillWhitNC(añoiN,añofN,serie,rutaNC=rutanc,añonc=añoiN,codigoEst=estaConsul.iat[0, 0],
                                   latEst=estaConsul.iat[0, 3],lonEst=estaConsul.iat[0, 4],varnc=varnc)
            ncfill.to_csv("/home/drosero/Escritorio/chirps/" + estaConsul.iat[0, 0] + "_RRfill.csv", sep=';',encoding='utf-8')

        # print("fin del metodo.....")
        #return normalesdf

    def fillWhitNC(self, añoI,añoF,serie,rutaNC, añonc,codigoEst,latEst,lonEst, varnc):
        #print("aqui en fill nc")
        ncclass=fnc.LoadNC()
        #,1981,latEst, lonEst,"precipitation")
        ncSerie=ncclass.readNc(rutaNC, añonc,latEst,lonEst,varnc)
        #print(ncSerie)
        #print(serie)
        head =["codigo", "anio", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        time = list(range(añoI,añoF+1))
        #nos asegurameo qeu el dataframe este completo
        #recorremos los años y biscamos en la serie si existe, si no completamos con el dataframe
        meses=["01","02","03","04","05","06","07","08","09","10","11","12"]
        inicio = True
        for i in time:
            #seriedbf = matrixDBF[(matrixDBF['ANNO'] == ac) & (self.udb.matrixDBF['CODIGO'] == normales.iat[i,1])]
            buscado = serie[(serie["anio"]==i)]
            if buscado.empty:
                datames=[codigoEst,i]
                #print(datames)
                for j in meses:
                    #buscar dentro de la serie nc los meses que faltan
                    dnc=ncSerie[(ncSerie["fecha"]==str(i)+'-'+j+'-01')]
                    #print(dnc.iat[0,1])
                    datames.extend([dnc.iat[0,1]])
                temdf=pd.DataFrame(datames,index=head)
                temdf=temdf.T
                #print(temdf)
            else:
                temdf=buscado
                #temdf=pd.DataFrame(buscado.values,index=head)
                #print(temdf)
            if inicio:
                result=temdf
            else:
                result=result.append(temdf)
            inicio=False

        return result

    def getSerieTemp(self,añoiN,añofN,codEsta = estaBol, rutadbf="/" ,tabla="V0001",prefix="tmax"):
        for es in codEsta:
            estaConsul = self.esConexion.getEstationbycod(es)
            serie = self.conecmch.getSerie(estaConsul.iat[0, 0], añoiN, añofN, tabla)
            print("procesando "+estaConsul.iat[0, 0])
            if serie.empty:
                print("No hay datos para la estacion "+estaConsul.iat[0, 0])
            else:
                serie.to_csv("/home/drosero/Escritorio/chirps/"+estaConsul.iat[0, 0]+"_"+prefix+".csv",sep=";",encoding='utf-8')




rs = "/home/drosero/Escritorio/chirps/"
bc = FillMController()
listado = bc.estaBol

##Para precipitacion
rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0001.DBF"
varnc="precipitation"
#bc.getSerie(1981,2017,listado,rdbf,tabla="V0001",rutanc="/home/drosero/Descargas/rrchirps.nc",varnc=varnc)

#temperaturas maxima
rdbf="/"

#rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0011.DBF"
rs = "/home/drosero/Escritorio/chirps/"
bc.getSerieTemp(1981,2017,listado,rutadbf=rdbf,tabla="V0011",prefix="Tmax")
##Para Temperatura minima
#rdbf = "/home/drosero/Documentos/Boletin/2018/BASES/T0012.DBF"
bc.getSerieTemp(1981,2017,listado,rutadbf=rdbf,tabla="V0012",prefix="Tmin")